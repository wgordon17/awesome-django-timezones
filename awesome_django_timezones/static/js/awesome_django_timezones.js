// Save client-side timezone to cookie that expires in 1 year
(function() {
    try {
        let timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
        document.cookie = 'timezone=' + encodeURIComponent(timezone) + ';path=/;samesite=strict;max-age=' + 60*60*24*365;
    } catch(err) {
        // `Intl` library not found
    }
}());
