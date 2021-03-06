from flask import Flask, jsonify, request, make_response
from PIL import Image
import base64
from werkzeug.utils import secure_filename
# import config
# import demo
import os
import io
import numpy as np
import cv2
import json
import time
import requests
from utils import show_results
from route.app_route import app_route

app = Flask(__name__)
# app.register_blueprint(app_route)


def serve_by_image(threshold, target_height, target_width, maxClsSize,target_features,image):

    """
    ===========================================================
                         build model
    ===========================================================
    """
    img = cv2.resize(image, (target_height, target_width))
    # tmp_images = []
    # tmp_images.append(img)
    # test_images = np.array(tmp_images, dtype=np.float32)

    test_images = np.expand_dims(img,axis=0)
    test_images = test_images/255.0
    test_images = np.array(test_images,dtype=np.float32)
    a=test_images.tolist()
    # Make a request
    data = json.dumps({"instances": test_images.tolist()})
    # print('Data: {} ... {}'.format(data[:50], data[len(data) - 52:]))
    headers = {"content-type": "application/json"}
    start = time.time()
    json_response = requests.post('http://192.168.80.5:8501/v1/models/eye:predict', data=data, headers=headers)
    # json_response = requests.post('http://0.0.0.0:8501/v1/models/eye:predict', data=data, headers=headers)
    print("elapsed time : ", time.time() - start)
    try:
        predictions = json.loads(json_response.text)['predictions']
    except:
        print(json.loads(json_response.text))
    predictions = np.array(predictions)
    # print(predictions)

    result_dict, result_prob_dict,  segmentation_image = \
        show_results.single_image_visual_result(test_images[0], predictions,target_features, threshold)



    return result_dict, result_prob_dict,  segmentation_image




@app.route('/predict', methods=['POST'])
def predict():
    # f = request.files['file']
    # in_memory_file = io.BytesIO()
    # f.save(in_memory_file)
    # data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
    color_image_flag = 1
    a=request
    data=request.form['data']
    imgdata = base64.b64decode(str(data))
    image = Image.open(io.BytesIO(imgdata))
    img = np.array(image)
    # img = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
    # data = np.fromstring(data, dtype=np.uint8)
    # img = cv2.imdecode(data, color_image_flag)
    # cv2.imwrite('/home/serving/alpha/data/test_saved3.png',img)


    threshold = 0.2
    target_height = 512
    target_width = 512
    maxClsSize = 45
    target_features = [1,4,5,26,27,28,29,30,31,32,33]
    print("target_height",target_height)
    result_dict, result_prob_dict,  segmentation_image = serve_by_image(threshold, target_height, target_width, maxClsSize,target_features,img)

    result=dict()
    result['predict']=json.dumps(str(result_dict))
    result['probability']=json.dumps(str(result_prob_dict))

    def myconverter(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        # elif isinstance(obj, datetime.datetime):
        #     return obj.__str__()

    json_object = json.dumps(result, indent=4, default=myconverter, ensure_ascii=False)
    return json_object

@app.route('/',methods=['GET'])
def index():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7014)