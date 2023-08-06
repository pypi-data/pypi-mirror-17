=====
django-monitor-client
=====

django-monitor-client is a simple Django app to send project infomation to server. 

Quick start
-----------

1. Add "monitor_client" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'monitor_client',
    )

2. Include the django-monitor-client URLconf in your project urls.py like this::

    url(r'^monitor_client/v1', include("monitor_client.urls")),
3. Add vars in setting file.
    MONITOR_SERVER_PUSH_URL (to post data url)
    PROJIECT_DOMAIN (your project domain)

3. Restart your project to register your project.
