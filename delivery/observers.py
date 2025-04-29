from abc import ABC, abstractmethod
from typing import List
from django.utils import timezone

class DeliveryStatusObserver(ABC):
    @abstractmethod
    def update(self, delivery_id: str, old_status: str, new_status: str):
        pass

class DeliveryStatusSubject:
    def __init__(self):
        self._observers: List[DeliveryStatusObserver] = []

    def attach(self, observer: DeliveryStatusObserver):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: DeliveryStatusObserver):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, delivery_id: str, old_status: str, new_status: str):
        for observer in self._observers:
            observer.update(delivery_id, old_status, new_status)

class DatabaseLogObserver(DeliveryStatusObserver):
    def update(self, delivery_id: str, old_status: str, new_status: str):
        # Log the status change in the database
        from .models import DeliveryLog
        DeliveryLog.objects.create(
            delivery_id=delivery_id,
            old_status=old_status,
            new_status=new_status,
            timestamp=timezone.now()
        )

# Singleton instance of the subject
delivery_status_subject = DeliveryStatusSubject() 