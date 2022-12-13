from Server import app
from flask import Response
import torch
import argparse
import io
import os
from PIL import Image
import cv2
import numpy as np
import bcrypt
import winsound

from Controllers.RoleController import list_roles
from Controllers.UserController import list_users, login, add_user, modify_user, delete_user
from Controllers.EmployeeController import list_employees, add_employee, delete_employee, modify_employee
from Controllers.ModelController import predict

app.add_url_rule('/users/login', 'login', login, methods=['POST'])
app.add_url_rule('/users', 'list_users', list_users, methods=['GET'])
app.add_url_rule('/users/adduser', 'add_user', add_user, methods=['POST'])
app.add_url_rule('/users/modifyuser', 'modify_user', modify_user, methods=['PUT'])
app.add_url_rule('/users/deleteuser/<user_id>', 'delete_user', delete_user, methods=['DELETE'])


app.add_url_rule('/employees', 'list_employees', list_employees, methods=['GET'])
app.add_url_rule('/employees/addemployee', 'add_employee', add_employee, methods=['POST'])
app.add_url_rule('/employees/modifyemployee', 'modify_employee', modify_employee, methods=['PUT'])
app.add_url_rule('/employees/deleteemployee/<employee_id>', 'delete_employee', delete_employee, methods=['DELETE'])

app.add_url_rule('/predict', 'predict', predict, methods=['GET'])

@app.route('/alarm', methods=['GET'])
def index():
    frequency = 2500  # Set Frequency To 2500 Hertz
    duration = 60000  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)
    return "ok"

if __name__ == '__main__':
    app.run(debug=True)
