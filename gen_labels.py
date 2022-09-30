import dataset
import os


def main():
    classes = {}
    dirs = os.listdir("images/train/")


    for i, dire in enumerate(dirs):
        classes[i] = dire

        files = dataset.get_img_names(f"images/train/")
        for file in files:
            dataset.gen_label(file, i)
            desc = f"{file[:-4]}.yaml"
            try:
                os.remove(f"images/train/{desc}")
            except:
                pass

    print(f"Finished. Generated {len(classes.keys())} classes. \nOutput: {classes}")



if __name__ == "__main__":
    main()

