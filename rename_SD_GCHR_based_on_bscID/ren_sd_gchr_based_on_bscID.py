import gzip
import argparse
import os
import shutil
import zipfile
import re

def rename_sd(root_dir_of_sd):
    root_dir_of_sd = root_dir_of_sd

    for cur, dirs, files in os.walk(root_dir_of_sd):
        for file in files:
            if re.findall(r"BSC0", file):
                file_path = os.path.join(cur, file)
                print("file_path= {}".format(file_path))
                index = 0
                cur_dirname = os.path.basename(cur)
                for i in range(-1, (len(cur_dirname)-1)*-1,  -1):
                    if cur_dirname[i].isnumeric():
                        continue
                    else:
                        index = i+1
                        break
                bsc_id = str(cur_dirname)[index:]
                print("bsc_id is {}".format(bsc_id))
                new_file = str(file).replace("BSC0", "BSC{}".format(bsc_id))
                new_file_path = os.path.join(cur, new_file)
                try:

                    with zipfile.ZipFile(file_path, 'r') as sd_file_ob:
                        file_list = sd_file_ob.namelist()
                        for file_name in file_list:
                            print("Inside file name is {}".format(file))
                            with sd_file_ob.open(file_name) as file_ob:
                                file_serial = file_ob.read()
                                # replacement =
                                file_serial = file_serial.replace(b"BSCID: 0", "BSCID: {}".format(bsc_id).encode())
                            with zipfile.ZipFile(new_file_path, 'w') as new_sd_file_ob:
                                with new_sd_file_ob.open("{}.txt".format(new_file.rstrip(".zip")), 'w') as new_file:
                                    new_file.write(file_serial)
                except FileNotFoundError:
                    print("Expected file was not found")
                else:
                    os.remove(file_path)


def rename_gchr(root_dir_of_gchr):
    root_dir_of_gchr = root_dir_of_gchr
    for cur, dirs, files in os.walk(root_dir_of_gchr):
        for file in files:
            if re.findall(r"BSC0000", file):
                file_path = os.path.join(cur, file)
                print("file_path= {}".format(file_path))
                index = 0
                cur_dirname = os.path.basename(cur)
                for i in range(-1, (len(cur_dirname)-1)*-1,  -1):
                    if cur_dirname[i].isnumeric():
                        continue
                    else:
                        index = i+1
                        break
                bsc_id = str(cur_dirname)[index:]
                print("bsc_id is {}".format(bsc_id))
                new_file = str(file).replace("BSC0000", "BSC00{}".format(bsc_id))
                print("New GCHR file is {}".format(new_file))
                new_file_path = os.path.join(cur, new_file)
                shutil.move(file_path, new_file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("SD_root_dir", help="Provide input folder path as first argument")
    parser.add_argument("gchr_root_dir")
    print("Help contact : swapankumar.das@teoco.com")
    args = parser.parse_args()
    SD_root_dir = args.SD_root_dir
    gchr_root_dir = args.gchr_root_dir
    rename_sd(SD_root_dir)
    rename_gchr(gchr_root_dir)

