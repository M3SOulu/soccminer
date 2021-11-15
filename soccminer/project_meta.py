from soccminer.environment import Platform
from soccminer.source_code_details import PackageInfo, ClassInfo, InterfaceInfo, MethodInfo, StaticBlockInfo, EnumInfo, FileInfo
from soccminer.comments import CommentInfo
from soccminer.json_serialization import SerializeSoCCMiner
from soccminer.process_parameters import ProcessParameter
from soccminer.parse_source_files import SourceFiles
from soccminer.helper import Utility
import logging
import os


class Project:
    def __init__(self):
        self.source_file_info = None  # For holding source file details i.e., sourcefiles object

    def set_source_file_info(self, source_file_info_obj):
        self.source_file_info = source_file_info_obj

    def get_project_source_files(self):
        return self.source_file_info

    @staticmethod
    def fetch_project_dir_name(url):
        if Platform.is_unix_platform():
            return url.split("/")[-1]
        elif Platform.is_windows_platform():
            return url.split("\\")[-1]


class ProjectMeta(Project):
    def __init__(self):
        self.project_name = None
        self.project_loc = 0
        super().__init__()

    def set_project_name(self, proj):
        self.project_name = proj

    def get_project_name(self):
        return self.project_name if self.project_name is not None else "NA"

    def set_project_loc(self, loc):
        self.project_loc = loc

    def get_project_loc(self):
        return self.project_loc


class JavaProjectMeta(ProjectMeta):
    def __init__(self, source_url: str):
        self.package_info = []  # For holding package details in a project, i.e., package objects
        self.master_file_list = []
        self.master_class_list = []
        self.master_method_list = []
        self.master_enum_list = []
        self.master_interface_list = []
        self.master_static_block_list = []
        self.master_comment_list = []
        self.file_level_comment_list = []
        self.package_level_comment_list = []
        self.class_level_comment_list = []
        self.method_level_comment_list = []
        self.interface_level_comment_list = []
        self.static_block_level_comment_list = []
        self.enum_level_comment_list = []

        super().__init__()
        self.set_project_name(Project.fetch_project_dir_name(source_url))

    def append_package_level_comment(self, comment_obj):
        self.package_level_comment_list.append(comment_obj)

    def append_class_level_comment(self, comment_obj):
        self.class_level_comment_list.append(comment_obj)

    def append_file_level_comment(self, comment_obj):
        self.file_level_comment_list.append(comment_obj)

    def append_enum_level_comment(self, comment_obj):
        self.enum_level_comment_list.append(comment_obj)

    def append_interface_level_comment(self, comment_obj):
        self.interface_level_comment_list.append(comment_obj)

    def append_method_level_comment(self, comment_obj):
        self.method_level_comment_list.append(comment_obj)

    def append_static_block_level_comment(self, comment_obj):
        self.static_block_level_comment_list.append(comment_obj)

    def append_package_info(self, package_info_obj):
        self.package_info.append(package_info_obj)

    def append_project_file(self, file_obj):
        self.master_file_list.append(file_obj)

    def append_project_class(self, class_obj):
        self.master_class_list.append(class_obj)

    def append_project_enum(self, enum_obj):
        self.master_enum_list.append(enum_obj)

    def append_project_method(self, method_obj):
        self.master_method_list.append(method_obj)

    def append_project_interface(self, interface_obj):
        self.master_interface_list.append(interface_obj)

    def append_project_static_block(self, static_block_obj):
        self.master_static_block_list.append(static_block_obj)

    def append_project_comments(self, comment_obj):
        self.master_comment_list.append(comment_obj)

    def get_packages(self):
        return self.package_info

    def get_files(self):
        return self.master_file_list

    def get_classes(self):
        return self.master_class_list

    def get_enums(self):
        return self.master_enum_list

    def get_methods(self):
        return self.master_method_list

    def get_interfaces(self):
        return self.master_interface_list

    def get_static_blocks(self):
        return self.master_static_block_list

    def fetch_comments(self):
        return self.master_comment_list

    def fetch_project_loc(self):
        project_loc = 0
        for package_obj in self.get_packages():
            project_loc += package_obj.get_package_loc()
            logging.debug("fetch_project_loc: Package Name: {}".format(package_obj.get_package_name()))
            logging.debug("fetch_project_loc: Package LOC: {}".format(package_obj.get_package_loc()))
            logging.debug("fetch_project_loc: Project LOC: {}".format(project_loc))
        return project_loc

    def fetch_avg_file_loc(self):
        file_loc = 0
        for file_obj in self.get_files():
            file_loc += file_obj.get_file_loc()
        file_len = 1 if len(self.get_files()) == 0 else len(self.get_files())
        avg_file_loc = file_loc / file_len
        logging.debug("fetch_avg_file_loc: Avg file LOC: {}".format(avg_file_loc))
        return avg_file_loc

    def populate_entity_stats(self, proj_dir):
        mined_entity_stats = {}
        comment_dir_list = []

        miner_params = ProcessParameter.fetch_program_parameters()

        # loading package details
        mined_entity_stats[type(PackageInfo()).__name__] = len(self.get_packages())
        # comments at file level instead of package level
        # comments outside other entities in a source file are associated with file
        if miner_params['mining_level'] != 3:
            comments_dir = proj_dir + '/' + type(FileInfo()).__name__ + '/comments/'
            comment_dir_list.append(comments_dir)
        logging.debug("populate_entity_stats() - Packages: {}".format(len(self.get_packages())))

        # loading file details
        file_count = 0
        if miner_params['mining_level'] == 3 or miner_params['mining_level'] == 4:
            attr_dir = proj_dir + '/' + type(FileInfo()).__name__ + '/attributes/'
            file_count = Utility.fetch_entity_count(attr_dir, 'json')
            mined_entity_stats[type(FileInfo()).__name__] = file_count
        #if miner_params['mining_level'] != 3:
        #    comments_dir = proj_dir + '/' + type(FileInfo()).__name__ + '/comments/'
        #    comment_dir_list.append(comments_dir)
        #logging.debug("populate_entity_stats() - Classes: {}".format(file_count))


        # loading class details
        class_count = 0
        if miner_params['mining_level'] == 3 or miner_params['mining_level'] == 4:
            attr_dir = proj_dir + '/' + type(ClassInfo()).__name__ + '/attributes/'
            class_count = Utility.fetch_entity_count(attr_dir, 'json')
            mined_entity_stats[type(ClassInfo()).__name__] = class_count
        if miner_params['mining_level'] != 3:
            comments_dir = proj_dir + '/' + type(ClassInfo()).__name__ + '/comments/'
            comment_dir_list.append(comments_dir)
        logging.debug("populate_entity_stats() - Classes: {}".format(class_count))

        # loading enum details
        enum_count = 0
        if miner_params['mining_level'] == 3 or miner_params['mining_level'] == 4:
            attr_dir = proj_dir + '/' + type(EnumInfo()).__name__ + '/attributes/'
            enum_count = Utility.fetch_entity_count(attr_dir, 'json')
            mined_entity_stats[type(EnumInfo()).__name__] = enum_count
        if miner_params['mining_level'] != 3:
            comments_dir = proj_dir + '/' + type(EnumInfo()).__name__ + '/comments/'
            comment_dir_list.append(comments_dir)
        logging.debug("populate_entity_stats() - Classes: {}".format(enum_count))

        # loading interface details
        interface_count = 0
        if miner_params['mining_level'] == 3 or miner_params['mining_level'] == 4:
            attr_dir = proj_dir + '/' + type(InterfaceInfo()).__name__ + '/attributes/'
            interface_count = Utility.fetch_entity_count(attr_dir, 'json')
            mined_entity_stats[type(InterfaceInfo()).__name__] = interface_count
        if miner_params['mining_level'] != 3:
            comments_dir = proj_dir + '/' + type(InterfaceInfo()).__name__ + '/comments/'
            comment_dir_list.append(comments_dir)
        logging.debug("populate_entity_stats() - Interfaces: {}".format(interface_count))

        # loading method details
        method_count = 0
        if miner_params['mining_level'] == 3 or miner_params['mining_level'] == 4:
            attr_dir = proj_dir + '/' + type(MethodInfo()).__name__ + '/attributes/'
            method_count = Utility.fetch_entity_count(attr_dir, 'json')
            mined_entity_stats[type(MethodInfo()).__name__] = method_count
        if miner_params['mining_level'] != 3:
            comments_dir = proj_dir + '/' + type(MethodInfo()).__name__ + '/comments/'
            comment_dir_list.append(comments_dir)
        logging.debug("populate_entity_stats() - Methods: {}".format(method_count))

        # loading static block details
        static_block_count = 0
        if miner_params['mining_level'] == 3 or miner_params['mining_level'] == 4:
            attr_dir = proj_dir + '/' + type(StaticBlockInfo()).__name__ + '/attributes/'
            static_block_count = Utility.fetch_entity_count(attr_dir, 'json')
            mined_entity_stats[type(StaticBlockInfo()).__name__] = static_block_count
        if miner_params['mining_level'] != 3:
            comments_dir = proj_dir + '/' + type(StaticBlockInfo()).__name__ + '/comments/'
            comment_dir_list.append(comments_dir)
        logging.debug("populate_entity_stats() - StaticBlocks: {}".format(static_block_count))

        mined_entity_stats[type(CommentInfo()).__name__] = 0
        for comment_dir in comment_dir_list:
            comment_count = Utility.fetch_entity_count(comment_dir, 'json')
            mined_entity_stats[type(CommentInfo()).__name__] += comment_count
        logging.debug("populate_entity_stats() - Comments: {}".format(mined_entity_stats[type(CommentInfo()).__name__]))
        return mined_entity_stats

    def load_project_from_json(self, proj_dir, entity):
        package_attr_dir = None
        package_comments_dir = None
        class_attr_dir = None
        class_comments_dir = None
        interface_attr_dir = None
        interface_comments_dir = None
        method_attr_dir = None
        method_comments_dir = None
        static_block_attr_dir = None
        static_block_comments_dir = None
        enum_attr_dir = None
        enum_comments_dir = None
        file_attr_dir = None
        file_comments_dir = None

        if Platform.is_unix_platform():
            package_attr_dir = proj_dir + '/' + type(PackageInfo()).__name__ + '/attributes/'
            package_comments_dir = proj_dir + '/' + type(PackageInfo()).__name__ + '/comments/'
            class_attr_dir = proj_dir + '/' + type(ClassInfo()).__name__ + '/attributes/'
            class_comments_dir = proj_dir + '/' + type(ClassInfo()).__name__ + '/comments/'
            interface_attr_dir = proj_dir + '/' + type(InterfaceInfo()).__name__ + '/attributes/'
            interface_comments_dir = proj_dir + '/' + type(InterfaceInfo()).__name__ + '/comments/'
            method_attr_dir = proj_dir + '/' + type(MethodInfo()).__name__ + '/attributes/'
            method_comments_dir = proj_dir + '/' + type(MethodInfo()).__name__ + '/comments/'
            static_block_attr_dir = proj_dir + '/' + type(StaticBlockInfo()).__name__ + '/attributes/'
            static_block_comments_dir = proj_dir + '/' + type(StaticBlockInfo()).__name__ + '/comments/'
            enum_attr_dir = proj_dir + '/' + type(EnumInfo()).__name__ + '/attributes/'
            enum_comments_dir = proj_dir + '/' + type(EnumInfo()).__name__ + '/comments/'
            file_attr_dir = proj_dir + '/' + type(FileInfo()).__name__ + '/attributes/'
            file_comments_dir = proj_dir + '/' + type(FileInfo()).__name__ + '/comments/'
        elif Platform.is_windows_platform():
            package_attr_dir = proj_dir + '\\' + type(PackageInfo()).__name__ + '\\attributes\\'
            package_comments_dir = proj_dir + '\\' + type(ClassInfo()).__name__ + '\\comments\\'
            class_attr_dir = proj_dir + '\\' + type(ClassInfo()).__name__ + '\\attributes\\'
            class_comments_dir = proj_dir + '\\' + type(ClassInfo()).__name__ + '\\comments\\'
            interface_attr_dir = proj_dir + '\\' + type(InterfaceInfo()).__name__ + '\\attributes\\'
            interface_comments_dir = proj_dir + '\\' + type(InterfaceInfo()).__name__ + '\\comments\\'
            method_attr_dir = proj_dir + '\\' + type(MethodInfo()).__name__ + '\\attributes\\'
            method_comments_dir = proj_dir + '\\' + type(MethodInfo()).__name__ + '\\comments\\'
            static_block_attr_dir = proj_dir + '\\' + type(StaticBlockInfo()).__name__ + '\\attributes\\'
            static_block_comments_dir = proj_dir + '\\' + type(StaticBlockInfo()).__name__ + '\\comments\\'
            enum_attr_dir = proj_dir + '\\' + type(EnumInfo()).__name__ + '\\attributes\\'
            enum_comments_dir = proj_dir + '\\' + type(EnumInfo()).__name__ + '\\comments\\'
            file_attr_dir = proj_dir + '\\' + type(FileInfo()).__name__ + '\\attributes\\'
            file_comments_dir = proj_dir + '\\' + type(FileInfo()).__name__ + '\\comments\\'

        comment_dir_list = []
        level_mapping_dict = {1: 'comment', 2: 'comprehensive_comment', 3: 'project', 4: 'all', 0: 'none'}
        miner_params = ProcessParameter.fetch_program_parameters()
        logging.debug("Loading {} from json begins for proj_dir: {}".format(proj_dir, entity))

        src_file_dir = None
        src_file_and_proj_items = ['Entity_Project_Directory', 'Serialized_Project_Name',
                                   'Source_Files_List', 'Source_Xml_Mapping_Dict', 'Serialized_Mining_Level', 'Serialized_Project_KLOC' ]
        if entity == "source_file":
            # loading source file info
            if Platform.is_unix_platform():
                src_file_dir = proj_dir + '/' + proj_dir.split("/")[-1] + '.json'
            elif Platform.is_windows_platform():
                src_file_dir = proj_dir + '\\' + proj_dir.split("/")[-1] + '.json'

            if not os.path.isfile(src_file_dir):
                #print("Missing project_source_meta json.  Unable to load project. \n"
                #                "Please check your input folder containing mined entities for project {}".format(self.get_project_name()))
                exception_msg = "Missing project_source_meta json.  Unable to load project. \n " \
                                "Please check your input folder containing mined entities for project {}".format(self.get_project_name())
                #raise Exception(exception_msg)
                return exception_msg

            construct_info = SerializeSoCCMiner.load_from_json_file(src_file_dir)
            src_file_obj = SourceFiles(proj_dir)

            #  since there will be only one src_file_info json for one project
            for item_to_load in src_file_and_proj_items:
                if item_to_load not in construct_info[0]:
                    #print(
                    #    "Invalid json to load project. Does not contain {} for project {}".format(item_to_load, self.get_project_name()))
                    #raise Exception(
                    #    "Invalid json to load project. Does not contain {} for project {}".format(item_to_load, self.get_project_name()))
                    exception_msg = "Invalid json to load project. Does not contain {} for project {}".format(item_to_load, self.get_project_name())
                    return exception_msg

            src_file_obj.loc = construct_info[0]['Entity_Project_Directory']
            src_file_obj.files = construct_info[0]['Source_Files_List']
            src_file_obj.cd_file_xml_mapping_dict = construct_info[0]['Source_Xml_Mapping_Dict']

            if self.get_project_name() != construct_info[0]['Serialized_Project_Name']:
                exception_msg = ("Corrupted JSON. Input Load_Project workflow's, Project Name {}  \n" 
                                                " does not match with serialized project name {}"
                            "".format(self.get_project_name(), construct_info[0]['Serialized_Project_Name']))
                return exception_msg
                #raise Exception("Corrupted JSON. Input Load_Project workflow's, Project Name {}  \n" \
                #                                " does not match with serialized project name {}"
                #            "".format(self.get_project_name(), construct_info[0]['Serialized_Project_Name']))
            elif miner_params['mining_level'] != construct_info[0]['Serialized_Mining_Level']:
                exception_msg = ("Project Load failed as Load_Level ({}) does not match with serialized project's Mining_Level ({}) for project {}"
                      "".format(level_mapping_dict[miner_params['mining_level']], level_mapping_dict[construct_info[0]['Serialized_Mining_Level']], self.get_project_name()))
                return exception_msg
                #raise Exception("Project Load failed as Load_Level ({}) does not match with serialized project's Mining_Level ({}) for project {}"
                #      "".format(level_mapping_dict[miner_params['mining_level']], level_mapping_dict[construct_info[0]['Serialized_Mining_Level']], self.get_project_name()))

            self.set_project_loc(construct_info[0]['Serialized_Project_KLOC'] * 1000)
            self.set_source_file_info(src_file_obj)
            logging.debug("load_project_from_json() - {}".format(entity))

        if entity == "package" or entity == "project":
            # loading package details
            # Package info is required at all param levels as it is used to calculate project loc, KLOC
            construct_info = SerializeSoCCMiner.load_from_json_file(package_attr_dir)
            for package_info_dict in construct_info:
                package_obj = PackageInfo()
                package_obj.set_package_name(package_info_dict['Package_Name'])
                package_obj.set_package_loc(package_info_dict['Package_LOC'])
                package_obj.set_package_line_no(package_info_dict['Package_Line_No'])
                package_obj.set_package_source(package_info_dict['Package_Source_File'])
                self.append_package_info(package_obj)
            if miner_params['mining_level'] != 3:
                comment_info = SerializeSoCCMiner.load_comment_info(package_comments_dir)
                if len(comment_info) > 0:
                    self.master_comment_list.extend(comment_info)
                    self.package_level_comment_list.extend(comment_info)
                logging.debug("load_project_from_json() - {}: {}".format("comment", len(self.package_level_comment_list)))
            logging.debug("load_project_from_json() - {}: {}".format(entity, len(self.get_packages())))

        if entity == "file" or entity == "project":
            # loading package details
            # File info is required at all param levels as it is used to calculate project loc, KLOC
            construct_info = SerializeSoCCMiner.load_from_json_file(file_attr_dir)
            for file_info_dict in construct_info:
                file_obj = FileInfo()
                file_obj.set_file_source(file_info_dict['Source_File'])
                file_obj.set_file_loc(file_info_dict['File_LOC'])
                file_obj.set_file_comments_count(file_info_dict['File_Comments_Count'])
                self.append_project_file(file_obj)
            if miner_params['mining_level'] != 3:
                comment_info = SerializeSoCCMiner.load_comment_info(file_comments_dir)
                if len(comment_info) > 0:
                    self.master_comment_list.extend(comment_info)
                    self.file_level_comment_list.extend(comment_info)
                logging.debug("load_project_from_json() - {}: {}".format("comment", len(self.file_level_comment_list)))
            logging.debug("load_project_from_json() - {}: {}".format(entity, len(self.get_files())))

        if entity == "class" or entity == "project":
            # loading class details
            if miner_params['mining_level'] == 3 or miner_params['mining_level'] == 4:
                construct_info = SerializeSoCCMiner.load_from_json_file(class_attr_dir)
                for class_info_dict in construct_info:
                    class_obj = ClassInfo()
                    class_obj.set_class_name(class_info_dict['Class_Name'])
                    class_obj.set_class_type(class_info_dict['Class_Type'])
                    class_obj.set_class_specifier(class_info_dict['Class_Specifier'])
                    class_obj.set_nested_level(class_info_dict['Class_Nested_Level'])
                    class_obj.set_class_signature(class_info_dict['Class_Signature'])
                    class_obj.set_class_loc(class_info_dict['Class_LOC'])
                    class_obj.set_class_line_no(class_info_dict['Class_Line_No'])
                    class_obj.set_class_source(class_info_dict['Class_Source_File'])
                    self.append_project_class(class_obj)
            if miner_params['mining_level'] != 3:
                comment_info = SerializeSoCCMiner.load_comment_info(class_comments_dir)
                if len(comment_info) > 0:
                    self.master_comment_list.extend(comment_info)
                    self.class_level_comment_list.extend(comment_info)
                logging.debug("load_project_from_json() - {}: {}".format("comment", len(self.class_level_comment_list)))
            logging.debug("load_project_from_json() - {}: {}".format(entity, len(self.get_classes())))

        if entity == "enum" or entity == "project":
            # loading enum details
            if miner_params['mining_level'] == 3 or miner_params['mining_level'] == 4:
                construct_info = SerializeSoCCMiner.load_from_json_file(enum_attr_dir)
                for enum_info_dict in construct_info:
                    enum_obj = EnumInfo()
                    enum_obj.set_enum_name(enum_info_dict['Enum_Name'])
                    enum_obj.set_enum_specifier(enum_info_dict['Enum_Specifier'])
                    enum_obj.set_enum_signature(enum_info_dict['Enum_Signature'])
                    enum_obj.set_enum_loc(enum_info_dict['Enum_LOC'])
                    enum_obj.set_enum_line_no(enum_info_dict['Enum_Line_No'])
                    enum_obj.set_enum_source(enum_info_dict['Enum_Source_File'])
                    self.append_project_class(enum_obj)
            if miner_params['mining_level'] != 3:
                comment_info = SerializeSoCCMiner.load_comment_info(enum_comments_dir)
                if len(comment_info) > 0:
                    self.master_comment_list.extend(comment_info)
                    self.enum_level_comment_list.extend(comment_info)
                logging.debug("load_project_from_json() - {}: {}".format("comment", len(self.enum_level_comment_list)))
            logging.debug("load_project_from_json() - {}: {}".format(entity, len(self.get_enums())))

        if entity == "interface" or entity == "project":
            # loading interface details
            if miner_params['mining_level'] == 3 or miner_params['mining_level'] == 4:
                construct_info = SerializeSoCCMiner.load_from_json_file(interface_attr_dir)
                for interface_info_dict in construct_info:
                    interface_obj = InterfaceInfo()
                    interface_obj.set_interface_name(interface_info_dict['Interface_Name'])
                    interface_obj.set_interface_specifier(interface_info_dict['Interface_Specifier'])
                    interface_obj.set_interface_signature(interface_info_dict['Interface_Signature'])
                    interface_obj.set_interface_loc(interface_info_dict['Interface_LOC'])
                    interface_obj.set_interface_line_no(interface_info_dict['Interface_Line_No'])
                    interface_obj.set_interface_source(interface_info_dict['Interface_Source_File'])
                    self.append_project_interface(interface_obj)
            if miner_params['mining_level'] != 3:
                comment_info = SerializeSoCCMiner.load_comment_info(interface_comments_dir)
                if len(comment_info) > 0:
                    self.master_comment_list.extend(comment_info)
                    self.interface_level_comment_list.extend(comment_info)
                logging.debug("load_project_from_json() - {}: {}".format("comment", len(self.interface_level_comment_list)))
            logging.debug("load_project_from_json() - {}: {}".format(entity, len(self.get_interfaces())))

        if entity == "method" or entity == "project":
            # loading method details
            if miner_params['mining_level'] == 3 or miner_params['mining_level'] == 4:
                construct_info = SerializeSoCCMiner.load_from_json_file(method_attr_dir)
                for method_info_dict in construct_info:
                    method_obj = MethodInfo()
                    method_obj.set_method_name(method_info_dict['Method_Name'])
                    method_obj.set_method_type(method_info_dict['Method_Type'])
                    method_obj.set_method_specifier(method_info_dict['Method_Specifier'])
                    method_obj.set_method_signature(method_info_dict['Method_Signature'])
                    method_obj.set_method_category(method_info_dict['Method_Category'])
                    method_obj.set_method_category(method_info_dict['Method_Param_Count'])
                    method_obj.set_method_loc(method_info_dict['Method_LOC'])
                    method_obj.set_method_line_no(method_info_dict['Method_Line_No'])
                    method_obj.set_method_source(method_info_dict['Method_Source_File'])
                    self.append_project_method(method_obj)
            if miner_params['mining_level'] != 3:
                comment_info = SerializeSoCCMiner.load_comment_info(method_comments_dir)
                if len(comment_info) > 0:
                    self.master_comment_list.extend(comment_info)
                    self.method_level_comment_list.extend(comment_info)
                logging.debug("load_project_from_json() - {}: {}".format("comment", len(self.method_level_comment_list)))
            logging.debug("load_project_from_json() - {}: {}".format(entity, len(self.get_methods())))

        if entity == "static_block" or entity == "project":
            # loading static block details
            if miner_params['mining_level'] == 3 or miner_params['mining_level'] == 4:
                construct_info = SerializeSoCCMiner.load_from_json_file(static_block_attr_dir)
                for static_block_dict in construct_info:
                    static_block_obj = StaticBlockInfo()
                    static_block_obj.set_static_block_loc(static_block_dict['Static_Block_LOC'])
                    static_block_obj.set_static_block_line_no(static_block_dict['Static_Block_Line_No'])
                    static_block_obj.set_static_block_source(static_block_dict['Static_Block_Source_File'])
                    self.append_project_static_block(static_block_obj)
            if miner_params['mining_level'] != 3:
                comment_info = SerializeSoCCMiner.load_comment_info(static_block_comments_dir)
                if len(comment_info) > 0:
                    self.master_comment_list.extend(comment_info)
                    self.static_block_level_comment_list.extend(comment_info)
                logging.debug("load_project_from_json() - {}: {}".format("comment", len(self.static_block_level_comment_list)))
            logging.debug("load_project_from_json() - {}: {}".format(entity, len(self.get_static_blocks())))

        return "success"
