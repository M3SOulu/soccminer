**About**
=========

.. figure:: _static/soccminer_stack.png
   :align: center
   :scale: 50 %

   **SoCCMiner Technology Stack**

SoCC-Miner (Source Code-Comments Miner), a novel tool accepts raw source code as input and outputs natural language and source code attributes as data pipelines. It mines raw source code and offers different data pipelines that can be used for multiple use cases related with source code comments (for example: Source code Summarization, Program Comprehension, Automatic Comment scoping, Comment Generation, Technical Debt Detection, etc.,). It is novel as in, it can mine and extract granular level natural language comments and its associated contextual attributes. Example, for Java project: package level, class level, interface level, method level, static block level comments and its associated attributes can be mined. This tool can be easily extended to mine other attributes or create additional pipelines that can be easily integrated as data pipelines for AI networks. Currently, it supports only Java projects. It offers four different pipelines for now:

1.   **CommentsMetaAttribute:** Contains basic comment attributes such as Comment Content, Comment Line Number in the source file and the name of the source file.
2.   **ComprehensiveCommentsAttribute:** Contains comprehensive contextual attributes pertaining to the comment such as the preceding and succeeding source code, type of comment, category of comment (i.e., header or non-header comment), comment level and other attributes.
3.  **JavaMetaAttribute:** Contains the attributes pertaining to the source code entities in the project. The programming language construct (such as package, class, method, etc.,) is referred to as entity.
4.  **JavaMiner:** Combines ComprehensiveCommentsAttribute and JavaMetaAttribute pipelines.
