from django.contrib.staticfiles.management.commands.runserver import Command as RunserverCommand
from django.contrib.sessions.models import Session


class Command(RunserverCommand):

    def inner_run(self, *args, **options):
        Session.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(
                'Sessões existentes foram encerradas.'
            )
        )

        super().inner_run(*args, **options)