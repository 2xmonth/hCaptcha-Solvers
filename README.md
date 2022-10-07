# Current Status:
I have trained a yolov7 model on the following prompts:
- a rabbit in grass
- a plant hanging from the ceiling
- a house in the beach
- a dead and dried plant in the pot
- a horse running
- a penguin surrounded by flowers
- a toy rabbit
- a toy turtle
- a toy house
- a duck

~~The model sucks. It's really good at recognizing images made with stable diffusion (as it should be), but it sucks for the hcaptcha prompts~~
This model isn't as bad as I thought it was, it has recently been performing pretty well.


If you want the full dataset (of the stable diffusion images, i dont know why you would want them though) make an issue and ill add it to releases (or something)


# hCaptcha-Solvers
My hCaptcha solver + dataset creator.

I am using stable diffusion to create my dataset because hCaptcha is now using txt2img to generate captcha images.  


### hCaptcha + txt2img

![alt text](https://github.com/2xmonth/hCaptcha-Solvers/blob/main/resources/txt2img.png?raw=true)

Imgs: 1, 2, 8, and 9 have either no wake in the water, or incorrect wake (2 and 9)

Imgs: 4, 7 and even the sample image have some really messed up legs. Also, all their toy rabbit images follow the same pattern, pale rabbit on a white background with some shadows.
Img 7 also has a red scarf (?) drooping down into the forefront of the image, it looks like it is hanging off some but there is nothing there.
I don't know how else to explain this, the images are clearly messed up.

Also, look at:
![alt text](https://github.com/2xmonth/hCaptcha-Solvers/blob/main/resources/txt2img2.png?raw=true)

This one is clearly wrong as well.


### hCaptcha prompt extraction
To extract prompts run prompts.py. Use a vpn to help prevent ip bans.

I'm not sure how effective the prompt extractor is on 1 ip, I would recommend proxies so that you will have the highest chance of getting new prompts because hcaptcha is probably only giving each ip a selection of prompts

## Installing

Todo


## Training

I made a couple thousand images for each class, later on I will do this with only a 1k images for each class.
Make sure that the images stick to the general idea of the base image while also being different enough.

Generate img2img images with stable diffusion (0.72 on denoising strength, all the other settings I have liked)
Go into <stable-diffusion-dir>/outputs/img2img-samples/samples/<all-your-classes>
Take all of those files and paste them over into hCaptcha-Solvers/images/train/
Then run gen_labels.py
Next put make a yolov7 compatible dataset (ex. yolov7/hcaptcha/images/train/, yolov7/hcaptcha/label/train/, yolov7/hcaptcha/images/val/, yolov7/hcaptcha/label/val/)
Then train it using yolov7's train.py


#### I WILL NOT BE HELPING ANYONE WITH TRAINING, IF YOU'RE TRYING TO TRAIN YOUR OWN MODEL I AM EXPECTING THAT YOU ALREADY HAVE SOME EXPERIENCE WITH YOLO 