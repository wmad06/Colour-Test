import tkinter as tk
import random

# Constants
NUMBER_OF_BOXES_WIDE = 2
NUMBER_OF_BOXES_TALL = 2
VERTICAL_PADDING = 10
HORIZONTAL_PADDING = 10
BOX_WIDTH = 100
BOX_HEIGHT = 100
HORIZONTAL_BOX_SPACING = 20
VERTICAL_BOX_SPACING = 20
TEST_COLOURS = [
   "#FFFF00",
   "#FF0000",
   "#00FF00",
   "#0000FF",
]
# Calculated constants
rootWidth = HORIZONTAL_PADDING*2 + BOX_WIDTH*NUMBER_OF_BOXES_WIDE + HORIZONTAL_BOX_SPACING*(NUMBER_OF_BOXES_WIDE-1)
rootHeight = VERTICAL_PADDING*2 + BOX_HEIGHT*NUMBER_OF_BOXES_TALL + VERTICAL_BOX_SPACING*(NUMBER_OF_BOXES_TALL-1)
rootGeometry = f"{rootWidth}x{rootHeight}"
# End constants

# function definition
def on_click(event):
   clicked_id = canvas.find_withtag("current")[0]
   canvas.itemconfig(clicked_id, fill = random_colour())
   print(clicked_id)
   print(event)

def random_colour():
   r = random.randint(0,255)
   g = random.randint(0,255)
   b = random.randint(0,255)

   return f"#{r:02x}{g:02x}{b:02x}"
   # RGB = f"#{r:02x}{g:02x}{b:02x}" 
   # print(RGB)
   # return(RGB)

root = tk.Tk()

root.title ("Colour Test")
root.geometry(rootGeometry)

canvas = tk.Canvas(root, bg="white")
canvas.pack(fill="both", expand=True)

boxes = []
for i in range(NUMBER_OF_BOXES_TALL):
   boxes.append([])
   for j in range(NUMBER_OF_BOXES_WIDE):
    boxes[i].append(canvas.create_rectangle(
        HORIZONTAL_PADDING + BOX_WIDTH*j + HORIZONTAL_BOX_SPACING*j,
        VERTICAL_PADDING + BOX_HEIGHT*i + VERTICAL_BOX_SPACING*i,
        HORIZONTAL_PADDING + BOX_WIDTH*(j+1) + HORIZONTAL_BOX_SPACING*j,
        VERTICAL_PADDING + BOX_HEIGHT*(i+1) + VERTICAL_BOX_SPACING*i,
        fill = "#FF0000",
        outline= "black"
    ))

for i in range(NUMBER_OF_BOXES_TALL):
  for j in range(NUMBER_OF_BOXES_WIDE):
    canvas.tag_bind(boxes[i][j], "<Button-1>", on_click)


root.mainloop()

# end
