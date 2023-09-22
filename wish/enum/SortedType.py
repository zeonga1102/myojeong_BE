from enum import Enum

class SortedType(Enum):
    recent = '-created_at'
    songpyeon = '-sp_sum'

    
sorted_type = { st.name:st for st in SortedType }

def get_sorted_type(name: str):
    if name in sorted_type:
        return sorted_type[name]
    
    return None
