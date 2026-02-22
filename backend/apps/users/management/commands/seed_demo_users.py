from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Create demo users for MVP'

    def handle(self, *args, **options):
        users = [
            ('998900000001', 'customer', 'customer123'),
            ('998900000002', 'supplier', 'supplier123'),
            ('998900000003', 'driver', 'driver123'),
            ('998900000004', 'admin', 'admin123'),
        ]
        for phone, role, password in users:
            user, created = User.objects.get_or_create(phone=phone, defaults={'role': role})
            if created:
                user.set_password(password)
                if role == 'admin':
                    user.is_staff = True
                    user.is_superuser = True
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Created {role}: {phone}'))
            else:
                self.stdout.write(f'Exists {phone}')
