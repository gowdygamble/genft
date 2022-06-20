import glob
import random
from PIL import Image

fn = "snek_1"

component_folders = glob.glob(fn + "/*")

#print(component_folders)


def generate_image(component_folders):

    image_components = []

    for component_folder in component_folders:
        components = glob.glob(component_folder + "/*.png")

        selected_component = random.choice(components)
        image_components.append(selected_component)

    print(image_components)
    combine_snek_components(image_components)

def combine_snek_components(components):
    comp_names_ordered = ["backgrounds", "bodies","eyes", "accessories"]

    img = 0

    for comp_name in comp_names_ordered:

        for img_comp in components:

            if comp_name in img_comp:
                _tmp = Image.open(img_comp)
                if img == 0:
                    img = 1
                    final = Image.new("RGBA", _tmp.size)

                final = Image.alpha_composite(final, _tmp)


    fn = str(random.randint(100000,2000000)) + ".png"

    final.show()
    final.save(fn)

generate_image(component_folders)
