from soccminer.comments_miner import CommentsMiner
from soccminer.soccminer_logger import SoCCMinerLogger
from soccminer.helper import RepoDownloader
from soccminer.environment import Platform
from collections import Counter
import logging
import argparse
import traceback
import os
import sys


def is_empty_file(file_loc):
    # validate if file is empty
    return os.stat(file_loc).st_size == 0


def is_dir(dir_loc):
    # validate if dir
    return os.path.exists(dir_loc) and os.path.isdir(dir_loc)


def validate_inp_dir(dir_loc):
    # validate if dir exists and not empty
    if CommentsMiner.is_dir(dir_loc):
        if CommentsMiner.is_empty_dir(dir_loc):  # if returned list has file entry items allow process
            return True  # not empty
        else:
            print("Empty input directory")
            return False  # empty
    else:
        print("{} not a directory".format(dir_loc))
        return False
        
        
def is_empty_dir(dir_loc):
    # validate if empty dir
    return os.listdir(dir_loc)


def is_existing_file(file_loc):
    # validate if file exists
    return os.path.isfile(file_loc)


def validate_cli(cl_args):
    global local_inp_dir, inp_dir, level, load_proj_flag, log, programming_language, serialize_flag, output_dir, mode, context_span
    local_inp_dir = cl_args.input

    # level comment - Basic Comment and Project Attributes, level comprehensive_comment - Comprehensive Comment Attributes
    # level project - Project Meta Attributes, level all - Project and Comprehensive Comment attributes
    level = cl_args.level
    log = cl_args.log  # 0 - No log, 1 - Debug, 2 - Info
    programming_language = cl_args.language.lower()
    load_proj_flag = cl_args.direct_load
    output_dir = cl_args.output
    context_span = int(cl_args.context_span)
    if type(load_proj_flag) == str:
        if load_proj_flag.lower() == 'true':
            load_proj_flag = True
        elif load_proj_flag.lower() == 'false':
            load_proj_flag = False

    if load_proj_flag not in [0, 1]:
        load_proj_flag = str(load_proj_flag).lower()
        if load_proj_flag == "true" or load_proj_flag:
            load_proj_flag = 1
        if load_proj_flag == "false" or not load_proj_flag:
            load_proj_flag = 0

    if not os.path.isdir(output_dir):
        print("Invalid output directory {}".format(output_dir))
        return False

    if ('http' in local_inp_dir or
            'https' in local_inp_dir or
            'www' in local_inp_dir) and 'github.com' in local_inp_dir:
        if load_proj_flag:
            print("Project cannot be loaded from Github repository, please specify a local directory containing SoCC-Miner mined entities")
            return False
        if RepoDownloader.validate_repo_url(local_inp_dir):
            cloned_folder = RepoDownloader.clone_repo(local_inp_dir)
            if not cloned_folder:
                print("Issue with input url, please check input url: {}".format(local_inp_dir))
                return False
            else:
                local_inp_dir = cloned_folder
                if Platform.is_unix_platform():
                    inp_dir = local_inp_dir[:-1] if local_inp_dir.endswith('/') else local_inp_dir
                elif Platform.is_windows_platform():
                    inp_dir = local_inp_dir[:-1] if local_inp_dir.endswith('\\') else local_inp_dir

                if mode != 'single':
                    print("Mode cannot be multiple/files for GitHub project repository, forcing it to 'single'")
                    mode = 'single'
    elif not validate_inp_dir(local_inp_dir):
        print("Issue with Directory input ({})".format(local_inp_dir))
        return False

    if load_proj_flag not in [0, 1]:
        print("Incorrect value for load_project. Can be either True/False, {}".format(type(load_proj_flag)))
        return False

    if not level.strip().lower() in ["comment", "comprehensive_comment", "project", "all"]: #, "none"]:
        print("Issue with mining level input {}".format(level.strip().lower()))
        return False
    else:
        if level.strip().lower() == "comment":
            level = 1
        elif level.strip().lower() == "comprehensive_comment":
            level = 2
        elif level.strip().lower() == "project":
            level = 3
        elif level.strip().lower() == "all":
            level = 4

    if not log.strip().lower() in ["nolog", "info", "debug"]:
        print("Issue with log level input")
        return False
    else:
        if log.strip().lower() == "none" or log.strip().lower() == "nolog":
            log = 0
        elif log.strip().lower() == "debug":
            log = 2
        elif log.strip().lower() == "info":
            log = 1

    if programming_language not in ['java']:
        print("Issue with programming language input {}".format(programming_language))
        return False

    if context_span < 1:
        print("Issue with context span input, context span cannot be less than 1")
        return False

    return True

def demo_project(cm):
    # Loads JavaMetaAttribute object for mining level 'project' that contains project
    # meta for all the entities.
    for proj in cm.fetch_mined_project_meta():
        ############################################################
        # Java project meta attributes
        print("Package Count: {}".format(proj.get_package_count()))
        print("Class Count: {}".format(proj.get_class_count()))
        print("Enum Count: {}".format(proj.get_enum_count()))
        print("Method Count: {}".format(proj.get_method_count()))
        print("Interface Count: {}".format(proj.get_interface_count()))
        print("Static Block Count: {}".format(proj.get_static_block_count()))


def demo(cm):
    # Loads JavaMiner object for mining level 'all' that contains both project
    # meta and comprehensive comments
    mined_proj_obj_list = cm.fetch_mined_project_meta_and_comments()
    for proj in mined_proj_obj_list:
        ############################################################
        # Java project meta attributes
        print("Package Count: {}".format(proj.get_package_count()))
        print("Class Count: {}".format(proj.get_class_count()))
        print("Enum Count: {}".format(proj.get_enum_count()))
        print("Method Count: {}".format(proj.get_method_count()))
        print("Interface Count: {}".format(proj.get_interface_count()))
        print("Static Block Count: {}".format(proj.get_static_block_count()))
        for file_obj in proj.get_file_meta_attr():
            print("{}".format(type(file_obj)))
            print("File LOC: {}".format(file_obj.file_loc))

        for package_obj in proj.get_package_meta_attr():
            print("Package Name: {}".format(package_obj.package_name))
            print("Package LOC: {}".format(package_obj.package_loc))
            print("Package Line #: {}".format(package_obj.package_line_no))
            print("Package Java Source File: {}".format(package_obj.source_file_name))

        for class_obj in proj.get_class_meta_attr():
            print("Class Name: {}".format(class_obj.class_name))
            print("Class Type: {}".format(class_obj.class_type))
            print("Class Specifier: {}".format(class_obj.class_specifier))
            print("Class Line #: {}".format(class_obj.class_line_no))
            print("Class Nested Level: {}".format(class_obj.nested_level))
            print("Class Signature: {}".format(class_obj.class_signature))
            print("Class LOC: {}".format(class_obj.class_loc))
            print("Class Java Source File #: {}".format(class_obj.class_source_file))

            # fetch all comprehensive comments
            for comprehensive_comments_obj in proj.get_comprehensive_comment_attr():
                print("Comment content: {}".format(comprehensive_comments_obj.comment_text))
                print("Comment line #: {}".format(comprehensive_comments_obj.comment_line_no))
                print("Comment source file: {}".format(comprehensive_comments_obj.file_name))
                print("Comment preceding code statement type: {}".format(comprehensive_comments_obj.preceding_node))
                print("Comment preceding code: {}".format(comprehensive_comments_obj.preceding_code))
                print("Comment succeeding code statement type: {}".format(comprehensive_comments_obj.succeeding_node))
                print("Comment succeding code: {}".format(comprehensive_comments_obj.succeeding_code))
                print("Comment parent identifier: {}".format(comprehensive_comments_obj.comment_parent_identifier))
                print("Comment parent identifier trace: {}".format(comprehensive_comments_obj.comment_trace))
                print("Comment category: {}".format(comprehensive_comments_obj.comment_category))
                print("Comment is a first statement in: {}".format(comprehensive_comments_obj.first_element_in))
                print("Comment is a last statement in: {}".format(comprehensive_comments_obj.last_element_in))
                print("Comment type: {}".format(comprehensive_comments_obj.comment_type))

            # fetch package level comprehensive comments
            for comprehensive_comments_obj in proj.get_comprehensive_file_comment_attr():
                print("Comment content: {}".format(comprehensive_comments_obj.comment_text))
                print("Comment line #: {}".format(comprehensive_comments_obj.comment_line_no))
                print("Comment source file: {}".format(comprehensive_comments_obj.file_name))
                print("Comment preceding code statement type: {}".format(comprehensive_comments_obj.preceding_node))
                print("Comment preceding code: {}".format(comprehensive_comments_obj.preceding_code))
                print("Comment succeeding code statement type: {}".format(comprehensive_comments_obj.succeeding_node))
                print("Comment succeding code: {}".format(comprehensive_comments_obj.succeeding_code))
                print("Comment parent identifier: {}".format(comprehensive_comments_obj.comment_parent_identifier))
                print("Comment parent identifier trace: {}".format(comprehensive_comments_obj.comment_trace))
                print("Comment category: {}".format(comprehensive_comments_obj.comment_category))
                print("Comment is a first statement in: {}".format(comprehensive_comments_obj.first_element_in))
                print("Comment is a last statement in: {}".format(comprehensive_comments_obj.last_element_in))
                print("Comment type: {}".format(comprehensive_comments_obj.comment_type))

def demo_compre_comment(cm):
    # Loads ComprehensiveCommentsAttribute object for mining level 'comprehensive_comment' that contains
    # comprehensive comment attributes for all the entities.
    for proj in cm.fetch_mined_comment_attributes(): #mined_proj_obj_list
        # fetch all comprehensive comments
        for comprehensive_comments_obj in proj.get_comprehensive_comment_attr():
            print("Comment content: {}".format(comprehensive_comments_obj.comment_text))

        print("Total file level comments: ",len(proj.get_comprehensive_file_comment_attr()))
        print("Total class level comments: ",len(proj.get_comprehensive_class_comment_attr()))
        print("Total method level comments: ",len(proj.get_comprehensive_method_comment_attr()))
        print("Total interface level comments: ",len(proj.get_comprehensive_interface_comment_attr()))
        print("Total enum level comments: ",len(proj.get_comprehensive_enum_comment_attr()))
        print("Total StaticBlock level comments: ", len(proj.get_comprehensive_static_block_comment_attr()))


def validate_cli_args():
    global inp_dir, m_level, load_proj, log_level, prog_lang, output_dir, mode, context_span
    # parse input arguments
    parser = argparse.ArgumentParser(prog='main.py', description='Source Code Comments miner')
    parser.add_argument("-i", "--input",
                        help="Defines the input to the tool. Mandatory input argument. Can be 'local_dir' containing project source files or containing project repositories as sub-directories or 'Git Repo URL'")
    parser.add_argument("-l", "--language", default='java',
                        help="The programming language of the project, for now only java project are handled by SoCCMiner")
    parser.add_argument("-lvl", "--level", default='comment',
                        help="Defines the mining/project entity loading level. Can be 'comment' to mine/load basic comment info, "
                                             "'comprehensive_comment' to mine/load comprehensive comment attributes, "
                                             "'project' to mine/load project attributes), "
                                             "'all' (for project and comprehensive attributes) "
                                             " NOTE: While loading entities with 'direct_load' input argument set to True, SoCCMiner expects the same mining level with which the project was mined.")
    parser.add_argument("-dl", "--direct_load", default=False,
                        help="direct_load - If True, loads the data pipelines with project entities from the mined entities directory containing the soccminer serialized json files. "
              "If False, mines source code projects for comments, source code entities and their attributes according to the mining level input and then loads the data pipelines."
              " NOTE: Mined Project can only be loaded from local directory, if load_project is set to True, input should be local directory containing SoCC-Miner Mined Entities")

    parser.add_argument("-log", "--log", default='nolog',
                        help="Defines the logging level. Can be one of nolog(NOLOG), info(INFO), debug(DEBUG)"
                             "NOTE: Enabling log creates very huge file log file for huge source code repositories. Enable it for debugging after ensuring enough disk space is available.")
    parser.add_argument("-o", "--output", default=os.getcwd(),
                        help="Defines the output directory where the mined entities will be stored by default it is current working directory. Accepts only valid existing directory.")
    parser.add_argument("-m", "--mode", default='single',
                        help="Defines SoCC-Miner execution mode, can be 'single' to mine single project directory (i.e., all files and directories within input directory will be treated as a single project), \n"
                             "'multiple' to mine multiple project directories in which all sub-directories within the input directory will be treated as separate project directories, or \n"
                             "NOTE: SoCC-Miner expects an input directory that contains only project directory/ies as sub-directory/ies in 'multiple' mode. \n")
                             #"'files' to mine individual source files that are not part of any project, all the individual files will be collectively treated as a single project. \n"
                             #"NOTE: SoCC-Miner expects an input directory that contains only project directory/ies as sub-directory/ies in 'multiple' mode. \n")
    parser.add_argument("-cs", "--context_span", default=1,
                        help="Length of the context span (in number of lines) to be fetched for both preceding and succeeding context for a source code context")

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    cl_args = parser.parse_args()
    inp_dir = cl_args.input
    m_level = cl_args.level
    load_proj = cl_args.direct_load
    log_level = cl_args.log
    prog_lang = cl_args.language
    output_dir = cl_args.output
    mode = cl_args.mode
    context_span = int(cl_args.context_span)

    ret_stat = validate_cli(cl_args)
    if not ret_stat:
        parser.print_help()
        sys.exit(1)


def main():
    global local_inp_dir, level, load_proj_flag, log, programming_language, output_dir
    global inp_dir, m_level, load_proj, log_level, prog_lang, mode, context_span
    project_name = None

    try:
        validate_cli_args()
        if log is not None or log != 0:
            SoCCMinerLogger(log, "")
        print("Instantiating from Main")

        # total_project_repositories = len(CommentsMiner.get_repo_folders_to_process(inp_dir))
        # logging.debug("Found {} project repositories in the input dir argument {}".format(total_project_repositories, inp_dir))

        logging.info("Input Mining Level: {}".format(m_level))
        logging.info("Input Load_Project: {}, {}".format(load_proj, load_proj_flag))
        # Passing the args as rcvd from commandline without validation as there's a validation in the API call
        # However this validation here happens when invoked from commandline only

        cm = CommentsMiner(inp_dir, prog_lang, m_level, load_proj, log_level, output_dir, mode, context_span)
        if not load_proj_flag and cm.invalid_ing_arg_flag:
            print("Unable to mine the source code as SoccMiner did not execute due to invalid input argument.")
            sys.exit(1)
        elif load_proj_flag and cm.invalid_ing_arg_flag:
            print("Unable to load project as SoccMiner did not execute due to invalid input argument.")
            sys.exit(1)

        if not load_proj_flag and not cm.miner_status_flag:
            print("SoccMiner Mining Failed.")
            sys.exit(1)
        elif load_proj_flag and not cm.load_status:
            print("SoccMiner Loading Failed.")
            sys.exit(1)
        else:
            if not cm.invalid_ing_arg_flag:
                #demo_compre_val(cm)
                #demo_project(cm)
                #demo(cm)
                #demo_compre_comment(cm)
                print("SoccMiner Completed Execution")
    except Exception as ex:
        error_message = traceback.format_exc()
        logging.error("Unexpected error {} {}".format(error_message, ex))
        sys.exit(1)


local_inp_dir = ""
inp_dir = ""
output_dir = ""
level = ""
m_level = ""
log = ""
log_level = ""
programming_language = ""
prog_lang = ""
load_proj_flag = ""
load_proj = ""
mode = ""
context_span = 0

# Main function
if __name__ == '__main__':
    main()


