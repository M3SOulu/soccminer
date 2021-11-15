from soccminer import CommentsMiner


def demo(cm):
    # Loads CommentsMetaAttribute object for mining level 'comment' that contains
    # basic comment info.
    for proj in cm.fetch_mined_comments():  # mined_proj_obj_list
        # fetch all comments basic info
        # get_comments() fetches all comments, i.e., for all the entities
        for basic_comment_attr_obj in proj.get_comments():
            print("Comment content: {}".format(basic_comment_attr_obj.comment_text))
            print("Comment line #: {}".format(basic_comment_attr_obj.comment_line_no))
            print("Comment source file: {}".format(basic_comment_attr_obj.file_name))

            # Similarly other entity level comments can be mined using
            # proj.get_file_level_comments()  for file level
            # proj.get_class_level_comments()  for class level
            # proj.get_enum_level_comments()  for enum level
            # proj.get_method_level_comments()  for method level
            # proj.get_interface_level_comments()  for interface level
            # proj.get_static_block_level_comments()  for static block level


############# Main #############	
# for mining source code
# input directory contains Java repository/ies
mining_obj = CommentsMiner(source_url='/home/murali/Downloads/pysoccer_test_data/microsoft_appcenter-sampleapp-android/', m_level='comment')
demo(mining_obj)

# for loading already mined entites (i.e., passive loading)
# here the SoCCMiner_Mined_Entities directory is created by the script while mining the source code
# by default, it will be in the current working directory during execution.
# For example, if the script is executed at /usr/desktop/soccminer/ then SoCCMiner_Mined_Entities dir
# will be available at /usr/desktop/soccminer/SoCCMiner_Mined_Entities
# NOTE: loading need not happen after mining. Repos can be mined in one location, zipped and transfered to another location
# then, the input dir must point to the unzipped directory containing mined_entities of projects.
load_obj = CommentsMiner(source_url='/home/murali/PycharmProjects/soccminer/SoCCMiner_Mined_Entities/microsoft_appcenter-sampleapp-android', m_level='comment', direct_load=True)
demo(load_obj)
