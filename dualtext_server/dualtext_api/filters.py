from django_filters import rest_framework as filters
from .models import Annotation, Task

class AnnotationFilter(filters.FilterSet):
    label = filters.NumberFilter(field_name='labels__id', lookup_expr='contains')
    label_name = filters.CharFilter(field_name='labels__name', lookup_expr='contains')
    annotation_group = filters.NumberFilter(field_name='annotation_group__id')

class TaskFilter(filters.FilterSet):
    is_finished = filters.BooleanFilter(field_name='is_finished')
    action = filters.ChoiceFilter(field_name='action', choices=Task.ACTION_CHOICES)
    annotator = filters.NumberFilter(field_name='annotator__id')
    annotator_username = filters.CharFilter(field_name='annotator__username')
