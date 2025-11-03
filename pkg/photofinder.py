import os, re
from pathlib import Path

PATTERN = re.compile(r'(2\d{3})-(\d{2})-(\d{2})\s-\s.*') #compiling pattern object: "YYYY-MM-DD - Foldername"

def directory_validation(source: Path):
    # """
    # checks the existance of source directory and whether its empty
    # """
    if not source.is_dir():     
        raise Exception('source folder not found, check directory or settings')
    
    if not os.listdir(source): 
        raise Exception('source directory is empty')

def name_matching(source: Path) -> list:
    # """
    # finds all the matching folder names in the source directory
    # """
    #matching_list = [entry for entry in source.iterdir() if entry.is_dir() and PATTERN.search(entry.name)]
    matching_list = []
    for entry in source.iterdir():
        if entry.is_dir and PATTERN.search(entry.name):
            matching_list.append(entry)
    if not matching_list:
        raise Exception('No matching folder found!')
    return matching_list

def size_calculator(matching_list: list) -> int:
    # """
    # calculates the size of the files that are supposed to be moved
    # outputs size in bytes
    # """
    total_size = 0 
    for folder in matching_list:  #calculating total size of found files in GB
        total_size += sum(file.stat().st_size for file in folder.rglob('*') if file.is_file())
    return total_size

def files_for_upload():
    # TODO find the photos for the cloud uploader
    pass

def main(source: Path):
    
    directory_validation(source)
    matching_list = name_matching(source)

    print(f'following folders found in {str(source)}:\n')
    for entry in matching_list:
        print(f'{entry.name}')

    print('-' * 20)
    total_size = size_calculator(matching_list)
    print(f'\ntotal size: {(total_size  / (1024 ** 3)):.2f} GB')

    return matching_list, total_size #list of matching path objects, total size int (bytes)

if __name__ == "__main__":
    pass