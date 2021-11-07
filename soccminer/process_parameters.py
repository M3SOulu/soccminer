from soccminer.environment import Platform
import logging
import os


class ProcessParameter:
    config_file = None
    miner_params = {}

    @staticmethod
    def fetch_program_parameters():
        try:
            cfg_file_loc = None
            temp_dir_loc = None
            if Platform.is_unix_platform():
                temp_dir_loc = os.getcwd() + '/'
            elif Platform.is_windows_platform():
                temp_dir_loc = os.getcwd() + '\\'
            cfg_file_loc = temp_dir_loc + 'soccminer.cfg'  # current working dir/miner.cfg default location for cfg file
            if cfg_file_loc is not None:
                if os.path.exists(cfg_file_loc):
                    line_no = 0
                    fh = open(cfg_file_loc, 'r', encoding='utf-8')
                    while True:
                        line_no += 1
                        param = fh.readline()
                        if line_no == 1:
                            ProcessParameter.miner_params['proj_url'] = param.strip()
                        elif line_no == 2:
                            ProcessParameter.miner_params['lang'] = param.strip()
                        elif line_no == 3:
                            ProcessParameter.miner_params['mining_level'] = int(param.strip())
                        elif line_no == 4:
                            ProcessParameter.miner_params['load_project'] = param.strip()
                        elif line_no == 5:
                            ProcessParameter.miner_params['log'] = int(param.strip())
                        elif not param:
                            break
                        else:
                            break
                    return ProcessParameter.miner_params
                else:
                    logging.error("Unexpected Error. Config file does not exist at the loc {}".format(cfg_file_loc))
                    raise
            else:
                logging.error(
                    "Unexpected Error. Config file param is None".format(cfg_file_loc))
                raise
        except Exception as e:
            logging.error("Unexpected error while fetching program parameters")
            raise



