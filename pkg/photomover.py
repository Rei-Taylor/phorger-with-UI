import shutil, os, sys, logging, time
from pathlib import Path
from tqdm import tqdm

logging.basicConfig(filename="log.txt", filemode='w', level=logging.DEBUG, format=' %(asctime)s -  %(levelname)s -  %(message)s')

def main(source_list: list,destination: Path, size: int, confrimation: bool):
    logging.debug(f'''   
        file mover initialized\n
        source list:\n{source_list}
        destination:\n{destination}         
    ''')
    
    path_validator(destination, size)
    files_to_move = duplicate_checker(source_list, destination)

    if confrimation == True: #confirmation dialogue before moving files
        while True:
            user_input = input('files ready for migrating, press y to confirm or exit:')
            if user_input == 'y':
                move_execution(files_to_move, destination)
                break
            elif user_input == 'exit':
                print('program cancelled, exiting...')
                sys.exit(0)
            else:
                print('invalid command, try again')
    else:
        move_execution(files_to_move, destination)

def path_validator(destination: Path, size: int):
    if not destination.is_dir(): #checking destination folder
        raise Exception('destination folder not found, check directory or settings')
    total, used, free = shutil.disk_usage(destination.anchor) #checking for available space on destination drive
    print(f'available space on destination drive {free / (1024 ** 3):.2f} GB')
    if free < size:
        raise Exception('not enough disk space, exiting')

    return print('destination valid, proceeding...')


def duplicate_checker(source_list: list, destination: Path) -> list:
    print('checking for duplicates...') #checking for existing folder in destination
    duplicates = [file for file in destination.iterdir() if file.name == file.name for file in source_list]
    logging.debug(f'duplicate list:\n{duplicates}')
    if duplicates:
        print('duplicate folder found at destination:')
        for duplicate_file in duplicates:
            print(duplicate_file.name)
        files_to_move = [file for file in source_list if file not in duplicates] #adjusting the source file list to exclude duplicates
        if not files_to_move:
            raise Exception('Files already exist at destination, exiting')
    else:
        print('no duplicates found, proceeding...')
        files_to_move = source_list

    logging.debug(f'files to move:\n{files_to_move}')
    return files_to_move


def move_execution(files_list: list, destination: Path): #actually moves the files
    files_moved = 0
    for file in files_list:
        print(f'moving {file.name}...')
        shutil.move(file, destination)
        files_moved += 1
    return print(f'successfully moved {files_moved} file(s)!')

# def move_file_with_progress(file, destination, chunk_size=1024*1024): 
#     total_size = os.path.getsize(file)
#     start_time = time.time()
#     moved_bytes = 0

#     with open(file, 'rb') as fsrc, open(destination, 'wb') as fdst, tqdm(
#         total=total_size,
#         unit='B',
#         unit_scale=True, 
#         unit_divisor=1024,
#         desc=f"Moving {os.path.basename(file)}",
#     ) as bar:
#         while True:
#             chunk = fsrc.read(chunk_size)
#             if not chunk:
#                 break
#             fdst.write(chunk)
#             moved_bytes += len(chunk)
#             elapsed = time.time() - start_time
#             speed = moved_bytes / elapsed if elapsed > 0 else 0
#             bar.set_postfix_str(f"{speed/1024/1024:.2f} MB/s")
#             bar.update(len(chunk))
#     os.remove(file)



if __name__ == "__main__":
    pass