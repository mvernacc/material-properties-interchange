"""classes for representing and querying properties of a material."""
import numpy as np

import materials.variation_with_state as vstate


class Property:
    """A property of a material."""

    def __init__(self, name, yaml_dict):
        self.name = name
        self.default_value = yaml_dict['default_value']
        self.units = yaml_dict['units']
        self.reference = yaml_dict['reference']

    def query_value(self):
        """Query the value of the property."""
        return self.default_value

    def __str__(self):
        return '{:s} = {:.4g} {:s} [Data from {:s}]'.format(
            self.name, self.query_value(), self.units, self.reference)


class StateDependentProperty(Property):
    """A property of a material which depends on state (e.g. temperature)."""

    def __init__(self, name, yaml_dict):
        Property.__init__(self, name, yaml_dict)
        self.variations_with_state = {}
        for vs_name, vs_subdict in yaml_dict['variations_with_state'].items():
            self.variations_with_state[vs_name] = vstate.build_from_yaml(vs_subdict)
        self.default_state_model = list(self.variations_with_state.keys())[0]

    def query_value(self, state, state_model=None, model_args_dict=None):
        """Query the value of the property at a particular state."""
        if state_model is None:
            state_model = self.default_state_model
        if model_args_dict is None:
            model_args_dict = {}
        values = self.variations_with_state[state_model].query_value(state, **model_args_dict)
        if self.variations_with_state[state_model].value_type == 'multiplier':
            values = self.default_value * values
        return values

    def __getitem__(self, key):
        """Shorthand for self.variations_with_state[key]."""
        if key not in self.variations_with_state:
            raise KeyError(
                'This Property does not have a {:s} variations with state model'.format(key)
                + '\nThe valid keys are {}'.format(self.variations_with_state.keys())
            )
        return self.variations_with_state[key]

    def __str__(self):
        string = '{:s}, a state-dependent property with a default value of {:.4g} {:s}'.format(
            self.name, self.default_value, self.units)
        string += '\n\tand with the following variation-with-state models:'
        for state_model_name in self.variations_with_state:
            string += '\n - {:s}: {:s}'.format(state_model_name, str(self[state_model_name]))
        return string
