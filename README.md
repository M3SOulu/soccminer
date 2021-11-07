# SoCC-Miner
Source Code-Comments Miner tool that mines raw source code for natural language with comprehensive contextual information and other source code attributes. It offers four different mining pipelines that can be fed to AI pipelines.

# Installation
Not mandatory but it is recommended to create a virtualenv.

$ virtualenv -p python3 <venv_name> \
$ source <venv_name>/bin/activate

Clone the repository
$ git clone https://github.com/M3SOulu/soccminer \
$ cd soccminer

Install the dependencies.
- srcML installation - Install the appropriate srcML client corresponding to your OS (Linux/Windows). https://www.srcml.org/#download
- soccminer dependencies - Install the soccminer dependencies. 

$ pip3 install -r requirements.txt

$ pip3 install soccminer

# Usage from commandline
Usage: python3 soccminer/bin/main.py '/usr/local/repositories_for_analysis/' 'java' 'comment' 'False' 'nolog'

positional arguments:
- inp          - Defines the input to the tool. Can be 'local_dir' containing project repositories as sub-directories or 'Git Repo URL'
		
- language      - The programming language of the project, for now only java project are handled by SoCCMiner

- mining_level  - Defines the mining/project entity loading level. Can be, 
  - 'comment' to mine/load basic comment info
  - 'comprehensive_comment' to mine/load comprehensive comment attributes
  - 'project' to mine/load project attributes)
  - 'all' (for project and comprehensive attributes) 
  - NOTE: While loading entities with load_project input argument set to True, SoCCMiner expects the same mining level with which the 
                    project was mined.
		   
- load_project  - If True, loads project entities from the mined entities directory containing the soccminer serialized json files.
                   If False, mines source code projects for comments, source code entities and their attributes according to the mining level input 
  
- log           - Defines the logging level. Can be one of nolog(NOLOG), info(INFO), debug(DEBUG)


# Usage from API
Refer scripts :
1. pysoccer_comments.py (for Comments Meta Attributes), 
2. pysoccer_comments_attr.py (for Comprehensive Comments Attributes), 
3. pysoccer_proj_attr.py (for Project Attributes) and 
4. pysoccer_proj_comments_attr.py (for both comprehensive comments and project attributes).
