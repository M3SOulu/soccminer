from soccminer import CommentsMiner


def demo(cm):    
    # Loads ComprehensiveCommentsAttribute object for mining level 'comprehensive_comment' that contains
    # comprehensive comment attributes for all the entities.
    for proj in cm.fetch_mined_comment_attributes(): #mined_proj_obj_list
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
        print("total comprehensive comments: {}".format(len(proj.get_comprehensive_file_comment_attr())))
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

            # Similarly other entity level comprehensive comments can be mined using
            # proj.get_comprehensive_class_comment_attr()  for class level
            # proj.get_comprehensive_method_comment_attr()  for method level
            # proj.get_comprehensive_interface_comment_attr()  for interface level
            # proj.get_comprehensive_static_block_comment_attr()  for static block level


############# Main #############	
# for mining source code
# input directory contains Java repository/ies
mining_obj = CommentsMiner(source_url='/home/murali/Downloads/pysoccer_test_data/microsoft_appcenter-sampleapp-android/', m_level='comprehensive_comment')
demo(mining_obj)

# for loading already mined entites (i.e., passive loading) the input 
# here is the SoCCMiner_Mined_Entities directory created by SoCCMiner while mining the source code.
# By default, it will be in the current working directory during execution.
# For example, if the script is executed at /usr/desktop/soccminer/ then SoCCMiner_Mined_Entities dir
# will be available at /usr/desktop/soccminer/SoCCMiner_Mined_Entities
# NOTE: Need not mine the entire project repo everytime to load the data pipelines. Repos can be mined in one location, zipped and transfered to another location
# then, the input dir must point to the unzipped directory containing mined_entities of projects.
load_obj = CommentsMiner(source_url='/home/murali/PycharmProjects/soccminer/SoCCMiner_Mined_Entities/microsoft_appcenter-sampleapp-android/', m_level='comprehensive_comment', direct_load=True)
demo(load_obj)
