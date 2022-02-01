**Pipelines**
=============


CommentsMetaAttribute Pipeline
------------------------------

This pipeline mines basic comment information such as comment content, the line number in the source file where it is located and the name of the source file.

.. figure:: _static/comment_attributes.png
   :scale: 75 %

   **A snapshot of CommentsMetaAttribute pipeline's JSON**

ComprehensiveCommentsAttribute
------------------------------

This pipeline offers 17 contextual information for a source code comment. It includes all three attributes from the previous CommentsMetaAttribute pipeline along with: 

      *    **Comment_Assoc_Block_Node:** Refers to the node of source code that spans a pair of curly braces Could be a conditional/loop/control/etc., block of statements. 
      *    **Comment_Category:** Indicates if a comment is either 'HEADER' or 'NON_HEADER' comment. 
      *    **Comment_Content:** Refers to the content of the comment.
      *    **Comment_First_Element_In:** Indicates if the comment is located at the beginning i.e., immediately follows an opening curly brace'{'. For example, a comment may immediately follow a conditional/control/loop/other construct such as class/method/interface, etc., This is either True/False.
      *    **Comment_Last_Element_In:** Indicates if the comment is located near the closure of a conditional/control/loop/other construct such as class/method/interface, etc., i.e., located just before a closing curly brace '}'. This is either True/False.
      *    **Comment_Immediate_Preceding_Source_Code:** Refers to the actual source code block which immediately precedes a source code comment.
      *    **Comment_Immediate_Succeeding_Source_Code:** Refers to the source code that follows a source code comment. 
      *    **Comment_Level:** Refers to the granular level of a comment, i.e., if a comment belongs to Package/File/Class/Interface/Method/Enumerator/Static Block level comment. 
      *    **Comment_Line_No:** Refers to the line number at which comment can be located in the source file.
      *    **Comment_Parent_Identifier:** Refers to the identifier of a comment with the programming language constructs' name such as Package/Class/Interface/Method/Enumerator name in the same hierarchy of its occurence. For example, package_name.class_name.method_signature if a comment is located in a method that belongs to a class which is part of a package.
      *    **Comment_Parent_Trace:** Refers to the statement block that actually contains the comment in a file. This can be thought of as a relative location of a comment in a source file. When combined with Comment_Parent_Identifier, it refers to the absolute location of a comment in a file. If a comment is present just inside a method outside all statements inside a construct (class/method/interface, etc.,), the comment parent trace remains blank (null) indicating it is present inside the parent identifier.
      *    **Comment_Preceding_Node:** Refers to the type of the statement block that is located just before a comment.
      *    **Comment_Succeedng_Node:** Refers to the type of the statement block that is located just after a comment.
      *    **Comment_Source_File:** Refers to the name of the source code file.
      *    **Comment_SubCategory:** Indicates if a comment belongs to either  'BLOCK_LEVEL' or 'NON_BLOCK_LEVEL', i.e., if a comment is located within a block of statements inside '{}' curly braces. This is applicable only for 'NON_HEADER' category comments. The objective of this attribute is to identify if a header type of comment is embedded in another construct which will reveal the nested nature of a NON_HEADER comment.
      *    **Comment_SubCatg_Type:** Indicates the statement block type of the Comment_SubCategory. This can be either 'CONTROL', or 'EXCEPTION', or 'DECLARATION', or 'EXPRESSION', or 'CONSTRUCT_ENTITY' (i.e. programming language constructs such as Class, Method, Interface, etc.,), or 'OTHERS'.
      *    **Comment_Type:** Indicates the type of comment either 'BLOCK' comment or 'LINE' comment.

.. figure:: _static/compre_comment_attributes.png
   :scale: 75 %

   **A snapshot ComprehensiveCommentsAttribute pipeline's JSON**

JavaMetaAttribute
-----------------

This pipeline mines the granular attributes of a project. Typically, this is programming language specific i.e., for every programming language the granularities (programming language constructs) will differ. At present, SoCCMiner supports only Java programming language, hence the granular attributes of Java project are mined through this JavaMetaAttribute pipeline. It mines a total of 30 attributes from Java project granularities including Package, File, Class, Interface, Method, Enumerator and, Static Block attributes. The attributes mined in this pipeline enable a unique feature that srcML cannot do. It enables calculating granularity level comments such as method, or class or interface, etc., along with the source code association with code comments. Further, these serve as the core granular identifier attributes that can be coupled with a host of other source code metrics from well established third party tools. Such holistic data enable SATD or Sentiment comments correlation study with the source code constructs (i.e., granularties of a project).

**Package Attributes**
^^^^^^^^^^^^^^^^^^^^^^
Package attributes 4 attributes mined for each package in a project.

.. figure:: _static/package_attributes.png
   :scale: 55 %
        
*    **Package_Name:** Refers to the name of the package that has been mined.
*    **Package_LOC:** Refers to the LOC resulting from the sum of all the source files in the package that has been mined.
*    **Package_Source_File:** Refers to the name of the source file/s that are part of the package.
*    **Package_Line_No:** Indicates the specific line number in the source file/s containing the package statement.


**File attributes**
^^^^^^^^^^^^^^^^^^^
File attributes include 3 attributes mined for each source file, (i.e., .java file) in the project.

.. figure:: _static/file_attributes.png
   :scale: 55 %
        
*    **Source_File:** Refers to the name of the source code file.
*    **File_LOC:** Refers to the LOC the source code file that has been mined.
*    **File_Comments_Count:** Indicates the total number of code comments that are present in the source code file.



**Class Attributes**
^^^^^^^^^^^^^^^^^^^^
There are 8 attributes mined for each class present in the project. Of the 8 attributes, 4 are meta attributes (Name, Signature, Line_No, and Source_File) and 4 are source code metrics (LOC, Nested_Level, Specifier and Type).

.. figure:: _static/class_attributes.png
   :scale: 55 %
        
*    **Class_Name:** Refers to the name of the class that has been mined.
*    **Class_LOC:** Refers to the LOC of the class.
*    **Class_Source_File:** Refers to the name of the source file in which the class is located.
*    **Class_Line_No:** Indicates the specific line number in the source file containing the class.
*    **Class_Signature:** Refers to the signature of the class including the specifier and the deriving/implementation clause if any. This class signature will be unique in the source file. Can be used as an unique identifier in the project when combined along with the source_file attribute.
*    **Class_Nested_Level:** Refers to the nested level of the class. *'0'* refers base class and subsequent increase by a factor of 1 reflects the nesting level of the class that has been mined.
*    **Class_Specifier:** Refers to the access specifier of the mined class. If no specifier exists, it returns *'NO_SPECIFIER'*.
*    **Class_Type:** Indicates the type of the class if *'REGULAR'(BASE)*, *'ANONYMOUS'*, *'DERIVED'* or *'GENERIC'* .


**Enum Attributes**
^^^^^^^^^^^^^^^^^^^^^^
These include 4 attributes mined for each enum in the project.

.. figure:: _static/enum_attributes.png
   :scale: 55 %
        
*    **Enum_Name:** Refers to the name of the enum that has been mined.
*    **Enum_LOC:** Refers to the LOC of the enum construct.
*    **Enum_Source_File:** Refers to the name of the source file in which enum is located.
*    **Enum_Line_No:** Indicates the specific line number in the source file containing the enum.
*    **Enum_Signature:** Refers to the signature of the enum, similar to class, this attribute can be used as an unique identifier for an enum when combined with source_file attribute.
*    **Enum_Specifier:** Refers to the access specifier of the mined enum construct. If no specifier exists, it returns *'NO_SPECIFIER'*.


**Interface Attributes**
^^^^^^^^^^^^^^^^^^^^^^^^
These include 6 attributes mined for each interface in the project.

.. figure:: _static/interface_attributes.png
   :scale: 55 %
        
*    **Interface_Name:** Refers to the name of the interface that has been mined.
*    **Interface_LOC:** Refers to the LOC of the interface.
*    **Interface_Source_File:** Refers to the name of the source file in which the interface is located.
*    **Interface_Line_No:** Indicates the specific line number in the source file containing the interface.
*    **Interface_Signature:** Refers to the signature of the interface. Similar to the previous signature attribute, this can be used as an unique identifier in the project for an interface when combined along with the source_file attribute.
*    **Interface_Specifier:** Refers to the access specifier of the mined interface. If no specifier exists, it returns *'NO_SPECIFIER'*.


**Method Attributes**
^^^^^^^^^^^^^^^^^^^^^
There are 9 attributes mined for each method present in the project.

.. figure:: _static/method_attributes.png
   :scale: 55 %
        
*    **Method_Name:** Refers to the name of the method that has been mined.
*    **Method_LOC:** Refers to the LOC of the method.
*    **Method_Source_File:** Refers to the name of the source file in which the method is located.
*    **Method_Line_No:** Indicates the specific line number in the source file containing the method.
*    **Method_Signature:** Refers to the signature of the method that can be used as an unique identifier in a project. Such unique identifiers enable identifying the number of comments in a particular granularity, i.e, number of comments in a class or method, etc.,
*    **Method_Category:** Refers to the category of the method which can be either *'CONSTRUCTOR'* or *'FUNCTION'*.
*    **Method_Specifier:** Refers to the access specifier of the mined method. If no specifier exists, it returns *'NO_SPECIFIER'*.
*    **Method_Type:** Indicates the type of the method if *'REGULAR'*, or *'GENERIC'*.
*    **Method_Param_Count:** Indicates the parameter count of a method, if none exists 0.



**Static Block Attributes**
^^^^^^^^^^^^^^^^^^^^^^^^^^^
These include the 3 attributes mined for each static block present in the project. Typically, static blocks do not have name or signature, hence the line_no along with the source_file attribute can be combined for uniquely identifying a static block.

.. figure:: _static/static_block_attributes.png
   :scale: 55 %
        
*    **Static_Block_LOC:** Refers to the LOC of the static block.
*    **Static_Block_Source_File:** Refers to the name of the source file in which the static block is located.
*    **Static_Block_Line_No:** Indicates the specific line number in the source file containing the static block.



JavaMiner
---------

This pipeline combines ComprehensiveCommentsAttribute and JavaMetaAttribute. It mines a total of 47 attributes.

