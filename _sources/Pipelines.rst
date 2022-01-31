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

This pipeline mines the programming language construct attributes that constitutes a project. This is programming language specific. It mines a total of 30 attributes for all programming language constructs of a Java project including Package, File, Class, Interface, Method, Enumerator and, Static Block. The attributes typically include name, type ('REGULAR' or 'DERIVED'), LOC (Lines of Code), signature, etc.,

.. figure:: _static/project_attributes.png
   :scale: 55 %

   **A snapshot JavaMetaAttribute pipeline JSONs merged together for illustration**

JavaMiner
---------

This pipeline combines ComprehensiveCommentsAttribute and JavaMetaAttribute. It mines a total of 47 attributes.

