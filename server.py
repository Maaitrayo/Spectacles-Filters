import cv2
import numpy as np
from PIL import Image
from datetime import datetime
from flask import Flask, request, render_template
import os

app = Flask(__name__)


face = cv2.CascadeClassifier('Model/haarcascade_frontalface_default.xml')
glasses_folder_path = "static\specs"
specs = os.listdir(glasses_folder_path)

def put_glass(glass, fc, x, y, w, h, save_path, count, glass_filters_face):
    face_width = w
    face_height = h

    hat_width = face_width + 1
    hat_height = int(0.40 * face_height) + 1

    glass = cv2.resize(glass, (hat_width, hat_height))

    
    count+=1
    print(fc.shape)
    for i in range(hat_height):
        for j in range(hat_width):
            if glass[i][j][0] not in [0, 255]:
                fc[y + i - int(-0.20 * face_height)][x + j] = glass[i][j]
    # print("ok")
    glass_filters_face.append(fc)
    print(len(glass_filters_face))
    print(f"count: {count}")

    cv2.imwrite(save_path, fc)


def create_spec_filters(save_folder, uploaded_img_path):
    image_arr = cv2.imread(uploaded_img_path)
    
    gray = cv2.cvtColor(image_arr, cv2.COLOR_BGR2GRAY)
    fl = face.detectMultiScale(gray,1.19,7)
    x, y, w, h = fl[0]
    # print(fl)
    # for spec in specs:
    count = 0
    print(len(specs))
    glass_filters_face = []

    for i in range(len(specs)):
        glass_path = os.path.join(glasses_folder_path, specs[i])
        glass = cv2.imread(glass_path)
        glass_save_path = os.path.join(save_folder, specs[i])

        image_arr = cv2.imread(uploaded_img_path)
        put_glass(glass, image_arr, x, y, w, h, glass_save_path, count, glass_filters_face)

    cv2.waitKey(0)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        file = request.files["query_img"]

        img =  Image.open(file.stream)
        uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":",".") + "_" + file.filename
        img.save(uploaded_img_path)
        
        processed_path = os.path.join('static/processed', datetime.now().isoformat().replace(":",".") + "_" + file.filename.split('.')[0])
        os.makedirs(processed_path)

        query = create_spec_filters(processed_path, uploaded_img_path)

        scores = [os.path.join(processed_path, image) for image in os.listdir(processed_path)]
        print(scores)

        for score in scores:
            print(score)

        return render_template("index.html", query_path=uploaded_img_path, scores=scores)
    else:
        return render_template("index.html")


if __name__ == "__main__":
    # app.run()
    app.run(host='192.168.0.102', port=5000)