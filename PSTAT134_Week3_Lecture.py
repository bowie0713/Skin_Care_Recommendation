from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import random
from typing import Optional

app = FastAPI() # create a basic api

cat_pic_dir = "images"

if not os.path.exists(cat_pic_dir):
    os.makedirs(cat_pic_dir) # make directory if doesn't exist. prevent application from failing

@app.get("/")
def read_root(): # access root end point
    return {"message": "Welcome to the Cat Pics API. Use /random to get a random picture of our cats!"}

@app.get("/random")
def get_random_image(cat_name: Optional[str] = None):
    image_files = [f for f in os.listdir(cat_pic_dir) if os.path.isfile(os.path.join(cat_pic_dir, f))]

    if cat_name: # did they input one at all. Default is set to None
        cat_name = cat_name.lower()
        if cat_name not in ["gal", "oppie"]:
            raise HTTPException(status_code = 400, detail = "Cat name must be either Gal or Oppie")
        image_files = [f for f in image_files if cat_name in f.lower()]

        if not image_files:
            raise HTTPException(status_code = 404, detail = "No images found")
        
    random_image = random.choice(image_files)
    image_path = os.path.join(cat_pic_dir, random_image)

    html_content = f"""
    <html>
        <head>
            <title> Random Picture of {cat_name if cat_name else 'Our Cats'} </title>
        </head>
        <body>
            <h1> Random Picture of {cat_name if cat_name else 'Our Cats'} </h1>
            <img src = "{image_path}" style = "max-width:30%; height: auto;">
        </body>
    </html>
    """

    return HTMLResponse(content=html_content)
app.mount("/images", StaticFiles(directory = cat_pic_dir), name="images")
        

# make an endpoint
# @app.get("/greet") # make a get request
# def greet():
#     return {"message": "Hello, friend!"}

if __name__ == "__main__": # check if script is being runned
    import uvicorn # python library to load the API
    uvicorn.run(app, host = "127.0.0.1", port = 8000)
