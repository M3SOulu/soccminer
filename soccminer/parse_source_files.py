import os
import sys
import subprocess
import logging
import logging.handlers
import glob
from soccminer.environment import Platform
import traceback
import gc


# check if it is a directory location
def validate_loc(loc):
    return True if os.path.isdir(loc) else False


class SourceFiles:
    def __init__(self, loc):  # loc can be url or local drive location
        if validate_loc(loc):
            self.loc = loc
        else:
            raise Exception("SoCCMiner failed due to invalid source location: {}".format(loc))
        self.files = []
        self.cd_file_xml_mapping_dict = {}

    def get_files(self):
        return self.files

    def get_source_xml_mapping(self):
        return self.cd_file_xml_mapping_dict

    def fetch_source_files(self, loc, file_type):
        logging.info("Parsing for source code files with extension {} at location {}".format(file_type, loc))
        if Platform.is_unix_platform():
            self.files = glob.glob(loc + '/**/*.' + file_type, recursive=True)
        elif Platform.is_windows_platform():
            self.files = glob.glob(loc + "\\**\\*." + file_type, recursive=True)
        logging.info("Total # number of source code files with extension .{} : {}".format(file_type, len(self.files)))

    def convert_srcfiles_to_xmlfiles(self, project_name, exception_obj):
        logging.info("source code to AST file conversion begins with current dir {}".format(os.getcwd()))
        try:
            temp_dir_loc = None
            if Platform.is_unix_platform():
                temp_dir_loc = os.getcwd() + "/soccminer_temp/temp/" + project_name
            elif Platform.is_windows_platform():
                temp_dir_loc = os.getcwd() + "\\soccminer_temp\\temp\\" + project_name
            if not os.path.exists(temp_dir_loc):
                os.makedirs(temp_dir_loc)
                logging.info("temp dir at {} created".format(temp_dir_loc))
        except OSError as e:
            logging.error("Unable to create temp folder to store AST files ~ Process failed")
            raise Exception("Comments Miner failed as temp folder creation failed")

        src_file_count = 0
        failed_files = []
        for code_file in self.files:
            src_file_count += 1
            try:
                logging.debug("AST conversion for #{} {} begins".format(src_file_count, code_file))
                logging.debug("xml_file_name: {}".format(code_file))
                xml_file_name = code_file.replace(self.loc, '')
                srcml_xml_file = ""
                if Platform.is_unix_platform():
                    xml_file_name = xml_file_name.split('/')[-1]
                    srcml_xml_file = temp_dir_loc + "/" + os.path.splitext(xml_file_name)[0]+'.xml'
                elif Platform.is_windows_platform():
                    xml_file_name = xml_file_name.split('\\')[-1]
                    srcml_xml_file = temp_dir_loc + "\\" + os.path.splitext(xml_file_name)[0]+'.xml'

                logging.debug("To be converted AST file: {}".format(srcml_xml_file))
                srcml_cd = None
                process = None
                print('\r Preparing source files for mining, completed for {}/{}'.format(src_file_count, len(self.files)), sep='', end='',
                      flush=True)
                try:
                    process = subprocess.Popen(['srcml', code_file, "-o", srcml_xml_file], stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE)
                    msg, err = process.communicate(timeout=3)
                    ret_code = process.returncode
                    message = process.stderr
                except subprocess.TimeoutExpired:
                    process.kill()
                    msg, err = process.communicate()
                    logging.debug("Potential Invalid Java source code file: {}".format(code_file))
                    logging.debug("Subprocess msg: {}, error: {}".format(msg, err))
                    exception_obj.update_warning_message(project_name, "Potential Invalid Source code File {}".format(code_file))
                    continue
                except Exception as pexcep:
                    error_message = traceback.format_exc()
                    logging.error("Error occured while conversion to AST for: {}, ERROR: {}".format(code_file, error_message))
                    continue
                else:
                    logging.debug("source code file : {}, conversion status:{}".format(code_file, ret_code))
                    if ret_code == 0:
                        self.cd_file_xml_mapping_dict[code_file] = srcml_xml_file
                    else:
                        logging.info("\n AST conversion failed with {}:{} for {}".format(ret_code, message, code_file))
                        failed_files.append(code_file)
                        exception_obj.update_warning_message(project_name,
                                                             "Failed AST conversion {}".format(
                                                                 code_file))
            except OSError as e:
                logging.info("AST conversion failed for {} ".format(code_file))
                failed_files.append(code_file)
                continue
            except Exception as src_file_cnv:
                logging.info("AST conversion failed for {} with {} {}".format(code_file, sys.exc_info()[0], src_file_cnv))
                failed_files.append(code_file)
                continue

        if len(failed_files) > 0:
            exception_obj.update_warning_message(project_name,
                                                   "Project {} has {} failed AST conversions".format(project_name, len(failed_files)))
        exception_obj.update_failed_ast_count(project_name, len(failed_files))
        for x in list(locals().keys())[:]:
            del locals()[x]
        gc.collect()

