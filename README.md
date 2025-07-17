# AIDEA to PyNite Structural Analysis System

A comprehensive structural analysis system that translates AIDEA model format to PyNite and performs complete structural analysis.

## Overview

This system provides a complete workflow for structural analysis:

1. **AIDEA Model Creation**: Define structural models using AIDEA format with nodes, members, materials, sections, loads, and supports
2. **Translation to PyNite**: Automatic conversion from AIDEA format to PyNite finite element model
3. **Structural Analysis**: Run linear static analysis using PyNite's powerful analysis engine
4. **Results Processing**: Extract and display comprehensive analysis results

## Project Structure

```
├── aidea_model.py                 # AIDEA model data structures (Pydantic models)
├── aidea_to_pynite_translator.py  # Core translator class
├── sample_two_storey_model.py     # Example two-storey building model
├── run_structural_analysis.py     # Main execution script
└── README.md                      # This documentation
```

## Features

### AIDEA Model Support
- **Materials**: Steel, concrete, and custom materials with full property definitions
- **Sections**: Standard and custom cross-sections (beams, columns)
- **Nodes**: 3D coordinate system with full DOF support
- **Members**: Beams and columns with end releases and offsets
- **Supports**: Fixed, pinned, roller, and custom support conditions
- **Loads**: Point loads, distributed loads, self-weight, and pressure loads
- **Load Combinations**: Multiple load combinations with factors

### PyNite Integration
- **Automatic Translation**: Seamless conversion of all AIDEA elements
- **Analysis Types**: Linear static, P-Delta, and nonlinear analysis support
- **Results Extraction**: Comprehensive results including displacements, forces, and reactions
- **Validation**: Built-in model validation and statics checking

## Example: Two-Storey Building

The included example demonstrates a complete two-storey rectangular building:

### Structure Details
- **Dimensions**: 6m × 4m × 6m (height)
- **Construction**: Steel frame with HEB200 columns and IPE300 beams
- **Floors**: Two levels at 3m and 6m height
- **Supports**: Fixed base connections for all columns
- **Loading**: Dead loads, live loads, and wind loads

### Model Components
- **12 Nodes**: Ground level (4), first floor (4), second floor (4)
- **16 Members**: 8 columns, 8 beams
- **1 Material**: Steel S355 (E=210 GPa, fy=355 MPa)
- **2 Sections**: HEB200 columns, IPE300 beams
- **4 Supports**: Fixed base supports
- **20 Loads**: Point loads and distributed loads
- **3 Load Combinations**: ULS and SLS combinations

## Usage

### Basic Usage

```python
from sample_two_storey_model import create_two_storey_structure
from aidea_to_pynite_translator import AideaToPyniteTranslator

# Create AIDEA model
aidea_model = create_two_storey_structure()

# Initialize translator
translator = AideaToPyniteTranslator()

# Translate to PyNite
pynite_model = translator.translate_model(aidea_model)

# Run analysis
translator.run_analysis(analysis_type='linear', log=True, check_statics=True)

# Get results
results = translator.get_results_summary()
```

### Complete Workflow

Run the complete analysis workflow:

```bash
python run_structural_analysis.py
```

This will:
1. Create the AIDEA model
2. Translate to PyNite format
3. Run structural analysis
4. Display comprehensive results
5. Perform model validation

## Analysis Results

The system provides comprehensive analysis results:

### Node Results
- **Displacements**: DX, DY, DZ translations
- **Rotations**: RX, RY, RZ rotations
- **Maximum values**: Identified with node locations

### Member Results
- **Forces**: Axial, shear, and moment forces
- **Extrema**: Maximum and minimum values along member length
- **Diagrams**: Shear, moment, and deflection diagrams (via PyNite)

### Support Reactions
- **Forces**: Reaction forces in all directions
- **Moments**: Reaction moments about all axes
- **Equilibrium**: Automatic statics checking

### Load Combinations
- **Multiple Combinations**: ULS and SLS combinations
- **Factored Results**: Properly factored load combinations
- **Envelope Results**: Maximum and minimum values across combinations

## Model Validation

The system includes comprehensive validation:

- **Geometry Validation**: Node connectivity and member orientation
- **Load Validation**: Load application and load combination factors
- **Support Validation**: Support condition verification
- **Statics Checking**: Global equilibrium verification
- **Stability Checking**: Model stability analysis

## Advanced Features

### Custom Materials
```python
material = Material(
    name='Custom Steel',
    elasticity_modulus=200000.0,  # MPa
    shear_modulus=77000.0,        # MPa
    density=7850.0,               # kg/m³
    poissons_ratio=0.3,
    yield_strength=355.0,         # MPa
    thermal_expansion_coefficient=12e-6  # 1/°C
)
```

### Custom Sections
```python
section = Section(
    name='Custom Beam',
    area=0.0053,      # m²
    Iz=8356e-8,       # m⁴ (strong axis)
    Iy=604e-8,        # m⁴ (weak axis)
    J=20.1e-8,        # m⁴ (torsion)
    material_id=1
)
```

### Load Combinations
```python
load_combo = LoadCombination(
    name='1.35G + 1.5Q',
    criteria='ULS',
    Dead=1.35,
    Live=1.5,
    Wind=0.9
)
```

## Analysis Types

### Linear Static Analysis
```python
translator.run_analysis(
    analysis_type='linear',
    log=True,
    check_stability=True,
    check_statics=True
)
```

### P-Delta Analysis
```python
translator.run_analysis(
    analysis_type='pdelta',
    log=True,
    max_iter=30
)
```

### Nonlinear Analysis
```python
translator.run_analysis(
    analysis_type='nonlinear',
    log=True,
    max_iter=30,
    num_steps=10
)
```

## Dependencies

- **PyNite**: Finite element analysis engine
- **Pydantic**: Data validation and settings management
- **NumPy**: Numerical computations
- **Python 3.8+**: Required Python version

## Installation

1. Install PyNite:
```bash
pip install PyNite
```

2. Install additional dependencies:
```bash
pip install pydantic numpy
```

3. Clone or download the project files

## Extending the System

### Adding New Element Types
1. Define new element in `aidea_model.py`
2. Add translation logic in `aidea_to_pynite_translator.py`
3. Update result extraction methods

### Custom Analysis Types
1. Extend the `run_analysis` method
2. Add new analysis parameters
3. Update result processing

### Additional Load Types
1. Define new load classes in `aidea_model.py`
2. Add translation methods in translator
3. Update load combination handling

## Troubleshooting

### Common Issues

1. **Missing Material Properties**: Ensure all required material properties are defined
2. **Invalid Node References**: Check that all member node references exist
3. **Load Application**: Verify load directions and magnitudes
4. **Support Conditions**: Ensure adequate support for stability

### Debugging

Enable detailed logging:
```python
translator.run_analysis(analysis_type='linear', log=True)
```

Check model validation:
```python
orphaned_nodes = pynite_model.orphaned_nodes()
if orphaned_nodes:
    print(f"Warning: Orphaned nodes found: {orphaned_nodes}")
```

## Performance

### Model Size Recommendations
- **Small Models**: < 100 nodes, < 200 members
- **Medium Models**: 100-1000 nodes, 200-2000 members  
- **Large Models**: > 1000 nodes, > 2000 members

### Analysis Performance
- **Linear Analysis**: Fast, suitable for most applications
- **P-Delta Analysis**: Moderate, for second-order effects
- **Nonlinear Analysis**: Slower, for advanced analysis

## License

This project is part of the AIDEA structural analysis system development.

## Contributing

1. Follow the existing code structure
2. Add comprehensive documentation
3. Include test cases for new features
4. Ensure backward compatibility

## Support

For questions and support, refer to:
- PyNite documentation: [PyNite GitHub](https://github.com/JWock82/PyNite)
- Pydantic documentation: [Pydantic Docs](https://pydantic-docs.helpmanual.io/)

---

**Note**: This system demonstrates the complete workflow from AIDEA model definition through PyNite analysis to results extraction. The example two-storey building provides a comprehensive template for creating more complex structural models.
