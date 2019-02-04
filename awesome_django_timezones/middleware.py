from ipaddress import ip_address
from urllib.parse import quote, unquote
from django.conf import settings
from django.utils import timezone
import pytz
import ipapi


class TimezonesMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Attempts to activate a timezone from a cookie. Otherwise uses IP API to lookup timezone
        """
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        tz = None

        # Must be setup to use timezones in order for this code to be usable
        if getattr(settings, 'USE_TZ', None):
            # check the cookie for `timezone`
            tz = request.COOKIES.get('timezone', None)
            if tz:
                # cookie timezones are URI encoded
                tz = unquote(tz)
            else:
                # no cookie set, use IP API to lookup timezone and use that to set the cookie
                ip_info = ipapi.location(ip=get_ip_address(request), key=getattr(settings, 'DJANGO_IPAPI_KEY', None))
                tz = ip_info.get('timezone', None)

            try:
                # attempt to activate the timezone - this might be an invalid timezone
                timezone.activate(pytz.timezone(tz))
            except (pytz.UnknownTimeZoneError, AttributeError):
                timezone.deactivate()

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        if getattr(settings, 'USE_TZ', None) and tz:
            # set or re-set the cookie if `tz` is provided, this extends the cookie expiration if it's already
            # set, or will set it initially by the API lookup to prevent future API lookups
            response.set_cookie('timezone', quote(tz, safe=''), max_age=60*60*24*365, samesite='Strict')

        return response


def get_ip_address(request):
    """ Makes the best attempt to get the client's real IP or return the loopback """
    POSSIBLE_HEADERS = [
        'HTTP_X_FORWARDED_FOR', 'HTTP_FORWARDED'
        'HTTP_X_REAL_IP', 'HTTP_CLIENT_IP', 'REMOTE_ADDR'
    ]
    ip = ''
    for header in POSSIBLE_HEADERS:
        possible_ip = request.META.get(header)
        if possible_ip:
            if 'for' in possible_ip and '=' in possible_ip:
                # Using new-ish `FORWADED` header
                # https://en.wikipedia.org/wiki/X-Forwarded-For#Alternatives_and_variations
                possible_ip = possible_ip.split('=')[1]
            if ',' in possible_ip:
                # Assume first IP address in list is the originating IP address
                # https://en.wikipedia.org/wiki/X-Forwarded-For#Format
                possible_ip = possible_ip.split(',')[0]
            try:
                ip = ip_address(possible_ip)
            except ValueError:
                # IP address isn't valid, keep checking headers
                continue
            # Ensure IP address isn't private or otherwise reserved
            if ip.is_multicast or ip.is_private or ip.is_unspecified or\
                    ip.is_reserved or ip.is_loopback or ip.is_link_local:
                # IP address isn't valid, keep checking headers
                continue

            if ip:
                # IP address is valid this far, consider it valid
                break

    return ip
