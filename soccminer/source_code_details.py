class MethodInfo:
    def __init__(self):
        self.method_detail = {}
        self.method_name = None
        self.method_signature = None
        self.method_param_count = None
        self.method_specifier = None
        self.method_type = None
        self.method_category = None
        self.method_line_no = None
        self.nested_class_in_method_info = []
        self.method_level_comments = []
        self.method_loc = 0
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

    def get_method_info_comments(self):
        return self.method_level_comments

    def get_method_info(self):
        self.method_detail["METHOD_NAME"] = self.method_name
        self.method_detail["METHOD_SIGNATURE"] = self.method_signature
        self.method_detail["METHOD_PARAM_COUNT"] = self.method_param_count
        self.method_detail["METHOD_SPECIFIER"] = self.method_specifier
        self.method_detail["METHOD_TYPE"] = self.method_type
        self.method_detail["METHOD_CATEGORY"] = self.method_category
        self.method_detail["METHOD_LINE_NO"] = self.method_line_no
        self.method_detail["METHOD_LOC"] = self.method_loc
        return self.method_detail

    def get_method_info_and_comments(self):
        method_meta_info_and_comments = {}
        method_meta_info_and_comments["METHOD_META"]=self.get_method_info()
        method_meta_info_and_comments["METHOD_COMMENTS"] = self.get_method_info_comments()
        return method_meta_info_and_comments

    def get_all_method_info_and_comments(self):
        all_method_meta_info_and_comments = {} #get_all_comments_from_method
        all_method_meta_info_and_comments["METHOD_META"]=self.get_method_info()
        all_method_meta_info_and_comments["METHOD_COMMENTS"] = self.get_all_comments_from_method()
        return all_method_meta_info_and_comments

    def append_method_level_comments(self, comment_obj):
        self.method_level_comments.append(comment_obj)

    def append_class_in_method_info(self, class_obj):
        self.nested_class_in_method_info.append(class_obj)

    def get_nested_class_in_method(self):
        return self.nested_class_in_method_info

    def get_all_comments_from_method(self):
        method_all_comments = self.get_method_info_comments()
        for class_obj in self.nested_class_in_method_info:  # can have a class inside a method
            method_all_comments.extend(class_obj.get_all_comments_from_class())
        return method_all_comments
        # why this has come here? not sure! need to validate.
        #for method_obj in self.method_level_comments:
        #    method_all_comments.extend(method_obj.get_all_comments_from_method())
        #return method_all_comments


class EnumInfo:
    def __init__(self):
        self.enum_detail = {}
        self.enum_name = None
        self.enum_specifier = None
        self.enum_line_no = None
        self.enum_source_file = None
        self.enum_signature = None
        self.enum_nested_level = 0
        self.enum_level_comments = []  # comments that are inside enum but not in method or static blocks
        self.enum_method_info = []     # for methods inside enum
        self.enum_static_block_info = []     # for static blocks inside enum
        self.enum_interface_info = []         # for holding interfaces
        self.enum_loc = 0

    def get_enum_loc(self):
        return self.enum_loc

    def set_enum_loc(self, loc):
        self.enum_loc = loc

    def get_enum_source(self):
        return self.enum_source_file

    def set_enum_source(self, file_name):
        self.enum_source_file = file_name

    def get_enum_interface_info(self):
        return self.enum_interface_info

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

    def get_enum_info_comments(self):
        return self.enum_level_comments

    def get_all_comments_from_enum(self):
        enum_all_comments = self.get_enum_info_comments()

        for enum_method_obj in self.enum_method_info:
            enum_all_comments.extend(enum_method_obj.get_method_info_comments())

        for static_block_obj in self.enum_static_block_info:
            enum_all_comments.extend(static_block_obj.get_static_block_info_comments())

        for interface_obj in self.enum_interface_info:
            enum_all_comments.extend(interface_obj.get_interface_info_comments())

    def get_enum_info(self):
        self.enum_detail["ENUM_NAME"] = self.enum_name
        self.enum_detail["ENUM_SPECIFIER"] = self.enum_specifier
        self.enum_detail["ENUM_LINE_NO"] = self.enum_line_no
        self.enum_detail["ENUM_SIGNATURE"] = self.enum_signature
        self.enum_detail["ENUM_LOC"] = self.enum_loc
        self.enum_detail["ENUM_METHOD_INFO"] = self.enum_method_info
        self.enum_detail["ENUM_STATIC_BLOCK_INFO"] = self.enum_static_block_info
        self.enum_detail["ENUM_INTERFACE_INFO"] = self.enum_interface_info
        return self.enum_detail

    # returns comments that are inside enum but not in method or static blocks;
    # invoke get_all_comments_from_enum to fetch all comments inside a enum
    def get_enum_info_and_comments(self):
        enum_meta_info_and_comments = {}
        enum_meta_info_and_comments["ENUM_META"]=self.get_enum_info()
        enum_meta_info_and_comments["ENUM_COMMENTS"] = self.get_enum_info_comments()
        enum_meta_info_and_comments["ENUM_ALL_COMMENTS"] = self.get_all_comments_from_enum()
        return enum_meta_info_and_comments

    def get_static_block(self):
        return self.enum_static_block_info

    def append_enum_level_comments(self, comment_obj):
        self.enum_level_comments.append(comment_obj)

    def append_enum_method_info(self, method_obj):
        self.enum_method_info.append(method_obj)

    def append_static_block_info(self, static_block_obj):
        self.enum_static_block_info.append(static_block_obj)

    def append_enum_lvl_interface_info(self, interface_obj):
        self.enum_interface_info.append(interface_obj)

    def get_method_info(self):
        return self.enum_method_info
###


class StaticBlockInfo:
    def __init__(self):
        self.static_block_detail = {}
        self.static_block_line_no = None
        self.static_block_comments = []
        self.static_block_loc = 0
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

    def get_static_block_info_comments(self):
        return self.static_block_comments

    def get_static_block_info(self):
        self.static_block_detail["STATIC_BLOCK_LINE_NO"] = self.static_block_line_no
        self.static_block_detail["STATIC_BLOCK_LOC"] = self.static_block_loc
        return self.static_block_detail

    def get_stat_block_info_and_comments(self):
        stat_block_meta_info_and_comments = {}
        stat_block_meta_info_and_comments["STAT_BLOCK_META"]=self.get_static_block_info()
        stat_block_meta_info_and_comments["STAT_BLOCK_COMMENTS"] = self.get_static_block_info_comments()
        return stat_block_meta_info_and_comments

    def append_static_block_level_comments(self, comment_obj):
        self.static_block_comments.append(comment_obj)


class ClassInfo:
    def __init__(self):
        self.class_detail = {}
        self.class_name = None
        self.class_type = None           # generic or derived or anonymous or regular
        self.class_specifier = None
        self.class_line_no = None
        self.nested_level = None
        self.class_source_file = None
        self.class_signature = None
        self.class_level_comments = []  # comments that are inside class but not in method or static blocks
        self.class_method_info = []     # for methods inside class
        self.static_block_info = []     # for static blocks inside class
        self.nested_class_info = []     # for holding nested class
        self.interface_info = []         # for holding interfaces
        self.class_loc = 0

    def get_class_loc(self):
        return self.class_loc

    def set_class_loc(self, loc):
        self.class_loc = loc

    def get_class_source(self):
        return self.class_source_file

    def set_class_source(self, file_name):
        self.class_source_file = file_name

    def get_interface_info(self):
        return self.interface_info

    def get_nested_class_info(self):
        return self.nested_class_info

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

    def get_class_info_comments(self):
        return self.class_level_comments

    def process_nested_level(self, level):
        if len(self.get_nested_class_info()) == 0:
            return
        for nested_class in self.get_nested_class_info():
            nested_class.set_nested_level(level)
        for nested_class in self.get_nested_class_info():
            nested_class.process_nested_level(level + 1)

    def get_all_comments_from_class(self):
        class_all_comments = self.get_class_info_comments()

        for class_method_obj in self.class_method_info:
            class_all_comments.extend(class_method_obj.get_method_info_comments())

        for class_method_obj in self.class_method_info:
            for class_in_method_obj in class_method_obj.get_nested_class_in_method():
                class_all_comments.extend(class_in_method_obj.get_all_comments_from_class())

        for static_block_obj in self.static_block_info:
            class_all_comments.extend(static_block_obj.get_static_block_info_comments())

        for interface_obj in self.interface_info:
            class_all_comments.extend(interface_obj.get_interface_info_comments())

        for nested_class_obj in self.nested_class_info:
            class_all_comments.extend(nested_class_obj.get_all_comments_from_class())
        return class_all_comments

    def get_class_info(self):
        self.class_detail["CLASS_NAME"] = self.class_name
        self.class_detail["CLASS_TYPE"] = self.class_type
        self.class_detail["CLASS_SPECIFIER"] = self.class_specifier
        self.class_detail["CLASS_LINE_NO"] = self.class_line_no
        self.class_detail["NESTED_LEVEL"] = self.nested_level
        self.class_detail["CLASS_SIGNATURE"] = self.class_signature
        self.class_detail["CLASS_LOC"] = self.class_loc
        self.class_detail["CLASS_METHOD_INFO"] = self.class_method_info
        self.class_detail["CLASS_STATIC_BLOCK_INFO"] = self.static_block_info
        self.class_detail["CLASS_INTERFACE_INFO"] = self.interface_info
        self.class_detail["NESTED_CLASS_INFO"] = self.nested_class_info
        return self.class_detail

    # returns comments that are inside class but not in method or static blocks;
    # invoke get_all_comments_from_class to fetch all comments inside a class
    def get_class_info_and_comments(self):
        class_meta_info_and_comments = {}
        class_meta_info_and_comments["CLASS_META"]=self.get_class_info()
        class_meta_info_and_comments["CLASS_COMMENTS"] = self.get_class_info_comments()
        class_meta_info_and_comments["CLASS_ALL_COMMENTS"] = self.get_all_comments_from_class()
        return class_meta_info_and_comments

    def get_static_block(self):
        return self.static_block_info

    def append_class_level_comments(self, comment_obj):
        self.class_level_comments.append(comment_obj)

    def append_class_method_info(self, method_obj):
        self.class_method_info.append(method_obj)

    def append_static_block_info(self, static_block_obj):
        self.static_block_info.append(static_block_obj)

    def append_class_lvl_interface_info(self, interface_obj):
        self.interface_info.append(interface_obj)

    def append_nested_class_info(self, class_info_obj):
        self.nested_class_info.append(class_info_obj)

    def get_class_method_info(self):
        return self.class_method_info


class InterfaceInfo:
    def __init__(self):
        self.interface_detail = {}
        self.interface_name = None
        self.interface_line_no = None
        self.interface_specifier = None
        self.interface_signature = None
        self.interface_comments = []
        self.interface_method_info = []
        self.nested_class_info = []
        self.interface_loc = 0
        self.interface_source_file = None

    def get_interface_source(self):
        return self.interface_source_file

    def set_interface_source(self, file_name):
        self.interface_source_file = file_name

    def get_interface_loc(self):
        return self.interface_loc

    def set_interface_loc(self, loc):
        self.interface_loc = loc

    def append_class_in_interface_info(self, class_obj):
        self.nested_class_info.append(class_obj)

    def get_class_in_interface_info(self):
        return self.nested_class_info

    def get_interface_method_info(self):
        return self.interface_method_info

    def set_interface_name(self, name):
        self.interface_name = name

    def set_interface_signature(self, signature):
        self.interface_signature = signature

    def set_interface_specifier(self, specifier):
        self.interface_specifier = specifier

    def set_interface_line_no(self, line_no):
        self.interface_line_no = line_no

    def get_interface_info_comments(self):
        return self.interface_comments

    def get_interface_name(self):
        return self.interface_name

    def get_interface_signature(self):
        return self.interface_signature

    def get_interface_specifier(self):
        return self.interface_specifier

    def get_interface_line_no(self):
        return self.interface_line_no

    def get_all_comments_from_interface(self):
        interface_all_comments = self.get_interface_info_comments()
        for interface_method_obj in self.interface_method_info:
            interface_all_comments.extend(interface_method_obj.get_method_info_comments())
        return interface_all_comments

    def get_interface_info(self):
        self.interface_detail["INTERFACE_NAME"] = self.interface_name
        self.interface_detail["INTERFACE_SPECIFIER"] = self.interface_specifier
        self.interface_detail["INTERFACE_SIGNATURE"] = self.interface_signature
        self.interface_detail["INTERFACE_LINE_NO"] = self.interface_line_no
        self.interface_detail["INTERFACE_LOC"] = self.interface_loc
        self.interface_detail["INTERFACE_METHOD_INFO"] = self.interface_method_info
        return self.interface_detail

    def get_interface_info_and_comments(self):
        interface_meta_info_and_comments = {}
        interface_meta_info_and_comments["INTERFACE_META"]=self.get_interface_info()
        interface_meta_info_and_comments["INTERFACE_COMMENTS"] = self.get_interface_info_comments()
        interface_meta_info_and_comments["INTERFACE_ALL_COMMENTS"] = self.get_all_comments_from_interface()
        return interface_meta_info_and_comments

    def append_interface_level_comments(self, comment_obj):
        self.interface_comments.append(comment_obj)

    def append_interface_method_info(self, method_obj):
        self.interface_method_info.append(method_obj)


class PackageInfo:
    def __init__(self):
        self.package_detail = {}
        self.package_name = None
        self.package_line_no = None
        self.source_file_name = None
        self.package_level_comments = []  # Comments inside a package but outside any construct such as class, interface, etc.,
        self.class_info = []
        self.enum_info = []
        self.interface_info = []
        self.method_info = []
        self.static_block_info = []
        self.package_loc = 0

    def append_package_static_block_info(self, static_block_obj):
        self.static_block_info.append(static_block_obj)

    def get_package_static_block(self):
        return self.static_block_info

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

    def get_package_class_info(self):
        return self.class_info

    def get_package_interface_info(self):
        return self.interface_info

    def get_method_info(self):
        return self.method_info

    def get_package_info_comments(self):
        return self.package_level_comments

    def get_all_info(self):
        all_construct_info = {}
        all_construct_info["PACKAGE_NAME"] = self.package_name
        all_construct_info["PACKAGE_LINE_NO"] = self.package_line_no
        all_construct_info["CLASS_INFO"] = self.class_info
        all_construct_info["INTERFACE_INFO"] = self.interface_info
        all_construct_info["METHOD_INFO"] = self.method_info
        all_construct_info["ENUM_INFO"] = self.enum_info
        package_all_comments = self.get_package_info_comments()
        for class_obj in self.class_info:
            package_all_comments.extend(class_obj.get_all_comments_from_class())

        for interface_obj in self.interface_info:
            package_all_comments.extend(interface_obj.get_all_comments_from_interface())

        for method_obj in self.method_info:
            package_all_comments.extend(method_obj.get_all_comments_from_method())

        for enum_obj in self.enum_info:
            package_all_comments.extend(enum_obj.get_all_comments_from_enum())

        all_construct_info["CLASS_INFO"] = self.class_info
        all_construct_info["INTERFACE_INFO"] = self.interface_info
        all_construct_info["METHOD_INFO"] = self.method_info
        return all_construct_info

    def get_all_comments_from_package(self):
        package_all_comments = self.get_package_info_comments()
        for class_obj in self.class_info:
            package_all_comments.extend(class_obj.get_all_comments_from_class())

        for interface_obj in self.interface_info:
            package_all_comments.extend(interface_obj.get_all_comments_from_interface())

        for method_obj in self.method_info:
            package_all_comments.extend(method_obj.get_all_comments_from_method())

        for static_block_obj in self.static_block_info:
            package_all_comments.extend(static_block_obj.get_static_block_info_comments())

        for enum_obj in self.enum_info:
            package_all_comments.extend(enum_obj.get_all_comments_from_enum())

        return package_all_comments

    def get_package_info(self):
        self.package_detail["PACKAGE_NAME"] = self.package_name
        self.package_detail["PACKAGE_LINE_NO"] = self.package_line_no
        self.package_detail["PACKAGE_LOC"] = self.package_loc
        self.package_detail["CLASS_INFO"] = self.class_info
        self.package_detail["INTERFACE_INFO"] = self.interface_info
        self.package_detail["METHOD_INFO"] = self.method_info
        self.package_detail["STATIC_BLOCK_INFO"] = self.static_block_info
        return self.package_detail

    def get_package_info_and_comments(self):
        package_meta_info_and_comments = {}
        package_meta_info_and_comments["PACKAGE_META"] = self.get_package_info()
        package_meta_info_and_comments["PACKAGE_COMMENTS"] = self.get_package_info_comments()
        package_meta_info_and_comments["PACKAGE_ALL_COMMENTS"] = self.get_all_comments_from_package()
        return package_meta_info_and_comments

    def append_package_level_comments(self, comment_obj):
        self.package_level_comments.append(comment_obj)

    def append_class_info(self, class_info_obj):
        self.class_info.append(class_info_obj)

    def append_enum_info(self, enum_info_obj):
        self.enum_info.append(enum_info_obj)

    def append_interface_info(self, interface_info_obj):
        self.interface_info.append(interface_info_obj)

    def append_method_info(self, method_info_obj):
        self.method_info.append(method_info_obj)

    def set_package_name(self,package_name):
        self.package_name = package_name

    def set_package_line_no(self,package_line_no):
        self.package_line_no = package_line_no

###


class FileInfo:
    def __init__(self):
        self.file_detail = {}
        self.source_file_name = None
        self.file_level_comments = []  # Comments in a file which are outside any construct such as class, interface, etc.,
        self.class_info = []
        self.enum_info = []
        self.interface_info = []
        self.method_info = []
        self.static_block_info = []
        self.file_loc = 0
        self.total_comments = 0

    def append_file_static_block_info(self, static_block_obj):
        self.static_block_info.append(static_block_obj)

    def get_file_static_block(self):
        return self.static_block_info

    def get_file_comments_count(self):
        return self.total_comments

    def get_file_loc(self):
        return self.file_loc

    def set_file_loc(self, loc):
        self.file_loc = loc

    def get_file_source(self):
        return self.source_file_name

    def set_file_source(self, filename):
        self.source_file_name = filename

    def set_file_comments_count(self, comments_count):
        self.total_comments = comments_count

    def get_file_class_info(self):
        return self.class_info

    def get_file_interface_info(self):
        return self.interface_info

    def get_file_method_info(self):
        return self.method_info

    def get_file_info_comments(self):  # comments in a file but outside all entities
        return self.file_level_comments

    def get_all_info(self):
        all_construct_info = {}
        all_construct_info["FILE_NAME"] = self.source_file_name
        all_construct_info["CLASS_INFO"] = self.class_info
        all_construct_info["INTERFACE_INFO"] = self.interface_info
        all_construct_info["METHOD_INFO"] = self.method_info
        file_all_comments = self.get_file_info_comments()
        for class_obj in self.class_info:
            file_all_comments.extend(class_obj.get_all_comments_from_class())

        for interface_obj in self.interface_info:
            file_all_comments.extend(interface_obj.get_all_comments_from_interface())

        for method_obj in self.method_info:
            file_all_comments.extend(method_obj.get_all_comments_from_method())

        return all_construct_info

    def get_all_comments_from_file(self):
        file_all_comments = self.get_file_info_comments()
        for class_obj in self.class_info:
            file_all_comments.extend(class_obj.get_all_comments_from_class())

        for interface_obj in self.interface_info:
            file_all_comments.extend(interface_obj.get_all_comments_from_interface())

        for method_obj in self.method_info:
            file_all_comments.extend(method_obj.get_all_comments_from_method())

        for static_block_obj in self.static_block_info:
            file_all_comments.extend(static_block_obj.get_static_block_info_comments())

        for enum_obj in self.enum_info:
            file_all_comments.extend(enum_obj.get_all_comments_from_enum())

        return file_all_comments

    def get_file_info(self):
        self.file_detail["FILE_SOURCE"] = self.source_file_name
        self.file_detail["FILE_LOC"] = self.file_loc
        self.file_detail["CLASS_INFO"] = self.class_info
        self.file_detail["INTERFACE_INFO"] = self.interface_info
        self.file_detail["METHOD_INFO"] = self.method_info
        self.file_detail["STATIC_BLOCK_INFO"] = self.static_block_info
        self.file_detail["ENUM_INFO"] = self.enum_info
        return self.file_detail

    def get_file_info_and_comments(self):
        file_meta_info_and_comments = {}
        file_meta_info_and_comments["FILE_META"] = self.get_file_info()
        file_meta_info_and_comments["FILE_COMMENTS"] = self.get_file_info_comments()
        file_meta_info_and_comments["FILE_ALL_COMMENTS"] = self.get_all_comments_from_file()
        return file_meta_info_and_comments

    def append_file_level_comments(self, comment_obj):
        self.file_level_comments.append(comment_obj)

    def append_class_info(self, class_info_obj):
        self.class_info.append(class_info_obj)

    def append_enum_info(self, enum_info_obj):
        self.enum_info.append(enum_info_obj)

    def append_interface_info(self, interface_info_obj):
        self.interface_info.append(interface_info_obj)

    def append_method_info(self, method_info_obj):
        self.method_info.append(method_info_obj)
###


class Entity:
    def __init__(self):
        self.instance_element = None
        self.construct_instance_object = None
        self.instance_element_line = None
        self.identifier = None
        self.parent_identifier = None
        self.instance_type = None

    def get_identifier(self):
        return self.identifier

    def set_identifier(self, identifier):
        self.identifier = identifier

    def get_parent_identifier(self):
        return self.identifier

    def set_parent_identifier(self, identifier):
        self.identifier = identifier

    def get_instance_type(self):
        return self.instance_type

    def set_instance_type(self, instance_type):
        self.instance_type = instance_type

    def get_instance_element_line(self):
        return self.instance_element_line

    def set_instance_element_line(self, line):
        self.instance_element_line = line

    def get_construct_instance_obj(self):
        return self.construct_instance_object

    def set_construct_instance_obj(self, instance_obj):
        self.construct_instance_object = instance_obj

    def set_instance_element(self, instance_element):
        self.instance_element = instance_element

    def get_instance_element(self):
        return self.instance_element

