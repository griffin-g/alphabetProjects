# ASCII characters from darkest to lightest
chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'."

import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog, Entry, Button, Label
import numpy as np 

downloads = os.path.join(os.path.expanduser("~"), "Downloads")
output_file = os.path.join(downloads, "asciiconversion.txt")

root = tk.Tk()
root.withdraw()

arr = np.array(list(chars)) 

def openFile():
    filepath = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"), ("All files", "*.*")]
    )
    return filepath
    
def convert(filepath, newWidth=100):
    if not filepath:
        return
    
    filepath = os.path.normpath(filepath)

    try:
        img = Image.open(filepath).convert("L")
    except Exception as e:
        return
    
    width, height = img.size
    aspectRatio = height / width
    newHeight = int(aspectRatio * newWidth)
    img = img.resize((newWidth, newHeight))

    gray = np.array(img)

    ascii_image = []
    for row in gray:
        line = ""
        for pixel in row:
            index = int(pixel / 255 * (len(arr) - 1))
            line += arr[index]
        ascii_image.append(line)
    
    ascii_art = "\n".join(ascii_image)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(ascii_art)
    
    return

def askWidthAndConvert(filepath):
    def callback(P):
        return P.isdigit() or P == ""

    def onSubmit():
        w = entry.get()
        if w.isdigit():
            convert(filepath, int(w))
            win.destroy()

    win = tk.Tk()
    win.title("ASCII Converter")

    Label(win, text="Image Width").pack(pady=(10, 0))

    vcmd = (win.register(callback), "%P")
    entry = Entry(win, validate="key", validatecommand=vcmd)
    entry.pack(pady=5)

    btn = Button(win, text="Convert", command=onSubmit)
    btn.pack(pady=10)

    win.mainloop()

if __name__ == "__main__":
    filepath = openFile()
    if filepath:
        askWidthAndConvert(filepath)
