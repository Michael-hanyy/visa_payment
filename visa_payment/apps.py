from django.apps import AppConfig

class VisaPaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'visa_payment'

    def ready(self):
        import visa_payment.signals
