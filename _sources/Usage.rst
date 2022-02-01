**Usage**
=====================

SoCCMiner's commandline usage can be used for quick ad-hoc source code mining and it can also be used in API calls for use in conjunction with other programs or applications.


Commandline Usage
-----------------
SoCCMiner expects project repositories as input, i.e, it expects an input directory location that contains only project folders, if there are non-project folders they will be treated as project folders and SoCCMiner will attempt to mine source code files. SoCCMiner can mine multiple project repositories at once through the **"multiple"** mode option.

Mining
^^^^^^

The input url for mining can be either github repository url or the local directory containing project repository/ies. Note that mining the project directory loads the project for immediate use without having to invoke a separate call for loading. Or the serialized mining data can be loaded separately in other programs/applications.  SoCCMiner supports loading of the mined data as a separate functionality as well. The mining will create a directory **"SoccMiner_Mined_Entities"** that contains the granular attributes and comments in individual directories. By default, this directory will be available in the current directory of SoCCMiner program. The following command mines the project microsoft_appcenter-sampleapp-android for basic comment attributes.
  
.. code-block:: python

   python3 bin/main.py -i https://github.com/microsoft/appcenter-sampleapp-android -lvl comment

If multiple project repositores are to be mined, then the input should be '/home/user/repositories_to_be_mined' directory containing all the project repositories to be mined.

.. code-block:: python

   python3 bin/main.py -i /home/user/repositories_to_be_mined/ -lvl comment -mode multiple
  
The mined output can be stored in a particular location using the **"output"** option. The above usage will store the SoCCMiner_Mined_Entities in the current directory of the soccminer program. To change this to another directory, output option can be used (output='/home/user/another_directory_to_store_soccminer_mined_entities/') while mining.

.. code-block:: python

  python3 bin/main.py -i /home/user/repositories_to_be_mined/ -lvl comment -mode multiple -output /home/user/output_location_to_store_soccminer_mining_output/
  
The **"lvl"** (mining level) input option should be changed for mining the project repository/directory with other pipelines. The available mining level are **"comment"** for mining comments from a project repository, **"comprehensive_comment"** for mining comprehensive comment attributes, **"project"** for mining granular meta attributes such as name, line number, signature, etc., and source code metrics such as granular (package/class/method/enum/interface/static_block) LOC, class nested level etc., and **"all"** for mining all the attributes from the previous options.

Loading
^^^^^^^

The serialized data from the mining can be loaded using the **"dl"** (direct loading) option. The following command loads the microsoft_appcenter-sampleapp-android project's data that has been mined for basic comments. **Note:** *It is important to use the same mining level with which the project has been serialized else, SoCCMiner will throw an error.* Here, the project has been mined at **"comment"** level and the same has been used for loading.

.. code-block:: python

  python3 bin/main.py -dl True -i /home/user/soccminer/SoCCMiner_Mined_Entities/microsoft_appcenter-sampleapp-android -lvl comment

Notice that when **"dl"** option is set to ``True`` the input path contains the SoCCMiner generated output (i.e., the mined data in JSON format). Consider the following example, which loads the serialized data that has been mined at **"comprehensive_comment"** level.
  
.. code-block:: python

  python3 bin/main.py -dl True -i /home/user/soccminer/SoCCMiner_Mined_Entities/microsoft_appcenter-sampleapp-android -lvl comprehensive_comment 


API
---

Mining
^^^^^^

For mining basic comment attributes of the microsoft_appcenter-sampleapp-android project repository stored in the local directory, instantiate CommentsMiner as the following:

.. code-block:: python
   
  from soccminer import CommentsMiner

  cm = CommentsMiner(source_url='/home/user/repositories_to_be_mined/microsoft_appcenter-sampleapp-android', m_level='comment')

Similar to commandline usage, the **"m_level"** (mining level) should be changed to mine the project directory/repository with the respective option from the available (**"comment"**, **"comprehensive_comment"**, **"project"**, **"all"**).
  
For other attributes of CommentsMiner, refer CommentsMiner section.


Loading
^^^^^^^

The mined attributes can be loaded for use in other applications/programs by setting the **"direct_load"** option as ``True`` and by using the appropriate mining level option with which the project directory/repository was mined.

.. code-block:: python
   
  from soccminer import CommentsMiner

  cm = CommentsMiner(source_url='/home/user/soccminer/SoCCMiner_Mined_Entities/microsoft_appcenter-sampleapp-android/', m_level='comment', direct_load=True)

Notice to change the the **"source_url"** option with the path that contains the mined data. If there are multiple project directories at the **"source_url"** path, all of them will be loaded for use in other programs/applications. 
