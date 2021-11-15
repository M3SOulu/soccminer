import itertools
import time

from soccminer.java_ast_parsing import SourceFiles
from soccminer.environment import Platform
#from alive_progress import alive_bar
from lxml import etree
import time
import gc
import traceback
import subprocess
import os
import logging
import requests
import shutil


class TrackProgress:
    @staticmethod
    def fetch_approx_mining_eta(files, mining_level):
        approx_eta_mins = 0.0
        if mining_level == 1:
            approx_eta_mins = (files / 15) / 60
        elif mining_level == 2:
            approx_eta_mins = (files / 5) / 60
        elif mining_level == 3:
            approx_eta_mins = (files / 2.5) / 60
        elif mining_level == 4:
            approx_eta_mins = (files / 1.5) / 60

        return round(approx_eta_mins, 2)

    @staticmethod
    def track_ast_parsing_progress(total_files, processed_source_file_dir, error_file_dir, project_name, mining_level):
        logging.info("track_ast_parsing_progress begins")
        os.makedirs(processed_source_file_dir) if not os.path.isdir(processed_source_file_dir) else None
        os.makedirs(error_file_dir) if not os.path.isdir(error_file_dir) else None
        if os.path.isdir(processed_source_file_dir) and os.path.isdir(error_file_dir):
            logging.info("processed_dir and error dir  exists")
            processed_files = TrackProgress.fetch_file_count(processed_source_file_dir, 'json') + TrackProgress.fetch_file_count(error_file_dir, 'error')
            processed_files = 1 if processed_files == 0 else processed_files

            approx_eta_mins = TrackProgress.fetch_approx_mining_eta(total_files, mining_level)

            if total_files != processed_files:
                print('\r {} - Mining source files completed for {}/{}. Approx ETA for completion {} minute/s'.format(project_name, processed_files, total_files, approx_eta_mins), sep='', end='', flush=True)
            else:
                approx_eta_mins = 0.0
                print('\r {} - Mining source files completed for {}/{}. Approx ETA for completion {} minute/s \n'.format(project_name, processed_files, total_files, approx_eta_mins), sep='', end='', flush=True)
                return True
            logging.info("Total valid files for progress tracking: {}".format(total_files))
            while processed_files <= total_files:
                approx_eta_mins = TrackProgress.fetch_approx_mining_eta(total_files - processed_files, mining_level)
                print('\r {} - Mining source files completed for {}/{}. Approx ETA for completion {} minute/s'.format(project_name, processed_files, total_files, approx_eta_mins), sep='', end='', flush=True)
                if total_files == processed_files:
                    logging.debug("Total files {} == processed_files {}".format(total_files, processed_files))
                    break
                else:
                    time.sleep(3)
                    processed_files = TrackProgress.fetch_file_count(processed_source_file_dir, 'json') + TrackProgress.fetch_file_count(
                    error_file_dir, 'error')
                    logging.info("Fetching processed_files after sleep {}".format(processed_files))
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
            print("Unexpected exception occurred while validating environment for srcML, ERROR: {}".format(error_message))
            return False
        if ret_code is not None and ret_code == 0:
            logging.info("srcML dependency validated. Environment dependency validation cleared for SoCCMiner")
            return True
        else:
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