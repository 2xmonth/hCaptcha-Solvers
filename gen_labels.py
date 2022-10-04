import dataset
import os


def main():
    classes = {}
    dirs = os.listdir("images/train/")

    for i, dire in enumerate(dirs):
        classes[i] = dire
        print(dire)
        files = dataset.get_img_names(f"images/train/{dire}")
        for file in files:
            dataset.gen_label(file, i)
            desc = f"{file[:-4]}.yaml"
            try:
                os.remove(f"images/train/{dire}/{desc}")
            except:
                pass

            os.rename(f"images/train/{dire}/{file}", f"images/train/{file}")

    print(f"Finished. Generated {len(classes.keys())} classes. \nOutput: {classes}")



if __name__ == "__main__":
    main()

