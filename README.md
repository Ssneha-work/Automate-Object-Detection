# Automate-Object-Detection

## Tutorial :

#### Click here for tutorial : [Collab](https://colab.research.google.com/drive/1ThuRxOM8OIFFcVtP-fUVnvcMzXDXS4G7?usp=sharing)

## Steps to run :
1. Upload your dataset folder containing `images (.jpg or .png)` and `annotation files (.xml , .json , .csv)` to Google Drive
2. Open the Google collab notebook and `mount your drive`.
3. Navigate to any folder and clone the repository
   >
   > ```markdown
   > ! git clone https://github.com/Ssneha-work/Automate-Object-Detection.git
   > ```
5. Run setup.py script to create necessary folder structure and downlaoding pretrained models
   >
   > #### Parameters:
   >
   > -m : Name of the pretrained model to be used<br>
   > -p : Path of the pretrained model coco configuration file
   >
   > ```markdown
   > %run setup.py -m "ssd_mobilenet_v1_coco_2017_11_17"  -p "/content/drive/MyDrive/Object_Detection/Automate-Object-Detection/tf/research/object_detection/samples/configs/ssd_mobilenet_v1_pets.config"
   > ```
6. Run resize_dataset.py this will resize images to 224x224 and change the annotation files accordingly so that they fit into colabs memory while training.
   >
   > #### Parameters:
   >
   > -p : Path to dataset data<br>
   > -s : Shape of the new image 
   >
   >```markdown
   > !python resize_dataset.py -p /content/drive/MyDrive/train -s 230 230
   > ```
7. Lets prepare our dataset and create tfrecords.
   >
   > #### Parameters
   > 
   > -s : Percentage of training data to be used
   >
   > ```markdown
   > %run prepare_dataset.py -s 80
   > ```
8. Start training our model.
   >
   > #### Parameters:
   >
   > -st : Number of steps in training<br>
   > -c : classes in dataset<br>
   > -ne : Number of examples to be evaluated in dataset<br>
   > -bs : Batch size for training<br>
   > -lr : Initial learning rate
   >
   > ```markdown
   > !python train.py -st 250 -c 2 -ne 7 -bs 20 -lr 0.003
   > ```
9. Freeze the trained model.
   > ```markdown
   > %run eval_freeze.py
   > ```
10. Check your predictions
   >
   > #### Parameters
   > 
   > -c : Number of classes in dataset<br>
   > -n : Number of images to show predictions on<br>
   > -s : Size, in inches of an output image of 
   >
   > ```markdown
   > %run plot.py -c 2 -n 14 -s 10 8
   > ```
   