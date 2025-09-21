import os
import tkinter as tk
from tkinter import filedialog, Label, Button
from PIL import Image, ImageTk

downloads = os.path.join(os.path.expanduser("~"), "Downloads")

root = tk.Tk()
root.title("RGB Channel Adjuster")

# User opens file from directory
def openFile():
    filepath = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"), ("All files", "*.*")]
    )
    return filepath
    
def clamp(newVal, minVal, maxVal):
    return max(minVal, min(newVal, maxVal))

def prog(filepath):
    for widget in root.winfo_children():
        widget.destroy()
    MAX_WIDTH, MAX_HEIGHT = 600, 600

    img = Image.open(filepath).convert("RGB")
    img.thumbnail((MAX_WIDTH, MAX_HEIGHT), Image.LANCZOS)

    tkImg = ImageTk.PhotoImage(img)

    label = Label(root, image=tkImg)
    label.image = tkImg
    label.pack()

    def onSelect(): 
        newImage = openFile()
        if newImage:
            prog(newImage)

    btn = Button(root, text="Select File", command=onSelect)
    btn.pack()

    redSlider = tk.Scale(root, from_=0.0, to=2.0, resolution=0.01, orient="horizontal", label="Red")
    redSlider.set(1.0)
    redSlider.pack()

    greenSlider = tk.Scale(root, from_=0.0, to=2.0, resolution=0.01, orient="horizontal", label="Green")
    greenSlider.set(1.0)
    greenSlider.pack()

    blueSlider = tk.Scale(root, from_=0.0, to=2.0, resolution=0.01, orient="horizontal", label="Blue")
    blueSlider.set(1.0)
    blueSlider.pack()

    def updateImage(*args):
        redMult = redSlider.get()
        greenMult = greenSlider.get()
        blueMult = blueSlider.get()

        r, g, b = img.split()

        r = r.point(lambda i: clamp(i * redMult, 0, 255))
        g = g.point(lambda i: clamp(i * greenMult, 0, 255))
        b = b.point(lambda i: clamp(i * blueMult, 0, 255))

        new_img = Image.merge("RGB", (r, g, b))
        tk_new = ImageTk.PhotoImage(new_img)

        label.config(image=tk_new)
        label.image = tk_new

    # Sliders use updateImage
    redSlider.config(command=updateImage)
    greenSlider.config(command=updateImage)
    blueSlider.config(command=updateImage)


if __name__ == "__main__":
    filepath = openFile()
    if filepath:
        prog(filepath)
        root.mainloop()
