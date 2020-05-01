from django.core.management.base import BaseCommand, CommandError

from mainapp.models import AttachmentTemplate, ATTACHMENT_TYPE_CHOICES


class Command(BaseCommand):
    help = 'Initializes database'

    def handle(self, *args, **options):
        for att_type in ATTACHMENT_TYPE_CHOICES:
            if not AttachmentTemplate.objects.filter(kind=att_type[0]).exists():
                AttachmentTemplate.objects.create(kind=att_type[0],
                                                  subject=att_type[1],
                                                  body=att_type[1])
                self.stdout.write(self.style.SUCCESS(
                    'Created attachment type {}'.format(att_type[0])
                ))
            else:
                self.stdout.write(self.style.SUCCESS(
                    'Attachment type {} already exists.'.format(att_type[0])
                ))
