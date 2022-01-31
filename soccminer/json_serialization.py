import ujson
import logging
import traceback
from soccminer.environment import Platform
from soccminer.helper import ASTHelper
from soccminer.process_parameters import ProcessParameter
from soccminer.parse_source_files import validate_loc
from soccminer.parse_source_files import SourceFiles
from soccminer.comments import CommentInfo
import os


class SerializeSoCCMiner:
    comprehensive_comments_json = 'soccminer_comprehensive_comments_info.json'
    proj_and_comment_attr_json = 'soccminer_proj_attr_and_comment_attr.json'
    java_proj_attr_json = 'soccminer_java_project_attr.json'
    comments_meta_json = 'soccminer_comments_meta_info.json'
    attribute_json_file_list = [comments_meta_json, proj_and_comment_attr_json, java_proj_attr_json, comments_meta_json]

    @staticmethod
    def write_json_file(file_name:str, json_dict:dict):
        fname = None
        logging.debug("write_json_file(): Serializing at {}".format(file_name))
        if Platform.is_unix_platform():
            fname = os.getcwd() + "/" + file_name if file_name in SerializeSoCCMiner.attribute_json_file_list else file_name + '.json'
        elif Platform.is_windows_platform():
            fname = os.getcwd() + "\\" + file_name if file_name in SerializeSoCCMiner.attribute_json_file_list else file_name + '.json'
        try:
            with open(fname, 'w') as fh:
                ujson.dump(json_dict, fh, indent=4, sort_keys=True)

            if not os.path.isfile(fname):
                logging.error("Entity not serialized: {} ".format(fname))
            else:
                logging.debug("Serialization successful for {}".format(fname))
        except Exception as json_write_error:
            logging.error("Serialization Failed: Failed to write file json file {}".format(fname))
            raise

    @staticmethod
    def load_from_json_file(file_name: str):
        files = []
        construct_info = []
        if validate_loc(file_name):
            json_files = SourceFiles(file_name)
            json_files.fetch_source_files(file_name, 'json')
            files = json_files.get_files()
        else:
            if file_name.endswith('.json'):
                files.append(file_name)
            else:
                # entity folders that does not exist
                return construct_info

        for json_file in files:
            try:
                fh = open(json_file, "r")
                construct_info.append(ujson.load(fh))
                fh.close()
            except Exception as json_read_error:
                error_message = traceback.format_exc()
                logging.error("Load from serialized object failed: Failed to load file json file {}. Error: {}".format(json_file, error_message))
                raise
        else:
            return construct_info

    @staticmethod
    def load_comment_info(comment_dir):
        comment_info = []
        ProcessParameter.fetch_program_parameters()
        construct_info = SerializeSoCCMiner.load_from_json_file(comment_dir)

        for comment_info_dict in construct_info:
            comment_obj = CommentInfo()
            if ProcessParameter.miner_params['mining_level'] == 1:
                comment_obj.set_comment_text(comment_info_dict['Comment_Content'])
                comment_obj.set_comment_line_no(comment_info_dict['Comment_Line_No'])
                comment_obj.set_comment_file_name(comment_info_dict['Comment_Source_File'])
            elif ProcessParameter.miner_params['mining_level'] == 2 or ProcessParameter.miner_params['mining_level'] == 4:
                comment_obj.set_comment_text(comment_info_dict['Comment_Content'])
                comment_obj.set_comment_line_no(comment_info_dict['Comment_Line_No'])
                comment_obj.set_comment_file_name(comment_info_dict['Comment_Source_File'])
                comment_obj.set_comment_parent_identifier(comment_info_dict['Comment_Parent_Identifier'])
                comment_obj.set_comment_trace(comment_info_dict['Comment_Parent_Trace'])
                comment_obj.set_succeeding_code(comment_info_dict['Comment_Immediate_Succeeding_Code'])
                comment_obj.set_preceding_code(comment_info_dict['Comment_Immediate_Preceding_Code'])
                comment_obj.set_preceding_node(comment_info_dict['Comment_Preceding_Node'])
                comment_obj.set_succeeding_node(comment_info_dict['Comment_Succeeding_Node'])
                comment_obj.set_first_element_in(comment_info_dict['Comment_First_Element_In'])
                comment_obj.set_last_element_in(comment_info_dict['Comment_Last_Element_In'])
                comment_obj.set_comment_assoc_block_ele(comment_info_dict['Comment_Assoc_Block_Node'])
                comment_obj.set_comment_level(comment_info_dict['Comment_Level'])
                comment_obj.set_comment_type(comment_info_dict['Comment_Type'])
                comment_obj.set_comment_category(comment_info_dict['Comment_Category'])
                comment_obj.set_comment_sub_category(comment_info_dict['Comment_SubCategory'])
                comment_obj.set_comment_sub_category_type(comment_info_dict['Comment_SubCatg_Type'])
            comment_info.append(comment_obj)
        return comment_info

    @staticmethod
    def serialize_project_source_file_info(proj_name, destination_dir, src_file_proj_info):
        src_file_info = {}
        file_name = None
        if Platform.is_unix_platform():
            file_name=destination_dir + '/' + proj_name
        elif Platform.is_windows_platform():
            file_name=destination_dir + '\\' + proj_name

        src_file_object = src_file_proj_info['src_file_obj']

        src_file_info['Serialized_Project_Name'] = src_file_proj_info['proj_name']
        src_file_info['Serialized_Project_KLOC'] = src_file_proj_info['proj_loc']
        src_file_info['Serialized_Project_Platform'] = src_file_proj_info['platform']
        src_file_info['Serialized_Mining_Level'] = src_file_proj_info['mining_level']
        src_file_info['Entity_Project_Directory'] = src_file_object.loc
        src_file_info['Source_Files_List'] = src_file_object.files
        src_file_info['Source_Xml_Mapping_Dict'] = {}  # This is not necessary while exporting the attribute jsons
                                                        # but the source files are neeeded for source file count
        SerializeSoCCMiner.write_json_file(file_name, src_file_info)

    @staticmethod
    def serialize_project_comments_meta_info(project_comments: list):
        project_meta = {}
        comment_info = {}
        comments = {}
        comments_meta_info = {}
        for proj_cmmnt in project_comments:
            project_meta['Project_Name'] = proj_cmmnt.get_project_name()
            project_meta['Project_KLOC'] = proj_cmmnt.get_project_loc()
            project_meta['Project_Src_File_Count'] = proj_cmmnt.get_source_file_count()
            comment_ind = 0
            for cmnt in proj_cmmnt.get_comments():
                comment_ind += 1
                comment_info['Comment_Content'] = cmnt.get_comment_text()
                comment_info['Comment_Line_No'] = cmnt.get_comment_line_no()
                comment_info['Comment_Source_File'] = cmnt.get_comment_file_name()
                comments[comment_ind] = comment_info
                comment_info = {}
        comments_meta_info['Project_Meta'] = project_meta
        comments_meta_info['Comments'] = comments
        SerializeSoCCMiner.write_json_file(SerializeSoCCMiner.comments_meta_json, comments_meta_info)

    @staticmethod
    def serialize_comprehensive_comment_attributes(project_comments:list):
        project_meta = {}
        comment_info = {}
        comments = {}
        comprehensive_comments_info = {}
        for proj_cmmnt in project_comments:
            project_meta['Project_Name'] = proj_cmmnt.get_project_name()
            project_meta['Project_KLOC'] = proj_cmmnt.get_project_loc()
            project_meta['Project_Src_File_Count'] = proj_cmmnt.get_source_file_count()
            comment_ind = 0
            for cmnt in proj_cmmnt.get_comments_with_attr():
                comment_ind += 1
                comment_info['Comment_Content'] = cmnt.get_comment_text()
                comment_info['Comment_Line_No'] = cmnt.get_comment_line_no()
                comment_info['Comment_Source_File'] = cmnt.get_comment_file_name()
                comment_info['Comment_Parent_Identifier'] = cmnt.get_comment_parent_identifier()
                comment_info['Comment_Parent_Trace'] = cmnt.get_comment_trace()
                comment_info['Comment_Immediate_Succeeding_Code'] = cmnt.get_succeeding_code()
                comment_info['Comment_Immediate_Preceding_Code'] = cmnt.get_preceding_code()
                comment_info['Comment_Preceding_Node'] = cmnt.get_preceding_node()
                comment_info['Comment_Succeeding_Node'] = cmnt.get_succeeding_node()
                comment_info['Comment_First_Element_In'] = cmnt.get_first_element_in()
                comment_info['Comment_Last_Element_In'] = cmnt.get_last_element_in()
                comment_info['Comment_Assoc_Block_Node'] = cmnt.get_comment_assoc_block_ele()
                comment_info['Comment_Level'] = cmnt.get_comment_level()
                comment_info['Comment_Type'] = cmnt.get_comment_type()
                comment_info['Comment_Category'] = cmnt.get_comment_category()
                comment_info['Comment_SubCategory'] = cmnt.get_comment_sub_category()
                comment_info['Comment_SubCatg_Type'] = cmnt.get_comment_sub_catg_type()
                comments[comment_ind] = comment_info
                comment_info = {}
        comprehensive_comments_info['Project_Meta'] = project_meta
        comprehensive_comments_info['Comments'] = comments
        SerializeSoCCMiner.write_json_file(SerializeSoCCMiner.comprehensive_comments_json, comprehensive_comments_info)

    @staticmethod
    def serialize_construct(construct_obj, serialization_file:str):
        construct_info = {}

        logging.info("Serializing object {} at {}".format(type(construct_obj).__name__, serialization_file))
        if ASTHelper.is_file_info_obj(construct_obj):
            construct_info['Source_File'] = construct_obj.get_file_source()
            construct_info['File_LOC'] = construct_obj.get_file_loc()
            construct_info['File_Comments_Count'] = construct_obj.get_file_comments_count()
        elif ASTHelper.is_class_info_obj(construct_obj):
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
            construct_info['Method_Param_Count'] = construct_obj.get_method_param_cnt()
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
                if ProcessParameter.miner_params['mining_level'] == 2 or ProcessParameter.miner_params['mining_level'] == 4:
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

        logging.debug("serialize_construct(): serialization_file: {} ".format(serialization_file))
        SerializeSoCCMiner.write_json_file(serialization_file, construct_info)

    @staticmethod
    def serialize_proj_attr_and_comp_comments(projects:list):
        project_meta = {}
        comment_info = {}
        comments = {}
        package_info = {}
        class_info = {}
        method_info = {}
        interface_info = {}
        static_block_info = {}
        package_meta = {}
        class_meta = {}
        interface_meta = {}
        method_meta = {}
        static_block_meta = {}
        proj_attr_and_comprehensive_comments_info = {}
        comment_ind = 0
        for proj in projects:
            project_meta['Project_Name'] = proj.get_project_name()
            project_meta['Project_KLOC'] = proj.get_project_loc()
            project_meta['Project_Src_File_Count'] = proj.get_source_file_count()
            project_meta['Project_Package_Count'] = proj.get_package_count()
            project_meta['Project_Class_Count'] = proj.get_class_count()
            project_meta['Project_Method_Count'] = proj.get_method_count()
            project_meta['Project_Interface_Count'] = proj.get_interface_count()
            project_meta['Project_Static_Block_Count'] = proj.get_static_block_count()
            package_ind = 0
            for meta_attr_obj in proj.get_package_meta_attr():
                package_ind += 1
                package_info['Package_Name'] = meta_attr_obj.get_package_name()
                package_info['Package_LOC'] = meta_attr_obj.get_package_loc()
                package_info['Package_Line_No'] = meta_attr_obj.get_package_line_no()
                package_info['Package_Source_File'] = meta_attr_obj.get_package_source()
                package_meta[package_ind] = package_info
                package_info = {}

            class_ind = 0
            for meta_attr_obj in proj.get_class_meta_attr():
                class_ind += 1
                class_info['Class_Name'] = meta_attr_obj.get_class_name()
                class_info['Class_Type'] = meta_attr_obj.get_class_type()
                class_info['Class_Specifier'] = meta_attr_obj.get_class_specifier()
                class_info['Class_Nested_Level'] = meta_attr_obj.get_nested_level()
                class_info['Class_Signature'] = meta_attr_obj.get_class_signature()
                class_info['Class_LOC'] = meta_attr_obj.get_class_loc()
                class_info['Class_Line_No'] = meta_attr_obj.get_class_line_no()
                class_info['Class_Source_File'] = meta_attr_obj.get_class_source()
                class_meta[class_ind] = class_info
                class_info = {}

            interface_ind = 0
            for meta_attr_obj in proj.get_interface_meta_attr():
                interface_ind += 1
                interface_info['Interface_Name'] = meta_attr_obj.get_interface_name()
                interface_info['Interface_Specifier'] = meta_attr_obj.get_interface_specifier()
                interface_info['Interface_Signature'] = meta_attr_obj.get_interface_signature()
                interface_info['Interface_LOC'] = meta_attr_obj.get_interface_loc()
                interface_info['Interface_Line_No'] = meta_attr_obj.get_interface_line_no()
                interface_info['Interface_Source_File'] = meta_attr_obj.get_interface_source()
                interface_meta[interface_ind] = interface_info
                interface_info = {}

            method_ind = 0
            for meta_attr_obj in proj.get_method_meta_attr():
                method_ind += 1
                method_info['Method_Name'] = meta_attr_obj.get_method_name()
                method_info['Method_Type'] = meta_attr_obj.get_method_type()
                method_info['Method_Specifier'] = meta_attr_obj.get_method_specifier()
                method_info['Method_Signature'] = meta_attr_obj.get_method_signature()
                method_info['Method_Category'] = meta_attr_obj.get_method_category()
                method_info['Method_LOC'] = meta_attr_obj.get_method_loc()
                method_info['Method_Line_No'] = meta_attr_obj.get_method_line_no()
                method_info['Method_Source_File'] = meta_attr_obj.get_method_source()
                method_meta[method_ind] = method_info
                method_info = {}

            static_block_ind = 0
            for meta_attr_obj in proj.get_static_block_meta_attr():
                static_block_ind += 1
                static_block_info['Static_Block_LOC'] = meta_attr_obj.get_static_block_loc()
                static_block_info['Static_Block_Line_No'] = meta_attr_obj.get_static_block_line_no()
                static_block_info['Static_Block_Source_File'] = meta_attr_obj.get_static_block_source()
                static_block_meta[static_block_ind] = static_block_info
                static_block_info = {}

            for cmnt in proj.get_comments_with_attr():
                comment_ind += 1
                comment_info['Comment_Content'] = cmnt.get_comment_text()
                comment_info['Comment_Line_No'] = cmnt.get_comment_line_no()
                comment_info['Comment_Source_File'] = cmnt.get_comment_file_name()
                comment_info['Comment_Parent_Identifier'] = cmnt.get_comment_parent_identifier()
                comment_info['Comment_Parent_Trace'] = cmnt.get_comment_trace()
                comment_info['Comment_Immediate_Succeeding_Code'] = cmnt.get_succeeding_code()
                comment_info['Comment_Immediate_Preceding_Code'] = cmnt.get_preceding_code()
                comment_info['Comment_Preceding_Node'] = cmnt.get_preceding_node()
                comment_info['Comment_Succeeding_Node'] = cmnt.get_succeeding_node()
                comment_info['Comment_First_Element_In'] = cmnt.get_first_element_in()
                comment_info['Comment_Last_Element_In'] = cmnt.get_last_element_in()
                comment_info['Comment_Assoc_Block_Node'] = cmnt.get_comment_assoc_block_ele()
                comment_info['Comment_Level'] = cmnt.get_comment_level()
                comment_info['Comment_Type'] = cmnt.get_comment_type()
                comment_info['Comment_Category'] = cmnt.get_comment_category()
                comment_info['Comment_SubCategory'] = cmnt.get_comment_sub_category()
                comment_info['Comment_SubCatg_Type'] = cmnt.get_comment_sub_catg_type()
                comments[comment_ind] = comment_info
                comment_info = {}
        proj_attr_and_comprehensive_comments_info['Project_Meta'] = project_meta
        proj_attr_and_comprehensive_comments_info['Package_Meta'] = package_meta
        proj_attr_and_comprehensive_comments_info['Class_Meta'] = class_meta
        proj_attr_and_comprehensive_comments_info['Interface_Meta'] = interface_meta
        proj_attr_and_comprehensive_comments_info['Method_Meta'] = method_meta
        proj_attr_and_comprehensive_comments_info['StaticBlock_Meta'] = static_block_meta
        proj_attr_and_comprehensive_comments_info['Comments'] = comments

        SerializeSoCCMiner.write_json_file(SerializeSoCCMiner.proj_and_comment_attr_json, proj_attr_and_comprehensive_comments_info)

    @staticmethod
    def serialize_proj_attr(projects: list):
        project_meta = {}
        package_info = {}
        class_info = {}
        method_info = {}
        interface_info = {}
        static_block_info = {}
        package_meta = {}
        class_meta = {}
        interface_meta = {}
        method_meta = {}
        static_block_meta = {}
        proj_attr = {}
        for proj in projects:
            project_meta['Project_Name'] = proj.get_project_name()
            project_meta['Project_KLOC'] = proj.get_project_loc()
            project_meta['Project_Src_File_Count'] = proj.get_source_file_count()
            project_meta['Project_Package_Count'] = proj.get_package_count()
            project_meta['Project_Class_Count'] = proj.get_class_count()
            project_meta['Project_Method_Count'] = proj.get_method_count()
            project_meta['Project_Interface_Count'] = proj.get_interface_count()
            project_meta['Project_Static_Block_Count'] = proj.get_static_block_count()
            package_ind = 0
            for meta_attr_obj in proj.get_package_meta_attr():
                package_ind += 1
                package_info['Package_Name'] = meta_attr_obj.get_package_name()
                package_info['Package_LOC'] = meta_attr_obj.get_package_loc()
                package_info['Package_Line_No'] = meta_attr_obj.get_package_line_no()
                package_info['Package_Source_File'] = meta_attr_obj.get_package_source()
                package_meta[package_ind] = package_info
                package_info = {}

            class_ind = 0
            for meta_attr_obj in proj.get_class_meta_attr():
                class_ind += 1
                class_info['Class_Name'] = meta_attr_obj.get_class_name()
                class_info['Class_Type'] = meta_attr_obj.get_class_type()
                class_info['Class_Specifier'] = meta_attr_obj.get_class_specifier()
                class_info['Class_Nested_Level'] = meta_attr_obj.get_nested_level()
                class_info['Class_Signature'] = meta_attr_obj.get_class_signature()
                class_info['Class_LOC'] = meta_attr_obj.get_class_loc()
                class_info['Class_Line_No'] = meta_attr_obj.get_class_line_no()
                class_info['Class_Source_File'] = meta_attr_obj.get_class_source()
                class_meta[class_ind] = class_info
                class_info = {}

            interface_ind = 0
            for meta_attr_obj in proj.get_interface_meta_attr():
                interface_ind += 1
                interface_info['Interface_Name'] = meta_attr_obj.get_interface_name()
                interface_info['Interface_Specifier'] = meta_attr_obj.get_interface_specifier()
                interface_info['Interface_Signature'] = meta_attr_obj.get_interface_signature()
                interface_info['Interface_LOC'] = meta_attr_obj.get_interface_loc()
                interface_info['Interface_Line_No'] = meta_attr_obj.get_interface_line_no()
                interface_info['Interface_Source_File'] = meta_attr_obj.get_interface_source()
                interface_meta[interface_ind] = interface_info
                interface_info = {}

            method_ind = 0
            for meta_attr_obj in proj.get_method_meta_attr():
                method_ind += 1
                method_info['Method_Name'] = meta_attr_obj.get_method_name()
                method_info['Method_Type'] = meta_attr_obj.get_method_type()
                method_info['Method_Specifier'] = meta_attr_obj.get_method_specifier()
                method_info['Method_Signature'] = meta_attr_obj.get_method_signature()
                method_info['Method_Category'] = meta_attr_obj.get_method_category()
                method_info['Method_LOC'] = meta_attr_obj.get_method_loc()
                method_info['Method_Line_No'] = meta_attr_obj.get_method_line_no()
                method_info['Method_Source_File'] = meta_attr_obj.get_method_source()
                method_meta[method_ind] = method_info
                method_info = {}

            static_block_ind = 0
            for meta_attr_obj in proj.get_static_block_meta_attr():
                static_block_ind += 1
                static_block_info['Static_Block_LOC'] = meta_attr_obj.get_static_block_loc()
                static_block_info['Static_Block_Line_No'] = meta_attr_obj.get_static_block_line_no()
                static_block_info['Static_Block_Source_File'] = meta_attr_obj.get_static_block_source()
                static_block_meta[static_block_ind] = static_block_info
                static_block_info = {}

        proj_attr['Project_Meta'] = project_meta
        proj_attr['Package_Meta'] = package_meta
        proj_attr['Class_Meta'] = class_meta
        proj_attr['Interface_Meta'] = interface_meta
        proj_attr['Method_Meta'] = method_meta
        proj_attr['StaticBlock_Meta'] = static_block_meta
        SerializeSoCCMiner.write_json_file(SerializeSoCCMiner.java_proj_attr_json, proj_attr)

