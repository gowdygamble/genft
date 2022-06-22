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
        norm_property_distribution(property_dict[k]["values"])

def check_normed_property_values(property_dist):
    property_sum = 0
    for value_name in property_dist:
        property_sum += property_dist[value_name]

    return property_sum


def check_config_against_directory(config_fn):
    with open(config_fn, 'r') as stream:
        try:
            parsed_yaml = yaml.safe_load(stream)
            #print(parsed_yaml)
        except yaml.YAMLError as exc:
            print(exc)

    property_folders = glob.glob(os.path.join(parsed_yaml["asset_directory"], "*"))
    property_folder_names = [os.path.basename(x) for x in property_folders]

    config_property_names = list(parsed_yaml["properties"])
    #print(config_property_names)

    errors = []

    print("1/4 Checking config properties against folders")
    for cfg_prop_name in config_property_names:
        if cfg_prop_name not in property_folder_names:
            #print("Config property missing from asset dir: ", cfg_prop_name)
            errors.append("Config property missing from asset dir: " + cfg_prop_name)


    print("2/4 Checking folders against config properties")
    for property_folder in property_folders:
        property_name = os.path.basename(property_folder)
        if property_name not in config_property_names:
            #print("Property folder not found in config: ", property_name)
            errors.append("Property folder not found in config: " + property_name)

    print("3/4 Checking property asset values against asset files")
    for property_name, property_folder in zip(property_folder_names, property_folders):
        if property_name in config_property_names:
            err = check_property_against_assets(property_name, parsed_yaml["properties"][property_name], property_folder)
            if err:
                errors.append(err)
        else:
            err = "Warning: " + property_name + " not in config, skipping asset check."
            print(err)
            errors.append(err)

    print("4/4 Checking property distribution normalization")
    for config_property_name in config_property_names:
        pd = parsed_yaml["properties"][config_property_name]["values"]
        dist_sum = check_normed_property_values(pd)
        if dist_sum != 1:
            errors.append("Property not normed: " + config_property_name)

    print("")
    print("--------------")
    print("")
    print("Errors:")
    for err in errors:
        print(err)
    print("")
    print("--------------")
    print("")
    print("Done checking config against directory")


def check_property_against_assets(property_name, property_distribution_dict, property_folder):
    property_asset_files = glob.glob(os.path.join(property_folder, "*"))
    property_asset_names =  [os.path.basename(x) for x in property_asset_files]
    property_asset_names =  [x.split(".")[0] for x in property_asset_names]

    config_prop_names = list(property_distribution_dict.keys())
    #print(property_name, property_asset_names, config_prop_names)
    if set(config_prop_names) == set(property_asset_names):
        return False
    else:
        return ("Asset file / config property value mismatch: " + property_name
        + ", config: " + str(config_prop_names) + ", asset files: "
        + str(property_asset_names))




def generate_config_from_directory(directory_name, project_name):
    property_folders = glob.glob(os.path.join(directory_name, "*"))
    property_dict = {

    }

    for property_folder in property_folders:
        property_name = os.path.basename(property_folder)
        property_dict[property_name] = {
            "inclusion_prob": 1,
            "values": {}
        }
        property_files = glob.glob(os.path.join(property_folder, "*"))

        for property_file in property_files:
            basename = os.path.basename(property_file)
            basename = basename.split(".")[0]
            print(property_name, basename)
            property_dict[property_name]["values"][basename] = 1


    norm_all_properties(property_dict)

    config_dict = {
        "project_name": project_name,
        "asset_directory": directory_name,
        "properties": property_dict
    }

    write_yaml_config_from_dict(config_dict, project_name + "_config.yml")
