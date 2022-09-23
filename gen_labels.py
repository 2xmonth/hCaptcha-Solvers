import dataset
import os


def main():
    classes = {}
    dirs = os.listdir("images/train/")


    for i, dire in enumerate(dirs):
        classes[i] = dire

        files = dataset.get_img_names(f"images/train/{dire}")
        for file in files:
            dataset.gen_label(dire, file, 0)
            desc = f"{file[:-4]}.yaml"
            try:
                os.remove(f"images/train/{dire}/{desc}")
            except:
                pass

    print(f"Finished. Generated {len(classes.keys())} classes. \nOutput: {classes}")



if __name__ == "__main__":
    main()

