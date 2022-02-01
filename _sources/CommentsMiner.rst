**CommentsMiner**
=================

The CommentsMiner is the core object of SoCCMiner that gets populated in all the pipelines. It has the following options,

      *    **source_url:** Refers to the github repository url or local directory location for mining. For loading, it always refers to the local directory containing the mined JSON data.
      *    **lang:** Refers to the programming language of the source code.  Default value is *'java'* now.
      *    **m_level:** Refers to the mining level, can be one of *'comment'*, *'comprehensive_comment'*, *'project'*, and *'all'*. Default value is *'comment'*.
      *    **direct_load:** Set to ``True`` for loading the already serialized data else ``False``. By default, it is set to ``False``.
      *    **log:** Used for debugging. It can be *'DEBUG'*, *'INFO'* or *'NOLOG'*. By default, log will not be generated. Must be set to either *'INFO'* for brief trace information or *'DEBUG'* for elaborate execution trace. The log file will be generated in the current working directory.
      *    **output_dir:** Used to set the local directory where the mined data should be serialized. By default, the serialized attributes will be available in the current working directory under the directory *'SoCCMiner_Mined_Entities'*.
      *    **mode:** Refers to the mode with which SoCCMiner mines the source code. It can be *'single'* that indicate the source_url contains only one project directory for mining or *'multiple'* to indicated the source_url contains multiple project repositories as subdirectories under the source_url. If this option is not set to *'multiple'* where there are multiple project repositories as sub-directories in the source_url, then SoCCMiner will treat all the projects as a single project.



CommentsMetaAttribute Pipeline
------------------------------
* **fetch_mined_comments():** This method fetches the mined projects at the basic "comment" level.
  
**Basic project attributes:** The basic project attributes of the mined projects can be retrieved as the following:

.. code-block:: python
   :linenos:   

   from soccminer import CommentsMiner

   cm = CommentsMiner(source_url='/home/user/soccminer/SoCCMiner_Mined_Entities/microsoft_appcenter-sampleapp-android/', m_level='comment', direct_load=True)

   for proj in cm.fetch_mined_comments():  # mined_proj_obj_list
       # fetch project meta info
       print("Project Name: {}".format(proj.proj_name))
       print("Project LOC: {}".format(proj.proj_loc))
       print("Project Source Code File count: {}".format(proj.source_file_count))


**Granular Comments:** The granular comments containing the three basic comment attributes comment content, line number at which the comment is located in the source file and the source file in the the comment is located.

.. code-block:: python
   :linenos:   

    for proj in cm.fetch_mined_comments():  # mined_proj_obj_list
        print("Entire project Comments count: {}".format(len(proj.get_comments())))  # for project level comments
        print("File Level Comments count: {}".format(len(proj.get_file_level_comments())))  # for file level comments
        print("Class Level Comments count: {}".format(len(proj.get_class_level_comments())))  # for class level comments
        print("Enum Level Comments count: {}".format(len(proj.get_enum_level_comments())))  # for enum level comments
        print("Method Level Comments count: {}".format(len(proj.get_method_level_comments())))  # for method level comments
        print("Interface Level Comments count: {}".format(len(proj.get_interface_level_comments())))  # for interface level comments
        print("Static Block Level Comments count: {}".format(len(proj.get_static_block_level_comments()))) # for static block level comments
    
**Basic Comment Attributes:** The three basic comment attributes of the CommentMetaAttributes pipeline can be fetched as:

.. code-block:: python
   :linenos:   

    for proj in cm.fetch_mined_comments():  # mined_proj_obj_list
        # fetch all comments basic info
        # get_comments() fetches all comments, i.e., for all the entities
        for basic_comment_attr_obj in proj.get_comments():
            print("Comment content: {}".format(basic_comment_attr_obj.comment_text))
            print("Comment line #: {}".format(basic_comment_attr_obj.comment_line_no))
            print("Comment source file: {}".format(basic_comment_attr_obj.file_name))


  

ComprehensiveCommentsAttribute Pipeline
---------------------------------------
* **fetch_mined_comment_attributes():** This method fetches the mined projects at the basic "comprehensive_comment" level.
  
**Basic project attributes:** The basic project attributes of the mined projects can be retrieved as the following:

.. code-block:: python
   :linenos:   

   from soccminer import CommentsMiner

   cm = CommentsMiner(source_url='/home/user/soccminer/SoCCMiner_Mined_Entities/microsoft_appcenter-sampleapp-android/', m_level='comprehensive_comment', direct_load=True)

    for proj in cm.fetch_mined_comment_attributes():  # mined_proj_obj_list
        # fetch project meta info
        print("Project Name: {}".format(proj.proj_name))
        print("Project LOC: {}".format(proj.proj_loc))
        print("Project Source Code File count: {}".format(proj.source_file_count))


**Granular Comments:** The granular comments containing the comprehensive comment attributes can be fetched as:

.. code-block:: python
   :linenos:   

    for proj in cm.fetch_mined_comment_attributes(): #mined_proj_obj_list
        print("Entire project level comprehensive comments: {}".format(len(proj.get_comprehensive_comment_attr())))
        print("File level comprehensive comments: {}".format(len(proj.get_comprehensive_file_comment_attr())))
        print("Class level comprehensive comments: {}".format(len(proj.get_comprehensive_class_comment_attr())))
        print("Method level comprehensive comments: {}".format(len(proj.get_comprehensive_method_comment_attr())))
        print("Interface level comprehensive comments: {}".format(len(proj.get_comprehensive_interface_comment_attr())))
        print("Enum level comprehensive comments: {}".format(len(proj.get_comprehensive_enum_comment_attr())))
        print("Static Block level comprehensive comments: {}".format(len(proj.get_comprehensive_static_block_comment_attr())))
    
**Comprehensive Comment Attributes:** The seventeen comprehensive comment attributes of the ComprehensiveCommentsAttribute pipeline can be fetched as:

.. code-block:: python
   :linenos:   

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




JavaMetaAttribute Pipeline
--------------------------
* **fetch_mined_project_meta():** This method fetches the mined projects metadata mined at the "project" level.
  
**Basic project attributes:** The basic project attributes of the mined projects can be retrieved as the following:

.. code-block:: python
   :linenos:   

    from soccminer import CommentsMiner

    cm = CommentsMiner(source_url='/home/user/soccminer/SoCCMiner_Mined_Entities/microsoft_appcenter-sampleapp-android/', m_level='project', direct_load=True)

    for proj in cm.fetch_mined_project_meta():
        # fetch project meta info
        print("Project Name: {}".format(proj.proj_name))
        print("Project LOC: {}".format(proj.proj_loc))
        print("Project Source Code File count: {}".format(proj.source_file_count))


   
**Project Meta Attributes:** The thirty project meta attributes of the JavaMetaAttribute pipeline can be fetched as:

.. code-block:: python
   :linenos:   

    for proj in cm.fetch_mined_project_meta():
        ############################################################
        # Java project meta attributes
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
        for interface_obj in proj.get_interface_meta_attr():
            print("Interface Name: {}".format(interface_obj.interface_name))
            print("Interface Specifier: {}".format(interface_obj.interface_specifier))
            print("Interface Line #: {}".format(interface_obj.interface_line_no))
            print("Interface Signature: {}".format(interface_obj.interface_signature))
            print("Interface LOC: {}".format(interface_obj.interface_loc))
            print("Interface Java Source File: {}".format(interface_obj.interface_source_file)) 
        for enum_obj in proj.get_enum_meta_attr():
            print("Enum Name: {}".format(enum_obj.enum_name))
            print("Enum Specifier: {}".format(enum_obj.enum_specifier))
            print("Enum Line #: {}".format(enum_obj.enum_line_no))
            print("Enum Signature: {}".format(enum_obj.enum_signature))
            print("Enum LOC: {}".format(enum_obj.enum_loc))
            print("Enum Java Source File: {}".format(enum_obj.enum_source_file))
        for method_obj in proj.get_method_meta_attr():
            print("Method Name: {}".format(method_obj.method_name))
            print("Method Type: {}".format(method_obj.method_type))
            print("Method Specifier: {}".format(method_obj.method_specifier))
            print("Method Line #: {}".format(method_obj.method_line_no))
            print("Method Nested Level: {}".format(method_obj.method_category))
            print("Method Signature: {}".format(method_obj.method_signature))
            print("Method LOC: {}".format(method_obj.method_loc))
            print("Method Parameter Count: {}".format(method_obj.method_param_count))
            print("Method Java Source File: {}".format(method_obj.method_source_file))
        for static_block_obj in proj.get_static_block_meta_attr():
            print("Static Block Line #: {}".format(static_block_obj.static_block_line_no))
            print("Static Block LOC: {}".format(static_block_obj.static_block_loc))
            print("Static Block Java Source File: {}".format(static_block_obj.static_block_source_file))


JavaMiner Pipeline
------------------

* **fetch_mined_project_meta_and_comments():** This method fetches the mined all the attributes mined at "all" mining level.
  
**Basic project attributes:** The basic project attributes of the mined projects can be retrieved as the following:

.. code-block:: python
   :linenos:   

   from soccminer import CommentsMiner

   cm = CommentsMiner(source_url='/home/user/soccminer/SoCCMiner_Mined_Entities/microsoft_appcenter-sampleapp-android/', m_level='all', direct_load=True)

   for proj in cm.fetch_mined_project_meta_and_comments():  # mined_proj_obj_list
       # fetch project meta info
       print("Project Name: {}".format(proj.proj_name))
       print("Project LOC: {}".format(proj.proj_loc))
       print("Project Source Code File count: {}".format(proj.source_file_count))


**Granular Comments:** All the attributes discussed in the previous mining levels are available in the "all" level. For example,

.. code-block:: python
   :linenos:   

    for proj in cm.fetch_mined_project_meta_and_comments(): #mined_proj_obj_list
        print("Method level comprehensive comments: {}".format(len(proj.get_comprehensive_method_comment_attr())))

    
**Project MetaAttributes:** All the project attributes of the JavaMetaAttribute pipeline can be retrieved, for example:

.. code-block:: python
   :linenos:   

    for proj in cm.fetch_mined_project_meta_and_comments():
        for package_obj in proj.get_package_meta_attr():
            print("Package Name: {}".format(package_obj.package_name))
            print("Package LOC: {}".format(package_obj.package_loc))
            print("Package Line #: {}".format(package_obj.package_line_no))
            print("Package Java Source File: {}".format(package_obj.source_file_name))




