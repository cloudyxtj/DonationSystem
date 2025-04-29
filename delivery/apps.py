from django.apps import AppConfig
from .observers import delivery_status_subject, DatabaseLogObserver


class DeliveryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'delivery'

    def ready(self):
        # Initialize database observer
        db_observer = DatabaseLogObserver()
        
        # Attach observer to the subject
        delivery_status_subject.attach(db_observer)
