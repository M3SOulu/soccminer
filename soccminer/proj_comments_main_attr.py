from soccminer.project_attributes import ProjectAttributes


class EntityLevelComment:
    def __init__(self, project_instance):
        self.main_comment_list = project_instance.fetch_comments()
        self.file_level_comment_list = project_instance.file_level_comment_list
        #self.package_level_comment_list = project_instance.package_level_comment_list
        self.class_level_comment_list = project_instance.class_level_comment_list
        self.method_level_comment_list = project_instance.method_level_comment_list
        self.interface_level_comment_list = project_instance.interface_level_comment_list
        self.static_block_level_comment_list = project_instance.static_block_level_comment_list
        self.enum_level_comment_list = project_instance.enum_level_comment_list

    # following will only fetch comment text, source file and line no
    def get_file_level_comments(self):
        comment_list = []
        for comment in self.file_level_comment_list:
            comment_list.append(comment.get_comment_meta())
        return comment_list

    def get_comments(self):
        comment_list = []
        for comment in self.main_comment_list:
            comment_list.append(comment.get_comment_meta())
        return comment_list

    def get_class_level_comments(self):
        comment_list = []
        for comment in self.class_level_comment_list:
            comment_list.append(comment.get_comment_meta())
        return comment_list

    def get_enum_level_comments(self):
        comment_list = []
        for comment in self.enum_level_comment_list:
            comment_list.append(comment.get_comment_meta())
        return comment_list

    def get_method_level_comments(self):
        comment_list = []
        for comment in self.method_level_comment_list:
            comment_list.append(comment.get_comment_meta())
        return comment_list

    def get_interface_level_comments(self):
        comment_list = []
        for comment in self.interface_level_comment_list:
            comment_list.append(comment.get_comment_meta())
        return comment_list

    def get_static_block_level_comments(self):
        comment_list = []
        for comment in self.static_block_level_comment_list:
            comment_list.append(comment.get_comment_meta())
        return comment_list


class EntityLevelComprehensiveComment(EntityLevelComment):
    def __init__(self, project_instance):
        super().__init__(project_instance)

    def get_comprehensive_comment_attr(self):
        return self.main_comment_list

    def get_comprehensive_file_comment_attr(self):
        return self.file_level_comment_list

    def get_comprehensive_class_comment_attr(self):
        return self.class_level_comment_list

    def get_comprehensive_method_comment_attr(self):
        return self.method_level_comment_list

    def get_comprehensive_interface_comment_attr(self):
        return self.interface_level_comment_list

    def get_comprehensive_static_block_comment_attr(self):
        return self.static_block_level_comment_list

    def get_comprehensive_enum_comment_attr(self):
        return self.enum_level_comment_list


class CommentsMetaAttribute(ProjectAttributes, EntityLevelComment):
    def __init__(self, project_instance):
        self.comment_meta_obj = self
        self.main_comment_list = project_instance.fetch_comments()
        self.file_level_comment_list = project_instance.file_level_comment_list
        #self.package_level_comment_list = project_instance.package_level_comment_list
        self.class_level_comment_list = project_instance.class_level_comment_list
        self.method_level_comment_list = project_instance.method_level_comment_list
        self.interface_level_comment_list = project_instance.interface_level_comment_list
        self.static_block_level_comment_list = project_instance.static_block_level_comment_list
        self.enum_level_comment_list = project_instance.enum_level_comment_list
        super().__init__(project_instance)




