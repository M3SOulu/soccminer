

class ProjectAttributes:
    def __init__(self, project_instance):
        self.project_instance = project_instance
        self.proj_name = project_instance.get_project_name()
        self.proj_loc = project_instance.get_project_loc()
        self.source_file_count = len(project_instance.get_project_source_files().get_files())

    def get_project_name(self):
        """
        Returns the project name.
                :param: None
                :returns: Name of the project
                :rtype: str
        """
        return self.proj_name

    def get_project_loc(self):
        """
        Returns the project kloc.
                :param: None
                :returns: KLOC of the project
                :rtype: float
        """
        return self.proj_loc

    def get_source_file_count(self):
        """
        Returns the count of source files in the project.
                :param: None
                :returns: Count of source files in the project
                :rtype: int
        """
        return self.source_file_count
