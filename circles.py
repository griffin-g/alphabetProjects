import os
from PIL import Image, ImageDraw, ImageTk
import tkinter as tk
from tkinter import filedialog
import numpy as np

downloads = os.path.join(os.path.expanduser("~"), "Downloads")

root = tk.Tk()
root.title("Circles :)")

tk_img = None  

def openFile():
    filepath = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"), ("All files", "*.*")]
    )
    return filepath

def convert(filepath):
    img = Image.open(filepath).convert("L")
    arr = np.array(img)

    height, width = arr.shape

    display = tk.Label(root)
    display.pack()

    blockSlider = tk.Scale(root, from_=5, to=100, resolution=1, orient="horizontal", label="Block Size")
    blockSlider.set(5)
    blockSlider.pack()

    def updateImage(val=None): 
        blockSize = blockSlider.get()

        heightCrop = height - (height % blockSize)
        widthCrop = width - (width % blockSize)
        cropped = arr[:heightCrop, :widthCrop]

        reshaped = cropped.reshape(heightCrop // blockSize, blockSize,
                                   widthCrop // blockSize, blockSize)
        blockedBrightness = reshaped.mean(axis=(1, 3))

        canvas = Image.new("L", (widthCrop, heightCrop), color=0)
        draw = ImageDraw.Draw(canvas)

        # Draw circles
        for i in range(blockedBrightness.shape[0]):
            for j in range(blockedBrightness.shape[1]):
                brightness = blockedBrightness[i, j]
                diam = (brightness / 255.0) * blockSize
                radius = diam / 2
                cx = j * blockSize + blockSize / 2
                cy = i * blockSize + blockSize / 2
                bbox = [cx - radius, cy - radius, cx + radius, cy + radius]
                draw.ellipse(bbox, fill=255)

        display_w, display_h = 800, 800  
        canvas_resized = canvas.resize((display_w, display_h), Image.LANCZOS)

        # Convert to Tkinter image
        global tk_img
        tk_img = ImageTk.PhotoImage(canvas_resized)
        display.config(image=tk_img)

    updateImage()
    blockSlider.config(command=updateImage)


if __name__ == "__main__":
    filepath = openFile()
    if filepath:
        convert(filepath)
        root.mainloop()
