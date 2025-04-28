from django.contrib.auth.models import Group
from .models import Donor, Recipient, Driver

class UserFactory:
    @staticmethod
    def create_user(form):
        user = form.save(commit=False)
        user.save()

        # Create role-based profile
        if user.role == 'Donor':
            Donor.objects.create(user=user)
            group, created = Group.objects.get_or_create(name='Donor')
        elif user.role == 'Recipient':
            Recipient.objects.create(user=user)
            group, created = Group.objects.get_or_create(name='Recipient')
        elif user.role == 'Driver':
            Driver.objects.create(user=user)
            group, created = Group.objects.get_or_create(name='Driver')

        user.groups.add(group)
        return user
