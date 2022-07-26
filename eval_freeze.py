import glob, os

def get_latest_checkpoint(path):
    check=0
    checkpoint=""
    for file in glob.glob(path+"/*.index"):
        fname =file.split(".")[1]
        num = int(fname.split("-")[1])
        if(num>check):
            checkpoint = "model."+fname
    print(checkpoint)
    return checkpoint



import os
PATH_ROOT = os.getcwd()
PATH_ROOT = PATH_ROOT.replace(" ","")
os.environ['PYTHONPATH'] += ':' + PATH_ROOT + '/tf/research/:'+PATH_ROOT+'/tf/research/slim/:'+PATH_ROOT+'/tf/research/object_detection/utils/:'+PATH_ROOT+'/tf/research/object_detection'

PATH_CHECK = PATH_ROOT+"/tf/trained"
PATH_CONFIG =  ''.join(glob.glob(PATH_ROOT+"/tf/*.config"))
PATH_GRAPH = PATH_ROOT + "/tf/research/object_detection/export_inference_graph.py"
PATH_OUTPUT = PATH_ROOT +"/tf/fine_tuned_model"
LATEST_CHECK = PATH_CHECK+ ("/"+get_latest_checkpoint(PATH_CHECK))
os.system("protoc "+PATH_ROOT+"/tf/research/object_detection/protos/*.proto --python_out=.")
os.system("python "+PATH_GRAPH+" --input_type=image_tensor --pipeline_config_path="+PATH_CONFIG+" --output_directory="+PATH_OUTPUT+" --trained_checkpoint_prefix="+LATEST_CHECK)
os.chdir(PATH_ROOT)
