# -*- coding: utf-8 -*-

"""
VMU Icon Editor (48x32) - Version 0.1
Author: Neoblast
Description:
This python application provides a VERY simple LCD editor to create monochrome 48x32 pixel LCD images for the Sega Dreamcast's VMU (Visual Memory Unit) to use in homebrew projects with KOS.
Users can draw on the canvas, save the icon as a C array, and clear the canvas.

Usage: 

Left click on a pixel to paint it.
Right click on a pixel to erase it.

Drag the left click over the canvas to paint the selected pixels.
Drag the right click over the canvas to erase the selected pixels.

Press on any of the buttons to copy the C array to the clipboard or as a header file to use in projects.

Features:
- Draw and erase pixels on a 48x32 grid
- Save the current icon as a C array that can be used in projects
- Clear the entire canvas

Note:
The icon is saved as a C array in a format suitable for the VMU screen. The data is generated row by row, reversing both the bits in each byte and the byte order.
"""


import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

class IconEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("VMU LCD Icon Editor")
        self.canvas_width = 48
        self.canvas_height = 32
        self.pixel_size = 10
        self.pixels = [[0 for _ in range(self.canvas_width)] for _ in range(self.canvas_height)]

        self.canvas = tk.Canvas(root, width=self.canvas_width * self.pixel_size, height=self.canvas_height * self.pixel_size, bg="white")
        self.canvas.pack()

        # Bind canvas events for drawing and erasing
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<Button-3>", self.on_canvas_right_click)
        self.canvas.bind("<B3-Motion>", self.on_canvas_right_drag)

        # Buttons for saving and clearing the canvas
        self.save_button = tk.Button(root, text="Save as C Array", command=self.save_as_c_array)
        self.save_button.pack()

        self.save_file_button = tk.Button(root, text="Save as .h File", command=self.save_as_file)
        self.save_file_button.pack()

        self.clear_button = tk.Button(root, text="Clear Canvas", command=self.clear_canvas)
        self.clear_button.pack()

        self.draw_grid()

    def draw_grid(self):
        # Draw the initial grid on the canvas
        for y in range(self.canvas_height):
            for x in range(self.canvas_width):
                x1 = x * self.pixel_size
                y1 = y * self.pixel_size
                x2 = x1 + self.pixel_size
                y2 = y1 + self.pixel_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="gray", fill="white")

    def on_canvas_click(self, event):
        # Handle pixel painting on left click
        self.paint_pixel(event.x, event.y)

    def on_canvas_drag(self, event):
        # Handle pixel painting when dragging with left click
        self.paint_pixel(event.x, event.y)

    def on_canvas_right_click(self, event):
        # Handle pixel erasing on right click
        self.erase_pixel(event.x, event.y)

    def on_canvas_right_drag(self, event):
        # Handle pixel erasing when dragging with right click
        self.erase_pixel(event.x, event.y)

    def paint_pixel(self, x, y):
        # Paint a pixel at the given canvas coordinates
        x = x // self.pixel_size
        y = y // self.pixel_size
        if 0 <= x < self.canvas_width and 0 <= y < self.canvas_height:
            if self.pixels[y][x] == 0:
                self.pixels[y][x] = 1
                color = "black"
                x1 = x * self.pixel_size
                y1 = y * self.pixel_size
                x2 = x1 + self.pixel_size
                y2 = y1 + self.pixel_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="gray", fill=color)

    def erase_pixel(self, x, y):
        # Erase a pixel at the given canvas coordinates
        x = x // self.pixel_size
        y = y // self.pixel_size
        if 0 <= x < self.canvas_width and 0 <= y < self.canvas_height:
            if self.pixels[y][x] == 1:
                self.pixels[y][x] = 0
                color = "white"
                x1 = x * self.pixel_size
                y1 = y * self.pixel_size
                x2 = x1 + self.pixel_size
                y2 = y1 + self.pixel_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="gray", fill=color)

    def bit_reverse(self, value):
        # Reverse the bits in a byte
        return int('{:08b}'.format(value)[::-1], 2)

    def save_as_c_array(self):
        # Generate the C array representation of the icon
        byte_array = []
        for y in range(self.canvas_height):
            row_bytes = []
            for x_byte in range(0, self.canvas_width, 8):
                byte = 0
                for i in range(8):
                    if x_byte + i < self.canvas_width and self.pixels[y][x_byte + i] == 1:
                        byte |= (1 << (7 - i))
                row_bytes.append(self.bit_reverse(byte))  # Reverse the bits of each byte
            byte_array.extend(row_bytes[::-1])  # Reverse the order of bytes for the row

        # Create the C array string
        c_array = "unsigned char icon[] = {"
        for i, byte in enumerate(byte_array):
            if i % 6 == 0:
                c_array += "\n    "
            c_array += "0x%02X, " % byte
        c_array = c_array.rstrip(', ') + ',\n};'

        # Copy the C array to the clipboard and show a message
        self.root.clipboard_clear()
        self.root.clipboard_append(c_array)
        self.root.update()  # Keep the content in the clipboard
        messagebox.showinfo("C Array", "The array has been generated and copied to the clipboard.")

    def save_as_file(self):
        # Generate the C array representation of the icon
        byte_array = []
        for y in range(self.canvas_height):
            row_bytes = []
            for x_byte in range(0, self.canvas_width, 8):
                byte = 0
                for i in range(8):
                    if x_byte + i < self.canvas_width and self.pixels[y][x_byte + i] == 1:
                        byte |= (1 << (7 - i))
                row_bytes.append(self.bit_reverse(byte))  # Reverse the bits of each byte
            byte_array.extend(row_bytes[::-1])  # Reverse the order of bytes for the row

        # Create the C array string
        c_array = "unsigned char icon[] = {"
        for i, byte in enumerate(byte_array):
            if i % 6 == 0:
                c_array += "\n    "
            c_array += "0x%02X, " % byte
        c_array = c_array.rstrip(', ') + ',\n};'

        # Save the C array to a file
        file_path = filedialog.asksaveasfilename(defaultextension=".h", filetypes=[("Header files", "*.h")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(c_array)
            messagebox.showinfo("Save File", "The file has been saved as .h file.")

    def clear_canvas(self):
        # Clear the canvas and reset the pixel grid
        self.pixels = [[0 for _ in range(self.canvas_width)] for _ in range(self.canvas_height)]
        self.canvas.delete("all")
        self.draw_grid()

if __name__ == "__main__":
    root = tk.Tk()
    app = IconEditor(root)
    root.mainloop()
