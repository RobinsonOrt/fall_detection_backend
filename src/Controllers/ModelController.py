from Controllers.EmployeeController import get_employee_phones
from flask import Response
import torch
import argparse
import io
from PIL import Image
import cv2
import numpy as np
import winsound
import pywhatkit
from Server import app
from datetime import datetime, timedelta

import os
from twilio.rest import Client

account_sid = ''#insert account ssid
auth_token = ''#insert auth token
client = Client(account_sid, auth_token)
# print("?==================================00")
parser = argparse.ArgumentParser(
    description="Flask app exposing yolov5 models")
parser.add_argument("--port", default=5000, type=int, help="port number")
args = parser.parse_args()


# custom/local model  # force_reload = recache latest code
model = torch.hub.load('ultralytics/yolov5', 'custom', 'best.pt')

model.eval()

def getVideo():
    vidcap = cv2.VideoCapture('test.mp4')
    success,frame = vidcap.read()
    while success:
        print("Read a new frame: ", success)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame1 = buffer.tobytes()
        img = Image.open(io.BytesIO(frame1))
        results = model(img)
        im = results.render()

        arr = np.array(im)
        coef = np.array(arr).ravel()
        # resize coef to 640x480 rgb
        coef = coef.reshape(1080, 1920, 3)
        # the coef is in BGR format, convert to RGB
        coef = cv2.cvtColor(coef, cv2.COLOR_BGR2RGB)
        ret, buffer = cv2.imencode('.jpg', coef)

        frame1 = buffer.tobytes()
        yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame1 + b'\r\n')  # concat frame one by one and show result




def getCamera():
    count = 0
    time = datetime.utcnow()
    camera = cv2.VideoCapture(1)
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame1 = buffer.tobytes()
            img = Image.open(io.BytesIO(frame1))
            results = model(img)
            classId = results.pandas().xyxy[0]['class']

            # results.ims # array of original images (as np array) passed to model for inference
            im = results.render()

            arr = np.array(im)
            coef = np.array(arr).ravel()
            # resize coef to 640x480 rgb
            coef = coef.reshape(480, 640, 3)
            # the coef is in BGR format, convert to RGB
            coef = cv2.cvtColor(coef, cv2.COLOR_BGR2RGB)

            # convert to jpg
            ret, buffer = cv2.imencode('.jpg', coef)

            frame1 = buffer.tobytes()
            if datetime.utcnow() > time:
                try:
                    if classId[0] == 0:
                        count += 1
                        print(count)
                        if count == 15:
                            with app.app_context():
                                employees = get_employee_phones()
                            for employee in employees:
                                #print("+57" + employee['phone'])
                                #pywhatkit.sendwhatmsg_instantly("+57" + employee['phone'], "Hola " + employee['name'] + " " + employee['last_name'] + " se ha detectado una victima de caída, por favor acudir inmediatamente.")
                                message = client.messages.create(
                                    from_='whatsapp:+14155238886',
                                    body="Hola " + employee['name'] + " " + employee['last_name'] + " se ha detectado una victima de caída, por favor acudir inmediatamente.",
                                    to='whatsapp:+57' + employee['phone']
                                )
                                frequency = 2500  # Set Frequency To 2500 Hertz
                                duration = 60000  # Set Duration To 1000 ms == 1 second
                                winsound.Beep(frequency, duration)
                                print("enviado a " + employee['name'] + " " + employee['last_name'])
                            print("enviado")
                            time = datetime.utcnow() + timedelta(minutes=1)
                            count = 0

                        """ with app.app_context():
                            
                            employees = get_employee_phones()
                        print(employees[0]['name'])
                        for employee in employees:
                            #pywhatkit.sendwhatmsg_instantly("+57" + employee['phone'], "Hola " + employee['name'] + " " + employee['last_name'] + " se ha detectado una victima de caída, por favor acudir inmediatamente.")
                            message = client.messages.create(
                                messaging_service_sid='MGc5c39f83ec12779d1e5f9c2a7ca16aa6',
          
                                body="Hola " + employee['name'] + " " + employee['last_name'] + " se ha detectado una victima de caída, por favor acudir inmediatamente.",
                                to='+57' + employee['phone']
                            )
                            #pywhatkit.sendwhatmsg_instantly("+57" + employee['phone'], "Hola " + employee['name'] + " " + employee['last_name'] + " se ha detectado una victima de caída, por favor acudir inmediatamente.")
                            #pywhatkit.sendwhats_image("+57" + employee['phone'], buffer, "Hola " + employee['name'] + " " + employee['last_name'] + " se ha detectado una victima de caída, por favor acudir inmediatamente.")

                        # create a count for next 60 seconds """

                        #print(" Falled Person, call ambulance")

                except IndexError:
                    print("No class detected")
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame1 + b'\r\n')  # concat frame one by one and show result


def predict():
    video = Response(
        getCamera(), mimetype='multipart/x-mixed-replace; boundary=frame')
        #getVideo(), mimetype='multipart/x-mixed-replace; boundary=frame')
    return video
