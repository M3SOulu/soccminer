from soccminer.java_ast_parsing import SourceFiles
from soccminer.environment import Platform
import time
import gc
import traceback
import subprocess
import os
import logging
import requests
import shutil
from datetime import datetime


class TrackProgress:
    @staticmethod
    def fetch_approx_mining_eta(files, processed_file_count, mining_level, invocation_order):
        approx_eta_mins = 0.0
        if mining_level == 3 or mining_level == 4:
            approx_eta_mins = (files - processed_file_count) / 60
        else:
            if invocation_order == 'first':
                approx_eta_mins = (files / 15) / 60  # 15 is the estimated average based on tests
            else:
                approx_eta_mins = (files - processed_file_count) / 60
        return round(approx_eta_mins, 2)

    @staticmethod
    def track_ast_parsing_progress(total_files, processed_source_file_dir, error_file_dir, project_name, mining_level):
        processed_file_count = 0
        initial_proc_count = 0
        timer = 0

        logging.info("track_ast_parsing_progress begins")
        if not os.path.isdir(processed_source_file_dir):
            try:
                os.makedirs(processed_source_file_dir)
            except FileExistsError:
                logging.debug("Directory {} already exists".format(processed_source_file_dir))
        if not os.path.isdir(error_file_dir):
            try:
                os.makedirs(error_file_dir)
            except FileExistsError:
                logging.debug("Directory {} already exists".format(error_file_dir))
        processed_file_count = TrackProgress.fetch_file_count(processed_source_file_dir, 'json') + TrackProgress.fetch_file_count(error_file_dir, 'error')
        processed_file_count = 1 if processed_file_count == 0 else processed_file_count
        if os.path.isdir(processed_source_file_dir) and os.path.isdir(error_file_dir):
            tot_processed_count = processed_file_count
            approx_eta = TrackProgress.fetch_approx_mining_eta(total_files, processed_file_count, mining_level, 'first')

            if total_files != processed_file_count:
                if approx_eta <= 60:
                    print("", sep='', end='', flush=True)
                    print('\r {} - Mining source files completed for {}/{}. Approx ETA for completion {} minutes'.format(project_name, processed_file_count, total_files, approx_eta), sep='', end='', flush=True)
                elif approx_eta > 60:
                    approx_eta = round(approx_eta/60, 2)
                    print('\r {} - Mining source files completed for {}/{}. Approx ETA for completion {} hours'.format(project_name, processed_file_count, total_files, approx_eta), sep='', end='', flush=True)
            else:
                logging.info("{} - Mining source files completed for {}/{}".format(project_name, processed_file_count, total_files))
                #approx_eta = 0.0
                #print('\r {} - Mining source files completed for {}/{}. Approx ETA for completion {} minutes \n'.format(project_name, processed_file_count, total_files, approx_eta), sep='', end='', flush=True)
            logging.info("Total valid files for progress tracking: {}".format(total_files))
            thirty_min_proc_file_cnt = 0  
            while processed_file_count <= total_files:
                if timer == 2100:
                    if processed_file_count == initial_proc_count or processed_file_count == thirty_min_proc_file_cnt:
                        logging.info("Unexpected behaviour process taking too long to mine a file, stopping mining process")
                        processed_file_count = total_files
                    timer = 0
                approx_eta = TrackProgress.fetch_approx_mining_eta(total_files, processed_file_count, mining_level, 'non-first')
                if approx_eta <= 60:
                    print('\r {} - Mining source files completed for {}/{}. Approx ETA for completion {} minutes'.format(project_name, processed_file_count, total_files, approx_eta), sep='', end='', flush=True)
                elif approx_eta > 60:
                    approx_eta = round(approx_eta / 60, 2)
                    print('\r {} - Mining source files completed for {}/{}. Approx ETA for completion {} hours'.format(project_name, processed_file_count, total_files, approx_eta), sep='', end='', flush=True)
                if total_files == processed_file_count:
                    logging.debug("Total files {} == processed_file_count {}".format(total_files, processed_file_count))
                    break
                else:
                    time.sleep(3)
                    processed_file_count = TrackProgress.fetch_file_count(processed_source_file_dir, 'json') + TrackProgress.fetch_file_count(error_file_dir, 'error')
                    timer += 3
                    if timer == 1800:
                        thirty_min_proc_file_cnt = processed_file_count
                    if timer == 3:
                        initial_proc_count = processed_file_count
                    logging.info("Fetching processed_file_count after sleep {}".format(processed_file_count))
        logging.info("track_ast_parsing_progress ends")


    @staticmethod
    def fetch_file_count(dir, file_type):
        dir_obj = SourceFiles(dir)

        dir_obj.fetch_source_files(dir, file_type)
        file_count = len(dir_obj.get_files())
        del dir_obj
        return file_count


class RepoDownloader:
    @staticmethod
    def validate_repo_url(repo_url):
        ret_stat = True
        try:
            r = requests.get(repo_url)
            if r.status_code != 200:
                print("Invalid URL: {} failed with return code {}".format(repo_url, r.status_code))
                ret_stat = False
                return ret_stat
            else:
                print("Valid Repo URL: {}".format(repo_url, r.status_code))
                return ret_stat
        except requests.exceptions.Timeout:
            print("URL: {} failed with timeout exception".format(repo_url))
            ret_stat = False
            return ret_stat
        except requests.exceptions.TooManyRedirects:
            print("URL: {} failed with too many redirect exception".format(repo_url))
            ret_stat = False
            return ret_stat
        except requests.exceptions.HTTPError as err:
            print("URL: {} failed with HTTP error {}".format(repo_url, err.strerror))
            ret_stat = False
            return ret_stat
        except requests.exceptions.RequestException as e:
            print("URL: {} failed with ambiguous exception {}".format(repo_url, e.strerror))
            ret_stat = False
            return ret_stat

    @staticmethod
    def clone_repo(url):
        ret_code = 1  # 1 for failure 0 for success
        err = ""
        folder = ""
        try:
            proj_name = url.split("/")[-1]
            cwd = os.getcwd()
            if Platform.is_unix_platform():
                folder = os.getcwd() + '/soccminer_temp/cloned_repository/' + proj_name + '/'
                if os.path.isdir(folder):
                    shutil.rmtree(folder)
            elif Platform.is_windows_platform():
                folder = os.getcwd() + '\\soccminer_temp\\cloned_repository\\' + proj_name + '\\'
            os.makedirs(folder)
            os.chdir(folder)
            process = subprocess.Popen(['git', 'clone', "--depth=1", url], stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            print('\r {} - Fetching source code repository'.format(proj_name), flush=True)
            msg, err = process.communicate()  # do not remove communicate, if removed process exits with None or Null returncode
            ret_code = process.returncode
            logging.info("url: {}, msg: {}, rc:{}".format(url, msg, ret_code))
            print('\r {} - Fetching source code repository completed!'.format(proj_name), flush=True)
        except Exception as pexcep:
            error_message = traceback.format_exc()
            print("Error occured with input url: {}, ERROR: {}, {}".format(url, error_message, pexcep))
            return ret_code
        else:
            os.chdir(cwd)
            return folder


class ASTHelper:

    @staticmethod
    def is_class_info_obj(construct_obj):
        return type(construct_obj).__name__ == "ClassInfo"

    @staticmethod
    def is_file_info_obj(construct_obj):
        return type(construct_obj).__name__ == "FileInfo"

    @staticmethod
    def is_enum_info_obj(construct_obj):
        return type(construct_obj).__name__ == "EnumInfo"

    @staticmethod
    def is_comment_info_obj(construct_obj):
        return type(construct_obj).__name__ == "CommentInfo"

    @staticmethod
    def is_interface_info_obj(construct_obj):
        return type(construct_obj).__name__ == "InterfaceInfo"

    @staticmethod
    def is_package_info_obj(construct_obj):
        return type(construct_obj).__name__ == "PackageInfo"

    @staticmethod
    def is_method_info_obj(construct_obj):
        return type(construct_obj).__name__ == "MethodInfo"

    @staticmethod
    def is_static_block_info_obj(construct_obj):
        return type(construct_obj).__name__ == "StaticBlockInfo"

    @staticmethod
    def clear_locals():
        for x in list(locals().keys())[:]:
            del locals()[x]
        gc.collect()

    @staticmethod
    def format_for_serialization(construct_obj, serialization_file, mining_level):
        construct_info = {}
        if ASTHelper.is_class_info_obj(construct_obj):
            construct_info['Class_Name'] = construct_obj.get_class_name()
            construct_info['Class_Type'] = construct_obj.get_class_type()
            construct_info['Class_Specifier'] = construct_obj.get_class_specifier()
            construct_info['Class_Nested_Level'] = construct_obj.get_nested_level()
            construct_info['Class_Signature'] = construct_obj.get_class_signature()
            construct_info['Class_LOC'] = construct_obj.get_class_loc()
            construct_info['Class_Line_No'] = construct_obj.get_class_line_no()
            construct_info['Class_Source_File'] = construct_obj.get_class_source()
        elif ASTHelper.is_enum_info_obj(construct_obj):
            construct_info['Enum_Name'] = construct_obj.get_enum_name()
            construct_info['Enum_Specifier'] = construct_obj.get_enum_specifier()
            construct_info['Enum_Signature'] = construct_obj.get_enum_signature()
            construct_info['Enum_LOC'] = construct_obj.get_enum_loc()
            construct_info['Enum_Line_No'] = construct_obj.get_enum_line_no()
            construct_info['Enum_Source_File'] = construct_obj.get_enum_source()
        elif ASTHelper.is_package_info_obj(construct_obj):
            construct_info['Package_Name'] = construct_obj.get_package_name()
            construct_info['Package_LOC'] = construct_obj.get_package_loc()
            construct_info['Package_Line_No'] = construct_obj.get_package_line_no()
            construct_info['Package_Source_File'] = construct_obj.get_package_source()
            # included serialization file for use in validating existing package
            construct_info['Package_Serialization_File_URL'] = serialization_file
        elif ASTHelper.is_interface_info_obj(construct_obj):
            construct_info['Interface_Name'] = construct_obj.get_interface_name()
            construct_info['Interface_Specifier'] = construct_obj.get_interface_specifier()
            construct_info['Interface_Signature'] = construct_obj.get_interface_signature()
            construct_info['Interface_LOC'] = construct_obj.get_interface_loc()
            construct_info['Interface_Line_No'] = construct_obj.get_interface_line_no()
            construct_info['Interface_Source_File'] = construct_obj.get_interface_source()
        elif ASTHelper.is_method_info_obj(construct_obj):
            construct_info['Method_Name'] = construct_obj.get_method_name()
            construct_info['Method_Type'] = construct_obj.get_method_type()
            construct_info['Method_Specifier'] = construct_obj.get_method_specifier()
            construct_info['Method_Signature'] = construct_obj.get_method_signature()
            construct_info['Method_Category'] = construct_obj.get_method_category()
            construct_info['Method_LOC'] = construct_obj.get_method_loc()
            construct_info['Method_Line_No'] = construct_obj.get_method_line_no()
            construct_info['Method_Source_File'] = construct_obj.get_method_source()
        elif ASTHelper.is_static_block_info_obj(construct_obj):
            construct_info['Static_Block_LOC'] = construct_obj.get_static_block_loc()
            construct_info['Static_Block_Line_No'] = construct_obj.get_static_block_line_no()
            construct_info['Static_Block_Source_File'] = construct_obj.get_static_block_source()
        elif ASTHelper.is_comment_info_obj(construct_obj):
            construct_info['Comment_Content'] = construct_obj.get_comment_text()
            construct_info['Comment_Line_No'] = construct_obj.get_comment_line_no()
            construct_info['Comment_Source_File'] = construct_obj.get_comment_file_name()
            if mining_level == 2 or mining_level == 4:
                construct_info['Comment_Parent_Identifier'] = construct_obj.get_comment_parent_identifier()
                construct_info['Comment_Parent_Trace'] = construct_obj.get_comment_trace()
                construct_info['Comment_Immediate_Succeeding_Code'] = construct_obj.get_succeeding_code()
                construct_info['Comment_Immediate_Preceding_Code'] = construct_obj.get_preceding_code()
                construct_info['Comment_Preceding_Node'] = construct_obj.get_preceding_node()
                construct_info['Comment_Succeeding_Node'] = construct_obj.get_succeeding_node()
                construct_info['Comment_First_Element_In'] = construct_obj.get_first_element_in()
                construct_info['Comment_Last_Element_In'] = construct_obj.get_last_element_in()
                construct_info['Comment_Assoc_Block_Node'] = construct_obj.get_comment_assoc_block_ele()
                construct_info['Comment_Level'] = construct_obj.get_comment_level()
                construct_info['Comment_Type'] = construct_obj.get_comment_type()
                construct_info['Comment_Category'] = construct_obj.get_comment_category()
                construct_info['Comment_SubCategory'] = construct_obj.get_comment_sub_category()
                construct_info['Comment_SubCatg_Type'] = construct_obj.get_comment_sub_catg_type()
        return construct_info


class Utility:

    @staticmethod
    def get_abs_subdir(location):
        if os.path.exists(location) and os.path.isdir(location):
            return [f.path for f in os.scandir(location) if os.path.isdir(f)]
        else:
            return []

    @staticmethod
    def validate_entity_folder(url):
        if Platform.is_unix_platform():
            url = url if url.endswith('/') else url + '/'
        elif Platform.is_windows_platform():
            url = url if url.endswith('\\') else url + '\\'
        for dir_item in os.listdir(url):
            if os.path.isfile(url + dir_item):
                if dir_item.endswith('.json'):
                    return True
        return False

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
        if Utility.is_dir(dir_loc):
            if Utility.is_empty_dir(dir_loc):  # if returned list has file entry items allow process
                return True
            else:
                print("Empty input directory {}".format(dir_loc))
                return False
        else:
            print("Input {} is not a directory".format(dir_loc))
            return False

    @staticmethod
    def get_repo_folders_to_process(local_loc):
        proj_dirs = None
        logging.debug("get_repo_folders_to_process() begins for {}".format(local_loc))
        validate_dir_rc = Utility.validate_inp_dir(local_loc)
        if validate_dir_rc:
            proj_dirs = os.listdir(local_loc)
            for proj in proj_dirs:
                logging.debug("Folders to be processed: {}".format(proj))
        else:
            logging.debug(
                "Input directory {} is either empty or does not contain with return value {}".format(local_loc,
                                                                                                     validate_dir_rc))
        return proj_dirs

    @staticmethod
    def multiple_mode_projects_for_loading(url):
        project_dir = ''
        proj_entity_dirs = Utility.get_repo_folders_to_process(url)
        project_name = ""
        for ind, proj_dir in enumerate(proj_entity_dirs):
            if Platform.is_unix_platform():
                if not url.endswith("/"):
                    url = url + '/'
            if Platform.is_windows_platform():
                if not url.endswith("\\"):
                    url = url + '\\'
            project_name = ""
            absolute_dir = url + proj_dir

            if os.path.isfile(absolute_dir):
                logging.info("Files cannot be present at this level while loading project, hence skipping {}".format(absolute_dir))
                print("Encountered file instead of directory for project loading, hence skipping {}".format(absolute_dir))
                continue

            if Utility.validate_entity_folder(project_dir):
                logging.info("Project JSON not found in the input folder {}. Not a valid SoCC-Miner Mined Entity folder. Exiting SoCCMiner.".format(project_dir))
                logging.info("Skipping for loading")
            else:
                project_dir = (Utility.create_temp_dir_for_loading(absolute_dir, 'multiple'))
        if Platform.is_unix_platform():
            return os.getcwd() + '/soccminer_temp/multiple'
        elif Platform.is_windows_platform():
            return os.getcwd() + '\\soccminer_temp\\multiple'


    @staticmethod
    def create_temp_dir_for_loading(url, mode):
        proj_directory = ''
        inner_proj_directory = ''
        if Platform.is_unix_platform():
            proj_name = url.split("/")[-2] if url.endswith("/") else url.split("/")[-1]
            main_load_proj_directory = ''
            inner_proj_directory = ''
            if mode == 'single':
                main_load_proj_directory = os.getcwd() + '/soccminer_temp/' + datetime.now().strftime(
                    "%d_%m_%Y_%H_%M_%S") + '/'
                inner_proj_directory = main_load_proj_directory + proj_name
            elif mode == 'multiple':
                main_load_proj_directory = os.getcwd() + '/soccminer_temp/'
                inner_proj_directory = main_load_proj_directory + 'multiple'
            proj_directory = inner_proj_directory + '/' + proj_name
        elif Platform.is_windows_platform():
            proj_name = url.split("\\")[-2] if url.endswith("\\") else url.split("\\")[-1]
            main_load_proj_directory = ''
            inner_proj_directory = ''
            if mode == 'single':
                main_load_proj_directory = os.getcwd() + '\\soccminer_temp\\' + datetime.now().strftime(
                    "%d_%m_%Y_%H_%M_%S") + '\\'  # + '\\single_mode_input_load_proj\\'
                inner_proj_directory = main_load_proj_directory + proj_name
            elif mode == 'multiple':
                main_load_proj_directory = os.getcwd() + '\\soccminer_temp\\'
                inner_proj_directory = main_load_proj_directory + 'multiple'
            proj_directory = inner_proj_directory + '\\' + proj_name
        shutil.copytree(url, proj_directory)
        return inner_proj_directory

    @staticmethod
    def fetch_absolute_inp_dir(input_url):
        existing_cwd = os.getcwd()
        os.chdir(input_url)
        input_absolute = os.getcwd()
        print("input absolute: {}".format(input_absolute))
        os.chdir(existing_cwd)
        return input_absolute

    @staticmethod
    def fetch_inp_dir(input_url):
        if Platform.is_unix_platform():
            input_url = input_url[:-1] if input_url.endswith('/') else input_url
        elif Platform.is_windows_platform():
            input_url = input_url[:-1] if input_url.endswith('\\') else input_url
        if Platform.is_unix_platform():
            return input_url[:input_url.rindex('/')+1], input_url[input_url.rindex('/')+1:]
        elif Platform.is_windows_platform():
            return input_url[:input_url.rindex('\\')+1], input_url[input_url.rindex('\\')+1:]

    @staticmethod
    def clear_temp_folders():
        temp_dir = ''
        logging.info("Checking temp folders: ")
        if Platform.is_unix_platform():
            temp_dir = os.getcwd() + '/soccminer_temp/'
        elif Platform.is_windows_platform():
            temp_dir = os.getcwd() + '\\soccminer_temp\\'
        if os.path.isdir(temp_dir):
            logging.info("Clearing temp directories and files at {}".format(temp_dir))
            shutil.rmtree(temp_dir)
        else:
            logging.info("No temp folders")

    @staticmethod
    def validate_srcml():
        process = None
        ret_code = None
        pl = 'Java'
        try:
            process = subprocess.Popen(['srcml', '--text="int i = 1;"', '--language', pl], stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            msg, err = process.communicate(timeout=3)
            ret_code = process.returncode
            message = process.stderr
        except subprocess.TimeoutExpired:
            process.kill()
            msg, err = process.communicate()
            logging.debug("Subprocess msg: {}, error: {}".format(msg, err))
            return False
        except Exception as pexcep:
            error_message = traceback.format_exc()
            logging.info("Unexpected exception occurred while validating environment for srcML, ERROR: {}".format(error_message))
            print("Unexpected exception occurred while validating environment for srcML, ERROR: {}".format(error_message))
            return False
        if ret_code is not None and ret_code == 0:
            logging.info("srcML dependency validated. Environment dependency satisfied for SoCCMiner")
            return True
        else:
            logging.info("Environment dependency validation failed for SoCCMiner, srcML unavailable in environment.")
            print("Environment dependency validation failed for SoCCMiner, srcML unavailable in environment.")
            return False


    @staticmethod
    def fetch_mining_level_mapping():
        mining_level = {1: 'comment', 2: 'comprehensive_comment', 3: 'project', 4: 'all'}
        return mining_level

    @staticmethod
    def check_exception_directory(proj_dir):
        exception_dir = ''
        if Platform.is_unix_platform():
            exception_dir = proj_dir + '/exceptions/'
        elif Platform.is_windows_platform():
            exception_dir = proj_dir + '\\exceptions\\'
        file_count = Utility.fetch_entity_count(exception_dir, 'error')
        return [file_count, exception_dir]

    @staticmethod
    def fetch_entity_count(entity_dir, type):
        logging.debug("fetch_entity_count() begins for type {} at {}".format(type, entity_dir))
        entity_count = 0
        if os.path.isdir(entity_dir):
            src_file_obj = SourceFiles(entity_dir)
            src_file_obj.fetch_source_files(entity_dir, type)
            entity_count = len(src_file_obj.get_files())
            del src_file_obj
        return entity_count
