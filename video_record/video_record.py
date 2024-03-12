import numpy as np
import cv2 as cv
import datetime
import os
import time
import tkinter as tk
from PIL import Image, ImageTk

video = cv.VideoCapture('rtsp://210.99.70.120:1935/live/cctv005.stream')
speed_table = [1/10, 1/8, 1/4, 1/2, 1, 2, 3, 4, 5, 8, 10]
speed_index = 4
fps = video.get(cv.CAP_PROP_FPS)
wait_msec = int(1/fps*1000)
overlay_image = cv.imread('camera.png', cv.IMREAD_UNCHANGED)

def on_button_click():
    print("Button clicked!")

def videowrite():
    #현재시간 가져오기
    currentTime = datetime.datetime.now()
    
    # 웹캠 설정
    video.set(3, 800)  # 영상 가로길이 설정
    video.set(4, 600)  # 영상 세로길이 설정
    
    # 가로 길이 가져오기
    streaming_window_width = int(video.get(3))
    # 세로 길이 가져오기
    streaming_window_height = int(video.get(4))
    
    #현재 시간을 '년도 달 일 시간 분 초'로 가져와서 문자열로 생성
    fileName = str(currentTime.strftime('%Y_%m_%d_%H_%M_%S'))
    
    #파일 저장하기 위한 변수 선언
    path = f'C:\\Users\\홍윤기\\Desktop\\컴퓨터비전\\{fileName}.mp4'

    fourcc = cv.VideoWriter_fourcc(*'XVID')
    
    #비디오 저장
    #cv2.VideoWriter(저장 위치, 코덱, 프레임, (가로, 세로))
    out = cv.VideoWriter(path, fourcc, fps, (streaming_window_width, streaming_window_height))

    print("record mode")

    overlay_image = cv.imread('recode.png', cv.IMREAD_UNCHANGED)
    
    while video.isOpened():
        ret, frame = video.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        if overlay_image is not None:
            # 추가할 이미지 크기 변경
            overlay_image_resized = cv.resize(overlay_image, (100, 100))
            # RTSP 스트리밍 프레임에 이미지 추가
            x_offset = 300  # 이미지가 추가될 x 좌표
            y_offset = min(350, frame.shape[0] - overlay_image_resized.shape[0])  # 이미지가 추가될 y 좌표
            alpha_s = overlay_image_resized[:, :, 3] / 255.0
            alpha_l = 1.0 - alpha_s
            for c in range(0, 3):
                frame[y_offset:y_offset + overlay_image_resized.shape[0], x_offset:x_offset + overlay_image_resized.shape[1], c] = \
                    (alpha_s * overlay_image_resized[:, :, c] + alpha_l * frame[y_offset:y_offset + overlay_image_resized.shape[0],
                                                                      x_offset:x_offset + overlay_image_resized.shape[1], c])
                
        cv.putText(frame, f"FPS: {int(fps)}", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv.imshow('frame', frame)
        out.write(frame)
        key = cv.waitKey(max(int(wait_msec/speed_table[speed_index]),1))
        if key == 27:
            out.release()
            break

def videoread():
    
    while video.isOpened():
        ret, frame = video.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        if overlay_image is not None:
            # 추가할 이미지 크기 변경
            overlay_image_resized = cv.resize(overlay_image, (100, 100))
            # RTSP 스트리밍 프레임에 이미지 추가
            x_offset = 300  # 이미지가 추가될 x 좌표
            y_offset = min(350, frame.shape[0] - overlay_image_resized.shape[0])  # 이미지가 추가될 y 좌표
            alpha_s = overlay_image_resized[:, :, 3] / 255.0
            alpha_l = 1.0 - alpha_s
            for c in range(0, 3):
                frame[y_offset:y_offset + overlay_image_resized.shape[0], x_offset:x_offset + overlay_image_resized.shape[1], c] = \
                    (alpha_s * overlay_image_resized[:, :, c] + alpha_l * frame[y_offset:y_offset + overlay_image_resized.shape[0],
                                                                      x_offset:x_offset + overlay_image_resized.shape[1], c])
            
        cv.putText(frame, f"FPS: {int(fps)}", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv.imshow('RTSP Stream', frame)

        key = cv.waitKey(max(int(wait_msec/speed_table[speed_index]),1))
        if key == 27:
            break
        elif key == ord('r') or key == ord('R'):
            cv.destroyAllWindows()
            videowrite()
            break
    
    video.release()
    cv.destroyAllWindows()
    

videoread()
