# SoCC-Miner
Source Code-Comments Miner tool that mines raw source code for natural language with comprehensive contextual information and other source code attributes. It offers four different mining pipelines that can be fed to AI pipelines.

# Installation
Not mandatory but it is recommended to create a virtualenv.

$ virtualenv -p python3 <venv_name> \
$ source <venv_name>/bin/activate

Clone the repository \
$ git clone https://github.com/M3SOulu/soccminer \
$ cd soccminer

Install the dependencies.
- srcML installation - Install the appropriate srcML client corresponding to your OS (Linux/Windows). https://www.srcml.org/#download

- Installing soccminer will install the required dependencies and then the soccminer package. \
$ pip3 install soccminer

# Usage from commandline
Usage: python3 bin/main.py -i /usr/local/project_repository_for_analysis/ -lvl comment

Options:
- i      - (--input) Defines the input to the tool. (**Mandatory argument**) Can be 'local_dir' containing project repositories as sub-directories or 'Git Repo URL'.  
		
- l      - (--language) The programming language of the project, for now only java project is handled by SoCCMiner. By default, it is set to 'java'.

- lvl    - (--level) Defines the mining/project entity loading level. By default, it is set to 'comment'. Can be, 
  - 'comment' to mine/load basic comment info,
  - 'comprehensive_comment' to mine/load comprehensive comment attributes,
  - 'project' to mine/load project attributes),
  - 'all' (for project and comprehensive attributes) 
  - **NOTE:** While loading entities with direct_load input argument set to True, SoCCMiner expects the same mining level with which the 
                    project was mined.
		   
- dl      - (--direct_load) If True, loads project entities from the mined entities directory containing the soccminer serialized json files.
                   If False, mines source code projects for comments, source code entities and their attributes according to the mining level input and then loads projects entities into respective pipelines. By default, it is set to False. 
  
- log     - (--logging) Defines the logging level. Can be one of nolog(NOLOG), info(INFO), debug(DEBUG). By default, it is 'nolog'. For other options, the log file will be created in the current working directory.  
                **NOTE:** Enabling log creates very huge log file for huge source code repositories. **Recommended enabling only for debugging** as it creates huge log files. Enable it for debugging after ensuring enough disk space is available (atleast 5GB for large to very large repositories with source files greater than 25000 in a project repository).
- o       - Defines the output directory where the mined entities will be stored. By default, it is current working directory.
- m       - Defines SoCC-Miner execution mode, can be 'single' to mine single project directory (i.e., all files and directories within input directory will be treated as a single project), or 
            can be 'multiple' to mine multiple project directories in which all sub-directories within the input directory will be treated as separate project directories. 
            **NOTE:** For GitHub repository URLs, SoCC-Miner defaults to 'single' mode. SoCC-Miner expects an input directory that contains only project directory/ies as sub-directory/ies in 'multiple' mode.
# Usage from API
Refer scripts :
1. soccminer_comments.py (for Comments Meta Attributes), 
2. soccminer_comments_attr.py (for Comprehensive Comments Attributes), 
3. soccminer_proj_attr.py (for Project Attributes) and 
4. soccminer_proj_comments_attr.py (for both comprehensive comments and project attributes).

Before execution, do not forget to change the input directories for mining and loading.

**NOTE:** In demo scripts, loading immediately follows mining in reality it need not be the same. 
One can mine the repos in one location, zip and transfer to another location, then mined_entities are 
unzipped and the folder location is given as input to the loading_project call, then the loaded objects
serve as pipelines for AI applications.

$python3 soccminer_comments.py

Similarly other scripts can be executed.