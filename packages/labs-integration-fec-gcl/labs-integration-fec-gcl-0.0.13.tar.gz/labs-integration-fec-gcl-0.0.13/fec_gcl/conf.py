from django.conf import settings
from appconf import AppConf

class FECGCLConf(AppConf):
    WSDL = 'https://api-uat-internal.fecredit.com.vn/GlobalCreditLimit?WSDL'
    WSDL_APS = 'https://api-uat-internal.fecredit.com.vn/APS_GCLValidation?WSDL'
    USERNAME = '36f8ffe70dbf43cfbef5ab3c435e7932'
    PASSWORD = '87156FC6369541cd8A0726DD7678e479'

    class Meta:
        prefix = 'gcl'
