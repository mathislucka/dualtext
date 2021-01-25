from django.db.models import Q
from django.utils import timezone
from dualtext_api.models import Run, Lap, Task

class RunService():
    MAX_IDLE_SECONDS = 10
    def __init__(self, task=None):
        self.task = task

    def log_lap(self, annotation):
        now = timezone.now()
        run = Run.objects.filter(Q(task=self.task) & Q(is_finished=False)).first()
        active_run = None
        try:
            newest = run.lap_set.order_by('-created_at').first()
            newest = newest.created_at
            idle = now - newest
            if idle.seconds > self.MAX_IDLE_SECONDS:
                run.is_finished = True
                delta = newest - run.created_at
                run.time_to_completion = delta.seconds
                run.save()
                active_run = Run(task=self.task)
                active_run.save()
            else:
                active_run = run
        except AttributeError:
            active_run = Run(task=self.task)
            active_run.save()

        lap = Lap(run=active_run, annotation=annotation)
        lap.save()

    def close_idle_runs(self):
        now = timezone.now()
        runs = Run.objects.all()

        for run in runs:
            laps = Lap.objects.filter(run=run).all()
            print(run.created_at)
            for lap in laps:
                print('lap time: {}'.format(lap.created_at.strftime("%m/%d/%Y, %H:%M:%S")))
            newest = run.lap_set.order_by('-created_at').first()
            newest = newest.created_at
            idle = now - newest
            print(idle)

            if idle.seconds > self.MAX_IDLE_SECONDS:
                run.is_finished = True
                delta = newest - run.created_at
                run.time_to_completion = delta.seconds
                run.save()


