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
        if 'variations_with_state' in property_dict:
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
        """Create a Material.

        We don't recommend using this function directly, instead use
        `load_from_yaml` to create a Material object from a YAML file
        of material property data.

        Arguments:
            name (string): Name of the material.
            form (string): The form in which the material was produced,
                e.g. 'extruded', 'forged', etc. We use form in the same sense as MMPDS [1].
                The form can effect some properties of the material.
            condition (string): The condition, heat treatment, or temper of the material.
                MMPDS [1] uses 'condition' or 'temper' to refer to this concept,
                depending on the alloy family.
                Different alloy families use different condition/temper designations,
                these designations are described in MMPDS or the relevant materials standards.
                The condition can effect some properties of the material.
            category (string): The broad category to which the material belongs,
                e.g. 'metal', 'ceramic' or 'plastic'.
            subcategory (string): The subcategory to which the material belongs,
                e.g. 'aluminum alloy' or 'thermoplastic'.
            references (list of string): References from which the material property data was gathered.
                Each string in the list should be a bibtex entry for one reference.
            properties_dict (dict): A dict of material property data derived from a YAML file.

        References:
            [1] Richard C Rice and Jana L Jackson and John Bakuckas and Steven Thompson,
                "Metallic Materials Properties Development and Standardization (MMPDS)",
                U.S. Department of Transportation, Federal Aviation Administration, 2001.
        """
        self.name = name
        self.form = form
        self.condition = condition
        self.category = category
        self.subcategory = subcategory
        self.references = references

        if properties_dict is not None:
            self.properties = build_properties(properties_dict)

    def __getitem__(self, key):
        """Get a property of the material by name.
        A Material is primarily a collection of properties, so we use []
        as a shorthand to access a property.
        i.e. `mat[key]` is a shorthand for `mat.properties[key]`.

        Argument:
            key (string): the name of a property.

        Returns:
            Property: `self.properties[key]`
        """
        if key not in self.properties:
            raise KeyError(
                'This Material does not have a {:s} property'.format(key)
                + '\nThe valid keys are {}'.format(self.properties.keys())
                )
        return self.properties[key]

    def __str__(self):
        string = self.name
        string += '\n' + '-'*len(self.name) + '\n'
        string += '{:s}, {:s}\n'.format(self.category, self.subcategory)
        string += 'Properties for the "{:s}" form, "{:s}" condition:\n'.format(self.form, self.condition)
        string += '\n\n'.join([str(prop) for prop in self.properties.values()])
        return string


def load_from_yaml(filename, form, condition):
    """Load a material from a YAML file.

    Arguments:
        filename (string): Path to the YAML file containing the material data.
        form (string): The form in which the material was produced,
            e.g. 'extruded', 'forged', etc. We use form in the same sense as MMPDS [1].
            The form can effect some properties of the material.
            Must be a key in the `forms` section of the YAML file.
        condition (string): The condition, heat treatment, or temper of the material.
            MMPDS [1] uses 'condition' or 'temper' to refer to this concept,
            depending on the alloy family.
            Different alloy families use different condition/temper designations,
            these designations are described in MMPDS or the relevant materials standards.
            The condition can effect some properties of the material.
            Must be a key in the `conditions` section of the YAML file for the given form.

    Returns:
        Material
    """
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
