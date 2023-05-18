import os
from PIL import Image
mod_dir = os.path.dirname(os.path.abspath(__file__))
qr_code_dir = os.path.join(mod_dir, "qrcodes")
output_dir = os.path.join(mod_dir, "output_folder")

template_path = "DM-Sticker_Custom-12x16cm_blank-for-template.png"
template_path = input("Background Image Location: ")
qr_code_dir = input("QR codes folder location: ")
output_dir = input("Output Folder Location: ")
if(not os.path.exists(output_dir)):
    os.makedirs(output_dir)
files = os.listdir(qr_code_dir)

def add_qr_to_image(qr_file, template_path, output_path, resize_params=(500,500), location=(220,780)):
    qr_image = Image.open(qr_file).convert("RGBA")
    qr_image = qr_image.resize(resize_params)
    print("Loaded QR: " + qr_file)
    template_Image = Image.open(template_path).convert("RGBA")
    template_Image.paste(qr_image, location, qr_image)
    template_Image.save(output_path)
    print("Output Generated: " + output_path)
    


# curr_file = os.path.join(qr_code_dir, files[10])
# add_qr_to_image(curr_file, template_path, "ouput.png")

count = 1
for curr_file in files:
    if ".png" in curr_file.lower():
        curr_file = os.path.join(qr_code_dir, curr_file)
        output_path = os.path.join(output_dir, "output-" + str(count) + ".png")
        add_qr_to_image(curr_file, template_path, output_path)
        count += 1


