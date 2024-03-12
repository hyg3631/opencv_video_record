import cv2
import tkinter as tk
from PIL import Image, ImageTk

def on_button_click():
    print("Button clicked!")

def show_frame():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(frame)
        panel.img = frame
        panel.config(image=frame)
    panel.after(10, show_frame)

root = tk.Tk()
root.title("OpenCV with Tkinter")

rtsp_url = 'rtsp://210.99.70.120:1935/live/cctv005.stream'
cap = cv2.VideoCapture(rtsp_url)

panel = tk.Label(root)
panel.pack(padx=10, pady=10)

button = tk.Button(root, text="Click me!", command=on_button_click)
button.pack(padx=10, pady=10)

show_frame()
root.mainloop()

cap.release()
