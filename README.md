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

## Installing

Todo



## Training

Make several thousand images using stable diffusion img2img with the base image as an actual image from hCaptcha (For best results only make a couple of hundred images (still figuring out the exact number) for each real image). Make sure that the images stick to the general idea of the base image while also being different enough (mess around with the variation slider)
