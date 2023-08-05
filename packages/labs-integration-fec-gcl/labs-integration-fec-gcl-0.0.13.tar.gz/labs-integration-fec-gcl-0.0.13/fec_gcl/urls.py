"""integrations URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url

from fec_gcl.views import GetTotalConsumedCRL, GetConsumedCRLPEGA, GetConsumedCRLF1CAS, GetConsumedCRLAcctDB, GetGCLValidation
from fec_gcl.views import GetTotalConsumedCRLAsync, GetConsumedCRLPEGAAsync, GetConsumedCRLF1CASAsync, GetConsumedCRLAcctDBAsync

urlpatterns = [
    url(r'^get_total_consumed_crl/$', GetTotalConsumedCRL.as_view()),
    url(r'^get_consumed_crl_pega/$', GetConsumedCRLPEGA.as_view()),
    url(r'^get_consumed_crl_f1cas/$', GetConsumedCRLF1CAS.as_view()),
    url(r'^get_consumed_crl_acctdb/$', GetConsumedCRLAcctDB.as_view()),
    url(r'^get_total_consumed_crl_async/$', GetTotalConsumedCRLAsync.as_view()),
    url(r'^get_consumed_crl_pega_async/$', GetConsumedCRLPEGAAsync.as_view()),
    url(r'^get_consumed_crl_f1cas_async/$', GetConsumedCRLF1CASAsync.as_view()),
    url(r'^get_consumed_crl_acctdb_async/$', GetConsumedCRLAcctDBAsync.as_view()),
    url(r'^get_gcl_validation/$', GetGCLValidation.as_view()),
]
