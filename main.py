from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
from io import BytesIO
from PIL import Image
import base64
import numpy as np
import numpy as np
import cv2
from image_processing import process

app = Flask('app')
socketio = SocketIO(app)

app.static_folder = 'static'

@app.route('/')
def index():
  return render_template('index.html')

# RASPI ROUTES
@app.route('/rpi/image', methods=['POST'])
def get_image():
 
  file = request.files['image']
  img = Image.open(file.stream)
  img.save('feed.jpg')

  image = cv2.imread('feed.jpg')
  qrCodeDetector = cv2.QRCodeDetector()
  decodedText, points, _ = qrCodeDetector.detectAndDecode(image)

  if points is not None:
    mat = cv2.getPerspectiveTransform(points, np.array([[650, 0], [0, 0], [0, 850], [650, 850]]).astype(np.float32))
    warped = cv2.warpPerspective(image, mat, (650, 850))
    cv2.imwrite('feedwarped.jpg', warped)

    bw = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    
    img = process(bw)
    cv2.imwrite('feedClassified.jpg', img)

  return "received"

app.run(host='0.0.0.0', port=81)