from django.core.management.base import BaseCommand, CommandError
class Command(BaseCommand):
    help = 'Builds feature values for the provided features'

    def add_arguments(self, parser):
        parser.add_argument('corpus', nargs=1, type=int)
        parser.add_argument('featurekey', nargs=1, type=str)

    def handle(self, *args, **options):
        pass # TODO implement re-indexing
        # runner = FeatureRunner()
        # runner.build_feature(options['featurekey'][0], options['corpus'][0])