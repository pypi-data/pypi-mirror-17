# -*- coding: utf-8 -*-
"""
URLs.
"""
from django.conf.urls import url

from status import settings
from status.api.views import RootAPIView, ProviderAPIView

providers = [url(r'^{}/?$'.format(a),
                 ProviderAPIView.as_view(provider=p, provider_args=args, provider_kwargs=kwargs),
                 name='api_{}'.format(a))
             for a, p, args, kwargs in settings.CHECK_PROVIDERS]

urlpatterns = providers

urlpatterns += [
    url(r'^$', RootAPIView.as_view())
]
