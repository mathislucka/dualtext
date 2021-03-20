from django_filters import rest_framework as filters
from .models import Annotation

class AnnotationFilter(filters.FilterSet):
    label = filters.NumberFilter(field_name='labels__id', lookup_expr='contains')
    label_name = filters.CharFilter(field_name='labels__name')
