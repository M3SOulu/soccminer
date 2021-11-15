from soccminer import CommentsMiner


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

        # Similarly interface_obj attributes, enum_obj attributes, static_block and method
        # attributes can be used in the pipeline

        ############################################################
        # Comprehensive Comment at entity level, i.e., ComprehensiveCommentsAttribute objects

        # fetch all comprehensive comments
        for comprehensive_comments_obj in proj.get_comprehensive_comment_attr():
            print("Comment content: {}".format(comprehensive_comments_obj.comment_text))
            print("Comment line #: {}".format(comprehensive_comments_obj.comment_text))
            print("Comment source file: {}".format(comprehensive_comments_obj.comment_text))
            print("Comment preceding code statement type: {}".format(comprehensive_comments_obj.preceding_node))
            print("Comment preceding code: {}".format(comprehensive_comments_obj.preceding_code))
            print("Comment succeeding code statement type: {}".format(comprehensive_comments_obj.succeeding_node))
            print("Comment succeding code: {}".format(comprehensive_comments_obj.succeeding_code))
            print("Comment parent identifier: {}".format(comprehensive_comments_obj.comment_parent_identifier))
            print("Comment parent identifier trace: {}".format(comprehensive_comments_obj.comment_trace))
            print("Comment category: {}".format(comprehensive_comments_obj.comment_trace))
            print("Comment is a first statement in: {}".format(comprehensive_comments_obj.first_element_in))
            print("Comment is a last statement in: {}".format(comprehensive_comments_obj.last_element_in))
            print("Comment type: {}".format(comprehensive_comments_obj.comment_type))

        # fetch package level comprehensive comments
        for comprehensive_comments_obj in proj.get_comprehensive_package_comment_attr():
            print("Comment content: {}".format(comprehensive_comments_obj.comment_text))
            print("Comment line #: {}".format(comprehensive_comments_obj.comment_text))
            print("Comment source file: {}".format(comprehensive_comments_obj.comment_text))
            print("Comment preceding code statement type: {}".format(comprehensive_comments_obj.preceding_node))
            print("Comment preceding code: {}".format(comprehensive_comments_obj.preceding_code))
            print("Comment succeeding code statement type: {}".format(comprehensive_comments_obj.succeeding_node))
            print("Comment succeding code: {}".format(comprehensive_comments_obj.succeeding_code))
            print("Comment parent identifier: {}".format(comprehensive_comments_obj.comment_parent_identifier))
            print("Comment parent identifier trace: {}".format(comprehensive_comments_obj.comment_trace))
            print("Comment category: {}".format(comprehensive_comments_obj.comment_trace))
            print("Comment is a first statement in: {}".format(comprehensive_comments_obj.first_element_in))
            print("Comment is a last statement in: {}".format(comprehensive_comments_obj.last_element_in))
            print("Comment type: {}".format(comprehensive_comments_obj.comment_type))

            # Similarly other entity level comprehensive comments can be mined using
            # proj.get_comprehensive_class_comment_attr()  for class level
            # proj.get_comprehensive_method_comment_attr()  for method level
            # proj.get_comprehensive_interface_comment_attr()  for interface level
            # proj.get_comprehensive_static_block_comment_attr()  for static block level


############# Main #############	
# for mining source code
# input directory contains Java repository/ies
mining_obj = CommentsMiner(source_url='/home/murali/Downloads/pysoccer_test_data/microsoft_appcenter-sampleapp-android/', m_level='all')
demo(mining_obj)

# for loading already mined entites (i.e., passive loading)
# here the SoCCMiner_Mined_Entities directory is created by the script while mining the source code
# by default, it will be in the current working directory during execution.
# For example, if the script is executed at /usr/desktop/soccminer/ then SoCCMiner_Mined_Entities dir
# will be available at /usr/desktop/soccminer/SoCCMiner_Mined_Entities
# NOTE: loading need not happen after mining. Repos can be mined in one location, zipped and transfered to another location
# then, the input dir must point to the unzipped directory containing mined_entities of projects.

load_obj = CommentsMiner(source_url='/home/murali/PycharmProjects/soccminer/SoCCMiner_Mined_Entities/microsoft_appcenter-sampleapp-android/', m_level='all', direct_load=True)
demo(load_obj)

