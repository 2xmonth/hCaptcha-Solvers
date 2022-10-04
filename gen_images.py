from time import sleep
import websocket
import base64
import httpx
import json
import cv2
import os

ua = "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"


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

    headers = {
        
        "User-Agent": ua,
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "http://localhost:7860/",
        "Content-Type": "application/json",
        "Origin": "http://localhost:7860",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
        
    }    

    print(httpx.post("http://localhost:7860/api/predict/", headers=headers, timeout=None, json={"fn_index": 34, "data": ["\"95556fc0be444c3c99504fbe54bfa3f6\""], "session_hash": "5mhfkx2ueug"}).text)
    print(httpx.post("http://localhost:7860/api/predict/", headers=headers, timeout=None, json={"fn_index": 33, "data": ["\"95556fc0be444c3c99504fbe54bfa3f6\""], "session_hash": "5mhfkx2ueug"}).text)



for prompt in open("prompts.txt"):
    try:
        for file in os.listdir(f"hcaptcha-imgs/{prompt[:-17]}/"):
            full_file = f"hcaptcha-imgs/{prompt[:-17]}/{file}"
            extract(prompt, 75, 0.74, full_file)
    except FileNotFoundError:
        pass
    print(f"Finished genning images for \"{prompt[:-2]}\"")

