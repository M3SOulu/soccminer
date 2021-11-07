from soccminer.java_project_meta_attributes import JavaMetaAttribute
from soccminer.proj_comments_main_attr import EntityLevelComprehensiveComment


class JavaMiner(JavaMetaAttribute, EntityLevelComprehensiveComment):
    def __init__(self, project_instance):
        super().__init__(project_instance)
        print("JavaMiner")
        print("----------")
        print("Package count: {}".format(self.package_count))
        print("Class count: {}".format(self.class_count))
        print("Method count: {}".format(self.method_count))
        print("Interface count: {}".format(self.interface_count))
        print("Static block count: {}".format(self.static_block_count))

