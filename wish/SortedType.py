from enum import Enum

class SortedType(Enum):
    recent = '-created_at'
    songpyeon = '-sp_sum'

    
sorted_type = { st.name:st for st in SortedType }

def get_sorted_type(value: str):
    if value in sorted_type:
        return sorted_type[value]
    
    return None
