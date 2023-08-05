from typing import Optional
import json


def from_json_maybe(json_text: str, dataclass_type: type) -> Optional[object]:
    """
    Convert a json string to a dataclass object.
    If the json string is invalid, return None.

    Parameters
    ----------
    json_text : str
        The json string to convert.
    dataclass_type : type
        The dataclass type to convert to.
    
    Returns
    -------
    obj : Optional[object]
        The converted dataclass object.
        If the json string is invalid, return None.
    """
    try:
        data = json.loads(json_text)
        obj = from_data_maybe(data, dataclass_type)
        return obj
    except:
        return None

def from_data_maybe(data: object, dataclass_type: type) -> Optional[object]:
    """
    Convert a object to a dataclass object.
    If the object is invalid, return None.

    Parameters
    ----------
    data : object
        The object to convert.
    dataclass_type : type
        The dataclass type to convert to.
    
    Returns
    -------
    obj : Optional[object]
        The converted dataclass object.
        If the dict is invalid, return None.
    """
    try:
        obj = dataclass_type(**data)
        return obj
    except:
        return None