import sys
import os
import shutil
from pathlib import Path

global dir_im
global dir_aud
global dir_vid
global dir_doc
global dir_arch
global dir_other
global my_sort_dir
my_sort_dir = 'images', 'documents', 'audio', 'video', 'archives', 'other'

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "_", "_", "", "ej", "yu", "ya", "je", "i", "ji", "g")
LATYN_ = 'aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ01234567890.'
CYRYLIC = tuple(CYRILLIC_SYMBOLS)
TRANS = {}

for c, l in zip(CYRYLIC, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(name):
    name_l = ""
    for a in name:
        name_l = name_l + a.translate(TRANS)
    name_f = ""
    for a in name_l:
        if a in LATYN_:
            name_f = name_f + a
        else:
            name_f = name_f + "_"
    return name_f


def newdir(fold):
    global dir_im
    global dir_aud
    global dir_vid
    global dir_doc
    global dir_arch
    global dir_other
    dir_im = os.path.join(fold, 'images')
    if not os.path.exists(dir_im):
        os.makedirs(dir_im)
    dir_doc = os.path.join(fold, 'documents')
    if not os.path.exists(dir_doc):
        os.makedirs(dir_doc)
    dir_aud = os.path.join(fold, 'audio')
    if not os.path.exists(dir_aud):
        os.makedirs(dir_aud)
    dir_vid = os.path.join(fold, 'video')
    if not os.path.exists(dir_vid):
        os.makedirs(dir_vid)
    dir_arch = os.path.join(fold, 'archives')
    if not os.path.exists(dir_arch):
        os.makedirs(dir_arch)
    dir_other = os.path.join(fold, 'other')
    if not os.path.exists(dir_other):
        os.makedirs(dir_other)


def sort_file(path_for_sort):
    global dir_im
    global dir_aud
    global dir_vid
    global dir_doc
    global dir_arch
    global dir_other
    image_type = '.jpg', '.png', '.jpeg', '.svg', '.gif', '.bmp', '.pcx', '.cdr'
    video_type = '.avi', '.mp4', '.mkv', '.mov'
    doc_type = '.doc', '.docx', '.txt', '.pdf', '.xls', '.xlsx', '.ppt', '.pptx'
    audio_type = '.mp3', '.ogg', '.wav', '.amr', '.flac'
    archi_type = '.zip', '.gz', '.tar'

    all_files = os.listdir(path_for_sort)

    for file in all_files:
        file_path = os.path.join(path_for_sort, file)
        if os.path.isfile(file_path):
            file_n = normalize(file)
            if file_path.endswith(image_type):
                new_file_path = os.path.join(dir_im, file_n)
                os.replace(file_path, new_file_path)
            elif file_path.endswith(video_type):
                new_file_path = os.path.join(dir_vid, file_n)
                os.replace(file_path, new_file_path)
            elif file_path.endswith(doc_type):
                new_file_path = os.path.join(dir_doc, file_n)
                os.replace(file_path, new_file_path)
            elif file_path.endswith(audio_type):
                new_file_path = os.path.join(dir_aud, file_n)
                os.replace(file_path, new_file_path)
            elif file_path.endswith(archi_type):
                new_file_path = os.path.join(dir_arch, file_n)
                os.replace(file_path, new_file_path)
            else:
                new_file_path = os.path.join(dir_other, file_n)
                os.replace(file_path, new_file_path)


def archivunpack():
    global dir_arch
    all_files = os.listdir(dir_arch)
    for file in all_files:
        file_path = os.path.join(dir_arch, file)
        if os.path.isfile(file_path):
            file_a = file.split('.')
            folder_for_new_arch = os.path.join(dir_arch, file_a[0])
            if not os.path.exists(folder_for_new_arch):
                os.makedirs(folder_for_new_arch)
            shutil.unpack_archive(file_path, folder_for_new_arch)
            os.remove(file_path)


def otherfiles(path):
    global dir_other
    all_files = os.listdir(dir_other)
    for file in all_files:
        old_file_path = os.path.join(path, file)
        new_file_path = os.path.join(dir_other, file)
        os.replace(new_file_path, old_file_path)
    os.rmdir(dir_other)


def sort_dir(path_for_sort):
    global my_sort_dir

    all_files = os.listdir(path_for_sort)
    for file in all_files:
        if file not in my_sort_dir:
            subfolder = os.path.join(path_for_sort, file)
            if os.path.isdir(subfolder):
                if not os.listdir(subfolder):
                    os.rmdir(subfolder)
                else:
                    sort_file(subfolder)
                    sort_dir(subfolder)


def delit_old_dir(path):
    global my_sort_dir
    all_files = os.listdir(path)
    for file in all_files:
        if file not in my_sort_dir:
            subfolder = os.path.join(path, file)
            if os.path.isdir(subfolder):
                if not os.listdir(subfolder):
                    os.rmdir(subfolder)
                else:
                    delit_old_dir(subfolder)
                    os.rmdir(subfolder)


def main():
    if len(sys.argv) < 2:
        print('Enter path to folder which should be cleaned')
        exit()
    folder = sys.argv[1]
    if not (os.path.exists(folder) and Path(folder).is_dir()):
        print('Path incorrect')
        exit()
    newdir(folder)
    sort_file(folder)
    sort_dir(folder)
    archivunpack()
    otherfiles(folder)
    delit_old_dir(folder)


if __name__ == "__main__":
    exit(main())
