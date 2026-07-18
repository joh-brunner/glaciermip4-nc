# GlacierMIP4 NetCDF Examples

This repository provides Python and Jupyter Notebook examples for generating **CF-compliant NetCDF files** for **GlacierMIP4** using **xarray**.

You can use the notebooks and Python code to create your own files. Alternatively, you can use the provided examples, which already follow the correct structure, and simply insert your own data.

If you have questions about the output format or data submission, please contact:

**johanmbr@uio.no**

- Individual glacier submissions for RGI7C can be discussed.
- CF checks were successful for regional files, but not for individual files due to character arrays in dimensions.
- Metadata should be added to not rely fully on file names.

## Contents

- Workflow Notebooks for creating cf-compliant GlacierMIP4 NetCDF files
- Example output data

## Requirements

- Python 3.12
- `xarray` and the packages listed in `requirements.txt`

## Installation

Create and activate a dedicated Conda environment:

```bash
conda create -n glaciermip-nc python=3.12
conda activate glaciermip-nc
pip install -r requirements.txt
```

## Getting Started

After installing the dependencies, open the Jupyter Notebooks to learn how to generate GlacierMIP4-compliant NetCDF output files.