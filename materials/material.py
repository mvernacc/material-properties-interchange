"""Representation of a material's engineering properties and other data."""
import yaml
from materials.property import Property, StateDependentProperty


def build_properties(properties_dict_yaml):
    """Create a dict of Property from a (YAML-derived) dictionary.

    Arguments:
        properties_dict_yaml (dict): A dict of material property data derived from a YAML file.

    Returns:
        properties_dict_py (dict): keys are property name strings, values are Property objects.
    """
    properties_dict_py = {}    # Dictionary of properties as python objects
    for property_name, property_dict in properties_dict_yaml.items():
        if 'variation_with_state' in property_dict:
            prop = StateDependentProperty(property_name, property_dict)
        else:
            prop = Property(property_name, property_dict)
        # TODO check that the property was properly constructed.
        properties_dict_py[property_name] = prop
    return properties_dict_py


class Material:
    """An engineering material, in a particular form and condition."""
    def __init__(self, name, form=None, condition=None, category=None, subcategory=None,
                 references=None, properties_dict=None):
        self.name = name
        self.form = form
        self.condition = condition
        self.category = category
        self.subcategory = subcategory
        self.references = references

        if properties_dict is not None:
            self.properties = build_properties(properties_dict)


def load_from_yaml(filename, form, condition):
    """Load a material from a YAML file."""
    with open(filename, 'r') as yaml_stream:
        matl_dict = yaml.load(yaml_stream)

    # Check that the reqested form and condition are present
    if not form in matl_dict['forms']:
        raise ValueError('Form {:s} not present in {:s}'.format(form, filename))
    if not condition in matl_dict['forms'][form]['conditions']:
        raise ValueError('Condition {:s} not present in {:s}, {:s}'.format(
            condition, form, filename))

    name = matl_dict['name']
    category = matl_dict['category']
    if 'subcategory' in matl_dict:
        subcategory = matl_dict['subcategory']
    else:
        subcategory = None
    references = matl_dict['references']

    properties_dict = matl_dict['forms'][form]['conditions'][condition]['properties']

    matl = Material(name, form, condition, category, subcategory,
                    references, properties_dict)

    return matl
