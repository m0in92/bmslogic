# BMSLogic Architecture Design Document

## Purpose
This document explains how the repository is organized and how the core execution paths work so developers can quickly understand where to add features, fix bugs, and run experiments.

## 1) High-level architecture
BMSLogic is a **hybrid Python + C++** simulation stack for battery management applications:

- **Python layer** handles orchestration, user-facing APIs, parameter loading, and many solver/model implementations.
- **C++ layer** provides performance-oriented implementations for cell simulation primitives and exposes them to Python via **pybind11** modules.
- **Data layer** is composed of parameter-set CSV files and function modules (`funcs.py`) used to materialize model objects.
- **Application layer** includes EV/pack-level calculations and a lightweight Django interface.

At build-time, CMake compiles pybind11 extensions and static libraries. At runtime, Python modules import these compiled extensions when available.

## 2) Repository map by architectural responsibility

### Core build and dependency orchestration
- Root `CMakeLists.txt` controls top-level compilation, external dependencies, and toggles between embedded and full builds.
- `bmslogic/CMakeLists.txt` wires the internal C++/binding subprojects.

### Numerical helpers and math primitives
- `bmslogic/calc_helpers/` contains constants, ODE helpers, Kalman filtering logic, and C++ helper bindings.
- C++ extension module target: `calc_helpers`.

### Cell simulation engine (core domain)
- `bmslogic/simulations/cell/` is the main simulation engine.
- It contains:
  - **battery components** (electrodes, electrolyte, battery cell abstractions),
  - **physics/equivalent models** (SPM/SPMe/P2D/ECM-related classes),
  - **cyclers** (charge/discharge protocols),
  - **solvers** (electrode concentration, potential, degradation, and top-level battery solver),
  - **solution objects** for captured outputs.
- C++ extension module target: `cell`.
- Static C++ library target: `cell_sim`.

### Application-level simulations
- `bmslogic/simulations/applications/` provides EV pack/drivetrain dynamics, drive cycle handling, and external condition models.

### Parameterization
- `bmslogic/parameter_sets/` stores named battery datasets (`param_*.csv`) and function hooks (`funcs.py`).
- `ParameterSets` reads these files and produces simulation-ready battery objects.

### Entry points and interfaces
- `examples/` provides runnable scripts and C++ examples for experimentation.
- `tests/` and `cpp_tests/` validate Python and C++ behavior.
- `django_project/` + `django_app/` provide a web UI prototype around simulation workflows.

## 3) Build architecture (CMake)

1. Root CMake includes third-party dependencies (`pybind11`, `eigen`, plotting libs).
2. For non-embedded builds, it compiles:
   - the `bmslogic` modules,
   - C++ unit tests,
   - examples.
3. `bmslogic/simulations/cell/CMakeLists.txt` builds:
   - `cell` Python extension module (pybind11),
   - `cell_sim` static library for native C++ usage.
4. `bmslogic/calc_helpers/CMakeLists.txt` builds:
   - `calc_helpers` Python extension module (pybind11).

This enables one codebase to support both Python workflows and native C++ targets.

## 4) Runtime architecture and control flow

### 4.1 Cell simulation flow
Typical Python flow:

1. **Load parameter set** via `ParameterSets(name=...)`.
2. **Create battery objects** from CSV+function definitions.
3. **Choose cycler** (e.g., charge, discharge, custom profile).
4. **Instantiate solver** (e.g., `PySPSolver`) with model options (isothermal/degradation/electrode solver).
5. **Run solve loop** over time increments until termination criteria.
6. **Collect solution** arrays (voltage, SOC, temperature, capacity, etc.).

### 4.2 Layered responsibilities during solve
- **Cycler layer** provides applied current profile and stop criteria.
- **Electrode SOC solvers** update electrode surface concentrations/SOC.
- **Model layer** computes terminal voltage + overpotential decomposition.
- **Thermal/degradation submodels** optionally update temperature and resistance growth.
- **Solution layer** persists simulation outputs for plotting/export.

## 5) Python/C++ boundary

The boundary is intentionally explicit:

- `bindings_cpp_py.cpp` exposes C++ classes/functions (electrodes, battery cells, models, cyclers, solvers, etc.) into the `cell` Python module.
- Python code can either:
  - consume these bindings directly, or
  - use pure-Python classes with similar semantics.
- This makes it possible to trade developer ergonomics for performance depending on use case.

## 6) Data architecture

Each parameter set directory generally includes:

- `param_pos-electrode.csv`
- `param_neg-electrode.csv`
- `param_electrolyte.csv`
- `param_battery-cell.csv`
- optional degradation/extended electrolyte files
- `funcs.py` (OCP and other constitutive functions)

`ParameterSets` maps these artifacts into strongly-typed simulation objects and gracefully handles missing optional fields for advanced models (e.g., electrolyte transport details).

## 7) Test architecture

- **Python tests (`tests/`)** validate model equations, components, solver behavior, and application utilities.
- **C++ tests (`cpp_tests/`)** validate native implementations and solver internals.

The dual test strategy protects both the numerical API contract and the performance-oriented native layer.

## 8) Web interface architecture (Django)

The Django app is a thin orchestration layer:

- form input → simulation input extraction,
- calls into `bmslogic.simulations.cell` modules,
- renders results in templates.

It currently behaves like a demo/operator UI and is separated from the core simulation engine, which keeps domain logic reusable for scripts and backend services.

## 9) Extension points for developers

### Add a new parameter set
1. Create new folder under `bmslogic/parameter_sets/`.
2. Add required `param_*.csv` files.
3. Implement `funcs.py` with OCP/derivative functions.
4. Use `ParameterSets('<new_name>')` to instantiate.

### Add a new solver/model
1. Implement in Python under `bmslogic/simulations/cell/solvers/` or `models.py`.
2. Add tests under `tests/simulations/cell/`.
3. If performance-critical, add C++ equivalent and bind it in `bindings_cpp_py.cpp`.

### Add a new application workflow (e.g., new EV scenario)
1. Extend `bmslogic/simulations/applications/`.
2. Add example usage under `examples/`.
3. Add tests under `tests/simulations/application/`.

## 10) Architectural trade-offs

- **Pros**
  - Flexible dual-language implementation path.
  - Clear domain segmentation (cell/application/helpers/data).
  - Reusable parameterization mechanism.
  - Strong test scaffolding across Python and C++.

- **Cons / complexity hotspots**
  - Some overlap between Python and C++ implementations can increase maintenance burden.
  - Optional fallback patterns (when native modules are unavailable) require careful consistency checks.
  - Mixed naming/style conventions across legacy/newer modules can slow onboarding.

## 11) Suggested onboarding path for new developers

1. Read `README.md` and this document.
2. Run Python tests for fast feedback.
3. Explore one complete example in `examples/simulations/cell/`.
4. Trace `ParameterSets` → `PyBatteryCell` → `PySPSolver.solve()` end-to-end.
5. If touching performance-critical paths, review `bindings_cpp_py.cpp` and CMake targets next.

---

This document is intended to be a living architecture reference. Update it whenever major module boundaries, build targets, or runtime workflows change.
