def user_group(request):
    user = request.user
    is_donor = False
    is_recipient = False
    is_driver = False

    if user.is_authenticated:
        is_donor = user.groups.filter(name='Donor').exists()
        is_recipient = user.groups.filter(name='Recipient').exists()
        is_driver = user.groups.filter(name='Driver').exists()

    return {
        'is_donor': is_donor,
        'is_recipient': is_recipient,
        'is_driver': is_driver,
    }
