from django.apps import AppConfig


class GCLConfig(AppConfig):
    name = 'fec_gcl'
    verbose_name = 'FEC GCL'

    # This key is used to identify the apps for Kuliza Labs Integration Broker.
    labs_integration_app = True

    # This key is used to define a prefix for all URL in the app.
    # This will only be honoured when the key 'labs_integration_app' is 'True'.
    labs_url_prefix = '/fec/gcl/'
