from selector import PropertySelector

config_fn = "snek_2_config.yml"

#generate_config_from_directory(d, "snek_2")
#check_config_against_directory(config_fn)
property_selector = PropertySelector(config_fn)

#u = property_selector.compute_maximum_unique_combinations()

batch = property_selector.create_batch(5)

print(len(batch))
for b in batch:
    print(b)
    print("")
