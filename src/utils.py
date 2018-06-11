from typing import List

def get_field_names_from_data_model(data_model: object) -> List[str]:
    return [key for key in data_model.__annotations__ ]