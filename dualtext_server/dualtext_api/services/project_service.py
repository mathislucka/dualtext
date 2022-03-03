from django.db.models import Q
from operator import itemgetter
from dualtext_api.models import Project, Annotation, Label, Task, Run, Lap
from collections import defaultdict
from .run_service import RunService
import math
import datetime

class ProjectService():
    def __init__(self, project_id):
        self.project = Project.objects.get(id=project_id)
        self.total_annotations = None
        self.annotated_annotations = None
        self.reviewed_annotations = None
        self.open_annotation_annotations = None
        self.open_review_annotations = None

        self.total_tasks = None
        self.annotated_tasks = None
        self.reviewed_tasks = None
        self.open_annotation_tasks = None
        self.open_review_tasks = None

        self.laps_by_annotation = None
        self.total_runs = None
        self.total_laps = None
        self.annotations_per_minute = None
        self.daily_average_annotation_seconds = None
        self.days_at_current_rate = None
        self.daily_average_annotation_count = None
        self.daily_annotation_seconds = None
        self.daily_average_annotation_count = None
        self.projected_minutes_left = None
        self.daily_annotation_count = None

    def get_total_annotations(self):
        if self.total_annotations is not None:
            return self.total_annotations
        else:
            tasks = self.get_total_tasks()
            self.total_annotations = Annotation.objects.filter(task__in=tasks.all())
            return self.total_annotations

    def get_annotated_annotations(self):
        if self.annotated_annotations is not None:
            return self.annotated_annotations
        else:
            annotations = self.get_total_annotations().filter(Q(task__is_finished=True) & Q(task__action=Annotation.ANNOTATE))
            self.annotated_annotations = annotations
            return self.annotated_annotations

    def get_reviewed_annotations(self):
        if self.reviewed_annotations is not None:
            return self.reviewed_annotations
        else:
            annotations = self.get_total_annotations().filter(Q(task__is_finished=True) & Q(task__action=Task.REVIEW))
            self.reviewed_annotations = annotations
            return self.reviewed_annotations
    
    def get_open_annotation_annotations(self):
        if self.open_annotation_annotations is not None:
            return self.open_annotation_annotations
        else:
            self.open_annotation_annotations = self.get_total_annotations().filter(Q(task__is_finished=False) & Q(task__action=Annotation.ANNOTATE))
            return self.open_annotation_annotations

    def get_open_review_annotations(self):
        if self.open_review_annotations is not None:
            return self.open_review_annotations
        else:
            self.open_review_annotations = self.get_total_annotations().filter(Q(task__is_finished=False) & Q(task__action=Annotation.REVIEW))
            return self.open_review_annotations
            

    def get_annotation_statistics(self):
        total = self.get_total_annotations().count()
        annotated = self.get_annotated_annotations().count()
        reviewed = self.get_reviewed_annotations().count()
        open_annotations = self.get_open_annotation_annotations().count()
        open_reviews = self.get_open_review_annotations().count()
        total_annotations = open_annotations + annotated
        total_reviews = open_reviews + reviewed
        
        if total_annotations != 0:
            percent_annotated = round(annotated / total_annotations, 2)
        else:
            percent_annotated = 0
        if total_reviews != 0:
            percent_reviewed = round(reviewed / total_reviews, 2)
        else:
            percent_reviewed = 0

        return {
            'total': total,
            'open_annotations': open_annotations,
            'annotated_absolute': annotated,
            'annotated_relative': percent_annotated,
            'open_reviews': open_reviews,
            'reviewed_absolute': reviewed,
            'reviewed_relative': percent_reviewed
        }

    def get_annotated_tasks(self):
        if self.annotated_tasks is not None:
            return self.annotated_tasks
        else:
            self.annotated_tasks = self.get_total_tasks().filter(Q(is_finished=True) & Q(action__in=[Task.ANNOTATE, Task.DUPLICATE]))
            return self.annotated_tasks

    def get_reviewed_tasks(self):
        if self.reviewed_tasks is not None:
            return self.reviewed_tasks
        else:
            self.reviewed_tasks = self.get_total_tasks().filter(Q(is_finished=True) & Q(action=Task.REVIEW))
            return self.reviewed_tasks

    def get_total_tasks(self):
        if self.total_tasks is not None:
            return self.total_tasks
        else:
            self.total_tasks = self.project.task_set
            return self.total_tasks
    
    def get_open_annotation_tasks(self, user):
        if self.open_annotation_tasks is not None:
            return self.open_annotation_tasks
        else:
            self.open_annotation_tasks = self.get_total_tasks().filter(
                Q(is_finished=False) &
                Q(action__in=[Task.ANNOTATE, Task.DUPLICATE]) &
                Q(annotator=None) &
                ~Q(copied_from__annotator=user)
            )
            return self.open_annotation_tasks
    
    def get_open_review_tasks(self, user):
        if self.open_review_tasks is not None:
            return self.open_review_tasks
        else:
            self.open_review_tasks = self.get_total_tasks().filter(
                Q(is_finished=False) &
                Q(action=Task.REVIEW) &
                Q(annotator=None) &
                ~Q(copied_from__annotator=user)
            )
            return self.open_review_tasks
    
    def claim_annotation_task(self, user):
        task = self.get_open_annotation_tasks(user).first()
        if task is not None:
            task.annotator = user
            task.save()
            return task
        else:
            return None
    
    def claim_review_task(self, user):
        task = self.get_open_review_tasks(user).first()
        if task is not None:
            task.annotator = user
            task.save()
            return task
        else:
            return None

    def get_task_statistics(self):
        total = self.get_total_tasks().count()
        annotated = self.get_annotated_tasks().count()
        reviewed = self.get_reviewed_tasks().count()
        if total != 0:
            percent_annotated = round(annotated / total, 2)
            percent_reviewed = round(reviewed / total, 2)
        else:
            percent_annotated = 0
            percent_reviewed = 0

        return {
            'total': total,
            'annotated_absolute': annotated,
            'annotated_relative': percent_annotated,
            'reviewed_absolute': reviewed,
            'reviewed_relative': percent_reviewed
        }

    def get_label_statistics(self):
        annotation_annotations = self.get_total_annotations().filter(Q(action=Annotation.ANNOTATE)).prefetch_related('labels')
        label_counts = defaultdict(int)

        for annotation in annotation_annotations:
            annotation_labels = annotation.labels.all()
            for label in annotation_labels:
                label_counts[label.name] += 1

        total_labels = sum(label_counts.values())
        relative_label_counts = {}
        for item in label_counts.items():
            if total_labels != 0:
                rel = round(item[1] / total_labels, 2)
            else:
                rel = 0
            relative_label_counts[item[0]] = rel

        return {
            'absolute': label_counts,
            'relative': relative_label_counts,
            'total': total_labels
        }

    def get_project_statistics(self):
        return {
            'annotations': self.get_annotation_statistics(),
            'labels': self.get_label_statistics(),
            'tasks': self.get_task_statistics(),
            # 'timetracking': self.get_timetracking_statistics(),
            #'agreement': self.get_annotator_reviewer_agreement()
        }

    def get_desired_label(self):
        label_statistics = self.get_label_statistics()['absolute']
        sorted_statistics = [(k, v) for k, v in label_statistics.items()]
        sorted_statistics.sort(key=itemgetter(1))
        labels = None
        if len(sorted_statistics) > 0:
            label_count = Label.objects.filter(project=self.project).count()
            LOWER_THRESHOLD = 40
            label_num = math.floor(label_count/100 * LOWER_THRESHOLD)
            label_names = [ name for name, val in sorted_statistics[0:label_num]]
            labels = Label.objects.filter(name__in=label_names, project=self.project).all()
        return labels

    def get_total_runs(self):
        if self.total_runs is not None:
            return self.total_runs
        else:
            self.total_runs = Run.objects.filter(Q(task__project=self.project) & Q(is_finished=True))
            return self.total_runs

    def get_total_laps(self):
        if self.total_laps is not None:
            return self.total_laps
        else:
            self.total_laps = Lap.objects.filter(run__in=self.get_total_runs().all())
            return self.total_laps

    def get_laps_by_annotation(self):
        if self.laps_by_annotation is not None:
            return self.laps_by_annotation
        else:
            all_laps = self.get_total_laps().select_related('annotation').all()
            seen_annotations = {}
            distinct = []
            for lap in all_laps:
                seen_annotations[lap.created_at.date()] = {}
            for lap in all_laps:
                #print('annotation id is {}, lap id is {}'.format(lap.annotation.id, lap.id))
                seen = seen_annotations[lap.created_at.date()].get(lap.annotation.id, None)
                if seen is None:
                    distinct.append(lap)
                    seen_annotations[lap.created_at.date()][lap.annotation.id] = True
            self.laps_by_annotation = distinct
            print('annotated annotations {}'.format(len(self.laps_by_annotation)))
            return self.laps_by_annotation

    def get_daily_annotation_seconds(self):
        if self.daily_annotation_seconds is not None:
            return self.daily_annotation_seconds
        else:
            runs = self.get_total_runs().all()
            dates = set([r.created_at.date() for r in runs])
            annotation_seconds = {}
            for date in dates:
                print(date)
                annotation_seconds[date] = 0
            print(annotation_seconds)
            print(dates)
            for run in runs:
                print(hash(run.created_at.date()))
                print(run.created_at)
                annotation_seconds[run.created_at.date()] += run.time_to_completion

            self.daily_annotation_seconds = annotation_seconds
            return self.daily_annotation_seconds

    def get_daily_annotation_count(self):
        if self.daily_annotation_count is not None:
            return self.daily_annotation_count
        else:
            laps = self.get_laps_by_annotation()
            dates = set([l.created_at.date() for l in laps])
            daily_annotation_count = {}
            for date in dates:
                daily_annotation_count[date] = 0
            for lap in laps:
                daily_annotation_count[lap.created_at.date()] += 1
            self.daily_annotation_count = daily_annotation_count

            return self.daily_annotation_count

    def get_daily_average_annotation_count(self):
        if self.daily_average_annotation_count is not None:
            return self.daily_average_annotation_count
        else:
            counts = list(self.get_daily_annotation_count().values())
            if len(counts) != 0:
                self.daily_average_annotation_count = sum(counts) / len(counts)
            else:
                self.daily_average_annotation_count = 0
            return self.daily_average_annotation_count

    def get_daily_average_annotation_seconds(self):
        if self.daily_average_annotation_seconds is not None:
            return self.daily_average_annotation_seconds
        else:
            seconds = list(self.get_daily_annotation_seconds().values())
            if len(seconds) != 0:
                self.daily_average_annotation_seconds = sum(seconds) / len(seconds)
            else:
                self.daily_average_annotation_seconds = 0
            return self.daily_average_annotation_seconds

    def get_annotations_per_minute(self):
        if self.annotations_per_minute is not None:
            return self.annotations_per_minute
        else:
            for r in self.get_total_runs().all():
                print('completion is {}'.format(r.time_to_completion))
            total_minutes = sum([r.time_to_completion for r in self.get_total_runs().all()]) / 60
            total_annotations = len(self.get_laps_by_annotation())
            if total_annotations != 0:
                self.annotations_per_minute = total_annotations / total_minutes
            else:
                self.annotations_per_minute = 0

            return self.annotations_per_minute

    def get_projected_minutes_left(self):
        if self.projected_minutes_left is not None:
            return self.projected_minutes_left
        else:
            open_annotations = self.get_open_annotation_annotations().count() + self.get_open_review_annotations().count()
            apm = self.get_annotations_per_minute()
            if apm != 0:
                self.projected_minutes_left = open_annotations / apm
            else:
                self.projected_minutes_left = 0
            return self.projected_minutes_left

    def get_days_at_current_rate(self):
        if self.days_at_current_rate is not None:
            return self.days_at_current_rate
        else:
            daily_minutes = self.get_daily_average_annotation_seconds() / 60
            minutes_left = self.get_projected_minutes_left()
            if daily_minutes != 0:
                self.days_at_current_rate = minutes_left / daily_minutes
            else:
                self.days_at_current_rate = 0
            return self.days_at_current_rate

    def get_timetracking_statistics(self):
        RunService().close_idle_runs()
        apm = self.get_annotations_per_minute()
        pml = self.get_projected_minutes_left()
        dacr = self.get_days_at_current_rate()
        dac = self.get_daily_annotation_count()
        das = self.get_daily_annotation_seconds()
        avgs = self.get_daily_average_annotation_seconds()
        avgc = self.get_daily_average_annotation_count()
        dates = sorted(list(das.keys()))

        timeseries = []

        for date in dates:
            entry = {}
            entry['seconds'] = das[date]
            entry['count'] = dac[date]
            entry['date'] = date
            timeseries.append(entry)
        if len(dates) != 0:
            last_date = dates[-1]
        else:
            last_date = datetime.datetime.now().date()
        num_days = math.ceil(dacr)
        for i in range(0, num_days):
            entry = {}
            entry['seconds'] = avgs
            entry['count'] = avgc
            entry['date'] = last_date + datetime.timedelta(days=i+1)
            entry['projected'] = True
            timeseries.append(entry)
        
        return {
            'timeseries': timeseries,
            'annotations_per_minute': apm,
            'projected_minutes_left': pml,
            'days_at_current_rate': dacr,
        }
