from soccminer.project_attributes import ProjectAttributes
from soccminer.proj_comments_main_attr import EntityLevelComprehensiveComment


class ComprehensiveCommentsAttribute(ProjectAttributes, EntityLevelComprehensiveComment):
    def __init__(self, project_instance):
        self.main_comment_list = project_instance.fetch_comments()
        self.file_level_comment_list = project_instance.file_level_comment_list
        #self.package_level_comment_list = project_instance.package_level_comment_list
        self.class_level_comment_list = project_instance.class_level_comment_list
        self.method_level_comment_list = project_instance.method_level_comment_list
        self.interface_level_comment_list = project_instance.interface_level_comment_list
        self.static_block_level_comment_list = project_instance.static_block_level_comment_list
        self.enum_level_comment_list = project_instance.enum_level_comment_list
        self.comprehensive_comment_obj = self
        super().__init__(project_instance)


