from django.urls import path, re_path
from rest_framework.authtoken.views import obtain_auth_token
from .views import LabelListView, ProjectListView, TaskListView, AnnotationListView, AnnotationDetailView
from .views import CorpusDetailView, DocumentListView, CorpusListView, DocumentDetailView, SearchView
from .views import CurrentUserView, ProjectDetailView, TaskDetailView

urlpatterns = [
    path('annotation/<int:annotation_id>', AnnotationDetailView.as_view(), name='annotation_detail'),
    path('corpus/<int:corpus_id>', CorpusDetailView.as_view(), name='corpus_detail'),
    path('document/<int:document_id>', DocumentDetailView.as_view(), name='document_detail'),
    path('corpus/<int:corpus_id>/document/', DocumentListView.as_view(), name='document_list'),
    path('corpus/', CorpusListView.as_view(), name='corpus_list'),
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('project/<int:project_id>', ProjectDetailView.as_view(), name='project_detail'),
    path('project/', ProjectListView.as_view(), name='project_list'),
    path('project/<int:project_id>/label', LabelListView.as_view(), name='label_list'),
    path('project/<int:project_id>/task/', TaskListView.as_view(), name='task_list'),
    path('task/<int:task_id>', TaskDetailView.as_view(), name='task_detail'),
    path('task/<int:task_id>/annotation/', AnnotationListView.as_view(), name='annotation_list'),
    path('user/current', CurrentUserView.as_view(), name='current_user'),
    re_path(r'search/$', SearchView.as_view(), name='search'),
]
