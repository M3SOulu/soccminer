from soccminer.comments_miner import CommentsMiner
from soccminer.soccminer_logger import SoCCMinerLogger
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


#def validate_inp_csv_file(inp_file):
#    if not is_existing_file(inp_file):
#        print("Input CSV file {} does not exist or inaccessible".format(inp_file))
#        return False
#    elif is_empty_file(inp_file):
#        print("Input CSV file {} is empty".format(inp_file))
#        return False
#    else:
#        try:
#            _ = pd.read_csv(inp_file, dtype={
#                               'Project_Id': str,
#                               'URL': str
#                            })
#        except Exception as ex:
#            print("Error with CSV: {}".format(ex))
#            return False
#        else:
#            return True


def validate_cli(cl_args):
    global local_inp_dir, mining_level, load_proj_flag, log, programming_language, serialize_flag
    local_inp_dir = cl_args.inp

    # level comment - Basic Comment and Project Attributes, level comprehensive_comment - Comprehensive Comment Attributes
    # level project - Project Meta Attributes, level all - Project and Comprehensive Comment attributes
    mining_level = cl_args.mining_level
    log = cl_args.log  # 0 - No log, 1 - Debug, 2 - Info
    programming_language = cl_args.language.lower()
    load_proj_flag = cl_args.load_project

    if load_proj_flag.lower() == "true":
        load_proj_flag = 1
    elif load_proj_flag.lower() == "false":
        load_proj_flag = 0

    if not validate_inp_dir(local_inp_dir):
        print("Issue with Directory input ({})".format(local_inp_dir))
        return False

    if load_proj_flag not in [0, 1]:
        print("Incorrect value for load_project. Can be either True/False, {}".format(type(load_proj_flag)))
        return False

    if not mining_level.strip().lower() in ["comment", "comprehensive_comment", "project", "all"]: #, "none"]:
        print("Issue with mining level input {}".format(mining_level.strip().lower()))
        return False
    else:
        if mining_level.strip().lower() == "comment":
            mining_level = 1
        elif mining_level.strip().lower() == "comprehensive_comment":
            mining_level = 2
        elif mining_level.strip().lower() == "project":
            mining_level = 3
        elif mining_level.strip().lower() == "all":
            mining_level = 4

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
    return True


def validate_cli_args():
    global inp_dir, m_level, load_proj, log_level, prog_lang
    # parse input arguments
    parser = argparse.ArgumentParser(prog='SoCCMiner', description='Source Code Comments miner')
    parser.add_argument("inp",
                        help="Defines the input to the tool. Can be 'local_dir' containing project repositories as sub-directories or 'Git Repo URL'")
    parser.add_argument("language",
                        help="The programming language of the project, for now only java project are handled by SoCCMiner")
    parser.add_argument("mining_level", help="Defines the mining/project entity loading level. Can be 'comment' to mine/load basic comment info, "
                                             "'comprehensive_comment' to mine/load comprehensive comment attributes, "
                                             "'project' to mine/load project attributes), "
                                             "'all' (for project and comprehensive attributes) "
                                             " NOTE: While loading entities with load_project input argument set to True, SoCCMiner expects the same mining level with which the project was mined.")
    parser.add_argument("load_project", help="load_project - If True, loads project entities from the mined entities directory containing the soccminer serialized json files. "
              "If False, mines source code projects for comments, source code entities and their attributes according to the mining level input")
    parser.add_argument("log", help="Defines the logging level. Can be one of nolog(NOLOG), info(INFO), debug(DEBUG)")

    if len(sys.argv) != 6:
        parser.print_help()
        sys.exit(1)
    cl_args = parser.parse_args()
    inp_dir = cl_args.inp
    m_level = cl_args.mining_level
    load_proj = cl_args.load_project
    log_level = cl_args.log
    prog_lang = cl_args.language

    ret_stat = validate_cli(cl_args)
    if not ret_stat:
        parser.print_help()
        sys.exit(1)


def main():
    global local_inp_dir, mining_level, load_proj_flag, log, programming_language
    global inp_dir, m_level, load_proj, log_level, prog_lang
    project_name = None

    try:
        validate_cli_args()
        if log is not None or log != 0:
            SoCCMinerLogger(log, "")
        print("Instantiating from Main")

        # Passing the args as rcvd from commandline without validation as there's a validation in the API call
        # However this validation here happens when invoked from commandline only
        cm = CommentsMiner(inp_dir, prog_lang, m_level, load_proj, log_level)
        total_project_repositories = len(CommentsMiner.get_repo_folders_to_process(inp_dir))
        logging.debug("Found {} project repositories in the input dir argument {}".format(total_project_repositories, inp_dir))

        logging.info("Input Mining Level: {}".format(m_level))
        logging.info("Input Load_Project: {}, {}".format(load_proj, load_proj_flag))

        if not load_proj_flag and not cm.miner_status_flag:
            raise Exception("SoccMiner Mining Failed.")
        elif load_proj_flag and not cm.load_status:
            raise Exception("SoccMiner Loading Failed.")
        else:
            if not cm.invalid_ing_arg_flag:
                print("SoccMiner Completed Execution")
    except Exception as ex:
        error_message = traceback.format_exc()
        logging.error("Unexpected error {} {}".format(error_message, ex))
        sys.exit(1)

local_inp_dir = ""
inp_dir = ""
mining_level = ""
m_level = ""
log = ""
log_level = ""
programming_language = ""
prog_lang = ""
load_proj_flag = ""
load_proj = ""

# Main function
if __name__ == '__main__':
    main()    
