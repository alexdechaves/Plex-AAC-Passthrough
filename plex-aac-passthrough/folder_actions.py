import os
import time
import logging
import threading
from torrentsort.torrent import TorrentAsset
import shutil


def config_folder(folder, subfolder):
    """
    Function to create watch folder structure if one is not present
    """
    if os.path.exists(folder):  # if folders exists, then do nothing
        if os.path.exists(os.path.join(folder, subfolder)):
            pass
        else:
            os.makedirs(os.path.join(folder, subfolder))
    else:  # create folders when they're not present
        try:
            os.makedirs(folder)
            os.makedirs(os.path.join(folder, subfolder))
        except RuntimeError:
            print("Error creating folders!")


def filter_out_index_file(path):
    """
    Removes DS_Store folder metadata file from a folder contents list on osx
    """
    stores = os.listdir(path)
    final = []
    for file in stores:
        if '.DS_Store' not in file:
            final.append(file)
    return final


def get_folder_size(folder):
    """
    Returns size of a folder
    Equivalent to os.path.getsize for folders
    """
    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += get_folder_size(itempath)
    return total_size


def find_files_with_ext(root):
    """
    Walks through any number of directories to filter out files that match extensions
    """
    contents = []
    patterns = ['.MXF', '.MOV', '.MP4', '.MTS', '.mxf', '.mov', '.mp4', '.mkv']
    for path, subdirs, files in os.walk(root):
        for name in files:
            for pattern in patterns:
                if name.endswith(pattern):
                    if not name.startswith('._'):
                        return os.path.join(path, name)


def get_copy_progress(src, dest):
    while get_folder_size(dest) != get_folder_size(src):
        return int(get_folder_size(dest)/get_folder_size(src) * 100)


def get_folder_names(torrent_folder, root_dir):
    asset = os.path.basename(torrent_folder)
    show_folder = os.path.join(root_dir, TorrentAsset(asset).get_show_name())
    season_folder = os.path.join(show_folder, 'S' + TorrentAsset(asset).get_season())
    config_folder(show_folder, season_folder)
    return asset, season_folder


def move_assets(torrent_folder, season_folder, asset):
    if not os.path.exists(os.path.join(season_folder, asset)):
        threading.Thread(target=lambda: shutil.copytree(torrent_folder, os.path.join(season_folder, asset))).start()
        time.sleep(1)
        threading.Thread(target=lambda: get_copy_progress(torrent_folder, os.path.join(season_folder, asset))).start()
    else:
        logging.error('Folder already exists!')