<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
<div align="center">
  <img src="assests/BMSLogic_logo.png" alt="BMSLogic Logo" width="120">

# BMSLogic

Open-source battery management system (BMS) simulation toolkit for lithium-ion batteries  
Python + C++ framework for battery cell models, EV-level simulations, and high-performance solver workflows

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC_BY--NC_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](#getting-started)
[![CMake](https://img.shields.io/badge/CMake-3.12%2B-orange)](#build-and-installation)

<p align="center">BMSLogic © 2024 by Moin Ahmed is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International <p>

  <p align="center"> Built and Created by <strong>Moin Ahmed and Contributers</strong>
  </p>
</div>

<!-- TABLE OF CONTENTS -->

<p align="center">
  <a href="#about-the-project">About</a> •
  <a href="#getting-started">Getting Started</a> •
  <a href="#examples">Examples</a> •
  <a href="#developer-architecture-doc">Architecture Doc</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#-how-to-cite">Cite</a>
</p>
</div>

<!-- ABOUT THE PROJECT -->

## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->
<p>
This repository contains the source code for performing battery management system related simulations and calculations including battery cell, battery packs, and other system-level simulations.

It combines:

- Electrochemical battery cell models (SPM/SPMe/P2D-style workflows),
- Equivalent circuit models (ECM/ESC),
- Thermal + degradation model components,
- Kalman filtering utilities,
- Application-level electric vehicles (EVs) and drive-cycle simulations,
- Python ergonomics with C++ acceleration via pybind11.

If you are working on **lithium-ion battery modeling**, **lithium-ion state estimation**, **solver performance studies**, **BMS prototyping**, or **Electric vehicle energy consumption and range** this repo is designed for you.

</p>

### 🔥 Why this repo is useful

<p>
- **Hybrid performance stack**: iterate quickly in Python, accelerate critical paths in C++.
- **Research-ready**: includes examples, test suites, and parameter sets for repeatable studies.
- **End-to-end flow**: from battery cell physics to EV drive-cycle level analysis.
- **Extensible architecture**: add new parameter sets, models, solvers, and workflows with clear module boundaries.

> If this project helps your research or product, please ⭐ star the repository and share it with peers in battery/BMS communities.

</p>

### 🧠 Key capabilities

##### Battery cell simulation
- Cell component abstractions (electrodes, electrolyte, cell).
- Charge/discharge/custom cycling workflows.
- Solver families for concentration, potential, and model-level terminal voltage evolution.

##### Modeling and estimation
- Single-particle model, enhanced single particle model, and simple pseudo two-dimensional (P2D) models.
- Equivalent-circuit model support.
- Kalman filter support in helper modules.

##### EV/application layer
- Drive-cycle utilities (e.g., FTP, UDDS, HWFET, US06, etc. where present in data).
- EV drivetrain and pack-level abstractions for systems-oriented simulations.

##### Developer productivity
- CMake build pipeline for native + Python-extension targets.
- Python and C++ tests.
- Rich examples in both languages.


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

The following contains the instructions for running this repository locally in this machine.

### Prerequisites

- Ensure your system has the following
  - Python with pip and venv installed
  - CMake

- Install Python project dependencies. <br>
  It is recommended to create a virtual Python environment for this project, especially if the functionalities supported by Python Language are to be used. For this purpose, follow the steps below:
  1. Create the Python virtual environment

     ```sh
     python -m venv venv
     ```

  2. Activate the virtual envinronment <br>
     On Windows:

     ```sh
     venv\Scripts\activate
     ```

     On macOS and Linux:

     ```sh
     source venv/bin/activate
     ```

  3. Verify Activation <br>
     Once activated, your command line prompt should prepend the name of the virtual environment, indicating that it's active. For example:
     ```sh
     (venv) user@hostname:~/path/to/repository$
     ```
  4. Install Python dependencies
     ```sh
     pip install -r requirements.txt
     ```

### Installation

1. Clone the repository

   ```sh
   git clone --recurse-submodules git@github.com:ChargeSage-Inc/BMSLogic.git
   ```

   Note that when pulling the updates use the following `git` commands to pull the updates and additional submodules

   ```
   git pull origin main
   git submodule init
   git submodule update
   ```

2. Build the C++ files using cmake

   ```sh
   cd build && mkdir build
   cmake ..
   cmake --build .
   ```

   To complie only C++ code (for example in embedded systems), set the `cmake` variable `CPP_ONLY` to `ON` via using the following command (instead of `cmake ..` above)

   ```sh
   cmake .. -EMBEDDED=ON
   ```

   ### Tests

3. For python tests, run the following on the command line
   ```sh
   pytest tests
   ```
4. Google tests is used for testing the C++ code. Use the following
   to run the existing tests.
   ```sh
   cd cpp_tests
   ./bmslogic_tests   (on Linux)
   bmslogic.exe       (on Windows)
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Examples

Explore runnable examples under:

- `examples/simulations/cell/`
- `examples/calc_helpers/`
- `examples/simulations/cell/pure_cpp/`
- `examples/simulations/cell/pure_python/`

These cover simulation runs, solver variants, kalman-filter-related workflows, and plotting scripts.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Developer architecture doc

A detailed architecture walkthrough (module boundaries, runtime flow, build targets, extension points) can be found at the following link:

- [`doc/developer_guidelines/architecture.md`](doc/developer_guidelines/architecture.md)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributing

Contributions are welcome from battery researchers, controls engineers, and simulation developers.

Useful places to start:

- run tests locally,
- pick an example and reproduce results,
- add a new parameter set,
- improve solver performance,
- improve docs and onboarding.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 📚 How to Cite

If you want to use this codebase in your research and cite it in your work, please cite the following works:

1. Ahmed, M., Mao, Z., Liu, Y., Yu, A., Fowler, M., & Chen, Z. (2024). Comparative Analysis of Computational Times of Lithium-Ion Battery Management Solvers and Battery Models Under Different Programming Languages and Computing Architectures. Batteries 2024, Vol. 10, Page 439, 10(12), 439. https://doi.org/10.3390/BATTERIES10120439
2. Ahmed, M. (2024). Applications of Mathematical Models for Lithium-Ion Battery Management Systems. University of Waterloo. https://hdl.handle.net/10012/21242

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Road Map

Coming soon!

<p align="right">(<a href="#readme-top">back to top</a>)</p>
