from collections import namedtuple


fields = (
    "psm_code",
    "psm_description",
    "psm_measure",
    "item_number",
    "item_code",
    "item_description",
    "item_measure",
    "comparison",
    "volume_formula",
    "notes",
    "criteria",
    "inspection",
    "file_name"
)

DataLine = namedtuple(typename='DataLine', field_names=fields, defaults=("",) * len(fields))
DataLine.__annotations__ = {
        "psm_code": str,
        "psm_description": str,
        "psm_measure": str,
        "item_number": str,
        "item_code": str,
        "item_description": str,
        "item_measure": str,
        "comparison": str,
        "volume_formula": str,
        "notes": str,
        "criteria": str,
        "inspection": str,
        "file_name": str,
}


