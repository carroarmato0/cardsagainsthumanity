from urllib.parse import urlparse
import importlib


def convert_to_dict(obj):
    """
    A function takes in a custom object and returns a dictionary representation of the object.
    :param obj: the object to be serialized
    :return: dict representation of the object
    """
    return obj.__dict__


def convert_to_dict_with_meta(obj):
    """
    A function takes in a custom object and returns a dictionary representation of the object.
    This dict representation includes meta data such as the object's module and class names.
    :param obj: the object to be serialized
    :return: dict representation of the object
    """
    #  Populate the dictionary with object meta data
    obj_dict = {
        "__class__": obj.__class__.__name__,
        "__module__": obj.__module__
    }

    #  Populate the dictionary with object properties
    obj_dict.update(obj.__dict__)

    return obj_dict


def dict_to_obj(our_dict):
    """
    Function that takes in a dict and returns a custom object associated with the dict.
    This function makes use of the "__module__" and "__class__" metadata in the dictionary
    to know which object type to create.
    :param our_dict: a dictionary representation
    :return: the Class object
    """
    if "__class__" in our_dict:
        # Pop ensures we remove metadata from the dict to leave only the instance arguments
        class_name = our_dict.pop("__class__")

        # Get the module name from the dict and import it
        module_name = our_dict.pop("__module__")

        # Load the module at run-time based on its name
        module = importlib.import_module(module_name)
        # Get the class from the module
        class_ = getattr(module, class_name)

        # Use dictionary unpacking to initialize the object
        obj = class_(**our_dict)
    else:
        obj = our_dict
    return obj


def uri_validator(x):
    """
    Validates if a given URI is valid
    :param x: the URI
    :return: Either False or the tuple representation of the URI
    """
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False
