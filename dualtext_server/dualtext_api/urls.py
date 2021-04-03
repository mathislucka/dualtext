from django.urls import path, re_path
from rest_framework.authtoken.views import obtain_auth_token
from .views import LabelListView, ProjectListView, TaskListView, AnnotationListView, AnnotationDetailView
from .views import CorpusDetailView, DocumentListView, CorpusListView, DocumentDetailView, SearchView
from .views import CurrentUserView, CurrentUserStatisticsView, ProjectDetailView, TaskDetailView, ProjectStatisticsView
from .views import ClaimTaskView, FeatureListView, SearchMethodsView, FeatureDetailView, DocumentBatchView, GroupListView

urlpatterns = [
    path('annotation/<int:annotation_id>', AnnotationDetailView.as_view(), name='annotation_detail'),
    path('corpus/<int:corpus_id>', CorpusDetailView.as_view(), name='corpus_detail'),
    path('document/<int:document_id>', DocumentDetailView.as_view(), name='document_detail'),
    path('corpus/<int:corpus_id>/document/', DocumentListView.as_view(), name='document_list'),
    path('corpus/<int:corpus_id>/document/batch/', DocumentBatchView.as_view(), name='document_batch'),
    path('corpus/', CorpusListView.as_view(), name='corpus_list'),
    path('feature/', FeatureListView.as_view(), name='feature_list'),
    path('feature/<int:feature_id>', FeatureDetailView.as_view(), name='feature_detail'),
    path('group/', GroupListView.as_view(), name='group_list'),
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('project/<int:project_id>', ProjectDetailView.as_view(), name='project_detail'),
    path('project/<int:project_id>/statistics', ProjectStatisticsView.as_view(), name='project_statistics'),
    path('project/', ProjectListView.as_view(), name='project_list'),
    path('project/<int:project_id>/label', LabelListView.as_view(), name='label_list'),
    path('project/<int:project_id>/task/claim/<str:claim_type>/', ClaimTaskView.as_view(), name='task_claim'),
    path('project/<int:project_id>/task/claim/', ClaimTaskView.as_view(), name='task_claimable'),
    re_path(r'project/(?P<project_id>[0-9]+)/task/$', TaskListView.as_view(), name='task_list'),
    path('task/<int:task_id>', TaskDetailView.as_view(), name='task_detail'),
    re_path(r'task/(?P<task_id>[0-9]+)/annotation/$', AnnotationListView.as_view(), name='annotation_list'),
    path('user/current', CurrentUserView.as_view(), name='current_user'),
    path('user/current/statistics', CurrentUserStatisticsView.as_view(), name='current_user_statistics'),
    path('search/methods', SearchMethodsView.as_view(), name='search_methods'),
    re_path(r'search/$', SearchView.as_view(), name='search'),
]
