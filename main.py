from PIL import Image, ImageDraw

img = Image.open('sample.jpg')
width, height = img.size

pix = img.load()
d = {}

monotheta = 30
theta = 60
howdark = 0.5

def toHex(pixel):
  l = list(pixel)
  l = [str(hex(x))[2:] for x in l]
  return '#' + ''.join(l)

def createPalette(palette):
  wide = 100
  dim = len(palette.keys()) * wide
  image = Image.new("RGB", (dim, dim), "white")
  draw = ImageDraw.Draw(image)
  for index, category in enumerate(palette.keys()):
    tlx = (index * wide)
    tly = 0
    brx = (index + 1) * wide
    bry = dim/2
    draw.rectangle([tlx, tly, brx, bry], fill=palette[category])
    print(category + ": " + str(palette[category]))
    tly += dim/2
    bry += dim/2
    dark = tuple([int(x*howdark) for x in list(palette[category])])
    print("dark " + category + ": " + str(dark))
    draw.rectangle([tlx, tly, brx, bry], fill=dark)
  for index, category in enumerate(palette.keys()):
    draw.text([(index * wide) + 10, wide], category, fill="#FFFFFF")
  del draw
  image.save("palette.png", "PNG")

def category(pixel):
  l = list(pixel)
  r, g, b = pixel

  if max(l) - min(l) < monotheta:
    s = sum(l)
    if s > 200:
      return ("white", s)
    elif s > 100:
      return ("lightgrey", s)
    elif s > 50:
      return ("darkgrey", s)
    return ("black", s)
  elif abs(r-g) < theta and (r + g) / 2 > b:
    return ("yellow", ((r+g)/2) - b)
  elif abs(r-b) < theta and (r + b) / 2 > g:
    return ("magenta", ((r+b)/2) - g)
  elif abs(g-b) > theta and (g + b) / 2 > r:
    return ("cyan", ((g+b)/2) - r)
  elif r > g and r > b:
    return ("red", r + r - ((g+b)/2))
  elif g > r and g > b:
    return ("green", g + g - ((r+b)/2))
  else:
    return ("blue", b + b - ((r+g)/2))

for x in range(0, width):
  for y in range(0, height):
    p = pix[x,y]
    h = toHex(p)
    c, weight = category(p)
    
    if not c in d or weight > d[c][1]:
        d[c] = (p, weight)

palette = {}
for category in d.keys():
  palette[category] = d[category][0]

createPalette(palette)

