import os
import glob
import json
import cv2
import numpy as np
import xml.etree.ElementTree as ET
import argparse



parser = argparse.ArgumentParser()

parser.add_argument(
    '-p',
    '--path',
    dest='dataset_path',
    help='Path to dataset data ?(image and annotations).',
    required=True
)
parser.add_argument(
    '-o',
    '--output',
    dest='output_path',
    help='Path that will be saved the resized dataset',
    default='./',
    required=False
)
parser.add_argument("-s",
                    "--new_image_size",
                    help="New Shape of the image to store",
                    nargs=2,
                    default=[224,224],
                    type=int)


args = parser.parse_args()



def get_file_name(path):
    base_dir = os.path.dirname(path)
    file_name, ext = os.path.splitext(os.path.basename(path))
    ext = ext.replace(".", "")
    return (base_dir, file_name, ext)


def resize_xml(xml_path, output_path, newSize):

    newBoxes = []
    xmlRoot = ET.parse(xml_path).getroot()

    image_name= xmlRoot.find('filename').text
    image_path = os.path.join(dataset_path ,image_name )
    image = cv2.imread(image_path)
    scale_x = newSize[0] / image.shape[1]
    scale_y = newSize[1] / image.shape[0]

    image = cv2.resize(image, (newSize[0], newSize[1]))


    size_node = xmlRoot.find('size')
    size_node.find('width').text = str(newSize[0])
    size_node.find('height').text = str(newSize[1])

    for member in xmlRoot.findall('object'):
        bndbox = member.find('bndbox')

        xmin = bndbox.find('xmin')
        ymin = bndbox.find('ymin')
        xmax = bndbox.find('xmax')
        ymax = bndbox.find('ymax')
        
        xmin.text = str(int(np.round(float(xmin.text) * scale_x)))
        ymin.text = str(int(np.round(float(ymin.text) * scale_y)))
        xmax.text = str(int(np.round(float(xmax.text) * scale_x)))
        ymax.text = str(int(np.round(float(ymax.text) * scale_y)))

        newBoxes.append([
            1,
            0,
            int(float(xmin.text)),
            int(float(ymin.text)),
            int(float(xmax.text)),
            int(float(ymax.text))
            ])

    (_, file_name, ext) = get_file_name(image_path)
    cv2.imwrite(os.path.join(output_path, '.'.join([file_name, ext])), image)
    
    tree = ET.ElementTree(xmlRoot)
    tree.write('{}/{}.xml'.format(output_path, file_name, ext))
    for shape in newBoxes :
        start_p = (shape[2] , shape[3])
        end_p = (shape[4] ,shape[5])
        image = cv2.rectangle(image,start_p,end_p, (255, 0, 0), 1)



def resize_json(file , output_path ,newSize):
    f = open(file)
    f_json = json.load(f)

    h = f_json["imageHeight"]
    w = f_json["imageWidth"]
    img_name = os.path.basename(f_json["imagePath"].replace("\\","/"))

    shapes = f_json["shapes"]
    x_scale = newSize[0] / h
    y_scale = newSize[1] / w

    for shape in shapes :
        shape["points"][0][0] = shape["points"][0][0]*y_scale
        shape["points"][0][1] = shape["points"][0][1]*x_scale
        shape["points"][1][0] = shape["points"][1][0]*y_scale
        shape["points"][1][1] = shape["points"][1][1]*x_scale    
        
    f_json["imageHeight"] = newSize[0]
    f_json["imageWidth"] = newSize[1]

    img = cv2.imread(os.path.join(dataset_path , img_name))
    
    print("\nImage Path:", os.path.join(dataset_path , img_name))
    
    img = cv2.resize(img, (newSize[0], newSize[1]))

    json_name = img_name.split(".")[0]+".json"

    with open(os.path.join(output_path, json_name) , 'w' , encoding='utf-8') as json_file :
        json.dump(f_json , json_file)

    cv2.imwrite(os.path.join(output_path, img_name),img)

    for shape in shapes :
        points = shape["points"]
        start_p = (int(points[0][0]) , int(points[0][1]))
        end_p = (int(points[1][0]) ,int(points[1][1]))
        img = cv2.rectangle(img,start_p,end_p, (255, 0, 0), 1)
    
    f.close()


PATH_ROOT = os.getcwd()
PATH_ROOT = PATH_ROOT.replace(" ","")

newSize = tuple(args.new_image_size)
dataset_path = args.dataset_path
out_path = os.path.join(PATH_ROOT,"images")
format = ""


files = glob.glob(dataset_path+"/*.json")
if len(files)==0:
    print("Annotation file format : XML")
    format = "xml"
    files = glob.glob(dataset_path+"/*.xml")
else :
    print("Annotation file format: JSON")
    format="json"

for file in files :
    if format=="json" :
        resize_json(file , out_path , newSize)
    else :
        resize_xml(file , out_path , newSize)
print("Resizing Completed")
os.chdir(PATH_ROOT)
