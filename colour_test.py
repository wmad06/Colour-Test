# Created by Will Madner on 08/10/2026
import tkinter as tk
import random
import math

# Constants
NUMBER_OF_BOXES_WIDE = 2
NUMBER_OF_BOXES_TALL = 2
VERTICAL_PADDING = 10
HORIZONTAL_PADDING = 10
BOX_WIDTH = 100
BOX_HEIGHT = 100
HORIZONTAL_BOX_SPACING = 20
VERTICAL_BOX_SPACING = 20
COLOUR_DISTANCE = 50
TEST_COLOURS = [
   "#FFFF00",
   "#FF0000",
   "#00FF00",
   "#0000FF",
]
# Calculated constants
rootWidth = HORIZONTAL_PADDING*2 + BOX_WIDTH*NUMBER_OF_BOXES_WIDE + HORIZONTAL_BOX_SPACING*(NUMBER_OF_BOXES_WIDE-1)
rootHeight = VERTICAL_PADDING*2 + BOX_HEIGHT*NUMBER_OF_BOXES_TALL + VERTICAL_BOX_SPACING*(NUMBER_OF_BOXES_TALL-1)
rootTestGeometry = f"{rootWidth}x{rootHeight}"
# End constants
# global variables
correct = 0
total = 0
# 

# function definition
def random_colour():
   r = random.randint(0,255)
   g = random.randint(0,255)
   b = random.randint(0,255)

   return f"#{r:02x}{g:02x}{b:02x}"
   # RGB = f"#{r:02x}{g:02x}{b:02x}" 
   # print(RGB)
   # return(RGB)
def start_screen():
   canvas.delete("all")
   root.geometry("400x300")
   start_box = canvas.create_rectangle(
   130, 115,270,185,
   fill = "#FF00BF",
   outline="black",
   width = 2
   )
   start_text = canvas.create_text(
   200, 150,
   text = "START",
   fill = "white",
   font = ("Arial", 20, "bold")
   )
   canvas.tag_bind(start_box, "<Button-1>", run_test)
   canvas.tag_bind(start_text, "<Button-1>", run_test)

def run_test(event):
   canvas.delete("all")
   root.geometry(rootTestGeometry)
   global correct, total
   correct = 0
   total = 0

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
         canvas.tag_bind(boxes[i][j], "<Button-1>", lambda event: on_click(event, boxes))
   randomize_colours(boxes)


def randomize_colours(boxes, base_colour=None):
   if base_colour == None:
      base_colour = random_colour()
   flat_boxes = [box for row in boxes for box in row]
   count = len(flat_boxes)
   global misfit
   misfit = random.randint(0,count-1)

   for i in range(count):
      if i == misfit:
         colour = offset_colour(base_colour, COLOUR_DISTANCE)
      else:
         colour = base_colour
      canvas.itemconfig(flat_boxes[i], fill = colour)

def offset_colour(colour, distance): #takes a given colour and returns a colour with a fixed offset but randomized direction
   rgb = [int(colour[i:i+2], 16) for i in (1,3,5)]
   for blank in range(256): #sets a maximum number of tries before it gives up
      direction = [random.gauss(0,1) for i in range(3)]

      magnitude = math.sqrt(sum(x*x for x in direction))
      offset = [x*distance / magnitude for x in direction]

      new_rgb = [round(c + d) for c, d in zip(rgb, offset)]
      if all(0 <= x <= 255 for x in new_rgb):
         return f"#{new_rgb[0]:02X}{new_rgb[1]:02X}{new_rgb[2]:02X}"
   # if it fails to find a functioning colour try the safe route
   offset = [abs(x)*distance / magnitude for x in direction]
   for i in range(len(rgb)):
      if rgb[i] <= 127:
         new_rgb[i] = round(rgb[i] + offset[i])
      else:
         new_rgb[i] = round(rgb[i] - offset[i])
   if all(0 <= x <= 255 for x in new_rgb):
            return f"#{new_rgb[0]:02X}{new_rgb[1]:02X}{new_rgb[2]:02X}"
   raise ValueError("Could not generate valid colour offset")

def on_click(event, boxes):
   global correct, total
   clicked_id = canvas.find_withtag("current")[0]
   # canvas.itemconfig(clicked_id, fill = random_colour())
   # print(f"Clicked id: {clicked_id}")

   flat_boxes = [box for row in boxes for box in row]
   clicked_index = flat_boxes.index(clicked_id)
   if clicked_index == misfit:
      correct += 1
   total += 1
   print(f"Total: {total}")
   print(f"Correct: {correct}")
   print(f"Score:{correct/total:.2%}")
   randomize_colours(boxes)


# initiate window
root = tk.Tk()
root.title ("Colour Test")
canvas = tk.Canvas(root, bg="white")
canvas.pack(fill="both", expand=True)
# start screen
start_screen()
# run window
root.mainloop()

# end