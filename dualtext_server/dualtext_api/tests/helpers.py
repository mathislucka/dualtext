from django.contrib.auth.models import User, Group
from dualtext_api.models import Project

def run_standard_setup():
    superuser = User(username="superuser", is_superuser = True, password='pass')
    superuser.save()
    group = Group(name='project_members')
    group.save()
    user = User(username="normal", password="pass")
    user.save()
    user.groups.add(group)
    user.save()
    project = Project(name="TestProject", creator=superuser)
    project.save()
    project.allowed_groups.add(group)
    project.save()
    return {'project': project, 'superuser': superuser, 'group': group, 'user': user}
