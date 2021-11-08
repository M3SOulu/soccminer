from soccminer.parse_source_files import SourceFiles
from soccminer.java_ast_parsing import XmlParsing
from soccminer.project_meta import JavaProjectMeta
from soccminer.exception_monitoring import ExceptionStack
from soccminer.performance_time import APIPerformanceTime
from soccminer.soccminer_logger import SoCCMinerLogger
from soccminer.environment import Platform
from soccminer.java_project_meta_attributes import JavaMetaAttribute
from soccminer.proj_comments_main_attr import CommentsMetaAttribute
from soccminer.proj_comments_comprehensive_attr import ComprehensiveCommentsAttribute
from soccminer.java_proj_miner import JavaMiner
from soccminer.parse_source_files import validate_loc
from soccminer.source_code_details import PackageInfo, ClassInfo, MethodInfo, InterfaceInfo, StaticBlockInfo, EnumInfo
from soccminer.comments import CommentInfo
from soccminer.json_serialization import SerializeSoCCMiner
from soccminer.helper import RepoDownloader
import sys
import traceback
import os
import logging
import time
import gc
from multiprocessing import Process
import shutil


class CommentsMiner:
    mining_level = None
    log = None
    lang = None
    proj_url = None
    load_project = None
    soccminer_cfg_file = None

    @staticmethod
    def save_program_parameters():
        try:

            params = [CommentsMiner.proj_url, CommentsMiner.lang, str(CommentsMiner.mining_level),
                      str(CommentsMiner.load_project), str(CommentsMiner.log)]
            with open(CommentsMiner.soccminer_cfg_file, 'w', encoding='utf-8') as fh:
                fh.write("\n".join(params))
        except IOError as ioexception:
            logging.error("Unable to save miner config parameters. Exiting the program.".format(ioexception.strerror))
            print("Unable to save miner config parameters. Exiting the program.".format(ioexception.strerror))

    @staticmethod
    def set_mining_level_inp(m_level):
        CommentsMiner.mining_level = m_level

    @staticmethod
    def set_log_inp(log):
        CommentsMiner.log = log

    @staticmethod
    def set_lang_inp(lang):
        CommentsMiner.lang = lang

    @staticmethod
    def set_source_url(proj_url):
        CommentsMiner.proj_url = proj_url

    @staticmethod
    def set_load_project(load_project):
        CommentsMiner.load_project = load_project

    @staticmethod
    def validate_soccminer_dir_structure(proj_dir):
        soccminer_dir = [type(PackageInfo()).__name__, type(ClassInfo()).__name__, type(MethodInfo()).__name__,
                        type(InterfaceInfo()).__name__, type(StaticBlockInfo()).__name__]
        empty_folders = False
        empty_folder_count = 0
        soccminer_entity_dir_count = 0
        attr_dir = 'attributes'
        comment_dir = 'comments'
        for folder in os.listdir(proj_dir):
            if CommentsMiner.is_dir(folder):
                if folder in soccminer_dir:
                    soccminer_entity_dir_count += 1
                    folder_content = None
                    attr_folder = None
                    comment_folder = None
                    if Platform.is_unix_platform():
                        folder_content = proj_dir + '/' + folder
                        attr_folder = folder_content + '/' + attr_dir
                        comment_folder = folder_content + '/' + comment_dir
                    elif Platform.is_windows_platform():
                        folder_content = proj_dir + '\\' + folder
                    # supposed to be 2 (attributes and comments) or either 1 of them empty or can be 0.
                    soccminer_subfolder_count = 0
                    attr_dir_file_count = None
                    comment_dir_file_count = None
                    for sub_folder in os.listdir(folder_content):
                        if sub_folder == attr_dir:
                            if CommentsMiner.is_dir(attr_folder):
                                soccminer_subfolder_count += 1
                                src_file_obj = SourceFiles(attr_folder)
                                src_file_obj.fetch_source_files(attr_folder, 'json')
                                attr_dir_file_count = len(src_file_obj.get_files())
                                del src_file_obj
                        elif sub_folder == comment_dir:
                            if CommentsMiner.is_dir(comment_folder):
                                soccminer_subfolder_count += 1
                                src_file_obj = SourceFiles(attr_folder)
                                src_file_obj.fetch_source_files(comment_folder, 'json')
                                comment_dir_file_count = len(src_file_obj.get_files())
                                del src_file_obj
                    if soccminer_subfolder_count == 1:
                        if attr_dir_file_count is not None and attr_dir_file_count == 0:
                            empty_folder_count += 1
                        elif comment_dir_file_count is not None and comment_dir_file_count == 0:
                            empty_folder_count += 1
                    if soccminer_subfolder_count == 2:
                        if attr_dir_file_count == 0 and comment_dir_file_count == 0:
                            empty_folder_count += 1
                    if soccminer_subfolder_count == 0:
                        empty_folder_count += 1
        if empty_folder_count == 5:
            empty_folders = True
        return empty_folders

    @staticmethod
    def validate_mining_input_dir(input_dir):
        #  source files are expected to be present inside project directory.
        #  input_dir contains one or more project directories and project
        #                directory contains one or more source code files.
        for item in os.listdir(input_dir):
            if item.endswith('.java'):
                return False
        return True

    def __init__(self, source_url, lang='java', m_level='comment', load_project=False, log: str = "nolog"):
        self.url = source_url
        if Platform.is_unix_platform():
            self.url = self.url + '/' if not self.url.endswith("/") else self.url
            CommentsMiner.soccminer_cfg_file = os.getcwd() + '/' + 'soccminer.cfg'
        elif Platform.is_windows_platform():
            self.url = self.url + '\\' if not self.url.endswith("\\") else self.url
            CommentsMiner.soccminer_cfg_file = os.getcwd() + '\\' + 'soccminer.cfg'
        self.lang = lang
        self.mining_level = m_level
        self.load_project = load_project
        self.log = log
        if not self.validate_args(self.url, lang, m_level, load_project, log):
            print("Exiting due to invalid arguments.")
            self.usage_warning()
            sys.exit(1)

        self.project = None
        self.invalid_ing_arg_flag = False
        self.project_details_mstr_dict = {}
        self.exception_obj = ExceptionStack()
        self.proj_comments_main_attr_obj_list = []  # Contains basic comment attribute objects (CommentMetaAttributes)
        self.proj_comments_all_attr_obj_list = []  # Contains all comment attributes objects (ComprehensiveCommentsAttribute)
        self.proj_meta_attr_obj_list = []  # Contains MetaAttribute objects (JavaMetaAttribute)
        self.proj_comments_and_attr_obj_list = []  # Contains MinerObjects (JavaMiner)
        self.proj_directories = []  # Contains project directories for mining project source code
        self.soccminer_proj_directories = []  # Contains soccminer tool mined project entities for later use suching loading project
        self.miner_status_flag = False
        self.load_status = False  # If Proj has been loaded from json successfully
        self.project_directory = ""
        self.empty_proj_flag = []  # Contains boolean indicating if a project is empty, i.e., no source code file
        self.soccminer_cfg_file = None
        self.log_dir = SoCCMinerLogger.log_dir
        self.mined_entity_dir = None

        self.log_file_obj = None

        logging.debug("Setting soccminer parameters")
        # set params
        CommentsMiner.set_source_url(self.url)
        CommentsMiner.set_mining_level_inp(self.mining_level)
        CommentsMiner.set_lang_inp(self.lang)
        CommentsMiner.set_load_project(self.load_project)
        CommentsMiner.set_log_inp(self.log)
        CommentsMiner.save_program_parameters()
        logging.debug("Config file created with program parameters")

        if self.log == 1 or self.log == 2:
            if SoCCMinerLogger.main_logger is None:
                self.log_file_obj = SoCCMinerLogger(self.log, "")

        logging.debug("Mining_Level and Load_Project in Comments_Miner initialization: {} , {}".format(self.mining_level, self.load_project))
        if self.mining_level != 0 and not self.load_project:
            logging.debug("Mining intiated")
            print("Mining intiated")
            self.initiate_mining()
            if self.miner_status_flag:
                if not self.invalid_ing_arg_flag:
                    logging.info("Project mining successful")
                    print("Project mining successful")
        elif self.mining_level != 0 and self.load_project:
            logging.debug("Load project from json initiated")
            print("Load project from json initiated")
            self.load_soccminer_entities()
            if self.load_status:
                logging.info("Project load successful")
                print("Project load successful")
        if os.path.exists(CommentsMiner.soccminer_cfg_file):
            os.remove(CommentsMiner.soccminer_cfg_file)

    def get_log(self):
        return self.log

    def get_mining_level(self):
        return self.mining_level

    def get_language(self):
        return self.lang

    @staticmethod
    def is_dir(dir_loc):
        # validate if dir
        return os.path.exists(dir_loc) and os.path.isdir(dir_loc)

    @staticmethod
    def is_empty_dir(dir_loc):
        # validate if empty dir
        return os.listdir(dir_loc)

    @staticmethod
    def validate_inp_dir(dir_loc):
        # validate if dir exists and not empty
        if CommentsMiner.is_dir(dir_loc):
            if CommentsMiner.is_empty_dir(dir_loc):  # if returned list has file entry items allow process
                return True
            else:
                print("Empty input directory")
                return False
        else:
            return False

    @classmethod
    def usage_warning(cls):
        print("inp - Defines the input to the tool. Can be 'local_dir' containing project repositories as sub-directories or 'Git Repo URL'")
        print("language - The programming language of the project, for now only java project are handled by soccminer")
        print("mining_level - Defines the mining/project entity loading level. \n"
              " Can be 'comment' to mine/load basic comment info, \n"
              " 'comprehensive_comment' to mine/load comprehensive comment attributes, \n"
              " 'project' to mine/load project attributes), \n"
              " 'all' (for project and comprehensive attributes), \n"
              " NOTE: While loading entities with load_project input argument set to True, SoCCMiner expects the same mining level with which the project was mined. \n")
        print("load_project - If True, loads project entities from the mined entities directory containing the soccminer serialized json files.  "
              "If False, mines source code projects for comments, source code entities and their attributes according to the mining level input")
        print("log - Defines the logging level. Can be one of none(NOLOG), info(INFO), debug(DEBUG)")

        logging.error("inp - Defines the input to the tool. Can be 'local_dir' containing project repositories as sub-directories or 'Git Repo URL'")
        logging.error("language - The programming language of the project, for now only java project are handled by soccminer")
        logging.error("mining_level - Defines the mining/project entity loading level. \n"
              " Can be 'comment' to mine/load basic comment info, \n"
              " 'comprehensive_comment' to mine/load comprehensive comment attributes, \n"
              " 'project' to mine/load project attributes), \n"
              " 'all' (for project and comprehensive attributes), \n"
              " 'none' (for loading mined soccminer project entities but not mining), \n")
        logging.error("load_project - If True, loads project entities from the soccminer serialized json files from the mined entities directory of "
              "respective projects.  "
              "If False, mines source code projects for comments, source code entities and their attributes according to the mining level input")
        logging.error("log - Defines the logging level. Can be one of none(NOLOG), info(INFO), debug(DEBUG)")

    @classmethod
    def mining_warning_msg(cls, mining_status):
        if not mining_status:
            logging.warning("Mining Comments failed, check log")
        else:
            logging.warning("Incorrect Mining level argument")
            logging.warning(
                "Mining Level - comment (for Basic Comment Attributes, "
                "Mining Level - comprehensive_comment (for Comprehensive Comment Attributes")
            logging.warning(
                "Mining Level - project (for Project Meta Attributes, "
                "Mining Level - all (for Comment and Project Meta attributes")

    @staticmethod
    def get_repo_folders_to_process(local_loc):
        proj_dirs = None
        logging.debug("get_repo_folders_to_process() begins for {}".format(local_loc))
        validate_dir_rc = CommentsMiner.validate_inp_dir(local_loc)
        if validate_dir_rc:
            proj_dirs = os.listdir(local_loc)
            for proj in proj_dirs:
                logging.debug("Folders to be processed: {}".format(proj))
        else:
            logging.debug(
                "Input directory {} is either empty or does not contain with return value {}".format(local_loc,
                                                                                                     validate_dir_rc))
        return proj_dirs

    def fetch_load_status(self):
        load_status = True
        for project in self.exception_obj.exception_dict:
            for exception in self.exception_obj.exception_dict[project]:
                print("{} - Exception: {}".format(project, exception))
                load_status = False
        for project in self.exception_obj.warning_dict:
            for warning in self.exception_obj.warning_dict[project]:
                print("{} - Warning: {}".format(project, warning))
                load_status = False
        return load_status

    def fetch_mining_status(self, proj_directories):
        proj_counter = 0
        failed_projects = 0
        project_name = ""
        total_project_repositories = len(proj_directories)
        for project_dict_ind in self.project_details_mstr_dict:
            try:
                project_name = self.project_details_mstr_dict[project_dict_ind].project_name
                if project_name in self.exception_obj.exception_dict:
                    failed_projects += 1 if len(self.exception_obj.exception_dict[project_name]) > 0 else 0
                proj_counter += 1
                if self.empty_proj_flag[project_dict_ind]:
                    #  Project does not contain any source code flag, problem with input not with mining process.
                    #  self.miner_status_flag = True
                    continue

                print("Project #: {}, Project Name: {}".format(project_dict_ind + 1, project_name))
                perf_obj = self.project_details_mstr_dict[project_dict_ind]
                if project_name in self.exception_obj.exception_dict:
                    issue = ",".join(self.exception_obj.exception_dict[project_name]) if \
                    self.exception_obj.exception_dict[project_name] \
                        else ",".join(self.exception_obj.warning_dict[project_name])
                    if issue:
                        print("Issue with input Project {}: {}".format(project_name, issue))
                        logging.info("Issue with input Project {} with error: {}".format(project_name, issue))
                    else:
                        self.miner_status_flag = True

                    print("Project XML_CONV_OVERHEAD_TIME: {}".format(perf_obj.xml_conv_overhead_time))
                    print("Project MINING_TIME: {}".format(perf_obj.mining_time))
                    print("Project ATTR_PROCESSING_TIME: {}".format(perf_obj.tot_attr_processing_time))
                    print("Project TOTAL_SRC_FILES_PROCESSED: {}".format(perf_obj.tot_src_files_processed))
                    print("Project PROJECT_KLOC: {}".format(perf_obj.tot_kloc_processed))
                    logging.info("Project XML_CONV_OVERHEAD_TIME: {}".format(perf_obj.xml_conv_overhead_time))
                    logging.info("Project MINING_TIME: {}".format(perf_obj.mining_time))
                    logging.info("Project ATTR_PROCESSING_TIME: {}".format(perf_obj.tot_attr_processing_time))
                    logging.info("Project TOTAL_SRC_FILES_PROCESSED: {}".format(perf_obj.tot_src_files_processed))
                    logging.info("Project PROJECT_KLOC: {}".format(perf_obj.tot_kloc_processed))

                    if self.mining_level != 3:
                        print("Project TOTAL_COMMENTS_MINED: {}".format(perf_obj.tot_comments_processed))
                        logging.info("Project TOTAL_COMMENTS_MINED: {}".format(perf_obj.tot_comments_processed))

                    if self.mining_level == 3 or self.mining_level == 4:
                        tot_proj_entities_mined = 0
                        print("Project Mined Entity Stats: ")
                        if perf_obj.tot_packages_processed > 0:
                            tot_proj_entities_mined += perf_obj.tot_packages_processed
                            print("\t TOTAL_PACKAGES_MINED: {}".format(perf_obj.tot_packages_processed))
                        if perf_obj.tot_classes_processed > 0:
                            tot_proj_entities_mined += perf_obj.tot_classes_processed
                            print("\t TOTAL_CLASSES_MINED: {}".format(perf_obj.tot_classes_processed))
                        if perf_obj.tot_enums_processed > 0:
                            tot_proj_entities_mined += perf_obj.tot_enums_processed
                            print("\t TOTAL_ENUMS_MINED: {}".format(perf_obj.tot_enums_processed))
                        if perf_obj.tot_methods_processed > 0:
                            tot_proj_entities_mined += perf_obj.tot_methods_processed
                            print("\t TOTAL_METHODS_MINED: {}".format(perf_obj.tot_methods_processed))
                        if perf_obj.tot_interfaces_processed > 0:
                            tot_proj_entities_mined += perf_obj.tot_interfaces_processed
                            print("\t TOTAL_INTERFACES_MINED: {}".format(perf_obj.tot_interfaces_processed))
                        if perf_obj.tot_static_blocks_processed > 0:
                            tot_proj_entities_mined += perf_obj.tot_static_blocks_processed
                            print("\t TOTAL_STATIC_BLOCKS_MINED: {}".format(perf_obj.tot_static_blocks_processed))
                        print("TOTAL_JAVA_PROJECT_SOURCE_ENTITIES_MINED: {}".format(tot_proj_entities_mined))
                        logging.info("Project TOTAL_PACKAGES_PROCESSED: {}".format(perf_obj.tot_packages_processed))
                        logging.info("Project TOTAL_CLASSES_PROCESSED: {}".format(perf_obj.tot_classes_processed))
                        logging.info("Project TOTAL_ENUMS_PROCESSED: {}".format(perf_obj.tot_enums_processed))
                        logging.info("Project TOTAL_METHODS_PROCESSED: {}".format(perf_obj.tot_methods_processed))
                        logging.info("Project TOTAL_INTERFACES_PROCESSED: {}".format(perf_obj.tot_interfaces_processed))
                        logging.info("Project TOTAL_STATIC_BLOCKS_PROCESSED: {}".format(perf_obj.tot_static_blocks_processed))

                for proj_dir in self.soccminer_proj_directories:
                    if project_name in proj_dir:
                        print("Mined Entities for project {} are stored at {}".format(project_name, proj_dir))
                        logging.info("Mined Entities for project {} are stored at {}".format(project_name, proj_dir))

                    if project_name in self.exception_obj.warning_dict:
                        if self.exception_obj.warning_dict[project_name]:
                            logging.warning("Potential {} Invalid Source Code Files for project: {}. Check Log for details."
                                         "".format(project_name, len(self.exception_obj.exception_dict[project_name])))
                project_name = None
            except Exception as project_exception:
                logging.error("Fetch_Mining_Status: - Unexpected error: {}".format(project_exception))
                error_message = traceback.format_exc()
                self.exception_obj.update_exception_message(project_name, error_message)
                continue

    def validate_args(self, input, programming_language, mining_level, load_proj_flag, log):
        # level 'comment' - Basic Comment attributes
        # level 'comprehensive_comment' - Comprehensive Comment Attributes
        # level 'project' - Project Meta Attributes,
        # level 'all' - Project and Comprehensive Comment attributes
        # log can be none/nolog(0), info (1), debug(2)

        programming_language = programming_language.lower()
        mining_level = str(mining_level).lower()
        if load_proj_flag not in [0, 1]:
            load_proj_flag = str(load_proj_flag).lower()
            if load_proj_flag == "true":
                load_proj_flag = 1
            if load_proj_flag == "false":
                load_proj_flag = 0
        self.load_project = load_proj_flag
        if 'http' in input or 'github.com' in input:
            if RepoDownloader.validate_repo_url(input):
                cloned_folder = RepoDownloader.clone_repo(input)
                if not cloned_folder:
                    print("Issue with input url, please check input url: {}".format(input))
                    self.invalid_ing_arg_flag = True
                else:
                    self.url = cloned_folder
        elif CommentsMiner.validate_inp_dir(input):
            self.url = input
            if not CommentsMiner.validate_mining_input_dir(input):
                return False
                self.invalid_ing_arg_flag = True
        else:
            print("Issue with input ({})".format(input))
            self.invalid_ing_arg_flag = True
            return False

        if load_proj_flag not in [0, 1]:
            print("Incorrect value for load_project. Can be either True/False, {},{}".format(load_proj_flag, type(load_proj_flag)))
            self.invalid_ing_arg_flag = True
            return False

        if not mining_level.strip().lower() in ["comment", "comprehensive_comment", "project", "all"]:  # , "none"]:
            print("Issue with mining level input {}".format(mining_level.strip().lower()))
            self.invalid_ing_arg_flag = True
            return False
        else:
            if mining_level.strip().lower() == "comment":
                self.mining_level = 1
            elif mining_level.strip().lower() == "comprehensive_comment":
                self.mining_level = 2
            elif mining_level.strip().lower() == "project":
                self.mining_level = 3
            elif mining_level.strip().lower() == "all":
                self.mining_level = 4

        if log is not None:
            if log.strip().lower() not in ['nolog', "false", "info", "debug"]:
                print("Issue with log level input {}".format(log))
                self.invalid_ing_arg_flag = True
                return False
            else:
                # default nolog --> 0
                self.log = 0
                if str(log).strip().lower() == "false" or str(log).strip().lower() == "nolog":
                    self.log = 0
                elif str(log).strip().lower() == "debug":
                    self.log = 2
                elif str(log).strip().lower() == "info":
                    self.log = 1
        else:
            self.log = 0

        if programming_language not in ['java']:
            print("Issue with programming language input {}".format(programming_language))
            self.invalid_ing_arg_flag = True
            return False
        else:
            self.lang = programming_language
        return True

    def initiate_mining(self):
        project_instance = None
        mining_objects_list = []
        logging.debug("initiate_mining() begins for {} containing {} programs".format(self.url, self.lang))
        proj_dirs = CommentsMiner.get_repo_folders_to_process(self.url)
        project_name = None
        logging.debug("Input directory path {}".format(self.url))
        for ind, proj_dir in enumerate(proj_dirs):
            try:
                project_name = ""
                absolute_dir = self.url + proj_dir
                self.proj_directories.append(absolute_dir)
                logging.debug("absolute_dir: {}".format(absolute_dir))

                if CommentsMiner.validate_inp_dir(absolute_dir):
                    logging.debug(" validated absolute_dir ".format(absolute_dir))
                    if Platform.is_unix_platform():
                        project_name = proj_dir.replace("/", "_")
                        SoCCMinerLogger.log_dir = SoCCMinerLogger.log_dir + '/' + project_name
                    elif Platform.is_windows_platform():
                        project_name = proj_dir.replace("\\", "_")
                        SoCCMinerLogger.log_dir = SoCCMinerLogger.log_dir + '\\' + project_name
                    self.project = project_name
                    self.exception_obj.set_project_stack(project_name)
                    logging.info("Project to be initiated for {},{} ".format(proj_dir, absolute_dir))
                    if self.lang.lower() == "java":
                        project_instance = JavaProjectMeta(absolute_dir)
                    perf_obj = APIPerformanceTime()

                    mining_objects_list.append(project_instance)
                    src_files = SourceFiles(absolute_dir)
                    mining_objects_list.append(src_files)
                    src_files.fetch_source_files(src_files.loc, self.lang)
                    conv_start_time = time.time()
                    process_start_time = time.time()
                    src_files.convert_srcfiles_to_xmlfiles(project_name, self.exception_obj)
                    project_instance.set_source_file_info(src_files)
                    logging.debug("Source file count for project {} is {}".format(project_name, len(src_files.get_files())))

                    if len(src_files.get_files()) != 0:
                        file_cntr = 0
                        empty_file_count = 0
                        logging.info("Total source code files: {} for project {}".format(len(src_files.get_files()), project_name))
                        conv_end_time = time.time()
                        perf_obj.xml_conv_overhead_time = conv_end_time - conv_start_time
                        attr_and_meta_attr_proc_start_time = time.time()

                        if Platform.is_unix_platform():
                            self.project_directory = os.getcwd() + '/SoCCMiner_Mined_Entities/' + project_instance.get_project_name()
                        elif Platform.is_windows_platform():
                            self.project_directory = os.getcwd() + '\\SoCCMiner_Mined_Entities\\' + project_instance.get_project_name()
                        self.soccminer_proj_directories.append(self.project_directory)
                        # remove if already exists
                        if validate_loc(self.project_directory):
                            shutil.rmtree(self.project_directory)

                        for xml_file in src_files.cd_file_xml_mapping_dict:
                            try:
                                file_cntr += 1
                                if os.path.getsize(xml_file) == 0:
                                    logging.warning("Potential invalid source code file or failed xml conversion for {} whose file size is 0 "
                                                    "".format(xml_file))
                                    empty_file_count += 1
                                #logging.debug("-------------------------------------------------------------------------")
                                #logging.debug("AST parsing for {} begins".format(xml_file))
                                #src_code_xml_properties = XmlProperties()

                                # Source Code Parsing
                                #XmlParsing.ast_parsing(src_code_xml_properties, xml_file,
                                #                     src_files.cd_file_xml_mapping_dict[xml_file],
                                #                     self.project_directory,file_cntr)
                                #XmlParsing.ast_parsing(xml_file, src_files.cd_file_xml_mapping_dict[
                                #    xml_file], self.project_directory, file_cntr, self.exception_obj
                                #self.release_obj(src_code_xml_properties)

                                # for simple comments extraction, single processor is better than multiprocessor utilization
                                #if CommentsMiner.mining_level == 1:
                                #    src_code_xml_properties = XmlProperties(xml_file)
                                #    XmlParsing.ast_parsing(src_code_xml_properties, xml_file,
                                #                           src_files.cd_file_xml_mapping_dict[xml_file], self.project_directory, file_cntr)

                                #    self.release_obj(src_code_xml_properties)
                                #else:

                                # Source Code Parsing
                                process = Process(target=XmlParsing.ast_parsing_multiprocessing,
                                                  args=(xml_file, src_files.cd_file_xml_mapping_dict[xml_file],
                                                        self.project_directory, file_cntr, self.exception_obj, self.log))
                                process.start()
                                process.join()

                            except Exception as proc_files_ex:
                                logging.error(
                                    "Error while processing source code file{} {} {}".format(xml_file, sys.exc_info()[0],
                                                                                             proc_files_ex))
                                error_message = traceback.format_exc()
                                self.exception_obj.update_exception_message(project_name, error_message)
                                continue

                        project_instance.load_project_from_json(self.project_directory, "package")
                        logging.debug("Type, # of packages from loaded project instance from json: {}, {}".format(type(project_instance).__name__,
                                                                                                                  len(project_instance.get_packages())))
                        project_instance.set_project_loc(project_instance.fetch_project_loc() / 1000)
                        entity_count_dict = project_instance.populate_entity_stats(self.project_directory)
                        if empty_file_count != 0:
                            self.exception_obj.update_warning_message(project_name,
                                                                      "Potential invalid source code or failed xml conversion, "
                                                                      "with {} empty files".format(empty_file_count))

                        process_end_time = time.time()
                        perf_obj.mining_time = process_end_time - process_start_time
                        perf_obj.tot_src_files_processed = file_cntr
                        perf_obj.tot_comments_processed = entity_count_dict[type(CommentInfo()).__name__]
                        perf_obj.tot_kloc_processed = project_instance.get_project_loc()

                        #  Serialize project source file info and project meta
                        src_file_proj_info = {}
                        src_file_proj_info['src_file_obj'] = src_files
                        src_file_proj_info['proj_name'] = project_name
                        src_file_proj_info['proj_loc'] = project_instance.get_project_loc()
                        src_file_proj_info['platform'] = Platform.fetch_platform()
                        src_file_proj_info['mining_level'] = self.mining_level
                        SerializeSoCCMiner.serialize_project_source_file_info(project_name, self.project_directory, src_file_proj_info)
                        src_file_proj_info = {}

                        if self.mining_level > 2:
                            perf_obj.tot_packages_processed += entity_count_dict[type(PackageInfo()).__name__]
                            perf_obj.tot_classes_processed += entity_count_dict[type(ClassInfo()).__name__]
                            perf_obj.tot_enums_processed += entity_count_dict[type(EnumInfo()).__name__]
                            perf_obj.tot_methods_processed += entity_count_dict[type(MethodInfo()).__name__]
                            perf_obj.tot_interfaces_processed += entity_count_dict[type(InterfaceInfo()).__name__]
                            perf_obj.tot_static_blocks_processed += entity_count_dict[type(StaticBlockInfo()).__name__]

                        attr_and_meta_attr_proc_end_time = time.time()
                        perf_obj.tot_attr_processing_time += attr_and_meta_attr_proc_end_time - attr_and_meta_attr_proc_start_time
                        perf_obj.project_name = project_name

                        self.project_details_mstr_dict[ind] = perf_obj
                        self.empty_proj_flag.append(False)
                        logging.info("Mining Ends for Project {},{} ".format(proj_dir, absolute_dir))
                    else:
                        self.exception_obj.update_warning_message(project_name,
                                                                  "Project {} does not contain any .java source code file".format(
                                                                      project_name))
                        perf_obj.project_name = project_name
                        self.project_details_mstr_dict[ind] = perf_obj
                        print("Project {} does not contain any .java source code file".format(project_name))
                        self.empty_proj_flag.append(True)
                else:
                    print("Invalid input project directory.  Please check your input.")
                    self.usage_warning()
                    self.miner_status_flag = True
                    self.invalid_ing_arg_flag = True
            except Exception as proc_dir_ex:
                logging.error("Unexpected error {} {}".format(sys.exc_info()[0], proc_dir_ex))
                error_message = traceback.format_exc()
                self.exception_obj.update_exception_message(project_name, error_message)
                logging.error("Error Trace Details: {}".format(error_message))
                continue
            else:
                if 1 in self.empty_proj_flag:
                    logging.warning("One or more project has empty source code files")
                else:
                    self.miner_status_flag = True


            # Releasing processed objects
            for processed_mining_object in mining_objects_list:
                logging.info("Releasing processed object {}".format(type(processed_mining_object).__name__))
                self.release_obj(processed_mining_object)
            mining_objects_list = []

        tot_src_files_processed = 0
        tot_packages_processed = 0
        tot_classes_processed = 0
        tot_enums_processed = 0
        tot_methods_processed = 0
        tot_interfaces_processed = 0
        tot_static_blocks_processed = 0
        tot_comments_processed = 0
        tot_kloc_processed = 0
        tot_xml_conv_overhead_time = 0.0
        tot_attr_processing_time = 0.0

        for project_ind in self.project_details_mstr_dict:
            perf_obj = self.project_details_mstr_dict[project_ind]
            tot_src_files_processed += perf_obj.tot_src_files_processed
            tot_packages_processed += perf_obj.tot_packages_processed
            tot_classes_processed += perf_obj.tot_classes_processed
            tot_enums_processed += perf_obj.tot_enums_processed
            tot_methods_processed += perf_obj.tot_methods_processed
            tot_interfaces_processed += perf_obj.tot_interfaces_processed
            tot_static_blocks_processed += perf_obj.tot_static_blocks_processed
            tot_comments_processed += perf_obj.tot_comments_processed
            tot_kloc_processed += perf_obj.tot_kloc_processed
            tot_xml_conv_overhead_time += perf_obj.xml_conv_overhead_time
            tot_attr_processing_time += perf_obj.tot_attr_processing_time

        self.fetch_mining_status(self.proj_directories)

        if self.miner_status_flag:
            logging.info("-------------------")
            logging.info("Total XML Conversion overhead time : {}".format(tot_xml_conv_overhead_time))
            logging.info("Total ATTR and META-ATTR processing time: {}".format(tot_attr_processing_time))
            logging.info("Total Source files processed: {}".format(tot_src_files_processed))
            logging.info("Total Packages processed: {}".format(tot_packages_processed))
            logging.info("Total Classes processed: {}".format(tot_classes_processed))
            logging.info("Total Methods processed: {}".format(tot_methods_processed))
            logging.info("Total Interfaces processed: {}".format(tot_interfaces_processed))
            logging.info("Total Static Blocks processed: {}".format(tot_static_blocks_processed))
            logging.info("Total Comments processed: {}".format(tot_comments_processed))
            logging.info("Total KLOC processed: {}".format(tot_kloc_processed))
        else:
            issue = ",".join(self.exception_obj.exception_dict[project_name]) if self.exception_obj.exception_dict[project_name] \
                else ",".join(self.exception_obj.warning_dict[project_name])
            print("Encountered issues while mining Project {} issue: {}".format(project_name, issue))
        self.clear_temp_folders()

    def clear_temp_folders(self):
        temp_dir = ''
        logging.info("Checking temp folders if any for project {}: ".format(self.project))
        if Platform.is_unix_platform():
            temp_dir = os.getcwd() + '/soccminer_temp/'
        elif Platform.is_windows_platform():
            temp_dir = os.getcwd() + '\\soccminer_temp\\'
        if os.path.isdir(temp_dir):
            logging.info("Clearing temp directories and files at {}".format(temp_dir))
            shutil.rmtree(temp_dir)
        else:
            logging.info("No temp folders for project {}: ".format(self.project))

    def release_obj(self, obj):
        del obj
        logging.info("comments_miner - GC status: {}".format(gc.isenabled()))
        gc.collect()

    def validate_soccminer_entity_input_dir(self,proj_entity_dir):
        soccminer_entity_dir_list = [type(PackageInfo()).__name__, type(ClassInfo()).__name__, type(MethodInfo()).__name__,
                                    type(InterfaceInfo()).__name__, type(StaticBlockInfo()).__name__, 'attributes', 'comments']
        proj_load_hierarchy_flag = True
        #  for proj_load_dir in proj_entity_dirs:
        logging.debug("validate_soccminer_entity_input_dir(): Validating proj_load_dir: {} ".format(proj_entity_dir))
        for dir_item in os.listdir(proj_entity_dir):
            logging.debug("dir_item: {}".format(dir_item))
            if dir_item in soccminer_entity_dir_list or dir_item.endswith(".json"):
                proj_load_hierarchy_flag = False
        return proj_load_hierarchy_flag

    def load_soccminer_entities(self):
        proj_entity_dirs = CommentsMiner.get_repo_folders_to_process(self.url)
        project_name = None

        logging.debug("load_soccminer_entities(): Validating dir: {}".format(self.url))
        if self.validate_soccminer_entity_input_dir(self.url):
            for ind, proj_dir in enumerate(proj_entity_dirs):
                try:
                    project_name = ""
                    absolute_dir = self.url + proj_dir
                    if Platform.is_unix_platform():
                        project_name = proj_dir.replace("/", "_")
                    elif Platform.is_windows_platform():
                        project_name = proj_dir.replace("\\", "_")
                    self.exception_obj.set_project_stack(project_name)

                    if CommentsMiner.validate_inp_dir(absolute_dir):
                        if not CommentsMiner.validate_soccminer_dir_structure(absolute_dir):
                            self.proj_directories.append(absolute_dir)
                            project_instance = JavaProjectMeta(absolute_dir)
                            #  load source file info object and project meta before loading other serialized entities
                            project_instance.load_project_from_json(absolute_dir, "source_file")

                            #  load entire project attributes and comments
                            project_instance.load_project_from_json(absolute_dir, "project")

                            if self.mining_level == 1:  # comment level
                                self.proj_comments_main_attr_obj_list.append(CommentsMetaAttribute(project_instance))
                            elif self.mining_level == 2:  # comprehensive_comment level
                                self.proj_comments_all_attr_obj_list.append(ComprehensiveCommentsAttribute(project_instance))
                            elif self.mining_level == 3:  # project level
                                self.proj_meta_attr_obj_list.append(JavaMetaAttribute(project_instance))
                            elif self.mining_level == 4:  # all level
                                self.proj_comments_and_attr_obj_list.append(JavaMiner(project_instance))
                            self.release_obj(project_instance)
                        else:
                            self.exception_obj.update_warning_message(project_name,
                                                                      "Unable to load SoCCMiner entities from empty directory {}".format(absolute_dir))
                    else:
                        self.exception_obj.update_warning_message(project_name,
                                                                      "Unable to load SoCCMiner entities from invalid input directory {}".format(
                                                                          absolute_dir))
                except Exception as load_soccminer_entity:
                    logging.error("load_soccminer_entity: Encountered error {} {}".format(sys.exc_info()[0], load_soccminer_entity))
                    error_message = traceback.format_exc()
                    self.exception_obj.update_exception_message(project_name, error_message)
                    logging.error("Error Trace Details: {}".format(error_message))
                    continue
                else:
                    self.load_status = self.fetch_load_status()
        else:
            logging.error(
                "Incorrect input folder hierarchy for loading project. \n"
                "Expected: Folder --> soccminer_project_entity_folder1, soccminer_project_entity_folderN, etc.,  containing  attributes/comments sub-directories \n"
                "Given input project load folder is: soccminer_project_entity \n"
                "Input Directory for project load: {} \n".format(self.url))
            print(
                "Incorrect input folder hierarchy for loading project. \n"
                "Expected: Folder --> soccminer_project_entity_folder1, soccminer_project_entity_folderN, etc.,  containing  attributes/comments sub-directories \n"
                "Given input project load folder is: soccminer_project_entity \n"
                "Input Directory for project load: {} \n".format(self.url))

    def fetch_mined_project_meta(self):
        """
        Fetches Project Meta Attributes specific to programming language,
        for example (Java): Class Name, Signature, Nested Level, Method Name, Signature, etc.,
        Works for mining level Project(Module input argument), else returns empty list.
                :param: None
                :returns: List of returned :class: JavaMetaAttr objects
                :rtype: list
        """
        proj_meta_attr_obj_list = []
        if len(self.proj_meta_attr_obj_list) > 0 and CommentsMiner.mining_level == 3:
            if CommentsMiner.lang == 'java':
                return self.proj_meta_attr_obj_list
        else:
            CommentsMiner.mining_warning_msg(False)
            return proj_meta_attr_obj_list

    def fetch_mined_comments(self):
        """
        Fetches Mined Comments.  i.e., text, line no and source file name
        Works for mining level comment(Module input argument), default mining level argument.
        Returns CommentsMetaAttribute objects in a list.

                :param: None
                :returns: List of returned :class: ProjCommentsMainAttr objects
                :rtype: list
        """
        proj_comments_main_attr_obj_list = []
        if len(self.proj_comments_main_attr_obj_list) > 0 and (CommentsMiner.mining_level == 1):
            if CommentsMiner.lang == 'java':
                return self.proj_comments_main_attr_obj_list
        else:
            CommentsMiner.mining_warning_msg(False)
            return proj_comments_main_attr_obj_list

    def fetch_mined_comment_attributes(self):
        """
        Fetches Project comments and comprehensive comment attributes, i.e., all attributes
        Works for mining level comprehensive_comment(Module input argument), else returns empty list.
        Returns ComprehensiveCommentsAttribute objects in a list.
                :param: None
                :returns: List of returned :class: ProjectMetaAttribute objects (JavaMetaAttribute for Java)
                :rtype: list
        """
        proj_comments_all_attr_obj_list = []
        if len(self.proj_comments_all_attr_obj_list) > 0 and (CommentsMiner.mining_level == 2):
            if CommentsMiner.lang == 'java':
                return self.proj_comments_all_attr_obj_list
        else:
            CommentsMiner.mining_warning_msg(False)
            return proj_comments_all_attr_obj_list

    def fetch_mined_project_meta_and_comments(self):
        """
        Fetches all Project comments with their attributes, Project attributes (file count, etc.,) and
        Meta-attributes (for java: package/class/interface/method/static block attributes)
        Works only for mining level all(Module input argument), else returns empty list.
        Returns ProjectMiner objects in a list (for Java programs JavaProjectMiner objects)
                :param: None
                :returns: List of returned :class: JavaProjectMiner objects
                :rtype: list
        """
        proj_all_comments_attr_obj_list = []
        if len(self.proj_comments_and_attr_obj_list) > 0 and (CommentsMiner.mining_level == 4):
            if CommentsMiner.lang == 'java':
                return self.proj_comments_and_attr_obj_list
        else:
            CommentsMiner.mining_warning_msg(False)
            return proj_all_comments_attr_obj_list

