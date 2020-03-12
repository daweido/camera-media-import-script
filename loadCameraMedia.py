import os
import time
import shutil
import sys
import uuid
from os.path import join
import logging

# TODO Check if it works correctly
# TODO try to make it completly automatic, without the need of entering the camera_type

def _logpath(path, names):
    logging.info('Working in %s' % path)
    return []   # nothing will be ignored

def safe_move(src, dst):
    copy_id = uuid.uuid4()
    tmp_dst = "%s.%s.tmp" % (dst, copy_id)
    shutil.copytree(src, tmp_dst, ignore=_logpath)
    os.rename(tmp_dst, dst)
    shutil.rmtree(src)


sd_card_name = sys.argv[1]
camera_type = sys.argv[2]

if camera_type == "CANON" or camera_type == "SONY":
    sd_card_path = join(os.sep, "Volumes",sd_card_name,"DCIM","100MSDCF")
    # TODO Change the names of directories
    hd_path = join(os.sep, "Volumes", "Rigaux_Mac", "Media", "Camera Media","Photos")
elif camera_type == "GOPRO":
    sd_card_path = join(os.sep, "Volumes",sd_card_name,"DCIM","100GOPRO")
    # TODO Change the names of directories
    hd_path = join(os.sep, "Volumes", "Rigaux_Mac", "Media", "GoPro Media","Photos")

os.chdir(sd_card_path)

for f in os.listdir('.'):
    f_creation_time = time.gmtime(os.path.getmtime(f))

    # Month creation processing to force double digit format
    month_creation = str(f_creation_time.tm_mon)
    month_creation = "0" + month_creation if len(month_creation) < 2 else month_creation

    # Day creation processing to force double digit format
    day_creation = str(f_creation_time.tm_mday)
    day_creation = "0" + day_creation if len(day_creation) < 2 else day_creation

    # New directory name processing
    creation_time_dir = str(f_creation_time.tm_year) + month_creation + day_creation


    if not os.path.isdir(creation_time_dir):
        os.mkdir(creation_time_dir)
    
    f_dest_path = join(creation_time_dir, f)
    shutil.move(f, f_dest_path)


for d in os.listdir('.'):
    # Go to Photos directory in HDD
    os.chdir(hd_path)

    path_current_date = hd_path

    # Year, month and day extraction from the directory name
    dir_year = d[:4]
    dir_month = d[4:6]
    dir_day = d[6:8]

    if not os.path.isdir(dir_year):
        os.mkdir(dir_year)
    
    path_current_date = join(path_current_date, dir_year)
    os.chdir(path_current_date)

    if not os.path.isdir(dir_year + dir_month):
        os.mkdir(dir_year + dir_month)
    
    path_current_date = join(path_current_date, dir_year + dir_month)
    os.chdir(path_current_date)

    os.chdir(sd_card_path)
    directory_dist_path = join(path_current_date, d)

    safe_move(d,directory_dist_path)