from soccminer import CommentsMiner


def demo(cm):
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
            print("Class Java Source File: {}".format(class_obj.class_source_file))

        # Similarly interface_obj attributes, enum_obj attributes, static_block and method
        # attributes can be used in the pipeline


############# Main #############	
# for mining source code
# input directory contains Java repository/ies
mining_obj = CommentsMiner(source_url='/home/murali/Downloads/pysoccer_test_data/microsoft_appcenter-sampleapp-android/', m_level='project')
demo(mining_obj)

# for loading already mined entites (i.e., passive loading) the input 
# here is the SoCCMiner_Mined_Entities directory created by SoCCMiner while mining the source code.
# By default, it will be in the current working directory during execution.
# For example, if the script is executed at /usr/desktop/soccminer/ then SoCCMiner_Mined_Entities dir
# will be available at /usr/desktop/soccminer/SoCCMiner_Mined_Entities
# NOTE: Need not mine the entire project repo everytime to load the data pipelines. Repos can be mined in one location, zipped and transfered to another location
# then, the input dir must point to the unzipped directory containing mined_entities of projects.
load_obj = CommentsMiner(source_url='/home/murali/PycharmProjects/soccminer/SoCCMiner_Mined_Entities/microsoft_appcenter-sampleapp-android/', m_level='project', direct_load=True)
demo(load_obj)

