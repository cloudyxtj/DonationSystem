from .models import Donor, Recipient, Driver

class UserFactory:
    @staticmethod
    def create_user(form):
        user = form.save(commit=False)
        user.save()

        # Create role-based profile
        if user.role == 'Donor':
            Donor.objects.create(user=user)
        elif user.role == 'Recipient':
            Recipient.objects.create(user=user)
        elif user.role == 'Driver':
            Driver.objects.create(user=user)

        return user
