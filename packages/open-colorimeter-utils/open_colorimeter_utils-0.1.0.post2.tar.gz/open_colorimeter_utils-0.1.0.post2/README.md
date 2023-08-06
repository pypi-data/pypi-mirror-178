# Utilities for IO Rodeo's Open Colorimeter 


## Installing
Install using pip 

```bash
$ pip install open-colorimeter-utils
```

## Installing from source

This package uses the [poetry](https://python-poetry.org/) dependency manager.
The installation instructions for poetry can be found
[here](https://python-poetry.org/docs/#installation)

Once poetry is installed the open-colorimeter-utils package can be installed using

```bash
$ poetry install
```

Additional documentation on using poetry can be found
[here](https://python-poetry.org/docs/)


## Using the Open Colorimeter calibration tool

The Open Colorimeter calibration tool "oc-cal" is a command line program which can fit
calibratin data and generate the calibration.json used by the Open Colorimeter.

```console
Usage: oc-cal [OPTIONS] [INPUT_FILES]...

  Generates an Open Colorimeter calibration .json file from the .toml input
  files

  .toml file format 
  -----------------
  name = "TestName"          # Name of the test
  led = 630                  # Led wavelength
  units = "ppm"              # Measurement units
  fit_type = "polynomial"    # Fit type, polynomial or linear
  fit_order = 2              # Order of the fit
  values = [                 # Array of measurements
      [c0, c1, .... , cn],   # Measurements in units
      [a1, a1, .... , an]    # Corresponding absorbances
      ]

Options:
  -o, --output-file FILENAME  output file
  --help                      Show this message and exit.
```

The input calibration data is provided in the from of one of more .toml files
with the following format

```toml
name = "Nitrite API"
led = 520 
units = "ppm" 
fit_type = "polynomial"
fit_order = 2
values = [ 
    [0.00, 0.40, 0.80, 1.20, 1.60, 2.00], # concentration
    [0.00, 0.30, 0.59, 0.88, 1.14, 1.39], # absorbance
    ]
```

In order to generate the calibrations simple run

```bash
$ oc-cal nitrite.toml
```
The oc-cal program will generate the calibrations.json file used by the open
colorimeter. An alternative name can be given to this file using the -o of
--output options.  

An example of the calibrations.json file generated using the data from the .toml
file above is shown below

```json
{
  "Nitrite API": {
    "units": "ppm",
    "led": "520",
    "fit_type": "polynomial",
    "fit_coef": [
      0.11543984594053638,
      1.2747960322708907,
      0.0
    ],
    "range": {
      "min": 0.0,
      "max": 1.39
    }
  }
}
```

In addtion the oc-cal program will fit the data and plots the results as shown below.

![example plot](images/nitrite_calibration_example.png)


An example of calibrations.json file made using multiple .toml input files is shown below
```json
{
  "Ammonia API": {
    "units": "ppm",
    "led": "630",
    "fit_type": "polynomial",
    "fit_coef": [
      1.0128521350438369,
      1.890930808804952,
      0.0
    ],
    "range": {
      "min": 0.0,
      "max": 2.0
    }
  },
  "Nitrate API": {
    "units": "ppm",
    "led": "520",
    "fit_type": "polynomial",
    "fit_coef": [
      0.32039213453320625,
      34.032597696304,
      0.0
    ],
    "range": {
      "min": 0.0,
      "max": 1.47
    }
  },
  "Nitrite API": {
    "units": "ppm",
    "led": "520",
    "fit_type": "polynomial",
    "fit_coef": [
      0.13111937060865314,
      1.2591439203550079,
      0.0
    ],
    "range": {
      "min": 0.0,
      "max": 1.4
    }
  }
}
```



