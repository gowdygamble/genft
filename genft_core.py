import glob
import os
import yaml

def write_yaml_config_from_dict(config_dict, filename):
    with open(filename, 'w') as f:
        yaml.dump(config_dict, f, default_flow_style = False)

def norm_property_distribution(property_distribution):
    dist_sum = 0
    for property_value in property_distribution:
        dist_sum += property_distribution[property_value]

    for property_value in property_distribution:
        property_distribution[property_value] /= dist_sum

def norm_all_properties(property_dict):
    for k in property_dict:
        norm_property_distribution(property_dict[k])

def generate_config_from_directory(directory_name, project_name):
    property_folders = glob.glob(os.path.join(directory_name, "*"))
    property_dict = {}

    for property_folder in property_folders:
        property_name = os.path.basename(property_folder)
        property_dict[property_name] = {}
        property_files = glob.glob(os.path.join(property_folder, "*"))

        for property_file in property_files:
            basename = os.path.basename(property_file)
            basename = basename.split(".")[0]
            print(property_name, basename)
            property_dict[property_name][basename] = 1


    norm_all_properties(property_dict)

    config_dict = {
        "project_name": project_name,
        "asset_directory": directory_name,
        "properties": property_dict
    }

    write_yaml_config_from_dict(config_dict, project_name + "_config.yml")
