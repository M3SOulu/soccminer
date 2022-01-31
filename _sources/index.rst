
SoCCMiner - Source Code Comments Miner
=======================================
.. image:: _static/soccminer_transparent.png
   :align: center
   :width: 300

============
SoCC-Miner
============

**SoCC-Miner** (Source Code-Comments Miner), a novel tool that extracts natural language, contextual source code fragments, source code construct level attributes from raw source code and offers different data pipelines for different use cases related with source code comments (for example: Source code Summarization, Program Comprehension, Automatic Comment scoping and generation). It is novel as in it can mine and extract entity level natural language text and contextual attributes. For example in Java project: package level, class level, interface level, method level, static block level source code comments and multiple associated attributes can be mined. Can be easily extended to mine other attributes or to create additional pipelines that can easily be integrated as data pipelines for AI networks. Currently, it supports only Java projects. It offers four different pipelines: 

- **CommentsMetaAttribute** - Contains basic comment attributes such as Comment Content, Comment Line Number in the source file and the name of the source file.
- **ComprehensiveCommentsAttribute** - Contains comprehensive contextual attributes pertaining to the comment such as the preceding and succeeding source code, type of comment, category of comment (i.e., header or non-header comment), comment level and other attributes.
- **JavaMetaAttribute** - Contains the attributes pertaining to the source code entities in the project. The programming language construct (such as package, class, method, etc.,) is referred to as entity.
- **JavaMiner** - Combines ComprehensiveCommentsAttribute and JavaMetaAttribute pipelines.
 


