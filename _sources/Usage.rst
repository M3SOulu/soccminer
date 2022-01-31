**Usage**
=====================

SoCCMiner's commandline usage can be used for quick ad-hoc source code mining and it can also be used in API calls for use in conjunction with other programs or applications.


Commandline Usage
-----------------
SoCCMiner expects project repositories as input, i.e, it expects an input directory location that contains project folders, if there are non-project folders they will be treated as project folders and will attempt to mine source code files. SoCCMiner can mine multiple project repositories at once through the "multiple" mode option.

CommentsMetaAttribute Pipeline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* **Mining:**
  Note that mining the project directory loads the project for immediate use or the serialized mining data can be loaded separately.  SoCCMiner supports loading of the mined data as a separate functionality also. The mining will create a directory "SoccMiner_Mined_Entities" that contains the granular attributes and comments in individual directories. By default, this directory will be available in the current directory of SoCCMiner program. The following command mines the project microsoft_appcenter-sampleapp-android for basic comments. 
  
.. code-block:: python

   python3 bin/main.py -i /home/user/repositories_to_be_mined/microsoft_appcenter-sampleapp-android -lvl comment

If multiple project repositores are to be mined, then the input should be '/home/user/repositories_to_be_mined' directory containing all the project repositories to be mined.

.. code-block:: python

   python3 bin/main.py -i /home/user/repositories_to_be_mined/ -lvl comment -mode multiple
  
The mined output can be stored in a particular location using the "output" option. The above usage will store the SoCCMiner_Mined_Entities in the current directory of the soccminer program. To change this to another directory, output option can be used (output='/home/user/another_directory_to_store_soccminer_mined_entities/') while mining.

.. code-block:: python

  python3 bin/main.py -i /home/user/repositories_to_be_mined/ -lvl comment -mode multiple -output /home/user/output_location_to_store_soccminer_mining_output/
  


* **Loading:**
  The serialized data from the mining can be loaded using the "dl" (direct loading) option. The following command loads the microsoft_appcenter-sampleapp-android project's data that has been mined for basic comments. **Note:** *It is important to use the same mining level with which the project has been serialized else, SoCCMiner will throw an error.* Here, the project has been mined at "comment" level and the same has been used for loading.

.. code-block:: python

  python3 bin/main.py -dl True -i /home/user/soccminer/SoCCMiner_Mined_Entities/microsoft_appcenter-sampleapp-android -lvl comment

    
  

ComprehensiveCommentsAttribute Pipeline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* **Mining:** For mining the comprehensive comments, the ComprehensiveCommentsAttribute pipeline is enable using the lvl (level) option. 

.. code-block:: python

  python3 bin/main.py -i /home/user/repositories_to_be_mined/microsoft_appcenter-sampleapp-android -lvl comprehensive_comment

* **Loading:** For loading,

.. code-block:: python

  python3 bin/main.py -dl True -i /home/user/soccminer/SoCCMiner_Mined_Entities/microsoft_appcenter-sampleapp-android -lvl comprehensive_comment


JavaMetaAttribute Pipeline
^^^^^^^^^^^^^^^^^^^^^^^^^^
* **Mining:** For mining the project meta attributes, the repository is mined at "project" level.

.. code-block:: python

   python3 bin/main.py -i /home/user/repositories_to_be_mined/microsoft_appcenter-sampleapp-android -lvl project

* **Loading:** For loading,

.. code-block:: python

  python3 bin/main.py -dl True -i /home/user/soccminer/SoCCMiner_Mined_Entities/microsoft_appcenter-sampleapp-android -lvl project


JavaMiner Pipeline
^^^^^^^^^^^^^^^^^^
* **Mining:** For mining all the attributes that were mined in the previous pipelines, the repository is mined at "all" level.

.. code-block:: python

  python3 bin/main.py -i /home/user/repositories_to_be_mined/microsoft_appcenter-sampleapp-android -lvl all

* **Loading:** For loading,

.. code-block:: python

  python3 bin/main.py -dl True -i /home/user/soccminer/SoCCMiner_Mined_Entities/microsoft_appcenter-sampleapp-android -lvl all


API
---

CommentsMetaAttribute Pipeline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* **Mining:** For mining basic comment attributes, instantiate CommentsMiner as the following:

.. code-block:: python

  cm = CommentsMiner(source_url='/home/user/repositories_to_be_mined/microsoft_appcenter-sampleapp-android', m_level='comment')

* **Loading:** For loading the mined data at "comment" level,

.. code-block:: python

  cm = CommentsMiner(source_url='/home/user/soccminer/SoCCMiner_Mined_Entities/microsoft_appcenter-sampleapp-android/', m_level='comment', direct_load=True)

ComprehensiveCommentsAttribute Pipeline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* **Mining:** For mining the comprehensive comments, the ComprehensiveCommentsAttribute pipeline is enable using the m_level (mining level) option. 

.. code-block:: python

  cm = CommentsMiner(source_url='/home/user/repositories_to_be_mined/microsoft_appcenter-sampleapp-android', m_level='comprehensive_comment')

* **Loading:** For loading,

.. code-block:: python

  cm = CommentsMiner(source_url='/home/user/soccminer/SoCCMiner_Mined_Entities/microsoft_appcenter-sampleapp-android/', m_level='comprehensive_comment', direct_load=True)


JavaMetaAttribute Pipeline
^^^^^^^^^^^^^^^^^^^^^^^^^^
* **Mining:** For mining the project meta attributes, the repository is mined at "project" level.

.. code-block:: python

  cm = CommentsMiner(source_url='/home/user/repositories_to_be_mined/microsoft_appcenter-sampleapp-android', m_level='project')

* **Loading:** For loading,

.. code-block:: python

  cm = CommentsMiner(source_url='/home/user/soccminer/SoCCMiner_Mined_Entities/microsoft_appcenter-sampleapp-android/', m_level='project', direct_load=True)


JavaMiner Pipeline
^^^^^^^^^^^^^^^^^^
* **Mining:** For mining all the attributes that were mined in the previous pipelines, the repository is mined at "all" level.

.. code-block:: python

  cm = CommentsMiner(source_url='/home/user/repositories_to_be_mined/microsoft_appcenter-sampleapp-android', m_level='all')

* **Loading:** For loading,

.. code-block:: python

  cm = CommentsMiner(source_url='/home/user/soccminer/SoCCMiner_Mined_Entities/microsoft_appcenter-sampleapp-android/', m_level='all', direct_load=True)

