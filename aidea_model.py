from typing import Dict, List, Literal, Optional, Any
from pydantic import BaseModel


# === Base classes for common patterns ===

class BaseOffset(BaseModel):
    offset_Ax: str
    offset_Ay: str
    offset_Az: str
    offset_Bx: str
    offset_By: str
    offset_Bz: str


class BaseStiffness(BaseModel):
    stiffness_A_Ry: float
    stiffness_A_Rz: float
    stiffness_B_Ry: float
    stiffness_B_Rz: float


class BaseLoad(BaseModel):
    load_id: int
    load_group: str


class BaseAxes(BaseModel):
    axes: Literal["global", "local"] = "global"


# === Models ===

class SettingsUnits(BaseModel):
    length: str = 'm'
    section_length: str = 'mm'
    material_strength: str = 'mpa'
    density: str = 'kg/m3'
    force: str = 'kn'
    moment: str = 'kn-m'
    pressure: str = 'kpa'
    mass: str = 'kg'
    translation: str = 'mm'
    stress: str = 'mpa'


class Settings(BaseModel):
    units: SettingsUnits = SettingsUnits()
    precision: str = 'fixed'
    precision_values: int = 3
    vertical_axis: str = 'Z'
    member_offsets_axis: str = 'local'
    solver_timeout: int = 600
    smooth_plate_nodal_results: bool = True
    auto_stabilize_model: bool = False
    only_solve_user_defined_load_combinations: bool = False


class Node(BaseModel):
    x: float
    y: float
    z: float


class Member(BaseOffset, BaseStiffness):
    type: str
    node_A: int
    node_B: int
    section_id: int
    rotation_angle: int
    fixity_A: str
    fixity_B: str


class Material(BaseModel):
    id: Optional[int]
    name: str
    elasticity_modulus: float
    shear_modulus: Optional[float]
    density: float
    poissons_ratio: float
    yield_strength: Optional[float]
    ultimate_strength: Optional[float]
    thermal_expansion_coefficient: Optional[float]
    aux: Optional[Any] = None


class Section(BaseModel):
    version: int
    name: str
    area: float
    Iz: float
    Iy: float
    material_id: int
    aux: Optional[Any] = None
    J: Optional[float] = None


class Plate(BaseModel):
    type: str = "plate"
    nodes: List[int]  # List of node IDs that define the plate corners
    material_id: int
    thickness: float
    membrane_thickness: Optional[float] = None
    bending_thickness: Optional[float] = None


class Support(BaseModel):
    tx: float = 0
    ty: float = 0
    tz: float = 0
    rx: float = 0
    ry: float = 0
    rz: float = 0
    node: int
    restraint_code: str


class PointLoad(BaseLoad):
    type: Literal['n', 'm'] = 'n'
    node: str | None = None
    member: str | None = None
    x_mag: float
    y_mag: float
    z_mag: float


class DistributedLoad(BaseLoad, BaseAxes):
    member: int | str
    x_mag_A: float = 0
    y_mag_A: float = 0
    z_mag_A: float = 0
    x_mag_B: float = 0
    y_mag_B: float = 0
    z_mag_B: float = 0
    position_A: float = 0
    position_B: float = 100


class Pressure(BaseLoad, BaseAxes):
    plate_id: int
    x_mag: float = 0
    y_mag: float = 0
    z_mag: float = 0


class SelfWeight(BaseModel):
    x: float
    y: float
    z: float
    load_group: str


class LoadCombination(BaseModel):
    model_config = {"extra": "allow"}
    
    name: str
    criteria: str


class LoadCases(BaseModel):
    AISC: Dict[str, str] = {}


class Model(BaseModel):
    settings: Settings
    details: List[Any]
    nodes: Dict[str, Node]
    members: Dict[str, Member]
    plates: Dict[str, Plate]
    meshed_plates: Dict[str, Any]
    materials: Dict[str, Material]
    sections: Dict[str, Section]
    supports: Dict[str, Support]
    settlements: Dict[str, Any]
    groups: Dict[str, Any]
    point_loads: Dict[str, PointLoad]
    moments: Dict[str, Any]
    distributed_loads: Dict[str, DistributedLoad]
    area_loads: Dict[str, Pressure]
    self_weight: Dict[str, SelfWeight]
    load_combinations: Dict[str, LoadCombination]
    load_cases: LoadCases
    nodal_masses: Dict[str, Any]
    design_input: List[Any]
