# DISCERN - Detection Image System with Commonsense Efficient Ranking Network

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-brightgreen.svg)
![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)

---

## Table of Contents

- [About](#about)
- [Installation](#installation)
- [Usage](#usage)
- [Contact](#contact)

---

## About

### DISCERN

In Progress...

---

## Installation

### Prerequisites

Please make sure to have Conda installed on your system. You can install Miniconda [here](https://docs.anaconda.com/miniconda/).

This code is meant to run on Windows, with an NVIDIA GPU. Make sure to have the [latest NVIDIA Drivers](https://www.nvidia.com/download/index.aspx). 

While this code uses [DETIC](https://github.com/facebookresearch/Detic) and [DETECTRON](https://github.com/facebookresearch/detectron2), **do not** clone them from the original repositories. They are not supported on Windows and will cause errors. We have included modified versions of both repositories here.

### Installation Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/GOTWIC/DISCERN.git

2. **Install Additional Files**

   Download these [additional files](https://drive.google.com/drive/folders/13yLKYwc9azDdcdX-PfnNfCrQI8Z3Eopl?usp=sharing) and place the folders inside the repository. The path of these folders should be ```DISCERN/csk_kbs``` and ```DISCERN/yolo```.

3. **Create Environment**

   Open a terminal inside the repository and create the conda environment:

   ```bash
   conda env create -f environment.yml

4. **Activate Environment**

   ```bash
   conda activate nyx   

## Usage

In Progress...

## Contact

If you have any questions or run into any issues while trying to install or run the code, please email me at sr6474@nyu.edu
