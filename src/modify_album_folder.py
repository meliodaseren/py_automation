#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import shutil
import re

def organize_album_folders(folder_path):
    for fn in os.listdir(folder_path):
        print(f"-----\n[DEBUG] {fn}")
        # NOTE: Backup the specific files
        if fn.endswith('.rar'):
            shutil.move(f"{folder_path}\\{fn}", f"{backup_path}\\{fn}")
            continue
        elif fn.endswith('.mp4'):
            shutil.move(f"{folder_path}\\{fn}", f"{backup_path}\\{fn}")
            continue
        elif fn.endswith('.avi'):
            shutil.move(f"{folder_path}\\{fn}", f"{backup_path}\\{fn}")
            continue

        fn_path = f"{folder_path}\\{fn}"
        #TODO: Doesn't support to clean up the *.url in folders
        '''
        print("[INFO] Processing", fn)
        print("[Stage 1-1] Check the *.url in folder")
        url_path = f"{fn_path}\\*.url"
        url_glob = glob.glob(url_path)
        for _ in url_glob:
            print(f"Remove the {_}")
            os.remove(_)
        '''
        print("[Stage 2-1] Move MP3 file to previous folder, and remove empty folder")
        mp3_folder = f"{fn_path}\\MP3"
        if os.path.isdir(mp3_folder):
            for fn in os.listdir(mp3_folder):
                filename = f"{mp3_folder}\\{fn}"
                shutil.move(filename, fn_path)
            os.removedirs(mp3_folder)

        print("[Stage 2-2] Rename the folder, replace『』to「」")
        if "『" in fn:
            fn_new_path = fn_path.replace("『", "「").replace("』", "」")
            print(f"  Rename {fn_path} -> {fn_new_path}")
            os.rename(f"{fn_path}", f"{fn_new_path}")

def remove_date_postfix(folder_path):
    '''
    找出資料夾名稱的開頭格式為 '[123456] '
    中括號內為 6 位數字，比對後取代為空字串。
    '''
    for fn in os.listdir(folder_path):
        if fn == 'backup': continue
        try:
            # [181017]
            match = re.sub(r'^\[\d{6}\]', '',fn)
            os.rename(f"{folder_path}\\{fn}", f"{folder_path}\\{match}")
            #print("[INFO] 成功去除開頭之日期格式：" + match)
        except PermissionError as e:
            print("[ERROR]", e)
            pass
        except FileExistsError as e:
            print("[ERROR]", e)
            pass

    for fn in os.listdir(folder_path):
        if fn == 'backup': continue
        try:
            # [2016.10.28]
            match = re.sub(r'^\[\d{4}\.\d{2}\.\d{2}\]', '',fn)
            os.rename(f"{folder_path}\\{fn}", f"{folder_path}\\{match}")
            #print("[INFO] 成功去除開頭之日期格式：" + match)
        except PermissionError as e:
            print("[ERROR]", e)
            pass
        except FileExistsError as e:
            print("[ERROR]", e)
            pass

def remove_suffix(folder_path):
    '''
    找出資料夾名稱的結尾格式為 ' [320K+BK]' 或 ' [320K]' 或 ' [MP3]'
    比對後取代為空字串。
    '''
    for fn in os.listdir(folder_path):
        if fn == 'backup': continue
        try:
            # [320K+BK], [320K], [MP3]
            if re.search(r'\[(320K\+BK|320K|MP3|MP3\s320K|MP3\s320K\+BK)\]$', fn):
                match = re.sub(r'\[(320K\+BK|320K|MP3|MP3\s320K|MP3\s320K\+BK)\]$', '', fn)
                print(f"  Rename {folder_path}\\{fn} -> {folder_path}\\{match}")
                os.rename(f"{folder_path}\\{fn}", f"{folder_path}\\{match}")
                #print("[INFO] 成功去除後綴格式：" + match)
        except PermissionError as e:
            print("[ERROR]", e)
            pass
        except FileExistsError as e:
            print("[ERROR]", e)
            pass

def remove_singer_info(folder_path):
    for fn in os.listdir(folder_path):
        if fn == 'backup': continue
        try:
            # 」／.*
            if re.search(r'」／.*', fn):
                match = re.sub(r'」／.*', '」',fn)
                print(f"  Rename {folder_path}\\{fn} -> {folder_path}\\{match}")
                os.rename(f"{folder_path}\\{fn}", f"{folder_path}\\{match}")
                #print("[INFO] 成功去除後綴之歌手資訊：" + match)
        except PermissionError as e:
            print("[ERROR]", e)
            pass
        except FileExistsError as e:
            print("[ERROR]", e)
            pass

if __name__ == '__main__':
    folder_path = input("Please enter your path: ")
    backup_path = f"{folder_path}\\backup"
    if not os.path.exists(backup_path):
        os.makedirs(backup_path)
    
    print("[Stage 1] Remove *.url in folder")
    os.system("rm */*.url")

    print("[Stage 2] Organize album folder")
    organize_album_folders(folder_path)
    remove_date_postfix(folder_path)

    print("[Stage 3] Remove the prefix and suffix of album folder")
    remove_suffix(folder_path)
    remove_singer_info(folder_path)
