from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Seed database with sample data and create a demo superuser'

    def add_arguments(self, parser):
        parser.add_argument('--no-superuser', action='store_true', help='Do not create demo superuser')

    def handle(self, *args, **options):
        self.stdout.write('Loading fixtures...')
        try:
            call_command('loaddata', 'students/fixtures/sample_data.json')
        except Exception as exc:
            # If fixtures are missing or fail to load, continue and still create user
            self.stdout.write(self.style.WARNING(f'Could not load fixtures: {exc}'))

        if not options['no_superuser']:
            if not User.objects.filter(username='admin').exists():
                self.stdout.write('Creating demo superuser (admin/pass)')
                User.objects.create_superuser('admin', 'admin@example.com', 'pass')
            else:
                self.stdout.write('Demo superuser already exists')
        self.stdout.write(self.style.SUCCESS('Seeding finished.'))
