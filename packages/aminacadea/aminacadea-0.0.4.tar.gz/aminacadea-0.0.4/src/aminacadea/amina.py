import os
from pathlib import Path
from PIL import Image
import imghdr  
# from tflite_model_maker import image_classifier
# from tflite_model_maker.image_classifier import DataLoader
from tflite_support import metadata
# import matplotlib.pyplot as plt
# from IPython.display import clear_output


def make_dir(directory):
  if not os.path.exists(directory):
    os.makedirs(directory)

def make_dir_structure(parent_dir_name, path, data):

  data_dict = {}
  parent_dir = os.path.join(path, parent_dir_name, 'data')
  model_dir = os.path.join(path, parent_dir_name, 'model')
  make_dir(parent_dir)
  data_dict["data_url"] = parent_dir
  make_dir(model_dir)
  data_dict["model"] = model_dir

  for label in data:
    label_dir = os.path.join(parent_dir, label)
    make_dir(label_dir)
  
  return data_dict

def clean_up(data,data_url):
  for label in data:
    destination_dir = os.path.join(data_url, label)
    list_of_files = os.listdir(destination_dir)
    if not os.listdir(destination_dir):
      os.rmdir(destination_dir)
      print(label, " was empty and has been deleted!")

    else:
      num_of_files = len(list_of_files)
      for filename in list_of_files:
        if filename.endswith(tuple(["JPG", "JPEG", "jpg", "jpeg", "png", "PNG"])):
          file_path = os.path.join(destination_dir, filename)
          # print(file_path)
          img_type = imghdr.what(file_path)
          if img_type is None:
            print(f"{file_path} is not an image")
          elif img_type not in ["JPG", "JPEG", "jpg", "jpeg", "png", "PNG"]:
            print(f"{file_path} is a {img_type}, not accepted by TensorFlow")

          #pass
        else:
          print('file to delete ', filename)
          file_path = os.path.join(destination_dir, filename)
          os.remove(file_path)
          print(filename, 'was deleted during cleanup. Only jpg and png files are allowed') 

def check_file_types_and_cleanup(data,data_url):
  # checks files to make sure they are the correct type for tensorflow and delete those that are not
  deleted_files = []
  for label in data:
    destination_dir = os.path.join(data_url, label)
    list_of_files = os.listdir(destination_dir)
    for filename in list_of_files:
      if filename.endswith(tuple(["JPG", "JPEG", "jpg", "jpeg", "png", "PNG"])):
        file_path = os.path.join(destination_dir, filename)
        img = Image.open(file_path)
        img_type = img.format
        print(filename, 'image type: ', img_type)

        if img_type is None:
          print(f"{file_path} is not an image")
          os.remove(file_path)
          print(filename, 'was deleted during cleanup. Only jpg and png files are allowed') 

        elif img_type not in ["JPG", "JPEG", "jpg", "jpeg", "png", "PNG"]:
          print(f"{file_path} is a {img_type}, not accepted by TensorFlow and has been deleted!")
          os.remove(file_path)
          deleted_files.append(filename)   
          
def get_labels_from_metadata(model_url):
  displayer = metadata.MetadataDisplayer.with_model_file(model_url)
  file_name = displayer.get_packed_associated_file_list()[0]
  label_map_file = displayer.get_associated_file_buffer(file_name).decode()
  label_list = list(filter(lambda x: len(x) > 0, label_map_file.splitlines()))
  try:
    label_list.remove('.ipynb_checkpoints')
  except:
    pass
  final_label_list = label_list
  string_label_list = ",".join(str(item) for item in final_label_list)
  
  return final_label_list, string_label_list
