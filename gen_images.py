# if you want to gen your own labels put your prompts in 'prompts.txt' and run stable diffusion webui (im using https://github.com/sd-webui/stable-diffusion-webui)
# next have the image you want to gen with in hcaptcha-imgs/<prompt><number>.png
# the prompt is the full prompts (duh) and the number is like 1, 2, 3, 4 ... for all the images of that type
# this is a terrible explanation just make an issue and ill rewrite this

# making ^ once this works

from time import sleep
import websocket
import base64
import random
import string
import httpx
import json
import cv2

ua = "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"

def extract(prompt, num_imgs, denoising, img_path):
    jpg_img = cv2.imencode('.jpg', cv2.imread(img_path))
    img_base64 = base64.b64encode(jpg_img[1]).decode('utf-8')

    ws = websocket.WebSocket()
    ws.connect("ws://localhost:7860/queue/join")
    ws.send(json.dumps({"hash": "5mhfkx2ueug"}))

    msg = ws.recv()
    while "send_data" not in msg:
        msg = ws.recv()
        sleep(0.01)

    print("Sending data")

    ws.send(json.dumps({"fn_index":36,"data":[prompt,"Mask","Keep masked area",3,False,50,"k_lms",["Normalize Prompt Weights (ensure sum of weights add up to 1.0)","Save individual images","Save grid","Sort samples by prompt","Write sample info files"],"RealESRGAN_x4plus",num_imgs,5,denoising,None,512,512,"Just resize",None,{"image":f"data:image/png;base64,{img_base64}","mask":"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHoAAAB6CAYAAABwWUfkAAABtklEQVR4Xu3TUQ0AIAzE0OFfNPCBCvqWTEDb3JqZfd99bmAJ/Xnhhyd0o/MILXTEQATTooWOGIhgWrTQEQMRTIsWOmIggmnRQkcMRDAtWuiIgQimRQsdMRDBtGihIwYimBYtdMRABNOihY4YiGBatNARAxFMixY6YiCCadFCRwxEMC1a6IiBCKZFCx0xEMG0aKEjBiKYFi10xEAE06KFjhiIYFq00BEDEUyLFjpiIIJp0UJHDEQwLVroiIEIpkULHTEQwbRooSMGIpgWLXTEQATTooWOGIhgWrTQEQMRTIsWOmIggmnRQkcMRDAtWuiIgQimRQsdMRDBtGihIwYimBYtdMRABNOihY4YiGBatNARAxFMixY6YiCCadFCRwxEMC1a6IiBCKZFCx0xEMG0aKEjBiKYFi10xEAE06KFjhiIYFq00BEDEUyLFjpiIIJp0UJHDEQwLVroiIEIpkULHTEQwbRooSMGIpgWLXTEQATTooWOGIhgWrTQEQMRTIsWOmIggmnRQkcMRDAtWuiIgQimRQsdMRDBtGihIwYimBYtdMRABNOihY4YiGBatNARAxFMi46EPjHUegElPhiUAAAAAElFTkSuQmCC"},None,"\"95556fc0be444c3c99504fbe54bfa3f6\"",False,False,False,3]}))

    msg = ws.recv()
    while "process_completed" not in msg:
        msg = ws.recv()
        sleep(0.01)

    print("Finished processing")





extract("a duck, hyperrealistic", "10", "0.72", "hcaptcha-imgs/a duck/0.19944892886786414.png")
























# wsheaders = {
#     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
#     "Accept": "*/*",
#     "Accept-Language": "en-US,en;q=0.5",
#     "Accept-Encoding": "gzip, deflate",
#     "Connection": "keep-alive, Upgrade",
#     "Sec-Fetch-Dest": "websocket",
#     "Sec-Fetch-Mode": "websocket",
#     "Sec-Fetch-Site": "same-origin",
#     "Pragma": "no-cache",
#     "Cache-Control": "no-cache"
# }
# # websocket.enableTrace(True)
# ws = websocket.WebSocket()
# ws.connect("ws://localhost:7860/queue/join", header=wsheaders)
#
# hash = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
# id = "".join(random.choices(string.ascii_lowercase + string.digits, k=32))
#
# ws.send(json.dumps({"hash": hash}))
# sleep(0.0001)
# for i in range(200):
#     resp = ws.recv()
#     print(resp)
#     if "send_data" in resp:
#         print("sending data")
#         break
#     sleep(0.001)
#
# jpg_img = cv2.imencode('.jpg', cv2.imread(img_path))  # i stole you from stack overflow
# img_base64 = base64.b64encode(jpg_img[1]).decode('utf-8')
# ws.send(json.dumps({"fn_index": 36, "data": [prompt, "Mask", "Keep masked area", 3, False, 50, "k_lms",
#                                              ["Normalize Prompt Weights (ensure sum of weights add up to 1.0)",
#                                               "Save individual images", "Save grid", "Sort samples by prompt",
#                                               "Write sample info files"], "RealESRGAN_x4plus", num_imgs, 5, denoising,
#                                              None, 512, 512, "Just resize", None,
#                                              {"image": f"data:image/png;base64,{img_base64}",
#                                               "mask": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHcAAAB1CAYAAAB08X6BAAAAAXNSR0IArs4c6QAAAaNJREFUeF7t1QEJADAQw8DOv+gNJuPIO0hC+bPtriMNnOKSXT9Ucd22xYXbFre4sgGYrZ9bXNgAjNZyiwsbgNFabnFhAzBayy0ubABGa7nFhQ3AaC23uLABGK3lFhc2AKO13OLCBmC0lltc2ACM1nKLCxuA0VpucWEDMFrLLS5sAEZrucWFDcBoLbe4sAEYreUWFzYAo7Xc4sIGYLSWW1zYAIzWcosLG4DRWm5xYQMwWsstLmwARmu5xYUNwGgtt7iwARit5RYXNgCjtdziwgZgtJZbXNgAjNZyiwsbgNFabnFhAzBayy0ubABGa7nFhQ3AaC23uLABGK3lFhc2AKO13OLCBmC0lltc2ACM1nKLCxuA0VpucWEDMFrLLS5sAEZrucWFDcBoLbe4sAEYreUWFzYAo7Xc4sIGYLSWW1zYAIzWcosLG4DRWm5xYQMwWsstLmwARmu5xYUNwGgtt7iwARit5RYXNgCjtdziwgZgtJZbXNgAjNZyiwsbgNFabnFhAzBayy0ubABGa7nFhQ3AaC23uLABGK3lFhc2AKO1XDjuAzSVdQHjw9cYAAAAAElFTkSuQmCC"},
#                                              None, f"\"{id}\"", False, False, False, 3]}))
#
# resp = ws.recv()
#
# while "process_completed" not in resp:
#     resp = ws.recv()
#     sleep(0.001)
#
# print(hash)
#
# temp = {
#     "sec-ch-ua": '"Chromium";v="103", ".Not/A)Brand";v="99"',
#     "sec-ch-ua-mobile": "?0",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36",
#     "sec-ch-ua-platform": '"Linux"',
#     "Content-Type": "application/json",
#     "Accept": "*/*",
#     "Origin": "http://localhost:7860",
#     "Sec-Fetch-Site": "same-origin",
#     "Sec-Fetch-Mode": "cors",
#     "Sec-Fetch-Dest": "empty",
#     "Referer": "http://localhost:7860/",
#     "Accept-Encoding": "gzip, deflate",
#     "Accept-Language": "en-US,en;q=0.9",
#     "Connection": "close"
#
# }
#
# # its an issue with my values
#
# payload = {"fn_index": 53, "data": [], "session_hash": hash}
# json_resp = httpx.post("http://localhost:7860/api/predict/", headers=temp, json=payload).json()
#
# id = json_resp["data"][0][1:][:-1]
# print(id)
#
# payload = {"fn_index": 34, "data": [f"\"{id}\""], "session_hash": hash}
#
# print(httpx.post("http://localhost:7860/api/predict/", headers=temp, json=payload).text)
#
# payload = {"fn_index": 33, "data": [f"\"{id}\""], "session_hash": hash}
# print(httpx.post("http://localhost:7860/api/predict/", headers=temp, json=payload).text)