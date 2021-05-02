from PIL import Image, ImageFont, ImageDraw
from jinja2 import Template
import time

class specimen:
    def __init__(self, image_config):
        self.image_config = image_config

    def save_image(self, filename, image):
        with open(filename, 'wb') as file:
            file.write(image.getvalue())

        img = Image.open(filename, "r").convert("RGBA")
        img_draw = ImageDraw.Draw(img)


        pos = (10, 20)
        bg_img = Image.new('RGBA', img.size, (0, 0, 0, 0))

        bg_draw = ImageDraw.Draw(bg_img)
        overlay_transparency = 100
        bg_draw.rectangle((pos[0], pos[1], pos[0], pos[1]), fill=(0, 0, 0, overlay_transparency), outline=(255, 255, 255))

        bg_img.save("./alpha.png")
#        img.paste(bg_img, box=(0,0))
        out = Image.alpha_composite(img, bg_img)
        print("Saving {}..".format(filename))
        r = out.convert('RGB')
        r.save(filename, "JPEG")
        print("Saved {}..OK".format(filename))

    def format(self, readings):
        degree_symbol=u"\u00b0"
        return "#growlab"

    def save_html(self, input_filename, output_path):
        img = Image.open(input_filename, "r")

        img = img.resize((int(self.image_config["width"]/2), int(self.image_config["height"]/2)), Image.ANTIALIAS)
        img.save(output_path+"/preview.jpg", "JPEG")

        template_text = ""
        with open("index.jinja", 'r') as file:
            template_text = file.read()

        template = Template(template_text)
        degree_symbol=u"\u00b0"
        vals = {}
        vals["uid"] = "{}".format(time.time())

        html = template.render(vals)
        with open(output_path+"/index.html", "w") as html_file:
            html_file.write(html)
            print("Wrote {}..OK".format(output_path+"/index.html"))
