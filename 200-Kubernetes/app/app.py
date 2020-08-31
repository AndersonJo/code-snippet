from tempfile import gettempdir

import cv2
import numpy as np
from flask import Flask, request, jsonify
from keras.models import load_model

app = Flask(__name__)
model = load_model('fasion_model.h5')


@app.route('/')
def hello_world():
    return 'Hello! Anderson!'


@app.route('/predict', methods=['POST'])
def predict():
    tmp_dir = gettempdir()
    f = request.files["image"]
    f.save(tmp_dir + '/img.jpg', cv2.IMREAD_COLOR)
    img = cv2.imread(tmp_dir + '/img.jpg', cv2.IMREAD_COLOR)[:, :, 0]
    img = np.expand_dims(img, axis=0)
    pred_y = model.predict(img)[0]
    pred_label = int(np.argmax(pred_y))
    prob = float(pred_y[pred_label])
    return jsonify({'prediction': pred_label, 'prob': prob})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
