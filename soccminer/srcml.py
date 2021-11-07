from soccminer.environment import Platform
import logging
from lxml import etree
import os


class SourceML:
    unit_element = "{http://www.srcML.org/srcML/src}unit"

    def __init__(self, ele=None, code=None):
        self.xml_element = ele
        self.code = code

    def get_xml_element(self):
        return self.xml_element

    def fetch_code_from_srcml(self, ele):
        temp_xml_tree = None
        if type(ele) == str:
            return ele
        else:
            # in order to fetch code xml, the prepped xml is first saved locally
            # in temp location, the srcml command to convert xml to source code is applied
            # for getting source code, following this approach for cleaner source code conversion
            # from xml
            if type(ele).__name__ == "_ElementTree":
                temp_xml_tree = ele
            else:
                logging.debug("fetch_code_from_srcml begins for {} whose top-level children(#) is {}".format(ele, len(list(ele))))
                temp_xml_root = etree.Element(SourceML.unit_element)
                temp_xml_root.append(ele)
                temp_xml_tree = etree.ElementTree(temp_xml_root)
            src_cd = None
            try:
                temp_dir_loc = None
                if Platform.is_unix_platform():
                    temp_dir_loc = os.getcwd() + '/soccminer_temp/src_cd_conversion_temp/'
                elif Platform.is_windows_platform():
                    temp_dir_loc = os.getcwd() + '\\soccminer_temp\\src_cd_conversion_temp\\'

                temp_xml_file = temp_dir_loc+ 'temp.xml'
                temp_output_file = temp_dir_loc+'temp.out'
                if not os.path.exists(temp_dir_loc):
                    os.makedirs(temp_dir_loc)
                    logging.debug("temp dir at {} created".format(temp_dir_loc))
                if os.path.exists(temp_xml_file):
                    os.remove(temp_xml_file)
                if os.path.exists(temp_output_file):
                    os.remove(temp_output_file)
                with open(temp_xml_file, 'wb') as fh:
                    temp_xml_tree.write(fh, encoding="utf-8", xml_declaration=True, pretty_print=True)
                cd_conv_command = "srcml {} > {}".format(temp_xml_file,temp_output_file)

                logging.debug("source code conversion command {}".format(cd_conv_command))
                src_cd_op = os.system("{}".format(cd_conv_command))
                if src_cd_op == 0:
                    logging.debug("source code conversion cmd exec status {}".format(src_cd_op))
                    with open(temp_output_file, 'r') as src_cd_out_fh:
                        src_cd = src_cd_out_fh.read()
                else:
                    logging.debug("source code conversion failed with exec status {}".format(src_cd_op))
                logging.debug("src code conversion for {} completed {}".format(temp_xml_file,src_cd))
            except IOError as e:
                logging.error("Unable to write temp xml file for source code conversion {}:{} ".format(e.errno, e.strerror))
                return src_cd
            finally:
                return src_cd
