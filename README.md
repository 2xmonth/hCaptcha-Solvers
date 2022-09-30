# Current Status:
I finished my test dataset of rabbits in grass, toy rabbits, and horses running, and my model worked pretty good.
Now I will gen all the other images for all of the current prompts. 


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

Make several thousand 512x512 images (I know hcaptcha uses 122x122, but stable diffusion doesn't do a great job making those images) with img2img with the base image as an actual image from hCaptcha (For best results only make a couple of hundred images (still figuring out the exact number) for each real image). 

Make sure that the images stick to the general idea of the base image while also being different enough.

Settings you should mess with:
Denoising strength (with my limited testing I have found between 0.67-0.73 works the best. I like 0.72, but it varies for each image)
Sampling steps (if you want better images)

I'll probably do all ^ later, but until then you have to figure out what works