from email.policy import default
import os
import shutil
import tarfile
from requests import get
import argparse

parser = argparse.ArgumentParser(
    description="Setting up the environment")

parser.add_argument("-m",
                    "--model_name",
                    help="Name of the pretrained model",
                    default="ssd_inception_v2_coco_2018_01_28",
                    type=str)

args = parser.parse_args()

PATH_ROOT = os.getcwd()
PATH_ROOT = PATH_ROOT.replace(" ","")
print(PATH_ROOT)

PATH_IMAGES = PATH_ROOT + "/images"
PATH_TFRECORD = PATH_ROOT + "/tfrecords"
os.system("pip install tensorflow==1.13.2")
print("Tensorflow installed")
os.system("pip install tf_slim")
print("tf_slim installed")
os.system("pip show tensorflow")

print("Cloning repository from https://github.com/iotiotdotin/tf.git")
os.system("git clone https://github.com/iotiotdotin/tf.git")
os.mkdir(PATH_IMAGES)
os.mkdir(PATH_TFRECORD)
shutil.move(PATH_ROOT + "/generate_tfrecord.py" ,PATH_ROOT+"/tf/research" )

print("Moved tfrecod.py sucessfully")
print("Testing files in cloned repo")
os.chdir(PATH_ROOT + "/tf/research")
os.system("protoc object_detection/protos/*.proto --python_out=.")
os.chdir(PATH_ROOT + "/tf/research/slim")
os.system("python setup.py build")
os.environ['PYTHONPATH'] += ':' + PATH_ROOT + '/tf/research/:'+PATH_ROOT+'/tf/research/slim/:'+PATH_ROOT+'/tf/research/object_detection/utils/:'+PATH_ROOT+'/tf/research/object_detection'

print("Running model_builder_test.py")
os.chdir(PATH_ROOT + "/tf/research/")
os.system("python object_detection/builders/model_builder_test.py")


print("Downloading pretrained model...")
# Downloading pretrained model
os.chdir(PATH_ROOT + "/tf")
MODEL=args.model_name
MODEL_FILE = MODEL + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'
DEST_DIR = 'pretrained_model'


if not (os.path.exists(MODEL_FILE)):
  with open(MODEL_FILE, "wb") as file:
    # get request
    response = get(DOWNLOAD_BASE + MODEL_FILE)
    # write to file
    file.write(response.content)


tar = tarfile.open(MODEL_FILE)
tar.extractall()
tar.close()

os.remove(MODEL_FILE)
if (os.path.exists(DEST_DIR)):
  shutil.rmtree(DEST_DIR)
os.rename(MODEL, DEST_DIR)
print("Moving config file to tf folder...")
shutil.move(PATH_ROOT+"/"+MODEL+".config", PATH_ROOT +"/tf") 
shutil.move(PATH_ROOT+"/config.py", PATH_ROOT +"/tf/research") 
os.chdir(PATH_ROOT)



