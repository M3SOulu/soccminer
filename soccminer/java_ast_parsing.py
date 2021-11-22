from soccminer.parse_source_files import SourceFiles
from soccminer.parse_source_files import validate_loc
from soccminer.source_code_details import Entity, ClassInfo, PackageInfo, MethodInfo, StaticBlockInfo, InterfaceInfo, EnumInfo, FileInfo
from soccminer.comments import CommentInfo
from soccminer.srcml import SourceML
from soccminer.process_parameters import ProcessParameter
from soccminer.environment import Platform
from soccminer.json_serialization import SerializeSoCCMiner
from soccminer.helper import ASTHelper, Utility
from soccminer.soccminer_logger import SoCCMinerLogger
from lxml import etree
import logging
import sys
import gc
from copy import copy
import os
import traceback
import shutil
from datetime import datetime


class XmlProperties:
    root_ele = '{http://www.srcML.org/srcML/src}unit'
    comment_ele = '{http://www.srcML.org/srcML/src}comment'

    class_element = '{http://www.srcML.org/srcML/src}class'
    enum_element = '{http://www.srcML.org/srcML/src}enum'
    interface_element = '{http://www.srcML.org/srcML/src}interface'
    interface_decl_element = '{http://www.srcML.org/srcML/src}interface_decl'
    function_element = '{http://www.srcML.org/srcML/src}function'
    function_decl_element = '{http://www.srcML.org/srcML/src}function_decl'
    constructor_element = '{http://www.srcML.org/srcML/src}constructor'
    static_block_element = '{http://www.srcML.org/srcML/src}static'
    package_element = '{http://www.srcML.org/srcML/src}package'
    lxml_element = '_Element'

    auxiliary_ele_list = ['{http://www.srcML.org/srcML/src}<block_content>',
                            '{http://www.srcML.org/srcML/src}<block>',
                            '{http://www.srcML.org/srcML/src}<name>',
                            '{http://www.srcML.org/srcML/src}<condition>',
                            '{http://www.srcML.org/srcML/src}<expr>',
                            '{http://www.srcML.org/srcML/src}<control>',
                            '{http://www.srcML.org/srcML/src}<if>',
                            '{http://www.srcML.org/srcML/src}<else>',
                            '{http://www.srcML.org/srcML/src}<case>']

    construct_ele_list = ['{http://www.srcML.org/srcML/src}class', '{http://www.srcML.org/srcML/src}interface',
                          '{http://www.srcML.org/srcML/src}interface_decl', '{http://www.srcML.org/srcML/src}function',
                          '{http://www.srcML.org/srcML/src}constructor', '{http://www.srcML.org/srcML/src}static',
                          '{http://www.srcML.org/srcML/src}package', '{http://www.srcML.org/srcML/src}function_decl',
                          '{http://www.srcML.org/srcML/src}enum']

    control_ele_list = ['{http://www.srcML.org/srcML/src}if_stmt', '{http://www.srcML.org/srcML/src}switch',
                        '{http://www.srcML.org/srcML/src}case', '{http://www.srcML.org/srcML/src}while',
                        '{http://www.srcML.org/srcML/src}do', '{http://www.srcML.org/srcML/src}for',
                        '{http://www.srcML.org/srcML/src}continue', '{http://www.srcML.org/srcML/src}break',
                        '{http://www.srcML.org/srcML/src}return']

    exception_ele_list = ['{http://www.srcML.org/srcML/src}try', '{http://www.srcML.org/srcML/src}catch',
                          '{http://www.srcML.org/srcML/src}throw', '{http://www.srcML.org/srcML/src}throws',
                          '{http://www.srcML.org/srcML/src}finally']

    expr_stmt_list = ['{http://www.srcML.org/srcML/src}expr_stmt', '{http://www.srcML.org/srcML/src}call',
                      '{http://www.srcML.org/srcML/src}ternary', '{http://www.srcML.org/srcML/src}lambda']

    others_stmt_list = ['{http://www.srcML.org/srcML/src}assert', '{http://www.srcML.org/srcML/src}default',
                        '{http://www.srcML.org/srcML/src}label', '{http://www.srcML.org/srcML/src}import',
                        '{http://www.srcML.org/srcML/src}synchronized']

    assert_ele = '{http://www.srcML.org/srcML/src}assert'
    default_ele = '{http://www.srcML.org/srcML/src}default'
    label_ele = '{http://www.srcML.org/srcML/src}label'
    return_ele = '{http://www.srcML.org/srcML/src}return'
    block_ele = '{http://www.srcML.org/srcML/src}block'
    block_content_ele = '{http://www.srcML.org/srcML/src}block_content'
    import_ele = '{http://www.srcML.org/srcML/src}import'
    sync_stmt_ele = '{http://www.srcML.org/srcML/src}synchronized'
    decl_stmt_ele = '{http://www.srcML.org/srcML/src}decl_stmt'
    if_stmt_ele = '{http://www.srcML.org/srcML/src}if_stmt'
    decl_ele = '{http://www.srcML.org/srcML/src}decl'
    if_ele = '{http://www.srcML.org/srcML/src}if'
    else_ele = '{http://www.srcML.org/srcML/src}if'
    expr_ele = '{http://www.srcML.org/srcML/src}expr'
    expr_stmt_ele = '{http://www.srcML.org/srcML/src}expr_stmt'

    sub_ele_list = ['{http://www.srcML.org/srcML/src}block_content', '{http://www.srcML.org/srcML/src}condition',
                    '{http://www.srcML.org/srcML/src}control', '{http://www.srcML.org/srcML/src}else',
                    '{http://www.srcML.org/srcML/src}expr', '{http://www.srcML.org/srcML/src}if',
                    '{http://www.srcML.org/srcML/src}incr', '{http://www.srcML.org/srcML/src}then',
                    '{http://www.srcML.org/srcML/src}type', '{http://www.srcML.org/srcML/src}block']

    unit_element = "{http://www.srcML.org/srcML/src}unit"
    name_element = '{http://www.srcML.org/srcML/src}name'
    specifier_element = '{http://www.srcML.org/srcML/src}specifier'
    type_element = '{http://www.srcML.org/srcML/src}type'
    super_element = '{http://www.srcML.org/srcML/src}super'
    annotation_element = '{http://www.srcML.org/srcML/src}annotation'
    super_list_element = '{http://www.srcML.org/srcML/src}super_list'
    param_list_element = '{http://www.srcML.org/srcML/src}parameter_list'
    argument_list_element = '{http://www.srcML.org/srcML/src}argument_list'
    cnstrct_type_generic = "GENERIC"
    cnstrct_type_derived = "DERIVED"
    cnstrct_type_anonymous = "ANONYMOUS"
    cnstrct_type_regular = "REGULAR"
    xml_open_angle_bracket = '&lt;'
    xml_close_angle_bracket = '&gt;'
    open_angle_bracket = '<'
    close_angle_bracket = '>'
    no_specifier_label = "NO_SPECIFIER"
    srcml_ns = "{http://www.srcML.org/srcML/src}"

    def __init__(self, xml_file):
        self.top_level_elements = []
        self.project_dir = None
        self.src_file_name = None
        self.comments_counter = 0
        self.nodes = []
        self.tree = etree.ElementTree()
        self.root = None
        self.comment_master_dict = {}
        self.file_header_comment = ''
        self.unit_ele = None
        self.unit_ele_attributes = {}
        self.constructs_master = []
        self.top_level_constructs = []
        self.parent_instance = None
        self.parent_instance_dict = {}
        self.construct_signature_list = []
        self.first_block = False
        self.construct_obj_instance = None
        self.construct_first_ele = None
        self.construct_specifier_flag = False
        self.construct_param_list = []  # for storing parameters of a construct, for example function
        self.processed_comment_dict = {}
        self.consecutive_comment_dict = {}
        self.consecutive_comment_first = None
        self.consecutive_comment_last = None
        self.package_instance = None
        self.construct_signature_dict = {}
        self.existing_package_flag = False
        self.entity_counter = {}
        self.project_comments_dir = None
        self.package_entity_element = None
        self.xml_file_num = None
        self.existing_pckg_serialization_url = None
        self.logger = None
        self.file_obj = None
        self.all_cmnts_cntr = 0
        self.project_name = None
        self.xml_file = xml_file

        # fetch the program parameters set in the driver module CommentsMiner
        ProcessParameter.fetch_program_parameters()

    def set_unit_element(self):
        self.unit_ele = etree.Element(XmlProperties.unit_element)

    def get_unit_element(self):
        return self.unit_ele

    def get_element_tag(self, node):
        return node if type(node) == str else node.tag

    def get_root(self):
        return self.tree.getroot()

    def get_parent(self, node):
        return node.getparent()

    def get_text(self, node):
        return node.text

    def get_children_iter(self, node):
        return node.iterchildren()

    def get_descendants_iter(self, node):
        return node.iterdescendants()

    def get_elements_iter(self, node):
        return node.iter()

    def get_ancestors_iter(self, node):
        return node.iterancestors()

    def convert_ele_to_xml(self, node):
        return etree.tostring(node)

    def get_next_element(self, node):
        return node.getnext()

    def get_element_line_number(self, node):
        return node.sourceline

    def get_previous_element(self, node):
        return node.getprevious()

    def is_package_element(self, node):
        if type(node) == str:
            return self.is_package_initialization_element(node)
        else:
            return self.get_element_tag(node) == XmlProperties.package_element

    def is_anonymous_package(self, node):
        '''
        Checks if input is anonymous package and returns True else False
        :param node: string containing node tag
        :return: bool
        '''
        if type(node) == str:
            return node == "ANONYMOUS_PACKAGE"
        else:
            return False

    def is_class_element(self, node):
        return self.get_element_tag(node) == XmlProperties.class_element

    def is_enum_element(self, node):
        return self.get_element_tag(node) == XmlProperties.enum_element

    def is_interface_element(self, node):
        return self.get_element_tag(node) == XmlProperties.interface_element

    def is_function_element(self, node):
        return self.get_element_tag(node) == XmlProperties.function_element

    def is_if_stmt_element(self, node):
        if type(node) == str:
            return node == XmlProperties.if_stmt_ele.replace(XmlProperties.srcml_ns, "")
        else:
            return self.get_element_tag(node) == XmlProperties.if_stmt_ele

    def is_if_ele(self, node):
        return self.get_element_tag(node) == XmlProperties.if_ele

    def is_else_ele(self, node):
        return self.get_element_tag(node) == XmlProperties.else_ele

    def is_expr_ele(self, node):
        return self.get_element_tag(node) == XmlProperties.expr_ele

    def is_decl_stmt_element(self, node):
        if type(node) == str:
            return node == XmlProperties.decl_stmt_ele.replace(XmlProperties.srcml_ns, "")
        else:
            return self.get_element_tag(node) == XmlProperties.decl_stmt_ele

    def is_decl_element(self, node):
        return self.get_element_tag(node) == XmlProperties.decl_ele

    def is_function_decl_element(self, node):
        return self.get_element_tag(node) == XmlProperties.function_decl_element

    def is_param_list_element(self, node):
        return self.get_element_tag(node) == XmlProperties.param_list_element

    def is_argument_list_element(self, node):
        return self.get_element_tag(node) == XmlProperties.argument_list_element

    def is_super_list_element(self, node):
        return self.get_element_tag(node) == XmlProperties.super_list_element

    def is_constructor_element(self, node):
        return self.get_element_tag(node) == XmlProperties.constructor_element

    def is_static_block_element(self, node):
        return self.get_element_tag(node) == XmlProperties.static_block_element

    def is_lxml_element(self, node):
        if type(node) == str:
            return False
        else:
            return type(node).__name__ == XmlProperties.lxml_element

    def is_comment_element(self, node):
        return self.get_element_tag(node) == XmlProperties.comment_ele

    def is_name_element(self, node):
        return self.get_element_tag(node) == XmlProperties.name_element

    def is_specifier_element(self, node):
        return self.get_element_tag(node) == XmlProperties.specifier_element

    def is_type_element(self, node):
        return self.get_element_tag(node) == XmlProperties.type_element

    def is_super_element(self, node):
        return self.get_element_tag(node) == XmlProperties.super_element

    def is_annotation_element(self, node):
        return self.get_element_tag(node) == XmlProperties.annotation_element

    def is_construct_element(self, node):
        if type(node) == str:
            return node in XmlProperties.construct_ele_list
        else:
            return self.get_element_tag(node) in XmlProperties.construct_ele_list

    def is_auxiliary(self, node):
        if type(node) == str:
            return node in XmlProperties.auxiliary_ele_list
        else:
            return self.get_element_tag(node) in XmlProperties.auxiliary_ele_list

    def is_control_element(self, node):
        if type(node) == str:
            return node in XmlProperties.control_ele_list
        else:
            return self.get_element_tag(node) in XmlProperties.control_ele_list

    def is_exception_element(self, node):
        if type(node) == str:
            return node in XmlProperties.exception_ele_list
        else:
            return self.get_element_tag(node) in XmlProperties.exception_ele_list

    def is_expr_stmt_element(self, node):
        if type(node) == str:
            return node in XmlProperties.expr_stmt_list
        else:
            return self.get_element_tag(node) in XmlProperties.expr_stmt_list

    def is_expression_stmt_element(self, node):
        if type(node) == str:
            return node == XmlProperties.expr_stmt_ele.replace(XmlProperties.srcml_ns, "")
        else:
            return self.get_element_tag(node) in XmlProperties.expr_stmt_ele

    def is_return_element(self, node):
        return self.get_element_tag(node) == XmlProperties.return_ele

    def is_block_element(self, node):
        return self.get_element_tag(node) == XmlProperties.block_ele

    def is_file_entity(self, node):
        return node == "File"

    def is_package_initialization_element(self, element):
        if type(element) == str:
            return element == "PACKAGE_INITIALIZATION"
        else:
            return False

    def is_block_content_element(self, node):
        return self.get_element_tag(node) == XmlProperties.block_content_ele

    def is_import_element(self, node):
        return self.get_element_tag(node) == XmlProperties.import_ele

    def is_synchronized_element(self, node):
        return self.get_element_tag(node) == XmlProperties.sync_stmt_ele

    def is_declaration_element(self, node):
        return self.get_element_tag(node) == XmlProperties.decl_stmt_ele

    def is_root_element(self, node):
        return self.get_element_tag(node) == XmlProperties.root_ele

    def is_other_element(self, node):
        return self.get_element_tag(node) in XmlProperties.others_stmt_list

    def set_file_header_comment(self, node):
        self.comment_master_dict['FILE_HEADER'] = self.get_text(node)

    def fetch_element_line_no(self, element):
        if not self.is_package_initialization_element(element)\
                and not self.is_anonymous_package(element):
            return element.sourceline - 1
        else:
            return 0

    def set_parent_instance(self, parent):
        prnt_instance = None
        existing_package_instance = None
        if self.fetch_element_line_no(parent) in self.parent_instance_dict and not self.is_anonymous_package(parent):
            self.logger.debug(
                "Setting existing parent in set_parent_instance() for {} at line {}, fetched from {} ".format(
                    self.get_element_tag(parent),
                    self.fetch_element_line_no(parent),
                    self.parent_instance_dict[self.fetch_element_line_no(parent)]))
            self.parent_instance = self.parent_instance_dict[self.fetch_element_line_no(parent)]
        else:
            if not self.is_package_element(parent) and not self.is_anonymous_package(parent):
                self.logger.debug("Creating new parent instance  for {} at line {}".format(self.get_element_tag(parent),
                                                                                           self.fetch_element_line_no(
                                                                                               parent)))
                prnt_instance = self.populate_instance(parent)
                # prnt_instance.set_instance_element(parent)
                prnt_instance.set_instance_element_line(self.fetch_element_line_no(parent))
                self.logger.debug("Newly created parent instance is of type {}".format(
                    type(prnt_instance.get_construct_instance_obj()).__name__))
            elif self.is_package_initialization_element(parent):
                self.logger.debug("Creating new parent instance for package initialization i.e., {} at line {}".format(
                    self.get_element_tag(parent),
                    self.fetch_element_line_no(parent)))
                prnt_instance = self.populate_instance(parent)
                prnt_instance.set_instance_element_line(self.fetch_element_line_no(parent))
                self.logger.debug("Newly created parent instance is of type {}".format(
                    type(prnt_instance.get_construct_instance_obj()).__name__))
            else:
                if self.is_package_element(parent) or self.is_anonymous_package(parent):
                    if 0 in self.parent_instance_dict:  # since 0 set as default for with or without package
                        prnt_instance = self.parent_instance_dict[0]
                        self.logger.debug(
                            "Fetching created package initialization instance  which is of type {} for {} element at line {}".format(
                                type(prnt_instance.get_construct_instance_obj()).__name__, self.get_element_tag(parent),
                                self.fetch_element_line_no(parent)))
                        existing_package_instance = self.fetch_existing_package(parent)
                        self.logger.debug("Checking for existing package for {}".format(parent))
                        if existing_package_instance is not None:
                            prnt_instance.set_construct_instance_obj(existing_package_instance)
                            self.existing_package_flag = True
                    else:
                        self.logger.debug(
                            "package_initialization element has not been set yet till the element {} at line {}".format(
                                self.get_element_tag(parent),
                                self.fetch_element_line_no(parent)))
            self.parent_instance = prnt_instance
            if self.is_anonymous_package(parent):
                # assuming line 1 for anonymous package
                self.parent_instance_dict[1] = prnt_instance
            else:
                self.parent_instance_dict[self.fetch_element_line_no(parent)] = prnt_instance

    def populate_instance(self, element):
        entity_obj = Entity()
        # instance_obj.set_instance_element(element)
        if type(element) != str:
            entity_obj.set_instance_element_line(self.fetch_element_line_no(element))
        entity_obj.set_construct_instance_obj(self.fetch_instance(element))
        entity_obj.set_instance_type(type(entity_obj.get_construct_instance_obj()).__name__)
        if entity_obj.get_instance_type() in self.entity_counter:
            self.entity_counter[entity_obj.get_instance_type()] += 1
        else:
            self.entity_counter[entity_obj.get_instance_type()] = 1
        self.logger.debug(
            "Setting entity_counter for element {} as {}".format(self.get_element_tag(element), self.entity_counter))
        instance_identifier = None
        self.logger.debug(
            "Populating instance identifier for {} instance in {} project".format(entity_obj.get_instance_type(),
                                                                                  self.project_dir))
        if Platform.is_unix_platform():
            instance_identifier = self.project_dir + '/' + entity_obj.get_instance_type() + '/attributes/'
        elif Platform.is_windows_platform():
            instance_identifier = self.project_dir + '\\' + entity_obj.get_instance_type() + '\\attributes\\'
        # instance_identifier += '_' + self.entity_counter[entity_obj.get_instance_type()]
        try:
            if not validate_loc(instance_identifier):
                if os.path.isdir(instance_identifier):
                    shutil.rmtree(instance_identifier)
                os.makedirs(instance_identifier)

        except OSError as e:
            self.logger.error(
                "Unable to create/delete entity directory {} ~ Process failed".format(instance_identifier))
            #Utility.clear_temp_folders()
            raise Exception("Comments Miner failed as entity directory creation failed")
        else:
            # append unique counter to make distinct json file xml_file_num
            entity_identifier = instance_identifier + entity_obj.get_instance_type() + '_' + str(self.xml_file_num) \
                                + '_' + str(self.entity_counter[entity_obj.get_instance_type()])
            entity_obj.set_identifier(entity_identifier)
            self.logger.debug("Setting instance_identifier for element {} as {}"
                              "".format(self.get_element_tag(element), entity_identifier))
        return entity_obj

    def fetch_parent_instance(self):
        return self.parent_instance

    def fetch_instance(self, element):
        if type(element) == str:
            if self.is_file_entity(element):
                return FileInfo()
            elif self.is_package_initialization_element(element):
                return PackageInfo()
        elif self.is_class_element(element):
            return ClassInfo()
        elif self.is_function_element(element) or self.is_constructor_element(element) or self.is_function_decl_element(element):
            return MethodInfo()
        elif self.is_static_block_element(element):
            return StaticBlockInfo()
        elif self.is_interface_element(element):
            return InterfaceInfo()
        elif self.is_enum_element(element):
            return EnumInfo()
        elif self.is_package_element(element) or self.is_package_initialization_element(element) or self.is_root_element(element):
            return PackageInfo()

    def fetch_existing_package(self, ele):
        """
        Check and fetch if package already instantiated in soccminer.
        :param ele: package element
        :return: PackageInstance if existing package else None
        """
        if not self.is_anonymous_package(ele):
            package_name = self.fetch_package_name(ele)
        else:
            package_name = "ANONYMOUS_PACKAGE"
        construct_info = []
        package_json_files = None
        entity_type = type(PackageInfo()).__name__
        package_json_dir = None
        if Platform.is_unix_platform():
            package_json_dir = self.project_dir + '/' + entity_type + '/attributes/'
        elif Platform.is_windows_platform():
            package_json_dir = self.project_dir + '\\' + entity_type + '\\attributes\\'
        if os.listdir(package_json_dir) != 0:
            construct_info = SerializeSoCCMiner.load_from_json_file(package_json_dir)

        for construct_info_dict in construct_info:
            if construct_info_dict['Package_Name'] == package_name or package_name == 'ANONYMOUS_PACKAGE':
                package_obj = PackageInfo()
                package_obj.set_package_name(package_name)
                package_obj.set_package_loc(construct_info_dict['Package_LOC'])
                package_obj.set_package_source(construct_info_dict['Package_Source_File'])
                package_obj.set_package_line_no(construct_info_dict['Package_Line_No'])
                self.existing_pckg_serialization_url = construct_info_dict['Package_Serialization_File_URL']
                return package_obj
            #elif package_name == 'ANONYMOUS_PACKAGE':
            #    return PackageInfo()
        return None

    def fetch_project_comments_count(self):
        self.logger.debug("fetch_project_comments_count(): {}".format(self.project_comments_dir))
        src_files = SourceFiles(self.project_comments_dir)
        src_files.fetch_source_files(src_files.loc, 'json')
        comment_count = len(src_files.get_files())
        del src_files
        return comment_count

    def proc_java_ast_elements(self, proj_dir, src_file_name, xml_file_name, xml_file_num):
        self.project_dir = proj_dir
        self.xml_file_num = xml_file_num
        self.src_file_name = src_file_name
        self.package_instance = None
        if Platform.is_unix_platform():
            proj_dir = proj_dir[:-1] if proj_dir.endswith('/') else proj_dir
            self.project_name = proj_dir.split('/')[-1].replace("/", "")
            if '/' in self.src_file_name:
                self.src_file_name = "/".join(src_file_name.split(self.project_name + '/')[1:]).replace("/", ".")
                self.src_file_name = self.src_file_name.replace("..", "." + self.project_name + ".")
                self.src_file_name = self.src_file_name[1:] if self.src_file_name.startswith(".") else self.src_file_name
        elif Platform.is_windows_platform():
            proj_dir = proj_dir[:-1] if proj_dir.endswith('\\') else proj_dir
            self.project_name = proj_dir.split('/')[-1].replace("\\", "")
            if "\\" in self.src_file_name:
                self.src_file_name = "\\".join(src_file_name.split(self.project_name + '\\')[1:]).replace("\\", ".")
                self.src_file_name = self.src_file_name.replace("..", "." + self.project_name + ".")
                self.src_file_name = self.src_file_name[1:] if self.src_file_name.startswith(".") else self.src_file_name

        # FileInfo entity
        file_instance_obj = self.populate_instance("File")
        self.file_obj = file_instance_obj.get_construct_instance_obj()
        self.file_obj.source_file_name = self.src_file_name
        self.file_obj.file_loc = self.fetch_construct_loc(src_file_name)
        self.logger.debug("File obj loc: {}, {}".format(self.file_obj.source_file_name, self.file_obj.file_loc))

        self.set_parent_instance("PACKAGE_INITIALIZATION")
        comments_before_package = []
        for ele in self.get_children_iter(self.root):
            package_name = None
            self.logger.debug("proc_java_ast_elements: {},{}".format(ele, len(list(self.root))))
            if self.is_package_element(ele):
                self.set_parent_instance(ele)
                self.logger.debug(
                    "verifying if package element at line {} instance set in {}".format(self.fetch_element_line_no(ele),
                                                                                        self.parent_instance_dict[
                                                                                            self.fetch_element_line_no(
                                                                                                ele)].get_instance_element_line()))
                self.logger.debug("Set instance of type {} for element at line {}".format(
                    type(self.fetch_parent_instance().get_construct_instance_obj()).__name__,
                    self.fetch_parent_instance().get_instance_element_line()))
                if not self.existing_package_flag:
                    self.package_entity_element = ele
                    # project_instance.package_info.append(self.fetch_parent_instance().get_construct_instance_obj())
                # since root serves as parent for top level elements/comments
                self.parent_instance_dict[self.fetch_element_line_no(self.root)] = self.fetch_parent_instance()
                self.package_instance = self.fetch_parent_instance().get_construct_instance_obj()

                self.logger.debug("Fetching file loc which contributes to Project KLOC")
                entity_obj = self.parent_instance_dict[self.fetch_element_line_no(ele)]
                if self.existing_package_flag:
                    file_loc = self.file_obj.file_loc
                    self.logger.debug("FILE LOC: {}".format(file_loc))
                    existing_pckg_loc = self.package_instance.get_package_loc() + file_loc
                    existing_pckg_source = self.package_instance.get_package_source()
                    existing_pckg_line_no = self.package_instance.get_package_line_no()
                    self.package_instance.set_package_loc(existing_pckg_loc)
                    self.package_instance.set_package_line_no(",".join([str(existing_pckg_line_no), str(self.fetch_element_line_no(ele))]))
                    self.package_instance.set_package_source(",".join([existing_pckg_source, self.src_file_name]))
                    self.package_instance.set_package_name(self.package_instance.get_package_name())
                    package_serialization_file = self.existing_pckg_serialization_url
                else:
                    self.package_instance.set_package_loc(self.fetch_construct_loc(xml_file_name))
                    self.package_instance.set_package_line_no(self.fetch_element_line_no(ele))
                    self.package_instance.set_package_source(self.src_file_name)
                    package_name = self.fetch_package_name(ele)
                    self.package_instance.set_package_name(package_name)
                    package_serialization_file = entity_obj.get_identifier()
                SerializeSoCCMiner.serialize_construct(self.package_instance, package_serialization_file)
            elif self.is_comment_element(ele) and self.fetch_element_line_no(ele) not in self.processed_comment_dict:
                if package_name is not None:
                    # CR - comments that are not in any entity particularly initial comments before class/interface
                    # or other entities
                    self.proc_comment_attributes(ele)
                else:
                    comments_before_package.append(ele)
            elif self.is_construct_element(ele):
                self.top_level_constructs.append(ele)
            self.logger.debug("processed child element {} at line {},{}".format(self.get_element_tag(ele),
                                                                                self.fetch_element_line_no(ele),
                                                                                len(list(self.root))))
        #  Processing initial comments that are present before
        #  package statement in source code just after the package statement has been processed by soccminer
        if len(comments_before_package) > 0:
            self.set_parent_instance(self.root)
            for comment_ele in comments_before_package:
                self.proc_comment_attributes(comment_ele)

        if self.package_instance is None:
            self.logger.debug("Processing anonymous package, self.package_instance: {}".format(self.package_instance))
            #self.set_parent_instance(self.root)
            self.set_parent_instance("ANONYMOUS_PACKAGE")

            #project_instance.package_info.append(self.fetch_parent_instance().get_construct_instance_obj())
            # assuming line 1 for anonymous package i.e., file without package
            self.parent_instance_dict[1] = self.fetch_parent_instance()
            self.package_instance = self.fetch_parent_instance().get_construct_instance_obj()
            self.package_instance.set_package_name("ANONYMOUS_PACKAGE")
            self.package_instance.set_package_line_no(self.fetch_element_line_no(self.root))
            self.package_instance.set_package_loc(self.fetch_construct_loc(xml_file_name))
            self.package_instance.set_package_source(self.src_file_name)
            if self.package_entity_element is not None:
                entity_obj = self.parent_instance_dict[self.fetch_element_line_no(self.package_entity_element)]
            else:
                entity_obj = self.parent_instance_dict[1]
            SerializeSoCCMiner.serialize_construct(self.package_instance, entity_obj.get_identifier())
        else:
            self.logger.debug("Package is present in the source file, self.package_instance: {}".format(self.package_instance))

        # fetch all constructs at all level
        for construct in self.top_level_constructs:
            self.fetch_constructs(construct)

        # process all constructs at all level and fetch the comments
        for construct in self.constructs_master:
            self.first_block = False  # resetting to capture signature of next construct
            self.construct_first_ele = None  # resetting
            self.construct_signature_list = []  # resetting
            self.construct_specifier_flag = False  # resetting

            self.logger.debug(
                "to begin identifying the parent of construct {} at line {}".format(self.get_element_tag(construct),
                                                                                    self.fetch_element_line_no(
                                                                                        construct)))
            prnt_construct = self.fetch_parent(construct)
            self.logger.debug(
                "{} at line {} is the parent of construct {} at line {}".format(self.get_element_tag(prnt_construct),
                                                                                self.fetch_element_line_no(
                                                                                    prnt_construct),
                                                                                self.get_element_tag(construct),
                                                                                self.fetch_element_line_no(construct)))
            if self.is_root_element(prnt_construct) or self.is_construct_element(prnt_construct):
                self.set_parent_instance(prnt_construct)
                #self.assoc_construct_to_construct(self.fetch_parent_instance(),
                #                                  self.parent_instance_dict[self.fetch_element_line_no(construct)])
                self.construct_obj_instance = self.parent_instance_dict[self.fetch_element_line_no(construct)].get_construct_instance_obj()
            self.logger.debug("Done associating construct {} at line {} with the parent {} at line {}"
                          "".format(self.get_element_tag(construct), self.fetch_element_line_no(construct),
                                    self.get_element_tag(prnt_construct), self.fetch_element_line_no(prnt_construct)))
            if ProcessParameter.miner_params['mining_level'] == 3 or ProcessParameter.miner_params['mining_level'] == 4:
                # line no attribute for construct
                self.set_construct_line_attr(construct)

                # construct category only for method construct
                if ASTHelper.is_method_info_obj(self.construct_obj_instance):
                    self.set_construct_catg_attr(self.fetch_construct_catg(construct))

            iter_index = 0
            for ele in self.get_children_iter(construct):
                self.logger.debug("Processing construct element {} at line {} commences".format(self.get_element_tag(ele),
                                                                                    self.get_element_line_number(ele)))
                self.proc_children(ele)
                if ProcessParameter.miner_params['mining_level'] == 3 or ProcessParameter.miner_params['mining_level'] == 4:
                    # name attribute for construct
                    if self.is_name_element(ele):
                        self.logger.debug("ATTR - name: {}".format(self.get_element_tag(ele)))
                        self.set_construct_name_attr(self.construct_obj_instance, ele)
                    # specifier attribute for class construct (<specifier> element is first level for class/interface
                    # but second level for method (will be under <type> element)
                    elif self.is_specifier_element(ele) or self.is_type_element(ele):
                        if self.is_type_element(ele):
                            for sub_ele in self.get_children_iter(ele):
                                if self.is_specifier_element(sub_ele):
                                    self.construct_specifier_flag = True
                                    self.logger.debug("ATTR - specifier(under type element): {}".format(self.get_element_tag(sub_ele)))
                                    self.set_construct_specifier_attr(self.construct_obj_instance, sub_ele)
                        else:
                            self.construct_specifier_flag = True
                            self.logger.debug("ATTR - specifier: {}".format(self.get_element_tag(ele)))
                            self.set_construct_specifier_attr(self.construct_obj_instance, ele)

                    # for anonymous class, to verify if the first element followed by class is super
                    iter_index += 1
                    if 1 == iter_index:
                        self.construct_first_ele = ele

                    if self.is_block_element(ele):
                        self.first_block = True  # so that further nodes are not appended in the signature

                    if not self.first_block:
                        self.construct_signature_list.append(ele)

                    # param_count attribute
                    # to fetch parameter count for construct (method)
                    if self.is_param_list_element(ele):
                        # param_count attribute
                        self.logger.debug("Setting param_count from parameter_list element at {}".format(self.fetch_element_line_no(ele)))
                        self.set_construct_param_cnt_attr(self.fetch_construct_param_count(ele))

                if ProcessParameter.miner_params['mining_level'] == 3 or \
                        ProcessParameter.miner_params['mining_level'] == 4:
                    # signature attribute
                    self.set_construct_signature_attr(self.construct_obj_instance,
                                                      self.fetch_construct_signature(self.construct_signature_list))
                    # type attribute
                    self.check_construct_type_attr()

                    # fetch the construct signature for anonymous class
                    if ASTHelper.is_class_info_obj(self.construct_obj_instance):
                        if self.construct_obj_instance.get_class_type() == XmlProperties.cnstrct_type_anonymous:
                            self.set_construct_name_attr(self.construct_obj_instance,
                                                         XmlProperties.cnstrct_type_anonymous)
                            _ = self.fetch_predecessor(construct)

                    # if no specifier element is present, replace default none with NO_SPECIFIER label
                    if not self.construct_specifier_flag:
                        self.logger.debug("construct_specifier_flag: {} for construct at line {} ".format(
                            self.construct_specifier_flag, self.fetch_element_line_no(construct)))
                        self.set_construct_specifier_attr(self.construct_obj_instance, XmlProperties.no_specifier_label)

                    # nested level if construct is of type class
                    nested_level_stack = []
                    nested_level_ind = 0
                    if ASTHelper.is_class_info_obj(self.construct_obj_instance):
                        nested_level_stack = self.fetch_predecessor(construct)
                        for stack_element in nested_level_stack:
                            if self.is_construct_element(stack_element):
                                nested_level_ind += 1
                        self.construct_obj_instance.set_nested_level(nested_level_ind)  # since base level is 0

                    # validating construct loc
                    construct_loc = self.fetch_construct_loc(construct)
                    self.set_construct_loc_attr(self.construct_obj_instance, construct_loc)

            # set project meta while parsing the constructs
            # project_instance; storing all constructs of project in master list
            # setting the source .java file of the respective construct as well
            if ProcessParameter.miner_params['mining_level'] == 3 or ProcessParameter.miner_params['mining_level'] == 4:
                entity_obj = self.parent_instance_dict[self.fetch_element_line_no(construct)]
                if ASTHelper.is_class_info_obj(self.construct_obj_instance):
                    # project_instance.append_project_class(self.construct_obj_instance)
                    self.construct_obj_instance.set_class_source(self.src_file_name)
                elif ASTHelper.is_method_info_obj(self.construct_obj_instance):
                    # project_instance.append_project_method(self.construct_obj_instance)
                    self.construct_obj_instance.set_method_source(self.src_file_name)
                elif ASTHelper.is_interface_info_obj(self.construct_obj_instance):
                    # project_instance.append_project_interface(self.construct_obj_instance)
                    self.construct_obj_instance.set_interface_source(self.src_file_name)
                elif ASTHelper.is_static_block_info_obj(self.construct_obj_instance):
                    # project_instance.append_project_static_block(self.construct_obj_instance)
                    self.construct_obj_instance.set_static_block_source(self.src_file_name)
                elif ASTHelper.is_enum_info_obj(self.construct_obj_instance):
                    # project_instance.append_project_static_block(self.construct_obj_instance)
                    self.construct_obj_instance.set_enum_source(self.src_file_name)
                SerializeSoCCMiner.serialize_construct(self.construct_obj_instance, entity_obj.get_identifier())

        self.file_obj.total_comments = self.all_cmnts_cntr
        SerializeSoCCMiner.serialize_construct(self.file_obj, file_instance_obj.get_identifier())
        self.logger.debug("Total comments in file: {}".format(self.all_cmnts_cntr))
        self.logger.debug("Total LOC: {}".format(self.file_obj.file_loc))
        #  resetting
        self.top_level_elements = []
        self.project_dir = None
        self.src_file_name = None
        self.comments_counter = 1
        self.nodes = []
        self.tree = None
        self.root = None
        self.comment_master_dict = {}
        self.file_header_comment = None
        self.unit_ele = None
        self.unit_ele_attributes = {}
        self.constructs_master = []
        self.top_level_constructs = []
        self.parent_instance = None
        self.parent_instance_dict = {}
        self.construct_signature_list = []
        self.first_block = None
        self.construct_obj_instance = None
        self.construct_first_ele = None
        self.construct_specifier_flag = None
        self.construct_param_list = []  # for storing parameters of a construct, for example function
        self.processed_comment_dict = {}
        self.consecutive_comment_dict = {}
        self.consecutive_comment_first = None
        self.consecutive_comment_last = None
        self.package_instance = None
        self.construct_signature_dict = {}
        self.existing_package_flag = None
        self.xml_file_num = None
        self.logger.info("{}: AST parsing ends for {}".format(xml_file_num, xml_file_name))
        # gc.disable()
        ASTHelper.clear_locals()
        # gc.enable()

    def set_construct_loc_attr(self, construct_obj, construct_loc):
        if ASTHelper.is_package_info_obj(construct_obj):
            construct_obj.set_package_loc(construct_loc)
        elif ASTHelper.is_class_info_obj(construct_obj):
            construct_obj.set_class_loc(construct_loc)
        elif ASTHelper.is_method_info_obj(construct_obj):
            construct_obj.set_method_loc(construct_loc)
        elif ASTHelper.is_interface_info_obj(construct_obj):
            construct_obj.set_interface_loc(construct_loc)
        elif ASTHelper.is_static_block_info_obj(construct_obj):
            construct_obj.set_static_block_loc(construct_loc)
        elif ASTHelper.is_enum_info_obj(construct_obj):
            construct_obj.set_enum_loc(construct_loc)

    def fetch_construct_loc(self, construct):
        ele_str = None
        construct_loc = 0
        src_lines = []
        self.logger.debug("Type of construct: {}".format(type(construct)))
        if self.is_lxml_element(construct):
            ele_str = self.convert_ele_to_xml(construct)
            # fetch the last index of construct element
            ele_list = ele_str.split(b'\n')
            ele_list.reverse()
            index = [ind for ind, list_item in enumerate(ele_list) if
                     self.get_element_tag(construct).split("}")[-1] in str(list_item)][0]
            construct_loc = len(ele_list) - index
            self.logger.debug(" LOC of {} at line {}: {} ".format(self.get_element_tag(construct),
                                                                   self.fetch_element_line_no(construct),
                                                                   construct_loc))
        else:
            if type(construct) == str:
                self.logger.debug(" Construct is of type str")
                if construct.lower().endswith("xml") or construct.lower().endswith("java"):
                    try:
                        fh = None
                        if construct.lower().endswith("java"):
                            fh = open(construct, "r", encoding='latin-1')
                        else:
                            fh = open(construct, "r")
                        src_lines = fh.readlines()
                        fh.close()
                        if construct.lower().endswith("xml"):
                            # removing 1 for xml declaration in xml format
                            construct_loc = len(src_lines) - 1
                        else:
                            construct_loc = len(src_lines)
                        src_lines = None
                        self.logger.debug(" LOC of file{}: {} ".format(construct, construct_loc))
                    except IOError as fh_exc:
                        self.logger.error("Error while fetching file loc for file {}: {}, {}".format(construct, fh_exc.errno, fh_exc.strerror))
                    else:
                        self.logger.debug(" LOC of file: {} ".format(construct_loc))
                else:
                    self.logger.debug(" Construct does not end with xml or java")
        return construct_loc

    def fetch_predecessor(self, ele):
        self.logger.debug("fetch_predecessor begins for {} at line {}".format(self.get_element_tag(ele),
                                                                          self.fetch_element_line_no(ele)))
        node_list = []
        while not self.is_root_element(ele):
            self.logger.debug("{} is not root element".format(self.get_element_tag(ele)))
            ele = self.get_parent(ele)
            node_list.append(copy(ele))  # copy to avoid removals while processing code elements
        if ASTHelper.is_class_info_obj(self.construct_obj_instance):
            if self.construct_obj_instance.get_class_type() == XmlProperties.cnstrct_type_anonymous:
                srcml_obj = SourceML()
                first_decl_statement = False
                for element in node_list:
                    self.logger.debug("{}".format(self.get_element_tag(element)))
                    if self.is_declaration_element(element) and not first_decl_statement:
                        first_decl_statement = True
                        self.set_construct_signature_attr(self.construct_obj_instance, srcml_obj.fetch_code_from_srcml(element))
        self.logger.debug("fetch_predecessor ends for {} at line {}".format(self.get_element_tag(ele),
                                                                          self.fetch_element_line_no(ele)))
        return node_list

    def check_and_process_consecutive_comment(self, comment_ele):
        """
        Handle continuous comments
        :param comment_ele: comment element
        :return: None
        """
        temp_comment_ele = comment_ele
        self.logger.debug("check_and_process_consecutive_comment() begins for comment at line {} ".format(self.fetch_element_line_no(comment_ele)))
        successive_comment_ele = temp_comment_ele
        successive_comment_cnt = 0
        local_comment_ele = None
        consecutive_comment_list = []
        try:
            comment_next_ele = self.get_next_element(temp_comment_ele)
            if comment_next_ele is not None: # comment at the end will return None
                if self.is_comment_element(comment_next_ele):
                    local_comment_ele = temp_comment_ele
                    self.consecutive_comment_dict[self.fetch_element_line_no(local_comment_ele)] = consecutive_comment_list

            while self.is_comment_element(successive_comment_ele): # 1 2
                if self.get_next_element(temp_comment_ele) is not None: # comment at the end will return None
                    if self.get_next_element(successive_comment_ele) is not None:
                        if self.is_comment_element(self.get_next_element(successive_comment_ele)):
                            next_comment_ele_line_no = self.fetch_element_line_no(self.get_next_element(successive_comment_ele))
                            self.processed_comment_dict[next_comment_ele_line_no] \
                                = self.get_next_element(successive_comment_ele)
                            self.consecutive_comment_dict[self.fetch_element_line_no(local_comment_ele)].append(next_comment_ele_line_no)
                            successive_comment_ele = self.get_next_element(successive_comment_ele)
                            successive_comment_cnt += 1
                        else:
                            successive_comment_ele = self.get_next_element(successive_comment_ele)
                    else:
                        break # break as next element is NoneType
                else:
                    break # break as next element is NoneType

            if successive_comment_cnt:
                self.consecutive_comment_first = comment_ele
                # fetch the last consecutive element form the stored value
                self.consecutive_comment_last = self.processed_comment_dict[self.consecutive_comment_dict[self.fetch_element_line_no(local_comment_ele)][-1]]
            else:
                self.logger.debug("Comment at line {} is not part of consecutive block of comments.".format(self.fetch_element_line_no(comment_ele)))
        except Exception as consecutive_cmnt_ex:
            self.logger.error("Unexpected error {} {}".format(sys.exc_info()[0], consecutive_cmnt_ex))
            pass

        self.logger.debug("check_and_process_consecutive_comment() ends for comment at line {} ".format(
            self.fetch_element_line_no(comment_ele)))

    def proc_children(self, element):
        if len(list(element)) != 0:
            for ele in self.get_children_iter(element):
                if not self.is_construct_element(ele):
                    self.logger.debug("proc_children: {} | {} | {}".format(ele.tag, ele.text, ele.sourceline))
                    if self.is_comment_element(ele) \
                            and self.fetch_element_line_no(ele) not in self.processed_comment_dict:
                        prnt_ele = self.fetch_parent(ele)
                        self.logger.debug("parent of comment at line {} is {} at line {}".format(self.fetch_element_line_no(ele),
                                                                                             self.get_element_tag(prnt_ele),
                                                                                             self.fetch_element_line_no(prnt_ele)))
                        self.set_parent_instance(prnt_ele)
                        self.proc_comment_attributes(ele)
                    self.proc_children(ele)
        else:
            return

    def check_construct_type_attr(self):
        self.logger.debug("check_construct_type_attr begins")
        generic_flag = self.validate_for_generic()
        derived_flag = self.validate_for_derived()
        anonymous_flag = self.validate_for_anonymous()
        self.logger.debug("generic_flag, derived_flag, anonymous_flag : {}, {}, {}".format(generic_flag, derived_flag, anonymous_flag))
        if anonymous_flag:
            self.set_construct_type_attr(XmlProperties.cnstrct_type_anonymous)
        elif generic_flag and derived_flag:
            self.set_construct_type_attr(XmlProperties.cnstrct_type_derived + '_' + XmlProperties.cnstrct_type_generic)
        elif generic_flag and not derived_flag:
            self.set_construct_type_attr(XmlProperties.cnstrct_type_generic)
        elif derived_flag and not generic_flag:
            self.set_construct_type_attr(XmlProperties.cnstrct_type_derived)
        else:
            self.set_construct_type_attr(XmlProperties.cnstrct_type_regular)
        self.logger.debug("check_construct_type_attr ends")

    def validate_for_derived(self):
        derived_flag = False
        for signature_element in self.construct_signature_list:
            element = copy(signature_element)
            if self.get_element_tag(element) == self.super_list_element:
                derived_flag = True
        return derived_flag

    def validate_for_anonymous(self):
        anonymous_flag = False
        for signature_element in self.construct_signature_list:
            element = copy(signature_element)
            if self.get_element_tag(element) == XmlProperties.super_element and \
                    self.get_element_tag(self.construct_first_ele) == XmlProperties.super_element:
                anonymous_flag = True
        return anonymous_flag

    def validate_for_generic(self):
        generic_flag = False
        for signature_element in self.construct_signature_list:
            element = copy(signature_element)
            for signature_descendent in self.get_descendants_iter(element):
                self.logger.debug("self.get_element_tag(signature_descendent): {}".format(self.get_element_tag(signature_descendent)))
                self.logger.debug("self.get_text(signature_descendent): {}".format(self.get_text(signature_descendent)))
                if self.get_element_tag(signature_descendent) == self.param_list_element and \
                        self.get_text(signature_descendent) == XmlProperties.open_angle_bracket or \
                        self.get_text(signature_descendent) == XmlProperties.xml_open_angle_bracket or \
                        self.get_text(signature_descendent) == XmlProperties.close_angle_bracket or \
                        self.get_text(signature_descendent) == XmlProperties.xml_close_angle_bracket:
                    generic_flag = True
        return generic_flag

    def set_construct_catg_attr(self, category):
        # applicable for method
        if type(self.construct_obj_instance).__name__ == "MethodInfo":
            self.construct_obj_instance.set_method_category(category)

    def set_construct_line_attr(self, construct):
        if ASTHelper.is_static_block_info_obj(self.construct_obj_instance):
            self.construct_obj_instance.set_static_block_line_no(self.fetch_element_line_no(construct))
        elif ASTHelper.is_method_info_obj(self.construct_obj_instance):
            self.logger.debug("ATTR: METHOD_LINE_NO {}".format(self.fetch_element_line_no(construct)))
            self.construct_obj_instance.set_method_line_no(self.fetch_element_line_no(construct))
        elif ASTHelper.is_class_info_obj(self.construct_obj_instance):
            self.construct_obj_instance.set_class_line_no(self.fetch_element_line_no(construct))
        elif ASTHelper.is_interface_info_obj(self.construct_obj_instance):
            self.construct_obj_instance.set_interface_line_no(self.fetch_element_line_no(construct))
        elif ASTHelper.is_enum_info_obj(self.construct_obj_instance):
            self.construct_obj_instance.set_enum_line_no(self.fetch_element_line_no(construct))

    def fetch_construct_catg(self, element):
        if self.is_function_element(element):
            return "FUNCTION"
        elif self.is_function_decl_element(element):
            return "FUNCTION_DECLARATION"
        elif self.is_constructor_element(element):
            return "CONSTRUCTOR"

    def set_construct_param_cnt_attr(self, param_count):
        # applicable for method
        if type(self.construct_obj_instance).__name__ == "MethodInfo":
            self.construct_obj_instance.set_method_param_cnt(param_count)

    def fetch_construct_param_count(self, construct_ele):
        self.logger.debug("ATTR: param_count: {}".format(len(list(construct_ele))))
        return len(list(construct_ele))  # assuming <parameter> are the only first level elements of <parameter_list>

    def set_construct_type_attr(self, construct_type):
        # applicable for class/method
        if type(self.construct_obj_instance).__name__ == "ClassInfo":
            self.construct_obj_instance.set_class_type(construct_type)
        if construct_type != XmlProperties.cnstrct_type_anonymous or \
                construct_type != XmlProperties.cnstrct_type_derived:
            if type(self.construct_obj_instance).__name__ == "MethodInfo":
                self.construct_obj_instance.set_method_type(construct_type)

    def set_construct_name_attr(self, construct_obj, attr_element):
        # applicable for class/method/interface
        if type(construct_obj).__name__ == "ClassInfo":
            if type(attr_element) == str:  # for attr_element
                construct_obj.set_class_name(attr_element)
            else:
                cls_name = self.get_text(attr_element)
                if cls_name is not None:
                    if len(cls_name) > 0:
                        construct_obj.set_class_name(cls_name)
                else:
                    for child_attr_element in self.get_children_iter(attr_element):
                        if self.is_name_element(child_attr_element):
                            cls_name = self.get_text(child_attr_element)
                            construct_obj.set_class_name(cls_name)
        elif type(construct_obj).__name__ == "InterfaceInfo":
            construct_obj.set_interface_name(self.get_text(attr_element))
        elif type(construct_obj).__name__ == "EnumInfo":
            construct_obj.set_enum_name(self.get_text(attr_element))
        elif type(construct_obj).__name__ == "MethodInfo":
            construct_obj.set_method_name(self.get_text(attr_element))

    def set_construct_signature_attr(self, construct_obj, signature):
        self.logger.debug("set_construct_signature_attr() - signature: {}".format(signature))
        # applicable for class/method/interface
        if type(construct_obj).__name__ == "ClassInfo":
            construct_obj.set_class_signature(signature)  #self.get_text(attr_element))
        elif type(construct_obj).__name__ == "InterfaceInfo":
            construct_obj.set_interface_signature(signature)
        elif type(construct_obj).__name__ == "EnumInfo":
            construct_obj.set_enum_signature(signature)
        elif type(construct_obj).__name__ == "MethodInfo":
            construct_obj.set_method_signature(signature)

    def set_construct_specifier_attr(self, construct_obj, attr_element):
        attr_element_text = attr_element if type(attr_element) == str else self.get_text(attr_element)
        # applicable for class/method/interface
        if ASTHelper.is_class_info_obj(construct_obj):
            curr_specifier = None
            if construct_obj.get_class_specifier() is not None:
                if construct_obj.get_class_specifier() == XmlProperties.no_specifier_label:
                    curr_specifier = attr_element_text
                else:
                    curr_specifier = construct_obj.get_class_specifier() + " " + attr_element_text
                construct_obj.set_class_specifier(curr_specifier)
            else:
                construct_obj.set_class_specifier(attr_element_text)
        elif ASTHelper.is_interface_info_obj(construct_obj):
            if construct_obj.get_interface_specifier() is not None:
                if construct_obj.get_interface_specifier() == XmlProperties.no_specifier_label:
                    curr_specifier = attr_element_text
                else:
                    curr_specifier = construct_obj.get_interface_specifier() + " " + attr_element_text
                construct_obj.set_interface_specifier(curr_specifier)
            else:
                construct_obj.set_interface_specifier(attr_element_text)
        elif ASTHelper.is_enum_info_obj(construct_obj):
            if construct_obj.get_enum_specifier() is not None:
                if construct_obj.get_enum_specifier() == XmlProperties.no_specifier_label:
                    curr_specifier = attr_element_text
                else:
                    curr_specifier = construct_obj.get_enum_specifier() + " " + attr_element_text
                construct_obj.set_enum_specifier(curr_specifier)
            else:
                construct_obj.set_enum_specifier(attr_element_text)
        elif ASTHelper.is_method_info_obj(construct_obj):
            if construct_obj.get_method_specifier() is not None:
                if construct_obj.get_method_specifier() == XmlProperties.no_specifier_label:
                    curr_specifier = attr_element_text
                else:
                    curr_specifier = construct_obj.get_method_specifier() + " " + attr_element_text
                construct_obj.set_method_specifier(curr_specifier)
            else:
                construct_obj.set_method_specifier(attr_element_text)

    def fetch_constructs(self, construct):
        for child in self.get_elements_iter(construct):
            if self.is_construct_element(child):
                self.logger.debug("fetch_construct begins for {} at {}".format(self.get_element_tag(child),
                                                                           self.fetch_element_line_no(child)))
                self.set_parent_instance(child)
                self.constructs_master.append(child)

    def fetch_package_name(self, element):
        package_name = []
        self.logger.debug(
            "fetch_package_name: retrieving package_name for {} at line {}".format(self.get_element_tag(element),
                                                                                   self.fetch_element_line_no(element)))
        for sub_ele in self.get_descendants_iter(element):
            name_seg = self.get_text(sub_ele)
            self.logger.debug("package name segment: {}".format(name_seg))
            package_name.append(name_seg)
        package_name_ne = filter(None.__ne__, package_name)
        return ''.join(package_name_ne)

    def fetch_construct_signature(self, signature_list):
        temp_xml_root = etree.Element(SourceML.unit_element)
        for signature_element in signature_list:
            element = copy(signature_element)
            self.logger.debug("appending to signature_tree: |{}|".format(element))
            temp_xml_root.append(element)
        temp_xml_tree = etree.ElementTree(temp_xml_root)
        srcml_obj = SourceML()
        signature_srcd = srcml_obj.fetch_code_from_srcml(temp_xml_tree)
        self.logger.debug("signature_srcd: |{}|".format(signature_srcd))
        return signature_srcd

    def release_obj(self, obj):
        del obj
        self.logger.debug("GC status: {}".format(gc.isenabled()))
        gc.collect()

    def fetch_parent(self, element):
        self.logger.debug("fetch_parent begins for {} at line {}".format(self.get_element_tag(element),
                                                                     self.get_element_line_number(element)))
        parent_ele = self.extract_assoc_block_ele(element)
        self.logger.debug("fetch_parent: parent_ele {}".format(self.get_element_tag(parent_ele),
                                                           self.get_element_line_number(parent_ele)))
        if not self.is_root_element(parent_ele):
            self.logger.debug("fetch_parent: parent_ele {} is not root element".format(self.get_element_tag(parent_ele)))
            #if not self.is_block_element(self.get_next_element(parent_ele)):
            while not self.is_construct_element(parent_ele) and not self.is_root_element(parent_ele):
                self.logger.debug("fetch_parent: parent_ele {} is not construct or root element, "
                              "invoking extract_assoc_block_ele".format(self.get_element_tag(parent_ele)))
                parent_ele = self.extract_assoc_block_ele(parent_ele)
        return parent_ele

    def assoc_comment_to_construct(self, parent_instance, comment_instance):
        if type(parent_instance).__name__ == "ClassInfo":
            parent_instance.append_class_level_comments(comment_instance)
        elif type(parent_instance).__name__ == "MethodInfo":
            parent_instance.append_method_level_comments(comment_instance)
        elif type(parent_instance).__name__ == "InterfaceInfo":
            parent_instance.append_interface_level_comments(comment_instance)
        elif type(parent_instance).__name__ == "StaticBlockInfo":
            parent_instance.append_static_block_level_comments(comment_instance)
        elif type(parent_instance).__name__ == "PackageInfo":
            parent_instance.append_package_level_comments(comment_instance)
        elif type(parent_instance).__name__ == "EnumInfo":
            parent_instance.append_enum_level_comments(comment_instance)

    def assoc_construct_to_construct(self, parent, construct):
        parent_instance = parent.get_construct_instance_obj()
        construct_instance = construct.get_construct_instance_obj()
        self.logger.debug("associating construct_instance {} at line {} with parent_instance {} at line {}"
                      "".format(type(construct_instance).__name__, construct.get_instance_element_line(),
                                type(parent_instance).__name__, parent.get_instance_element_line()))
        if type(construct_instance).__name__ == "ClassInfo":
            if type(parent_instance).__name__ == "PackageInfo":
                parent_instance.append_class_info(construct_instance)
            elif type(parent_instance).__name__ == "ClassInfo":
                parent_instance.append_nested_class_info(construct_instance)
            elif type(parent_instance).__name__ == "MethodInfo":
                parent_instance.append_class_in_method_info(construct_instance)
            elif type(parent_instance).__name__ == "InterfaceInfo":
                parent_instance.append_class_in_interface_info(construct_instance)
        elif type(construct_instance).__name__ == "EnumInfo":
            if type(parent_instance).__name__ == "PackageInfo":
                parent_instance.append_enum_info(construct_instance)
            elif type(parent_instance).__name__ == "ClassInfo":
                parent_instance.append_nested_class_info(construct_instance)
            elif type(parent_instance).__name__ == "MethodInfo":
                parent_instance.append_class_in_method_info(construct_instance)
            elif type(parent_instance).__name__ == "InterfaceInfo":
                parent_instance.append_class_in_interface_info(construct_instance)
        elif type(construct_instance).__name__ == "InterfaceInfo":
            if type(parent_instance).__name__ == "ClassInfo":
                parent_instance.append_class_lvl_interface_info(construct_instance)
            elif type(parent_instance).__name__ == "PackageInfo":
                parent_instance.append_interface_info(construct_instance)
        elif type(construct_instance).__name__ == "MethodInfo":
            if type(parent_instance).__name__ == "ClassInfo":
                parent_instance.append_class_method_info(construct_instance)
            elif type(parent_instance).__name__ == "InterfaceInfo":
                parent_instance.append_interface_method_info(construct_instance)
            elif type(parent_instance).__name__ == "PackageInfo":
                parent_instance.append_method_info(construct_instance)
        elif type(construct_instance).__name__ == "StaticBlockInfo":
            if type(parent_instance).__name__ == "PackageInfo":
                parent_instance.append_package_static_block_info(construct_instance)  # Encountered scenarios where it occurs outside class
            else:
                parent_instance.append_static_block_info(construct_instance)  # for Most often found in Class

    def fetch_succeeding_element(self, comment_instance, ele):
        try:
            if self.get_next_element(ele) is None:
                comment_instance.set_comment_category("NON-HEADER")
                self.logger.debug(
                    "fetch_succeding_element(): to identify parent of {} which is the last element".format(ele))
                assoc_parent_ele_next = self.identify_parent(ele)
                if not self.is_root_element(assoc_parent_ele_next):
                    comment_instance.set_last_element_in(self.get_element_tag(assoc_parent_ele_next))
                    self.logger.debug("***Comment Next element- (Last element in): {}".format(assoc_parent_ele_next))
                    if self.get_next_element(assoc_parent_ele_next) is None:
                        # last element in block, hence fetching parent of the block and get the next element
                        ele_for_src_cd = self.get_next_element(self.get_parent(assoc_parent_ele_next))
                        if ele_for_src_cd is not None:
                            self.logger.debug("***e Comment Next element- (Next to assoc parent element's parent): {} at line {}".format(ele_for_src_cd,self.fetch_element_line_no(ele_for_src_cd)))
                            comment_instance.set_succeeding_element(ele_for_src_cd)  # contains the xml element; input for succeeding code
                            comment_instance.set_succeeding_node(self.get_element_tag(ele_for_src_cd))  # contains the name (or tag)
                        else:
                            comment_instance.set_last_element_in("FILE")
                            comment_instance.set_succeeding_code("NA")
                            comment_instance.set_succeeding_element("EOF")
                            comment_instance.set_succeeding_node("EOF")  # contains the name (or tag)
                    else:
                        ele_for_src_cd = self.get_next_element(assoc_parent_ele_next)
                        self.logger.debug("***f Comment Next element- (Next to assoc parent element): {} at line {}".format(ele_for_src_cd,
                                      self.fetch_element_line_no(ele_for_src_cd)))
                        comment_instance.set_succeeding_element(ele_for_src_cd)
                        comment_instance.set_succeeding_node(self.get_element_tag(ele_for_src_cd))

                else:
                    comment_instance.set_last_element_in("FILE")
                    comment_instance.set_succeeding_code("NA")
                    comment_instance.set_succeeding_element("EOF")
                    comment_instance.set_succeeding_node("EOF")
            else:
                comment_instance.set_last_element_in("NA")
                ele_for_src_cd = self.get_next_element(ele)
                if self.get_element_tag(ele_for_src_cd) in XmlProperties.construct_ele_list:
                    comment_instance.set_comment_category("HEADER")
                else:
                    comment_instance.set_comment_category("NON-HEADER")
                    self.logger.debug("****** Comment Next element 3: {}".format(ele_for_src_cd))
                    self.logger.debug("Set succeeding element: {},{} with the len(child) is {}".format(self.get_element_tag(ele_for_src_cd),
                                                                 self.fetch_element_line_no(ele_for_src_cd),
                                                                 len(list(ele_for_src_cd))))
                comment_instance.set_succeeding_element(ele_for_src_cd)
                comment_instance.set_succeeding_node(self.get_element_tag(ele_for_src_cd))
        except Exception as ex:
            self.logger.error("Unexpected error in fetching succeeding element {} {}".format(sys.exc_info()[0], ex))
            raise

    def fetch_preceding_element(self, comment_instance, ele):
        if self.get_previous_element(ele) is None:
            assoc_parent_ele_prev = self.identify_parent(ele)
            self.logger.debug("fetch_precceding_element(): Parent of the element {} at line {} is {} ".format(ele, self.fetch_element_line_no(assoc_parent_ele_prev), assoc_parent_ele_prev))
            if not(self.is_root_element(assoc_parent_ele_prev) and self.fetch_element_line_no(assoc_parent_ele_prev) == 1):
                self.logger.debug("***********Comment Previous element parent (First element in): {}".format(assoc_parent_ele_prev))
                comment_instance.set_first_element_in(self.get_element_tag(assoc_parent_ele_prev))
                # since first element in construct/block, the construct/block is set as the preceding element, as
                # it will be invalid to fetch the previous element to the construct/block and set it as preceding element
                comment_instance.set_preceding_element(assoc_parent_ele_prev)
                comment_instance.set_preceding_node(self.get_element_tag(assoc_parent_ele_prev))
            else:
                comment_instance.set_first_element_in("FILE")
                comment_instance.set_comment_category("HEADER")
                comment_instance.set_preceding_code("NA")
                comment_instance.set_preceding_element("NA")
                comment_instance.set_preceding_node("NA")
        else:
            prev_ele = self.get_previous_element(ele)
            self.logger.debug("Comment Previous element 2: ".format(prev_ele))
            comment_instance.set_first_element_in("NA")
            comment_instance.set_preceding_element(prev_ele)
            comment_instance.set_preceding_node(self.get_element_tag(prev_ele))

    def identify_parent(self, element):
        try:
            self.logger.debug("identify_parent() begins for {} at line {}".format(element, self.fetch_element_line_no(element)))
            parent_node = self.get_parent(element)
            self.logger.debug(
                "identify_parent(): parent for {} at line {} is {}".format(element, self.fetch_element_line_no(element), parent_node))
            parent_node_element = self.get_element_tag(parent_node)
            if not self.is_root_element(parent_node):
                while self.is_block_element(self.get_element_tag(parent_node)) or \
                        self.is_block_content_element(self.get_element_tag(parent_node)):
                    if self.is_block_content_element(parent_node_element):
                        parent_node = self.get_parent(self.get_parent(parent_node))
                    elif self.is_block_element(parent_node_element):
                        parent_node = self.get_parent(parent_node)
        except Exception as ex:
            self.logger.error("Unexpected error {} {}".format(sys.exc_info()[0], ex))
            raise
        else:
            return parent_node

    def extract_assoc_block_ele(self, node):
        non_block_parent = None
        self.logger.debug("1. extract_assoc_block_ele begins for {} at line {}"
                      "".format(self.get_element_tag(node), self.fetch_element_line_no(node)))
        parent_node = self.get_parent(node)
        self.logger.debug("2. extract_assoc_block_ele: parent_node of {} at line{} is {} "
                      "".format(self.get_element_tag(node),self.fetch_element_line_no(node), self.get_element_tag(parent_node)))
        if not self.is_top_level_element(node):
            while not self.is_root_element(parent_node):
                self.logger.debug("3. extract_assoc_block_ele: {} {}".format(self.get_element_tag(parent_node), self.fetch_element_line_no(parent_node)))
                if self.is_block_element(parent_node):
                    block_parent = self.get_parent(parent_node)
                    self.logger.debug("4. extract_assoc_block_ele: {} {} {} {}".format(self.get_element_tag(parent_node),
                          self.fetch_element_line_no(parent_node), self.get_element_tag(block_parent),
                          self.fetch_element_line_no(block_parent)))
                    return self.get_parent(block_parent) if self.is_auxiliary(block_parent) else block_parent
                else:
                    self.logger.debug("b. extract_assoc_block_ele: {}".format(self.get_element_tag(parent_node),
                          self.fetch_element_line_no(parent_node)))
                    non_block_parent = parent_node
                    parent_node = self.get_parent(parent_node)
            return self.get_parent(non_block_parent) if self.is_auxiliary(non_block_parent) else non_block_parent
        else:
            self.logger.debug("extract_assoc_block_ele: top level element, hence returning {} at line {}".format(self.root,self.fetch_element_line_no(self.root)))
            return self.root

    def fetch_comment_assoc_block(self, comment_instance, comment_ele):
        comment_assoc_block_ele = self.extract_assoc_block_ele(comment_ele)
        self.logger.debug("comment at line {} is associated with block element {} at line {} ".format(self.fetch_element_line_no(comment_ele),
              self.get_element_tag(comment_assoc_block_ele), self.fetch_element_line_no(comment_assoc_block_ele)))
        if not self.is_root_element(comment_assoc_block_ele):
            if self.is_construct_element(self.get_element_tag(comment_assoc_block_ele)):
                comment_instance.set_comment_sub_category("NON_BLOCK_LEVEL")
                comment_instance.set_comment_sub_category_type("CONSTRUCT_ENTITY")
            elif self.is_control_element(self.get_element_tag(comment_assoc_block_ele)):
                comment_instance.set_comment_sub_category("BLOCK_LEVEL")
                comment_instance.set_comment_sub_category_type("CONTROL")
            elif self.is_exception_element(self.get_element_tag(comment_assoc_block_ele)):
                comment_instance.set_comment_sub_category("BLOCK_LEVEL")
                comment_instance.set_comment_sub_category_type("EXCEPTION")
            elif self.is_expr_stmt_element(self.get_element_tag(comment_assoc_block_ele)):
                comment_instance.set_comment_sub_category("BLOCK_LEVEL")
                comment_instance.set_comment_sub_category_type("EXPRESSION")
            else:
                comment_instance.set_comment_sub_category("BLOCK_LEVEL")
                comment_instance.set_comment_sub_category_type("OTHERS")
            comment_instance.set_comment_assoc_block_ele(
                "Package" if self.is_root_element(comment_assoc_block_ele) else self.get_element_tag(comment_assoc_block_ele))
        else:
            comment_instance.set_comment_sub_category("NON_BLOCK_LEVEL")
            comment_instance.set_comment_sub_category_type("PACKAGE_ENTITY")
            comment_instance.set_comment_assoc_block_ele(
                "Package" if self.is_root_element(comment_assoc_block_ele) else self.get_element_tag(self.root))

    def fetch_comment_level(self, comment_parent_instance):
        if type(comment_parent_instance).__name__ == "ClassInfo":
            return "Class"
        elif type(comment_parent_instance).__name__ == "MethodInfo":
            return "Method"
        elif type(comment_parent_instance).__name__ == "InterfaceInfo":
            return "Interface"
        elif type(comment_parent_instance).__name__ == "StaticBlockInfo":
            return "StaticBlock"
        elif type(comment_parent_instance).__name__ == "PackageInfo":
            return "Package"
        elif type(comment_parent_instance).__name__ == "EnumInfo":
            return "Enum"

    def fetch_element_attribute(self, element, attribute_name=None):
        if attribute_name is not None:
            if attribute_name in element.attrib:
                return element.attrib[attribute_name]
            else:
                self.logger.error(
                    "attribute_name: {} does not exist for the {}".format(attribute_name, self.get_element_tag(element)))
                print("attribute_name: {} does not exist for the {}".format(attribute_name, self.get_element_tag(element)))
                return None

    def process_comment_parents(self, comment_ele):
        comment_parents = []
        prnt_ele = self.get_parent(comment_ele)
        self.logger.debug("Parent of comment at line no {} is {}".format(self.fetch_element_line_no(comment_ele), prnt_ele))
        while not self.is_root_element(prnt_ele):
            if not self.is_block_element(prnt_ele):
                if not self.is_block_content_element(prnt_ele):
                    comment_parents.append(copy(prnt_ele))
            prnt_ele = self.get_parent(prnt_ele)

        # append package name if exists
        if self.package_instance is not None:
            self.logger.debug("appending package name: {}".format(self.package_instance.get_package_name()))
            comment_parents.append(self.package_instance.get_package_name())
        else:
            if len(comment_parents)  == 0:
                self.logger.debug("appending anonymous package as parent")
                comment_parents.append("ANONYMOUS_PACKAGE")
        self.logger.debug("Comment Parents: {}".format(comment_parents))
        return comment_parents

    #  Although functionality is generic, included to fetch method signature
    def fetch_construct_signature_list(self, construct_ele):
        self.logger.debug("Processing signature for element {} at line {}".format(self.get_element_tag(construct_ele),self.fetch_element_line_no(construct_ele)))
        signature_list = []
        first_block = False
        if len(list(construct_ele)) != 0:
            self.logger.debug("Len of construct element: {}".format(len(list(construct_ele))))
            for ele in self.get_children_iter(construct_ele):
                if self.is_block_element(ele):
                    first_block = True  # so that further nodes are not appended in the signature
                if not first_block:
                    self.logger.debug("Appending element to signature: {}".format(self.get_element_tag(ele)))
                    signature_list.append(ele)
        self.logger.debug("Signature List: {}".format(signature_list))
        return signature_list

    def is_leaf_node(self, node):
        if type(node) == str:
            return True
        else:
            return False if len(list(node)) != 0 else True

    def process_construct_name_element(self, construct_ele):
        self.logger.debug("Len of construct ele: {}, {}".format(len(list(construct_ele)), self.get_element_tag(construct_ele)))
        for ele in self.get_children_iter(construct_ele):
            if self.is_name_element(ele):
                return ele
        return "ANONYMOUS"

    def fetch_construct_name_element(self, construct_ele):
        name_ele = None
        while not self.is_leaf_node(construct_ele):
            name_ele = self.process_construct_name_element(construct_ele)
            self.logger.debug("Returned name_ele {} len is {}".format(name_ele,len(list(name_ele))))
            construct_ele = name_ele

        return name_ele

    def process_comment_parent_identifier(self, preceding_parents_list):
        comment_identifier = ""  # comment parent identifier
        comment_trace = ""       # code trace inside parent
        prev_comment_trace_ele = ""
        for ele in preceding_parents_list[::-1]:  # reverse order of preceding parents list
            parent_ele = ele
            self.logger.debug("Validating if comment parent ele {} is construct element".format(parent_ele))
            if self.is_construct_element(parent_ele):
                # empty code trace if intermediate construct (class/interface is encountered)
                if len(comment_trace) > 0:
                    # static block construct does not have name and is therefore necessary to retain trace
                    if not self.is_static_block_element(parent_ele):
                        comment_trace = ""
                if self.is_class_element(parent_ele) or self.is_interface_element(parent_ele)\
                        or self.is_enum_element(parent_ele) :
                    self.logger.debug("Len of class elements at line no {} is {}"
                                  "".format(self.fetch_element_line_no(parent_ele), len(list(parent_ele))))
                    name_ele = self.fetch_construct_name_element(parent_ele)
                    class_name = None
                    self.logger.debug("Fetched name element type, len, text: {}".format(type(name_ele).__name__))
                    if type(name_ele).__name__ == "_Element":
                        self.logger.debug("Fetched name element type, len, text: {},{}".format(type(name_ele).__name__,
                                                                                           self.get_text(name_ele)))
                        class_name = self.get_text(name_ele)
                    else:
                        if class_name is None:
                            class_name = "ANONYMOUS"
                    self.logger.debug("Class name text: {}".format(class_name))
                    comment_identifier += class_name + "."
                    self.logger.debug("Appending class/interface Comment Identifier: {}".format(comment_identifier))
                elif self.is_function_element(parent_ele) \
                        or self.is_constructor_element(parent_ele):
                    method_signature = None
                    if self.fetch_element_line_no(parent_ele) not in self.construct_signature_dict:
                        method_signature = self.fetch_construct_signature(
                            self.fetch_construct_signature_list(parent_ele)).strip()
                        self.construct_signature_dict[self.fetch_element_line_no(parent_ele)] = method_signature
                    else:
                        method_signature = self.construct_signature_dict[self.fetch_element_line_no(parent_ele)]
                    method_sign_annotation_rmvd = self.remove_annotation_from_signature(method_signature)
                    comment_identifier += method_sign_annotation_rmvd + "."
                    self.logger.debug("Appending function/constructor Comment Identifier: {}".format(comment_identifier))
            else:
                self.logger.debug("{} is other than construct element and is of type {}".format(parent_ele, type(parent_ele).__name__))
                if type(parent_ele).__name__ == "_Element":
                    # remove if_stmt followed by if with if_stmt, same applies for decl_stmt and expr_stmt
                    # this patter applies to only these three as per srcml java documentation
                    comment_trace_ele = self.get_element_tag(parent_ele).replace(XmlProperties.srcml_ns, "")
                    if len(prev_comment_trace_ele) > 0:
                        if (self.is_decl_element(parent_ele) and self.is_decl_stmt_element(prev_comment_trace_ele)) or \
                                (self.is_if_ele(parent_ele) and self.is_if_stmt_element(prev_comment_trace_ele)) or \
                                (self.is_else_ele(parent_ele) and self.is_if_stmt_element(prev_comment_trace_ele)) or \
                                (self.is_expr_ele(parent_ele) and self.is_expression_stmt_element(prev_comment_trace_ele)):
                            self.logger.debug("trace ele, prev trace ele: {},{}".format(parent_ele,prev_comment_trace_ele))
                            prev_comment_trace_ele = ""
                        else:
                            self.logger.debug("2 trace ele, prev trace ele: {},{}".format(parent_ele, prev_comment_trace_ele))
                            comment_trace +=  comment_trace_ele + "."
                            prev_comment_trace_ele = comment_trace_ele
                    else:
                        comment_trace +=  comment_trace_ele + "."
                        prev_comment_trace_ele = comment_trace_ele
                    self.logger.debug("Appending other element Comment Identifier: {}".format(comment_trace))
                elif type(parent_ele) == str:
                    comment_identifier += parent_ele + "."
                    self.logger.debug("Appending str (i.e., package name) Comment Identifier: {}".format(comment_identifier))

        if len(comment_trace) == 0:
            comment_trace = ""

        comment_identifier = comment_identifier[:-1] if comment_identifier[-1] == "." else comment_identifier
        comment_trace = comment_trace[:-1] if len(comment_trace) != 0 and comment_trace[-1] == "." else comment_trace

        self.logger.debug("Comment Identifier, Comment Trace: {}, {}".format(comment_identifier, comment_trace))
        return comment_identifier, comment_trace

    def remove_annotation_from_signature(self, signature):
        self.logger.debug("Remove annotation from signature for: {}".format(signature))
        annotation_rmvd_signature = ""
        signature_elements = signature.split("\n")
        for signature_element in signature_elements:
            if signature_element.startswith("@"):
                self.logger.debug("Ignoring the annotation {}".format(signature_element))
            else:
                annotation_rmvd_signature += signature_element.strip()
        return annotation_rmvd_signature

    def proc_comment_attributes(self, element):
        comment_instance = CommentInfo()
        comment_line_no = self.fetch_element_line_no(element)
        comment_instance.set_comment_file_name(self.src_file_name)
        self.all_cmnts_cntr += 1

        # check for consecutive comments
        self.consecutive_comment_first = None  # resetting
        self.consecutive_comment_last = None  # resetting
        self.check_and_process_consecutive_comment(element)
        comment_instance.set_comment_element(element)

        comment_parent_instance = self.fetch_parent_instance().get_construct_instance_obj()
        if ASTHelper.is_package_info_obj(comment_parent_instance):
            comment_parent_instance = self.file_obj
        self.project_comments_dir = self.project_dir + '/' + type(comment_parent_instance).__name__ + '/comments'

        #self.assoc_comment_to_construct(comment_parent_instance, comment_instance)
        self.logger.debug("Setting comment text attribute for comment at line {}".format(comment_line_no))
        # comment text attribute
        if self.fetch_element_line_no(element) in self.consecutive_comment_dict:
            consecutive_text = "" + self.get_text(element)
            for consecutive_comment_ele_line in self.processed_comment_dict:
                consecutive_text += "\n" + self.get_text(self.processed_comment_dict[consecutive_comment_ele_line])
            comment_instance.set_comment_text(consecutive_text)
        else:
            comment_instance.set_comment_text(self.get_text(element))
        # lineno
        comment_instance.set_comment_line_no(comment_line_no)

        # Only for mining level 2 (elaborate comment attributes) and mining level 4 (all attributes)
        self.logger.debug("proc_comment_attributes: Mining level param: {}".format(ProcessParameter.miner_params['mining_level']))
        if ProcessParameter.miner_params['mining_level'] == 2 or ProcessParameter.miner_params['mining_level'] == 4:
            self.logger.debug("Setting comment level attribute for comment at line {} {}".format(comment_line_no, len(list(self.root))))
            # comment level, sublevel can be manipulated from level
            comment_instance.set_comment_level(self.fetch_comment_level(comment_parent_instance))
            comment_instance.append_preceding_parents(self.process_comment_parents(element))
            self.logger.debug("3. Comment parents: {}".format(comment_instance.get_preceding_parents()))
            comment_parent_identifier, comment_trace = self.process_comment_parent_identifier(comment_instance.get_preceding_parents())
            comment_instance.set_comment_parent_identifier(comment_parent_identifier)
            comment_instance.set_comment_trace(comment_trace)

            self.logger.debug("Setting comment type attribute for comment at line {} {}".format(comment_line_no, len(list(self.root))))
            # type of comment line or block
            comment_instance.set_comment_type(self.fetch_element_attribute(element, "type"))
            self.logger.debug("Setting comment category, sub-category, assoc_block_ele for comment at line {} {}".format(comment_line_no, len(list(self.root))))
            # category, sub-category, assoc_block_ele
            self.fetch_comment_assoc_block(comment_instance, element)
            self.logger.debug("Setting comment succeeding element, code for comment at line {} {}".format(comment_line_no, len(list(self.root))))
            # last element in, succeeding element, succeeding code
            # if consecutive comments, pass the first and last comment for fetching preceding and succeeding element
            if self.consecutive_comment_last is not None:
                self.fetch_succeeding_element(comment_instance, self.consecutive_comment_last)
            else:
                self.fetch_succeeding_element(comment_instance, element)
            self.logger.debug("Setting comment preceding element, code for comment at line {} {}".format(comment_line_no, len(list(self.root))))
            if self.consecutive_comment_first is not None:
                self.fetch_preceding_element(comment_instance, self.consecutive_comment_first)
            else:
                self.fetch_preceding_element(comment_instance, element)
            # succeeding code - must be invoked after setting succeeding element
            srcml_obj = SourceML()
            comment_instance.set_succeeding_code(srcml_obj.fetch_code_from_srcml(copy(comment_instance.get_succeeding_element())))
            # preceding code - must be invoked after setting preceding element

            comment_instance.set_preceding_code(srcml_obj.fetch_code_from_srcml(copy(comment_instance.get_preceding_element())))

        self.create_dir(self.project_comments_dir)
        self.logger.debug("Comments Directory: {}".format(self.project_comments_dir))
        proj_entity_type_comments_count = self.fetch_project_comments_count()
        logging.debug("proj_entity_type_comments_count: {}".format(proj_entity_type_comments_count))
        self.comments_counter = 1 if proj_entity_type_comments_count == 0 else proj_entity_type_comments_count + 1
        logging.debug("comments_counter: {}".format(self.comments_counter))
        SerializeSoCCMiner.serialize_construct(comment_instance,
                                               self.project_comments_dir + '/comment_' + str(self.xml_file_num) + '_' + str(self.comments_counter))
        self.comments_counter += 1

    def create_dir(self, dir):
        if not validate_loc(dir):
            os.makedirs(dir)

    def is_top_level_element(self, node):
        return True if self.is_root_element(self.get_parent(node)) else False


class XmlParsing:

    @staticmethod
    def ast_parsing(xmlobj, src_file, xml_file, proj_dir, xml_file_number):
        logging.info("XML parsing begins for {}".format(xml_file))

        #xmlobj.logger = logging
        xmlobj.tree = etree.parse(xml_file)
        xmlobj.root = xmlobj.get_root()
        xmlobj.set_unit_element()
        xmlobj.proc_java_ast_elements(proj_dir, src_file, xml_file, xml_file_number)

        # Clearing
        del xmlobj
        ASTHelper.clear_locals()
        gc.collect()

    @staticmethod
    def ast_parsing_multiprocessing(src_file, xml_file, proj_dir, xml_file_number, exception_obj, log_level):
        source_ast_parser_obj = XmlProperties(xml_file)

        # create exception dir

        # log for each AST parsing
        #ast_log = ""
        #if Platform.is_unix_platform():
        #    ast_log = source_ast_parser_obj.xml_file.split('/')[-1].replace(".xml", "_" + datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + '.log')
        #elif Platform.is_windows_platform():
        #    ast_log = source_ast_parser_obj.xml_file.split('\\')[-1].replace(".xml", "_" + datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + '.log')
        #source_ast_parser_obj.logger = SoCCMinerLogger.fetch_ast_parsing_log(ast_log, log_level)
        source_ast_parser_obj.logger = logging
        source_ast_parser_obj.logger.info("{}: AST parsing begins for {}".format(xml_file_number, xml_file))

        try:
            source_ast_parser_obj.tree = etree.parse(xml_file)
            source_ast_parser_obj.root = source_ast_parser_obj.get_root()
            source_ast_parser_obj.set_unit_element()
            source_ast_parser_obj.proc_java_ast_elements(proj_dir, src_file, xml_file, xml_file_number)
        except Exception as ast_unknown_exception:
            project_name = ""
            exception_dir = ''
            java_file = ''

            if Platform.is_unix_platform():
                proj_dir = proj_dir[:-1] if proj_dir.endswith('/') else proj_dir
                project_name = proj_dir.split('/')[-1].replace("/", "")

                exception_dir = proj_dir + '/' + 'exceptions' + '/'
                java_file = src_file.split("/")[-1]
            elif Platform.is_windows_platform():
                proj_dir = proj_dir[:-1] if proj_dir.endswith('\\') else proj_dir
                project_name = proj_dir.split('\\')[-1].replace("\\", "")

                exception_dir = proj_dir + '\\' + 'exceptions' + '\\'
                java_file = src_file.split("\\")[-1]
            if not os.path.isdir(exception_dir):
                os.makedirs(exception_dir)
            error_message = traceback.format_exc()
            error_file = exception_dir + java_file.replace(".java", ".error")
            exception_obj.update_exception_message(project_name, error_message)
            with open(error_file, 'w') as writer:
                writer.write("{}".format(error_message))

            del source_ast_parser_obj
            ASTHelper.clear_locals()
            gc.collect()
        else:
            del source_ast_parser_obj
            ASTHelper.clear_locals()
            gc.collect()
