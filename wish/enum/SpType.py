from enum import Enum

class SpType(Enum):
    sp1 = 'sp1'
    sp2 = 'sp2'
    sp3 = 'sp3'


sp_type = { st.name:st for st in SpType }

def get_sp_type(name: str):
    if name in sp_type:
        return sp_type[name]
    
    return None
