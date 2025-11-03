import json, sys, logging
from pathlib import Path
from pkg import file_finder, file_mover, cloud_uploader
logging.basicConfig(filename="log.txt", filemode='w', level=logging.DEBUG, format=' %(asctime)s -  %(levelname)s -  %(message)s')

def main():
    mode = mode_selection()
    settings = setup()
    source_path: str = Path(settings['source_filepath'])
    target_path: str = Path(settings['destination_filepath'])
    confirmation: bool = settings['enable_confirmation_dialogue']
    # TODO file extension filter setting for cloud upload

    if mode == 'arc': #running phorger archive
        print('Launching phorger in archival mode \n')
        try:
            file_list, size = file_finder(source_path)
            logging.debug(f'return list file finder {file_list}')
            file_mover(file_list, target_path, size, confirmation)
        except Exception as err:
            print(f'ERROR:{err}')
            sys.exit(1)
    elif mode == 'cld': #running phorger cloud 
        print('launching phorger in cloud mode')
        try:
            file_list, size = file_finder(source_path)
            cloud_uploader(file_list)
        except Exception as err:
            print(f'ERROR:{err}')
            sys.exit(1)

def setup():
    # """
    # loading and validating the settings.json file
    # """
    try:
        with open('settings.json', mode='r', encoding='UTF-8') as setting_file: #opening settings file
            settings: dict = json.load(setting_file) #serializing json file into python readable format
    except (FileNotFoundError, UnboundLocalError):    
        print('ERROR: settings file not found or corrupt')
        sys.exit(1)

    if Path(settings['source_filepath']) == Path(settings['destination_filepath']): #checking for identical paths
        print('ERROR: Source and Destination Path cant be the same, check settings')
        sys.exit(1)
    if settings['enable_logging'] == False:
        logging.disable(logging.CRITICAL)
    logging.debug('Start of program')
    logging.debug(f'settings successfully loaded: {settings}')
    return settings

def mode_selection():
    # """
    # checking the arguments given from the command line and setting phorger to the correct mode
    # only "phorger arc", "phorcer cld" and "phorger" are valid input
    # """
    if len(sys.argv) == 2 and (sys.argv[1] == 'arc' or sys.argv[1] == 'cld'): #checks for single and correct argument
        mode = sys.argv[1]
    elif len(sys.argv) == 1: #when no argument ist given, run default mode: archive
        mode = 'arc'
    else:
        print('ERROR: invalid command')
        sys.exit(1)
    return mode



if __name__ == "__main__":
    main()


