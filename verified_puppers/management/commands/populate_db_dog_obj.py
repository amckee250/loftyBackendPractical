from urllib.error import HTTPError
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError, transaction

from verified_puppers.models import Dog
from verified_puppers.serializers import DogCreateSerializer


class Command(BaseCommand):
    help = 'Populates the database with two dozen images of dogs and any corresponding metadata' \
           ' from the images. Use --fresh_db flag to remove existing Dog objects and replace with new'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fresh_db',
            help='Remove existing Dog objects and replace with new',
        )

    def handle(self, *args, **options):
        """
        Future Development: Adding more complex logic to utilize bulk_create would be more efficient.
            We would need to still check to ensure no duplicate Dogs were pulled from api and created
        """
        if options['fresh_db']:
            dogs = Dog.objects.all()
            # :'( - Just bring them to a shelter instead!
            dogs.delete()

        # Create 24 non-conflicting Dog objects with processed metadata and image modifications
        dog_count, conn_error_count, dupl_confl_count, exif_error_count = 0, 0, 0, 0
        while dog_count < 24:
            try:
                dog_count += 1
                with transaction.atomic():
                    original_img = Dog.fetch_original_img()
                    serializer = DogCreateSerializer(data={'original_img': original_img})
                    serializer.is_valid(raise_exception=IntegrityError)
                    dog = serializer.save()
                    dog.extract_image_metadata()

                    # Successfully created
                    # dog_count += 1

            except (ConnectionError, HTTPError):
                conn_error_count += 1
            except IntegrityError:
                dupl_confl_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'{dog_count} Dog objects were successfully created \nConnection Errors: {conn_error_count}'
            f'\nDuplicate Errors: {dupl_confl_count} \nExif Extract Errors: {exif_error_count}'
        ))
