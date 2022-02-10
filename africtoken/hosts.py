from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'www', settings.ROOT_URLCONF, name='www'),  
    host(r'account', 'account.urls', name='account'),
    host(r'dashboard', 'user_dashboard.urls', name='dashboard'),
    host(r'admin', 'superuser.urls', name='superuser'),
)


handler404 = 'token_app.views.handler404'
handler500 = 'token_app.views.handler500'