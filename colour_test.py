# Created by Will Madner on 08/10/2026
import tkinter as tk
import random
import math

# Constants
# default values
NUMBER_OF_BOXES_WIDE = 2
NUMBER_OF_BOXES_TALL = 2
VERTICAL_PADDING = 10
HORIZONTAL_PADDING = 10
BOX_WIDTH = 100
BOX_HEIGHT = 100
HORIZONTAL_BOX_SPACING = 20
VERTICAL_BOX_SPACING = 20
COLOUR_DISTANCE = 50
NUMBER_OF_TRIALS = 20
TEST_COLOURS = [
   "#FF0000",
   "#FF774D",
   "#FFFF00",
   "#00FF00",
   "#0000FF",
]
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

def pass_function():
   pass

def generate_boxes(
               number_of_boxes_wide = NUMBER_OF_BOXES_WIDE,
               number_of_boxes_tall = NUMBER_OF_BOXES_TALL,
               functions = pass_function,
               text = None,
               box_width = BOX_WIDTH,
               box_height = BOX_HEIGHT,
               vertical_padding = VERTICAL_PADDING,
               horizontal_padding = HORIZONTAL_PADDING,
               horizontal_box_spacing = HORIZONTAL_BOX_SPACING,
               vertical_box_spacing = VERTICAL_BOX_SPACING,):
   # generate boxes
   boxes = []
   for i in range(NUMBER_OF_BOXES_TALL):
      boxes.append([])
      for j in range(NUMBER_OF_BOXES_WIDE):
         boxes[i].append(canvas.create_rectangle(
            horizontal_padding + box_width*j + horizontal_box_spacing*j,
            vertical_padding + box_height*i + vertical_box_spacing*i,
            horizontal_padding + box_width*(j+1) + horizontal_box_spacing*j,
            vertical_padding + box_height*(i+1) + vertical_box_spacing*i,
            fill = TEST_COLOURS[1],
            outline= "black"
         ))
   # generate text
   if text == None:
      pass
   elif type(text) == str:
      texts = []
      for i in range(NUMBER_OF_BOXES_TALL):
            texts.append([])
            for j in range(NUMBER_OF_BOXES_WIDE):
               texts[i].append(canvas.create_text(
                  horizontal_padding + box_width*(j+.5) + horizontal_box_spacing*j,
                  vertical_padding + box_height*(i+.5) + vertical_box_spacing*i,
                  text = text,
                  fill= "white",
                  font = ("Arial", 20, "bold")
               ))
   # assign functions to boxes
   if functions == None:
      pass
   elif callable(functions):
      for i in range(number_of_boxes_tall):
         for j in range(number_of_boxes_wide):
            canvas.tag_bind(boxes[i][j], "<Button-1>", lambda event: functions(event, boxes))
   elif isinstance(functions. list):
      while len(functions) < number_of_boxes_wide*number_of_boxes_tall:
         functions.append(pass_function)
      if all(callable(f) for f in functions):
         functionIndex = 0
         for i in range(number_of_boxes_tall):
            for j in range(number_of_boxes_wide):
               canvas.tag_bind(boxes[i][j], "<Button-1>", lambda event: functions[functionIndex](event, boxes))
      else:
         print("ERROR: FAILED TO FIND ONLY FUNCTIONS IN FUNCTION LIST")

   # set the window size
   windowWidth = horizontal_padding*2 + box_width*number_of_boxes_wide + horizontal_box_spacing*(number_of_boxes_wide-1)
   windowHeight = vertical_padding*2 + box_height*number_of_boxes_tall + vertical_box_spacing*(number_of_boxes_tall-1)
   rootGeometry = f"{windowWidth}x{windowHeight}"
   root.geometry(rootGeometry)
   return(boxes)


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
   canvas.tag_bind(start_box, "<Button-1>", start_clicked)
   canvas.tag_bind(start_text, "<Button-1>", start_clicked)
def start_clicked(event):
   run_test()

def run_test(
            mode = 0,
            number_of_trials = NUMBER_OF_TRIALS,
            number_of_boxes_wide = NUMBER_OF_BOXES_WIDE,
            number_of_boxes_tall = NUMBER_OF_BOXES_TALL,
            vertical_padding = VERTICAL_PADDING,
            horizontal_padding = HORIZONTAL_PADDING,
            box_width = BOX_WIDTH,
            box_height = BOX_HEIGHT,
            horizontal_box_spacing = HORIZONTAL_BOX_SPACING,
            vertical_box_spacing = VERTICAL_BOX_SPACING,
            colour_distance = COLOUR_DISTANCE,
            ):
   
   canvas.delete("all")
   global correct, total
   correct = 0
   total = 0
   boxes = generate_boxes(NUMBER_OF_BOXES_WIDE, NUMBER_OF_BOXES_TALL, on_click, "potato") #generate grid of boxes

   randomize_colours(boxes)


def randomize_colours(boxes, base_colour=None, colour_distance = COLOUR_DISTANCE):
   if base_colour == None:
      base_colour = random_colour()
   flat_boxes = [box for row in boxes for box in row]
   count = len(flat_boxes)
   global misfit
   misfit = random.randint(0,count-1)

   for i in range(count):
      if i == misfit:
         colour = offset_colour(base_colour, colour_distance)
      else:
         colour = base_colour
      canvas.itemconfig(flat_boxes[i], fill = colour)

def offset_colour(colour, distance): #takes a given colour and returns a colour with a fixed offset but randomized direction
   rgb = [int(colour[i:i+2], 16) for i in (1,3,5)]
   for _ in range(256): #sets a maximum number of tries before it gives up
      direction = [random.gauss(0,1) for __ in range(3)]

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

def update_colours(boxes, mode = 0):
   match mode:
      case 0:
         randomize_colours(boxes)
      case 1:
         print("MODE: 1")

def on_click(event, boxes, mode = 0):
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
   update_colours(boxes, mode)


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
