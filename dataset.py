import os


def get_img_names(dire):
    files = os.listdir(dire)
    images = set()
    for file in files:
        if file.endswith(".png"):
            images.add(file)

    return images


def gen_label(input_file_name, class_id):
    input_file_name = input_file_name[:-4]
    try:
        os.mkdir(f"labels/train/")
    except:
        pass
    with open(f"labels/train/{input_file_name}.txt", "w") as f:
        f.write(f"{class_id} 0.5 0.5 1 1")
