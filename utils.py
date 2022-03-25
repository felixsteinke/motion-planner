from tkinter import ttk

def setBackgroundColor(frame, color):
    style = ttk.Style()     # Create style
    style.configure("A.TFrame", background=color) # Set bg color
    frame.config(style='A.TFrame')    # Apply style to widget


def isPixelWhite(pixel):
    if pixel[0]==255:
        if pixel[1]==255:
            if pixel[2]==255:
                return True
    return False