import sys
import random

from config_processing import check_config_against_directory, load_config_dict_from_yaml


class PropertySelector:

    def __init__(self, config_fn):

        if check_config_against_directory(config_fn):
            self.config_fn = config_fn
            self.config_dict = load_config_dict_from_yaml(config_fn)
        else:
            print("PropertySelector not instantiated")
            sys.exit(1)

    def compute_maximum_unique_combinations(self):
        product = 1
        for property_name in self.config_dict['properties'].keys():
            product *= len(list(self.config_dict['properties'][property_name]['values'].keys()))

        return product

    def create_batch(self, batch_size):
        batch = []

        # need to check if requested batch size is greater than all combinations
        # if so then just make all combinations and return them

        while len(batch) <= batch_size:
            entity = self.generate_entity()
            #print(entity)
            if entity not in batch:
                batch.append(entity)

        return batch

    def generate_entity(self):
        # an entity is a dict of property-name : proprety-value

        properties = {}

        for property_name in self.config_dict['properties'].keys():

            # includes the possibility of NOT sampling it!
            sampled_property = self.sample_property(property_name)
            # property value will be false if not sampled
            properties[property_name] = sampled_property

        return properties

    def sample_property(self, property_name):

        inclusion_prob = self.config_dict['properties'][property_name]['inclusion_prob']
        inclusion_draw = random.random()

        if inclusion_draw < inclusion_prob:

            property_value_draw = random.random()
            property_value_sum = 0
            # definitely something wrong here
            # getting way too many of rare props 
            for value_name in self.config_dict['properties'][property_name]['values'].keys():
                value_prob = self.config_dict['properties'][property_name]['values'][value_name]
                property_value_sum += value_prob
                if property_value_sum < property_value_draw:
                    return value_name
            return value_name
        else:
            return False
