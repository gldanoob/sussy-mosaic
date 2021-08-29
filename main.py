import sys, glob
from PIL import Image
import numpy

# Function for changing transparency level to 0
def trans(img):
    p = img.getpalette()
    shift = 1
    arr = (numpy.array(img) + shift) % 256
    dst = Image.fromarray(arr).convert('P')
    dst.putpalette(p[-3*shift:] + p[:-3*shift])
    return dst

def twerk(path, size):
    if size is None: size = 50

    # Sussy frames & Output location
    raw = "assets/among_*.png"
    out = "twerk.gif"

    # Picture as mosaic pattern
    try:
        pic = Image.open(path).convert("RGBA")
    except:
        sys.exit(f"File not found or not an image: {path}")

    width, height = pic.size

    # Sample the color every unit of pixels
    # Max 50 samples per dimension
    unit = int(max(width, height) // size + 1)

    # Mosiac color array
    colors = [
        [
            pic.getpixel((x, y)) for x in range(0, width, unit)
        ] for y in range(0, height, unit)
    ]
        
    # List of among twerk images
    among = [Image.open(f) for f in sorted(glob.glob(raw))]

    # Size (width) of tiles
    size, _ = among[0].size

    mask = among[0].convert("RGBA")

    # Storage of frames
    sus = []
    for i in range(len(among)):
        print(f"Rendering frames... ({i + 1} of {len(among)})")

        frame = Image.new('RGBA', (size * len(colors[0]), size * len(colors)))

        for y, row in enumerate(colors):
            for x, bright in enumerate(row):

                # Shading color of the ass
                shade = tuple(v / 2 for v in bright[:-1]) + (bright[-1],)
                
                tile = among[(x + y - i) % len(among)].convert("RGBA")

                # Pixel array (r, g, b, a)
                pixels = numpy.array(tile)

                # Replace colors of imposter wif the given colors
                r, g, b, a = pixels.T                
                r_areas = (r == 197) & (g == 17) & (b == 17) & (a == 255)
                pixels[...][r_areas.T] = bright

                r, g, b, a = pixels.T
                dark_areas = (r == 122) & (g == 8) & (b == 56) & (a == 255)
                pixels[...][dark_areas.T] = shade

                # Paste sussy baka onto frame
                frame.paste(Image.fromarray(pixels), (size * x, size * y), mask)

        sus.append(trans(frame.quantize(method=2)))

    print("Writing GIF...")

    # Write the sus gif
    sus[0].save(
        fp=out, format='GIF', append_images=sus[1:],
        save_all=True, disposal=2, duration=50, loop=0, transparency=0
    )

    print(f"Saved gif to {out}")

if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1:
        sys.exit("""Among twerk mosaic art generator 
(https://github.com/gldanoob/sussy-mosiac)

Arguments
    <path-to-image>: required
    <max-size>: optional""")

    size = None
    if len(args) >= 3:
        try:
            size = int(args[2])
            if size <= 0: raise Exception()
        except:
            sys.exit(f"Invalid size: {args[2]}, must be an positive integer")
    
    twerk(args[1], size)
    
