from dualtext_api.models import Label

class LabelService():
    def __init__(self):
        self.colors = [
            {"standard": "#97E8D8", "light": "#EAFAF7"},
            {"standard": "#F68D89", "light": "#FDE8E7"},
            {"standard": "#8095FF", "light": "#E5EAFF"},
            {"standard": "#F380FF", "light": "#FDE5FF"},
            {"standard": "#F0C1EB", "light": "#FAEAF8"},
            {"standard": "#FFA380", "light": "#FFEDE5"},
            {"standard": "#FDEB81", "light": "#FFFBE6"},
            {"standard": "#E1AC9E", "light": "#F9EEEC"},
            {"standard": "#C5D7A8", "light": "#F3F7EE"},
            {"standard": "#CCB2C8", "light": "#F5F0F4"},
            {"standard": "#F3CA8C", "light": "#FDF4E8"},
            {"standard": "#B2C1CC", "light": "#F0F3F5"},
            {"standard": "#A4E896", "light": "#EDFAEA"},
            {"standard": "#81BEFE", "light": "#E6F2FF"},
            {"standard": "#FC839C", "light": "#FEE6EB"},
            {"standard": "#FFF880", "light": "#FFFEE5"},
            {"standard": "#97DEE7", "light": "#EAF8FA"},
            {"standard": "#ABD2D4", "light": "#EEF6F6"},
            {"standard": "#DCB2A3", "light": "#F8F0ED"},
        ]
        self.default_color = {"standard": "#97C0E8", "light": "#EAF2FA"}
    
    def create(self, serializer, project):
        color = self.find_unused_color(project)
        return serializer.save(project=project, color=color)

    def find_unused_color(self, project):
        unused_color = self.default_color
        for color in self.colors:
            already_used = Label.objects.filter(project=project).filter(color=color).count()
            if already_used == 0:
                unused_color = color
                break
        return unused_color

