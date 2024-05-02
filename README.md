<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->

<!-- [![Contributors][contributors-shield]][contributors-url] -->
<!-- [![Forks][forks-shield]][forks-url] -->
<!-- [![Stargazers][stars-shield]][stars-url] -->
<!-- [![Issues][issues-shield]][issues-url] -->
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC_BY--NC_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
<!-- [![LinkedIn][linkedin-shield]][linkedin-url] -->



<!-- PROJECT LOGO -->

<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="assests/BMSLogic_logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">BMSLogic</h3>
<p align="left">BMSLogic © 2024 by Moin Ahmed is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International <p> 


  <p align="center">
    Created by: Moin Ahmed 
    <br />
    Source code for the everything related to battery management systems (BMS), wriite mostly in Python and C++. The backend source code is mainly written in Python and C++.
    <!-- <br />
    <a href="https://github.com/github_username/repo_name"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/github_username/repo_name">View Demo</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a> -->
  </p>
</div>



<!-- TABLE OF CONTENTS -->

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

This repository contains the source code for performing battery management system related simulations and calculations including battery cell, battery packs, and other system-level simulations.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

The following contains the instructions for running this repository locally in this machine.

### Prerequisites

* Ensure your system has the following
    * Python with pip and venv installed
    * CMake


### Installation

1. Clone the repo
   ```sh
   git clone --recurse-submodules git@github.com:ChargeSage-Inc/BMSLogic.git
   ```
3. Build the C++ files using cmake
   ```sh
   cd build && mkdir build
   cmake ..
   cmake --build .
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>
