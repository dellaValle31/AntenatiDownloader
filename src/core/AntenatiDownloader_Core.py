import multiprocessing, functools, subprocess
import re, requests, os

from pathlib import Path
from enum import Enum
from PySide6.QtCore import QObject, Signal

multiprocessing.freeze_support()

# Global variables
GENERIC_FILENAME = 'Immagine'
GENERIC_EXTENSION = '.jpg'
COMMENT_MARK = '!'

class DL_TYPE(Enum):
    PARALLEL = 0
    SEQUENTIAL = 1

class GUI_TYPE(Enum):
    INIT = 0
    MANIFEST_OK = 1
    MANIFEST_KO = 2
    DIR_RESULT_OK = 3
    DIR_RESULT_KO = 4
    MANIFEST_DIR_OK = 5
    FREEZE_ALL = 6
    UNFREEZE_ALL = 7


def get_manifest_links(manifest):
    if os.path.isfile(manifest):
        # Open and read file, return manifest as list
        with open(manifest, 'r') as mf:
            raw = mf.readlines()
        return [r.strip() for r in raw if r[0] != COMMENT_MARK and r != "\n"]
    else:
        # Noting to do, return link
        return [manifest]


# Get canvases and link to file
def get_all_canvases(json_manifest):
    # Return variable
    all_imageMap = []

    for jmanifest in json_manifest:
        # Prepare dictionary
        imageMap = {}

        # Get all canvases, which define link to frames
        canvases = jmanifest['sequences'][0]['canvases']

        # For each canvas in canvases, get images
        for i, canvas in enumerate(canvases):
            # For each images in canvases, get resource, and build output dictionary
            for res in canvas['images']:
                try:
                    nPag = re.search(r"\d{1,4}", canvas['label'])
                    imageMap.update({nPag.group() : res['resource']['@id']})
                except Exception:
                    pass
        all_imageMap.append(imageMap)

    return all_imageMap


def download_iiif_file(url, page, folder, headers):
    # Download file
    r = requests.get(url, headers=headers)
    filename = os.sep.join([folder, GENERIC_FILENAME + '_' + page + GENERIC_EXTENSION])
    # Write file
    with open(filename, 'wb') as f:
        f.write(r.content)

    return r.status_code == requests.status_codes.codes.ALL_OK


def safe_create_folder(folder):
    Path(folder).mkdir(parents=True, exist_ok=True)
    return folder


def build_folders_name(proot, json_data):
    all_pathes = []
    # Build folder name as (for instance)
    # Archivio di Stato di Cosenza/Fiumefreddo/Stato civile napoleonico/1809-1809/Matrimoni/Registro 1
    for jdata in json_data:
        root_path = [x.strip() for x in jdata['metadata'][3]['value'].split('>')]
        root_path = os.sep.join([root_path[0], root_path[2]])

        sub1_path = re.sub(r"\s+", '', jdata['metadata'][2]['value']).strip()
        sub2_path = re.sub(r"[,]+", ' -', jdata['metadata'][1]['value']).strip()
        sub3_path = jdata['metadata'][0]['value'].strip()

        all_pathes.append(os.path.abspath(os.sep.join([proot, root_path, sub1_path, sub2_path, sub3_path])))
    return all_pathes

# Counts how many files are being downloaded
def get_download_status(folder):
    return sum([file.find(GENERIC_FILENAME) != -1 for file in os.listdir(folder)])

# Remove file in folder if necessary
def rm_file_in_folder(folder):
    for f in os.listdir(folder):
        os.remove(os.path.join(folder, f))

# Open results folder after download
def open_result_folder(folder):
    """Open results download folder"""
    subprocess.Popen(r'explorer /select, "{}"'.format(folder))


# Customized worker object for downloading process
class Worker_DL_Img(QObject):
    finished = Signal()
    results = Signal(list)

    def __init__(self, imageMap, folder, parallelism, headers):
        super().__init__()
        self.imageMap = imageMap
        self.folder = folder
        self.parallelism = parallelism
        self.headers = headers



    def run(self):
        # Launch downlader
        if not self.parallelism:
            dl_status = []
            for i, img in enumerate(self.imageMap):
                status = download_iiif_file(url=self.imageMap[img], folder=self.folder, page=img, headers=self.headers)
                dl_status.append(status)

        else:
            # Multithreaded downloader
            # Concatenate arguments
            arguments = [(url, page) for (page, url) in zip(self.imageMap.keys(), self.imageMap.values())]
            # Create partial function
            download_func = functools.partial(download_iiif_file, folder=self.folder, headers=self.headers)
            # Launch pool
            pool = multiprocessing.Pool(multiprocessing.cpu_count())
            dl_status = pool.starmap(download_func, arguments)
            pool.close()
            pool.join()

        self.results.emit(dl_status)
        self.finished.emit()


class Worker_DL_Manifest(QObject):
    finished = Signal()
    manifest_data = Signal(list)
    count = Signal(float)

    def __init__(self, link_manifest, headers):
        super().__init__()
        self.links = link_manifest
        self.headers = headers

    def run(self):
        raw_manifest = []
        status_code = []
        n = len(self.links)
        for i, mlink in enumerate(self.links):
            r = requests.get(mlink, headers=self.headers)
            raw_manifest.append(r.json() if r.status_code == requests.status_codes.codes.ALL_OK else [])
            status_code.append(r.status_code == requests.status_codes.codes.ALL_OK)
            self.count.emit((i+1)/n)
        self.finished.emit()
        self.manifest_data.emit([raw_manifest, status_code])

