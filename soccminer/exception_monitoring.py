

class ExceptionStack:
    def __init__(self):
        self.exception_dict = {}
        self.warning_dict = {}

    def set_project_stack(self, project_name):
        self.exception_dict[project_name] = []
        self.warning_dict[project_name] = []

    def update_exception_message(self, proj_name, error_message):
        self.exception_dict[proj_name].append(error_message)

    def update_warning_message(self, proj_name, error_message):
        self.warning_dict[proj_name].append(error_message)

