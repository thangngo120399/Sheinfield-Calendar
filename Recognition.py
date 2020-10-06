import cv2
import numpy as np
import sqlite3
import os
from PIL  import Image
from datetime import datetime
from playsound import playsound
from gtts import gTTS
import array
import xlwt

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.read("D:\\Documents Try\\Python\\Face_Projet\\Example\\recognizer\\trainningData.yml")
arr1 =  array.array('i',[0])
wb = xlwt.Workbook()
ws = wb.add_sheet("A test")
ws.write(0, 0, 'Mã SV')
ws.write(0, 1, 'Tên SV')
ws.write(0, 2, 'Thời gian')
columm=0
search = 0
cap = cv2.VideoCapture(0)
fontface: int = cv2.FONT_HERSHEY_SIMPLEX
check = 0;
def inputA ():
    name = input('Enter name: ')
    return name
course = inputA()
def getProfile(id):
	conn = sqlite3.connect("D:\\Documents Try\\Python\\Face_Projet\\Example\\data.db")
	query = "SELECT * FROM people WHERE ID =" + str(id)
	cursor = conn.execute(query)

	profile = None
	for row in cursor:
		profile = row

	conn.close()
	return profile
def process(id,name,column):
	arr1.insert(len(arr1) - 1, id)
	print(name)
	now = datetime.now()
	dt_string = now.strftime("%H:%M:%S")
	dt_course = now.strftime("%d/%m/%Y")
	print("Ngay va gio hien tai =", dt_string)
	playsound('D:\\Documents Try\\Python\\Face_Projet\\Example\\dataSetAudio\\' + str(id) + '.mp3')
	column = column + 1
	ws.write(column, 0, id)
	ws.write(column, 1, name)
	ws.write(column, 2, dt_string)
	# wb.save(nameOfCourse +"_"+dt_course+ ".xls")
	wb.save("writing.xls")
	return column
# input()
while True:
	ret, frame = cap.read()

	frame= cv2.flip(frame,1)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray)
	for (x, y, w, h) in faces:
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 225, 0), 2)
		roi_gray = gray[y: y + h, x: x + w]
		id, confidence = recognizer.predict(roi_gray)
		if confidence < 40:
			profile = getProfile(id)
			if profile is not None:
				cv2.putText(frame, "" + str(profile[1]), (x + 10, y + h + 30), fontface, 1, (0, 255, 0), 2)
				check += 1
		else:
			cv2.putText(frame, "Unknow", (x + 10, y + h + 30), fontface, 1, (0, 0, 255), 2)


	cv2.imshow("Recognitting", frame)

	if cv2.waitKey(1) == ord('q'):
		break
	if check >0:
		for i in arr1:
			if (i == profile[0]):
				search = 1
				break
			else:
				search = 0
		if search == 0:
			columm=process(profile[0],str(profile[1]),columm)
			check = 0

cap.release()
cv2.destroyAllWindows()

