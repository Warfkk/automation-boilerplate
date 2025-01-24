from enum import Enum, auto


class UnitTypes(Enum):
    """Class to represent the different types of units / phases, must correspond to
    the table in excel under _configs"""

    PHASE = "Phase"
    LINE_UNIT = "Line_Unit"
    TANK_UNIT = "Tank_Unit"
    LINE_SROUCE = "Line_Source"
    LINE_DESTINATION = "Line_Destination"
    PHASE_ORDERNO_RECIPENO = "Phase_OrderNo_RecipeNo"
    CIP_TANK_UNIT = "CIP_Tank_Unit"
    CIP_LINE_UNIT = "CIP_Line_Unit"
