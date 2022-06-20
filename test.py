from genft_core import generate_config_from_directory, check_config_against_directory

d = "art/snek_1"
config_fn = "snek_2_config.yml"

#generate_config_from_directory(d, "snek_1")
check_config_against_directory(config_fn)
