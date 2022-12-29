import unittest
import cv2
import numpy as np
import face_recognition

from src.main.python.AttendanceProject import markattendance, cap, classNames, photos, findencodings
import src.main.python.AttendanceProject

class TestAttendanceMarking(unittest.TestCase):
    def setUp(self):
        # Set up test data by adding a known face to the list of photos
        self.test_image = cv2.imread('test.jpg')
        photos.append(self.test_image)
        classNames.append('Test Person')
        self.encodelistknown = findencodings(photos)

    def test_markattendance(self):
        # Test that the markattendance function adds an entry to the Attendance.csv file
        markattendance('Test Person')
        with open('Attendance.csv', 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 2)  # there should be 2 lines in the file (1 header, 1 entry)
            self.assertEqual(lines[1].split(',')[0], 'Test Person')

    def test_face_recognition(self):
        # Test that the face recognition correctly identifies the known face
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(self.encodelistknown, encodeFace)
            faceDis = face_recognition.face_distance(self.encodelistknown, encodeFace)
            matchIndex = np.argmin(faceDis)
            self.assertLess(faceDis[matchIndex], 0.60)
            self.assertEqual(classNames[matchIndex], 'Test Person')

if __name__ == '__main__':
    unittest.main()
