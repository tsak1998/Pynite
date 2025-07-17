from typing import Dict, List, Literal, Optional, Any
from pydantic import BaseModel, Field


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


class Member(BaseModel):
    type: str

    node_A: int
    node_B: int
    section_id: int
    rotation_angle: int
    fixity_A: str
    fixity_B: str
    offset_Ax: str
    offset_Ay: str
    offset_Az: str
    offset_Bx: str
    offset_By: str
    offset_Bz: str
    stiffness_A_Ry: float
    stiffness_A_Rz: float
    stiffness_B_Ry: float
    stiffness_B_Rz: float


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


class Support(BaseModel):
    tx: float = 0
    ty: float = 0
    tz: float = 0
    rx: float = 0
    ry: float = 0
    rz: float = 0
    node: int
    restraint_code: str


class PointLoad(BaseModel):
    load_id: int
    type: Literal['n', 'm'] = 'n'
    node: str | None = None
    member: str | None = None
    x_mag: float
    y_mag: float
    z_mag: float
    load_group: str


class DistributedLoad(BaseModel):
    load_id: int
    member: int
    x_mag_A: float = 0
    y_mag_A: float = 0
    z_mag_A: float = 0
    x_mag_B: float = 0
    y_mag_B: float = 0
    z_mag_B: float = 0
    position_A: float = 0
    position_B: float = 100
    load_group: str
    axes: Literal["global", "local"] = 'global'


class AreaLoad(BaseModel):
    type: str
    nodes: str
    members: Optional[Any]
    mag: float
    direction: str
    elevations: Optional[Any]
    mags: Optional[Any]
    column_direction: str
    elevation_direction: Optional[Any]
    loaded_members_axis: Optional[Any]
    LG: str


class SelfWeight(BaseModel):
    x: float
    y: float
    z: float
    load_group: str


class LoadCombination(BaseModel):
    name: str
    criteria: str

    class Config:
        extra = "allow"


class LoadCases(BaseModel):
    AISC: Dict[str, str] = {}


class Model(BaseModel):
    settings: Settings
    details: List[Any]
    nodes: Dict[str, Node]
    members: Dict[str, Member]
    plates: Dict[str, Any]
    meshed_plates: Dict[str, Any]
    materials: Dict[str, Material]
    sections: Dict[str, Section]
    supports: Dict[str, Support]
    settlements: Dict[str, Any]
    groups: Dict[str, Any]
    point_loads: Dict[str, Any]
    moments: Dict[str, Any]
    distributed_loads: Dict[str, Any]
    area_loads: Dict[str, AreaLoad]
    self_weight: Dict[str, SelfWeight]
    load_combinations: Dict[str, LoadCombination]
    load_cases: LoadCases
    nodal_masses: Dict[str, Any]
    design_input: List[Any]