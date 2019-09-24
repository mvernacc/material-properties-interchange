"""File path utilities."""
import os.path


def get_database_dir():
    """Get the directory containing the materials data YAML files.

    Returns:
        string
    """
    here = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(here, 'materials_data')
