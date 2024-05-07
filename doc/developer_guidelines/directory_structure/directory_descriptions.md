# Project Directory Structure

This repository follows a standard directory structure to organize its files and resources. Below is an explanation of each directory and file:

- **assests**: Contains images, icons, favicons, etc., for the project.

- **bmslogic**: Contains the source code for the project.
  - *calc_helpers*: contains source code that aids in the simulation calculations.
  - *extern*: external libraries or dependencies for the simulations.
  - *parameter_sets*: contains the datasets for the simulations.
  - *simulations*: Configuration files for build tools.
    - *application*: source code for the battery pack applications, including electric vehicles (EVs)
    - *cell*: source code for the battery cell simulations
    - *pack*: source code for the battery pack simulations

- **docs**: Documentation related to the project.
  - *changelog*: Documentation for API endpoints.
  - *developer_guidelines*: Guides on how to use the project or its features.
    - *code_standards*
    - *conducting_tests*
    - *deployment*
    - *directory_structure*
    - *version_control*
  - *release_info*: Images used in the documentation.
  - *source*: source directory for the Sphinx documentation package (https://www.sphinx-doc.org/en/master/).

- **examples**: Code examples demonstrating features or use cases.

- **extern**: third party libraries and dependencies.
  - *pybind11*: Used for binding the C++ code to Python.

- **tests**: Third-party libraries and dependencies installed via npm or yarn.

- **.gitignore**: Specifies intentionally untracked files to ignore in version control.

- **.gitmodules**: Tracks information on the used Github repositories used in this project.

- **README.md**: Overview of the project, how to get started, and other relevant information for developers.

This structure helps in organizing the project files, making it easier for developers to navigate and contribute to the codebase. For more detailed information, refer to the specific directories and files in this repository.
