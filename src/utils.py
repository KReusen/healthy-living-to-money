from typing import List

def get_field_names_from_data_model(data_model: object) -> List[str]:
    return [key for key in data_model.__annotations__ ]

def create_model_from_dict(model: object, d: dict) -> object:
    allowed_keys = get_field_names_from_data_model(model)
    safe_dict = {}
    for key, value in d.items():
        if key in allowed_keys:
            safe_dict[key] = value
    return model(**safe_dict)