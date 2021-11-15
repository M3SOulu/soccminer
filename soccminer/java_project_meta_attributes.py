from soccminer.project_attributes import ProjectAttributes


class JavaFileMeta:
    def __init__(self):
        self.source_file_name = None
        self.file_loc = None
        self.total_comments = None

    def get_file_name(self):
        return self.source_file_name

    def get_file_loc(self):
        return self.file_loc

    def set_file_loc(self, loc):
        self.file_loc = loc

    def set_file_name(self, filename):
        self.source_file_name = filename

    def set_file_comment_count(self, comment_count):
        self.total_comments = comment_count

    def get_file_comment_count(self):
        return self.total_comments


class JavaPackageMeta:
    def __init__(self):
        self.package_name = None
        self.package_loc = None
        self.package_line_no = None
        self.source_file_name = None

    def get_package_line_no(self):
        return self.package_line_no if self.package_line_no is not None else "NA"

    def get_package_name(self):
        return self.package_name if self.package_name is not None else "ANONYMOUS"

    def get_package_loc(self):
        return self.package_loc

    def set_package_loc(self, loc):
        self.package_loc = loc

    def get_package_source(self):
        return self.source_file_name

    def set_package_source(self, filename):
        self.source_file_name = filename

    def set_package_name(self, package_name):
        self.package_name = package_name

    def set_package_line_no(self, package_line_no):
        self.package_line_no = package_line_no


class JavaClassMeta:
    def __init__(self):
        self.class_name = None
        self.class_type = None
        self.class_specifier = None
        self.class_line_no = None
        self.nested_level = None
        self.class_signature = None
        self.class_loc = None
        self.class_source_file = None

    def get_class_loc(self):
        return self.class_loc

    def set_class_loc(self, loc):
        self.class_loc = loc

    def get_class_source(self):
        return self.class_source_file

    def set_class_source(self, file_name):
        self.class_source_file = file_name

    def set_class_signature(self, signature):
        self.class_signature = signature

    def set_nested_level(self, nested_level):
        self.nested_level = nested_level

    def set_class_name(self, class_name):
        self.class_name = class_name

    def set_class_type(self, class_type):
        self.class_type = class_type

    def set_class_specifier(self, class_specifier):
        self.class_specifier = class_specifier

    def set_class_line_no(self, line_no):
        self.class_line_no = line_no

    def get_class_signature(self):
        return self.class_signature

    def get_nested_level(self):
        return self.nested_level

    def get_class_name(self):
        return self.class_name

    def get_class_type(self):
        return self.class_type

    def get_class_specifier(self):
        return self.class_specifier

    def get_class_line_no(self):
        return self.class_line_no


class JavaEnumMeta:
    def __init__(self):
        self.enum_name = None
        self.enum_specifier = None
        self.enum_line_no = None
        self.enum_signature = None
        self.enum_loc = None
        self.enum_source_file = None

    def get_enum_loc(self):
        return self.enum_loc

    def set_enum_loc(self, loc):
        self.enum_loc = loc

    def get_enum_source(self):
        return self.enum_source_file

    def set_enum_source(self, file_name):
        self.enum_source_file = file_name

    def set_enum_signature(self, signature):
        self.enum_signature = signature

    def set_enum_name(self, enum_name):
        self.enum_name = enum_name

    def set_enum_specifier(self, enum_specifier):
        self.enum_specifier = enum_specifier

    def set_enum_line_no(self, line_no):
        self.enum_line_no = line_no

    def get_enum_signature(self):
        return self.enum_signature

    def get_enum_name(self):
        return self.enum_name

    def get_enum_specifier(self):
        return self.enum_specifier

    def get_enum_line_no(self):
        return self.enum_line_no


class JavaMethodMeta:
    def __init__(self):
        self.method_name = None
        self.method_type = None
        self.method_specifier = None
        self.method_line_no = None
        self.method_category = None
        self.method_signature = None
        self.method_loc = None
        self.method_param_count = None
        self.method_source_file = None

    def get_method_source(self):
        return self.method_source_file

    def set_method_source(self, file_name):
        self.method_source_file = file_name

    def get_method_loc(self):
        return self.method_loc

    def set_method_loc(self, loc):
        self.method_loc = loc

    def set_method_name(self, name):
        self.method_name = name

    def set_method_signature(self, signature):
        self.method_signature = signature

    def set_method_param_cnt(self, param_cnt):
        self.method_param_count = param_cnt

    def set_method_specifier(self, specifier):
        self.method_specifier = specifier

    def set_method_type(self, method_type):
        self.method_type = method_type

    def set_method_category(self, category):
        self.method_category = category

    def set_method_line_no(self, line_no):
        self.method_line_no = line_no

    def get_method_name(self):
        return self.method_name

    def get_method_signature(self):
        return self.method_signature

    def get_method_param_cnt(self):
        return self.method_param_count

    def get_method_specifier(self):
        return self.method_specifier

    def get_method_type(self):
        return self.method_type

    def get_method_category(self):
        return self.method_category

    def get_method_line_no(self):
        return self.method_line_no


class JavaInterfaceMeta:
    def __init__(self):
        self.interface_name = None
        self.interface_signature = None
        self.interface_specifier = None
        self.interface_line_no = None
        self.interface_loc = None
        self.interface_source_file = None

    def get_interface_source(self):
        return self.interface_source_file

    def set_interface_source(self, file_name):
        self.interface_source_file = file_name

    def get_interface_loc(self):
        return self.interface_loc

    def set_interface_loc(self, loc):
        self.interface_loc = loc

    def set_interface_name(self, name):
        self.interface_name = name

    def set_interface_signature(self, signature):
        self.interface_signature = signature

    def set_interface_specifier(self, specifier):
        self.interface_specifier = specifier

    def set_interface_line_no(self, line_no):
        self.interface_line_no = line_no

    def get_interface_name(self):
        return self.interface_name

    def get_interface_signature(self):
        return self.interface_signature

    def get_interface_specifier(self):
        return self.interface_specifier

    def get_interface_line_no(self):
        return self.interface_line_no


class JavaStaticBlockMeta:
    def __init__(self):
        self.static_block_line_no = None
        self.static_block_loc = None
        self.static_block_source_file = None

    def get_static_block_source(self):
        return self.static_block_source_file

    def set_static_block_source(self, file_name):
        self.static_block_source_file = file_name

    def get_static_block_loc(self):
        return self.static_block_loc

    def set_static_block_loc(self, loc):
        self.static_block_loc = loc

    def set_static_block_line_no(self, line_no):
        self.static_block_line_no = line_no

    def get_static_block_line_no(self):
        return self.static_block_line_no


class JavaMetaAttribute(ProjectAttributes):
    def __init__(self, project_instance):
        self.source_file_count = len(project_instance.get_files())
        self.package_count = len(project_instance.get_packages())
        self.class_count = len(project_instance.get_classes())
        self.method_count = len(project_instance.get_methods())
        self.interface_count = len(project_instance.get_interfaces())
        self.static_block_count = len(project_instance.get_static_blocks())
        self.enum_count = len(project_instance.get_enums())
        super().__init__(project_instance)

    def get_package_count(self):
        """
        Returns the count of packages in the Java project.
                :param: None
                :returns: Count of packages in the project
                :rtype: int
        """
        return self.package_count

    def get_file_count(self):
        """
        Returns the count of packages in the Java project.
                :param: None
                :returns: Count of packages in the project
                :rtype: int
        """
        return self.source_file_count

    def get_class_count(self):
        """
        Returns the count of classes in the Java project.
                :param: None
                :returns: Count of classes in the project
                :rtype: int
        """
        return self.class_count

    def get_enum_count(self):
        """
        Returns the count of enums in the Java project.
                :param: None
                :returns: Count of enums in the project
                :rtype: int
        """
        return self.enum_count

    def get_method_count(self):
        """
        Returns the count of methods in the Java project.
                :param: None
                :returns: Count of methods in the project
                :rtype: int
        """
        return self.method_count

    def get_interface_count(self):
        """
        Returns the count of interfaces in the Java project.
                :param: None
                :returns: Count of interfaces in the project
                :rtype: int
        """
        return self.interface_count

    def get_static_block_count(self):
        """
        Returns the count of static blocks in the Java project.
                :param: None
                :returns: Count of static blocks in the project
                :rtype: int
        """
        return self.static_block_count

    def get_file_meta_attr(self):
        """
        Fetches File Meta Attributes for all source files in a project.
        for example (Java): Source File name, File LOC etc.,
                :param: None
                :returns: List of :class: JavaFileMeta objects
                :rtype: list
        """
        file_meta = []
        for source_file_obj in self.project_instance.get_packages():
            file_obj = JavaFileMeta()
            file_obj.set_file_name(source_file_obj.get_file_name())
            file_obj.set_file_loc(source_file_obj.get_file_loc())
            file_obj.set_file_comment_count(source_file_obj.get_file_comment_count())
            file_meta.append(file_obj)
        return file_meta

    def get_package_meta_attr(self):
        """
        Fetches Package Meta Attributes for all packages in a project.
        for example (Java): Package name, Package LOC etc.,
                :param: None
                :returns: List of :class: JavaPackageMeta objects
                :rtype: list
        """
        package_meta = []
        for package_obj in self.project_instance.get_packages():
            pckg_obj = JavaPackageMeta()
            pckg_obj.set_package_name(package_obj.get_package_name())
            pckg_obj.set_package_loc(package_obj.get_package_loc())
            pckg_obj.set_package_line_no(package_obj.get_package_line_no())
            pckg_obj.set_package_source(package_obj.get_package_source())
            package_meta.append(pckg_obj)
        return package_meta

    def get_class_meta_attr(self):
        """
        Fetches Class Meta Attributes (total of 8 meta attributes) for all classes in a project.
        for example (Java): Class name, Class LOC, Class Nested Level etc.,
                :param: None
                :returns: List of :class: JavaClassMeta objects
                :rtype: list
        """
        class_meta = []
        for class_obj in self.project_instance.get_classes():
            cls_obj = JavaClassMeta()
            cls_obj.set_class_name(class_obj.get_class_name())
            cls_obj.set_class_type(class_obj.get_class_type())
            cls_obj.set_class_specifier(class_obj.get_class_specifier())
            cls_obj.set_class_line_no(class_obj.get_class_line_no())
            cls_obj.set_nested_level(class_obj.get_nested_level())
            cls_obj.set_class_signature(class_obj.get_class_signature())
            cls_obj.set_class_loc(class_obj.get_class_loc())
            cls_obj.set_class_source(class_obj.get_class_source())
            class_meta.append(cls_obj)
        return class_meta

    def get_enum_meta_attr(self):
        """
        Fetches Enum Meta Attributes (total of 6 meta attributes) for all classes in a project.
        for example (Java): Enum name, Enum LOC, etc.,
                :param: None
                :returns: List of :class: EnumClassMeta objects
                :rtype: list
        """
        enum_meta = []
        for enum_obj in self.project_instance.get_enums():
            enm_obj = JavaClassMeta()
            enm_obj.set_class_name(enum_obj.get_enum_name())
            enm_obj.set_class_specifier(enum_obj.get_enum_specifier())
            enm_obj.set_class_line_no(enum_obj.get_enum_line_no())
            enm_obj.set_class_signature(enum_obj.get_enum_signature())
            enm_obj.set_class_loc(enum_obj.get_enum_loc())
            enm_obj.set_class_source(enum_obj.get_enum_source())
            enum_meta.append(enm_obj)
        return enum_meta

    def get_method_meta_attr(self):
        """
        Fetches Method Meta Attributes (total of 9 meta attributes) for all methods in a project.
        for example (Java): Method name, Method LOC, etc.,
                :param: None
                :returns: List of :class: JavaMethodMeta objects
                :rtype: list
        """
        method_meta = []
        for method_obj in self.project_instance.get_methods():
            mthd_obj = JavaMethodMeta()
            mthd_obj.set_method_name(method_obj.get_method_name())
            mthd_obj.set_method_type(method_obj.get_method_type())
            mthd_obj.set_method_specifier(method_obj.get_method_specifier())
            mthd_obj.set_method_line_no(method_obj.get_method_line_no())
            mthd_obj.set_method_category(method_obj.get_method_category())
            mthd_obj.set_method_signature(method_obj.get_method_signature())
            mthd_obj.set_method_loc(method_obj.get_method_loc())
            mthd_obj.set_method_param_cnt(method_obj.get_method_param_cnt())
            mthd_obj.set_method_source(method_obj.get_method_source())
            method_meta.append(mthd_obj)
        return method_meta

    def get_interface_meta_attr(self):
        """
        Fetches Interface Meta Attributes (total of 6 meta attributes) for all interfaces in a project.
        for example (Java): Interface name, Interface LOC, etc.,
                :param: None
                :returns: List of :class: JavaMethodMeta objects
                :rtype: list
        """
        interface_meta = []
        for interface_obj in self.project_instance.get_interfaces():
            intrfc_obj = JavaInterfaceMeta()
            intrfc_obj.set_interface_name(interface_obj.get_interface_name())
            intrfc_obj.set_interface_signature(interface_obj.get_interface_signature())
            intrfc_obj.set_interface_specifier(interface_obj.get_interface_specifier())
            intrfc_obj.set_interface_line_no(interface_obj.get_interface_line_no())
            intrfc_obj.set_interface_loc(interface_obj.get_interface_loc())
            intrfc_obj.set_interface_source(interface_obj.get_interface_source())
            interface_meta.append(intrfc_obj)
        return interface_meta

    def get_static_block_meta_attr(self):
        """
        Fetches Static Block Meta Attributes (total of 3 meta attributes) for all interfaces in a project.
        for example (Java): Static Block source, Static Block Line no., Static Block LOC.
                :param: None
                :returns: List of :class: JavaStaticBlockMeta objects
                :rtype: list
        """
        static_block_meta = []
        for static_block_obj in self.project_instance.get_static_blocks():
            stat_blk_obj = JavaStaticBlockMeta()
            stat_blk_obj.set_static_block_line_no(static_block_obj.get_static_block_line_no())
            stat_blk_obj.set_static_block_loc(static_block_obj.get_static_block_loc())
            stat_blk_obj.set_static_block_source(static_block_obj.get_static_block_source())
            static_block_meta.append(stat_blk_obj)
        return static_block_meta
