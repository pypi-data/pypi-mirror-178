from django.apps import AppConfig


class RepaymentConfig(AppConfig):
    name = 'fec_repayment'
    verbose_name = 'FEC REPAYMENT'

    # This key is used to identify the apps for Kuliza Labs Integration Broker.
    labs_integration_app = True

    # This key is used to define a prefix for all URL in the app.
    # This will only be honoured when the key 'labs_integration_app' is 'True'.
    labs_url_prefix = '/fec/repayment/'
