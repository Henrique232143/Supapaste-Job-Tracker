from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session


class Command(BaseCommand):
    help = 'Remove todas as sessões ativas.'

    def handle(self, *args, **options):
        quantidade = Session.objects.count()

        Session.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(
                f'{quantidade} sessão(ões) removida(s).'
            )
        )