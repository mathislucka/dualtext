from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Project, Corpus

def check_member_status(entity, user):
    user_groups = user.groups.all()
    entity_groups = entity.allowed_groups.all()
    ug_set = set(user_groups)
    eg_set = set(entity_groups)
    return bool(len(ug_set.intersection(eg_set)) > 0 or user.is_superuser)

class MembersEdit(BasePermission):
    def has_permission(self, request, view):
        entity = None
        if 'corpus_id' in view.kwargs:
            entity = Corpus.objects.get(id=view.kwargs['corpus_id'])
        elif 'project_id' in view.kwargs:
            entity = Project.objects.get(id=view.kwargs['project_id'])
        
        if entity is not None and request.user:
            return check_member_status(entity, request.user)
        else:
            return False
    
    def has_object_permission(self, request, view, obj):
        if request.user:
            return check_member_status(obj, request.user)
        else:
            return False

class MembersReadAdminEdit(BasePermission):
    def has_permission(self, request, view):
        # allow reads for users in the allowed_groups of a project and for superusers
        if request.method in SAFE_METHODS:
            if 'corpus_id' in view.kwargs:
                entity = Corpus.objects.get(id=view.kwargs['corpus_id'])
            elif 'project_id' in view.kwargs:
                entity = Project.objects.get(id=view.kwargs['project_id'])
            if entity and request.user:
                return check_member_status(entity, request.user)
            else:
                return False
        # restrict creation to admin users
        else:
            return bool(request.user and request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            if request.user:
                return check_member_status(obj, request.user)
        else:
            return bool(request.user.is_superuser)

class AuthenticatedReadAdminCreate(BasePermission):
    def has_permission(self, request, view):
        # allow reads for authenticated users
        if request.method in SAFE_METHODS:
            return bool(request.user.is_authenticated)
        # restrict creation to admin users
        else:
            return bool(request.user and request.user.is_superuser == True)

class TaskPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        # allow access to all tasks for admins
        if request.user and request.user.is_superuser == True:
            return True
        # allow access to assigned annotators
        else:
            return bool(request.user == obj.annotator)

class AnnotationPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        # allow access to all annotations for admins
        if request.user and request.user.is_superuser == True:
            return True
        # allow access to assigned annotators
        else:
            print(obj.task.annotator)
            return bool(request.user == obj.task.annotator)

class DocumentPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        # allow access to all documents for admins
        if request.user and request.user.is_superuser == True:
            return True
        # allow access to corpus members only
        else:
            return check_member_status(obj.corpus, request.user)

class AdminReadOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS and request.user and request.user.is_superuser:
            return True
        else:
            return False
