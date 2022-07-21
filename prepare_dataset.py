import os
import shutil
import argparse
import glob
import urllib
import tarfile
from requests import get

PATH_ROOT = os.getcwd()
PATH_ROOT = PATH_ROOT.replace(" ","")
print(PATH_ROOT)
parser = argparse.ArgumentParser(
    description="Data generation in tfrecord fromat")
parser.add_argument("-s",
                    "--split",
                    help="Percentage to split data set into",
                    default="70",
                    type=str)
parser.add_argument("-f",
                    "--filename",
                    help="path to xml json csv file",
                    type=str)

args = parser.parse_args()
filename=""
if args.filename is not None:
    filename = args.filename
file_path = PATH_ROOT + "/images/"+ filename
images_path = PATH_ROOT + "/images"
output_path = PATH_ROOT + "/tfrecords"
csv_path = PATH_ROOT + "/tfrecords"                    

os.system("python "+ PATH_ROOT+"/tf/research/generate_tfrecord.py -f " + file_path +" -i "+ images_path + " -o "+output_path+" -c "+csv_path+" -s "+args.split)
os.chdir(PATH_ROOT)