import cozmo
import socket
from socket import error as socket_error
from cozmo.objects import LightCube1Id
import asyncio
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
from PIL import Image, ImageOps, ImageDraw, ImageFont
import cv2
import numpy as np
import time
import logging

SLEEP_DURATION = 0.1
card = []
card_to_value = {
        "A": 11,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 10,
        "Q": 10,
        "K": 10,
    }

def send(self, ip: str = "10.0.1.10", port: int = 5000, table_num = 1, card_num = 1):
    server_socket = socket.socket()

    try:
        server_socket.connect((ip, port))
    except Exception as e:
        logging.error(f"Unable to connect to socket! \n {e}")
        return
    #Fix this to format message correctly
    message = f'Table{table_num};Dylan;{card_num};{card_to_value[card[0]]}'
    server_socket.sendall(bytes(message, "ascii"))
    server_socket.close()

def processQRCode(robot: cozmo.robot.Robot, message: str) -> None:
    # Add image to hand
    card = message.split(';')

    # Get face image
    image_path = f"./images/{message.replace(';','')}_face.png"

    # Read in face image
    raw_image = Image.open(image_path)
    print("####### Loaded Image")
    # Resize and convert image to something Cozmo can display
    resized_image = raw_image.resize(cozmo.oled_face.dimensions(), Image.BICUBIC)
    resized_image = ImageOps.invert(resized_image)
    face_image = cozmo.oled_face.convert_image_to_screen_data(
        resized_image, invert_image=True
    )
    print("####### Formatted Image")

def lookForCards( robot: cozmo.robot.Robot, card_num = 1, table_num = 1):
    # Turn on camera
    robot.camera.image_stream_enabled = True
    robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()

    # Instantiate QR code detector
    detector = cv2.QRCodeDetector()

    # Look for codes
    while True:
        # Get current image
        image = robot.world.latest_image

        if image is not None:
            # Check for qr codes
            code_detected, decoded_string, _, _ = detector.detectAndDecodeMulti(
                np.array(image.raw_image)
            )

            # If a qr code was detected, then process it
            if code_detected and decoded_string[0] != "":
                processQRCode(robot, decoded_string[0])
                break
        
        time.sleep(SLEEP_DURATION)

    print("####### Has complete hand")

    ## Send out message with cards
    try:
        send(table_num=table_num, card_num=card_num)
        print("###### Sent message")
    except:
        pass

    return card_to_value[card[0]]