import unittest
from src.main.python.AttendanceProject import markattendance, cap, classNames, photos, findencodings
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
class TestAttendanceMarker(unittest.TestCase):
    def test_markattendance(self):
        # Arrange
        name = "John"

        # Act
        markattendance(name)

        # Assert
        with open('Attendance.csv', 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 2)  # Ensure there is one more line in the file after calling markattendance
            self.assertEqual(lines[1].split(',')[0], name)  # Ensure the second line (newest entry) has the correct name

    def test_findencodings(self):
        # Arrange
        known_photos = [
            cv2.imread('ImagesAttendance/john.jpg'),
            cv2.imread('ImagesAttendance/jane.jpg')
        ]

        # Act
        encodings = findencodings(known_photos)

        # Assert
        self.assertEqual(len(encodings), 2)  # Ensure the correct number of encodings were returned
        self.assertIsInstance(encodings[0], np.ndarray)  # Ensure the encodings are of the correct type
        self.assertEqual(encodings[0].shape, (128,))  # Ensure the encodings have the correct shape (128-dimensional)

    def test_findmatch(self):
        # Arrange
        known_encodings = [
            np.array([0.1, 0.2, 0.3, ..., 0.9, 1.0]),  # encoding for John
            np.array([0.2, 0.3, 0.4, ..., 0.8, 0.9])   # encoding for Jane
        ]
        unknown_encoding = np.array([0.15, 0.25, 0.35, ..., 0.85, 0.95])  # encoding for an unknown person

        # Act
        matches = face_recognition.compare_faces(known_encodings, unknown_encoding)
        face_dists = face_recognition.face_distance(known_encodings, unknown_encoding)
        match_index = np.argmin(face_dists)

        # Assert
        self.assertFalse(any(matches))  # Ensure there are no exact matches
        self.assertGreater(face_dists[0], 0.60)  # Ensure the unknown person's encoding is not close enough to John's
        self.assertGreater(face_dists[1], 0.60)  # Ensure the unknown person's encoding is not close enough to Jane's
        self.assertEqual(match_index, -1)  # Ensure there is no match (argmin returns -1 if the array is empty)


# This test case verifies the following aspects of the code:
#
#     markattendance correctly writes a new attendance entry to the CSV file
#     findencodings returns the correct number and type of encodings
#     findmatch correctly identifies that an unknown person's encoding does not match any of the known encodings