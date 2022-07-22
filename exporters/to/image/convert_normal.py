import sys
from PIL import Image

if len(sys.argv) < 2:
  print("Usage: python", sys.argv[0], "file", "to|from")
  sys.exit()

file = sys.argv[1]
direction = "to" if len(sys.argv) < 3 else sys.argv[2]

extpos = file.rfind(".")

if direction != "to" and direction != "from":
  print("Invalid direction, must be either \"to\" or \"from\"!")
  sys.exit()

img = Image.open(file).convert("RGBA")
R, G, B, A = img.split()

if (direction == "to"):
  newImg = Image.merge("RGBA", [ G, G, G, R ])
  newImg.save(file[:extpos] + "_pd2" + file[extpos:])
else:
  B.paste(255, [0,0,B.size[0],B.size[1]])
  newImg = Image.merge("RGBA", [ A, G, B, B ])
  newImg.save(file[:extpos] + "_regular" + file[extpos:])