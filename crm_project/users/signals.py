from django.db.models.signals import post_save
from django.contrib.auth.models import User
from accounts.models import Customer
from django.contrib.auth.models import Group


def customer_profile(sender, instance, created, **kwargs):
    groups = Group.objects.all()
    if len(groups) == 0:
        Group.objects.create(name='customer')
        if created:
            group = Group.objects.get(name='customer')
            instance.groups.add(group)
            Customer.objects.create(
                user=instance,
                name=instance.username,
            )
            print('Profile created')

    else:
        if created:
            group = Group.objects.get(name='customer')
            instance.groups.add(group)
            Customer.objects.create(
                user=instance,
                name=instance.username,
            )
            print('Profile created')


post_save.connect(customer_profile, sender=User)
