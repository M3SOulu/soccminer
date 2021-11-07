from soccminer.project_attributes import ProjectAttributes
from soccminer.proj_comments_main_attr import EntityLevelComprehensiveComment


class ComprehensiveCommentsAttribute(ProjectAttributes, EntityLevelComprehensiveComment):
    def __init__(self, project_instance):
        self.comprehensive_comment_obj = self
        super().__init__(project_instance)


