# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['open_colorimeter_utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'matplotlib>=3.6.1,<4.0.0',
 'numpy>=1.23.4,<2.0.0',
 'tomli>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['oc-cal = '
                     'open_colorimeter_utils.calibration_cli_app:app_main']}

setup_kwargs = {
    'name': 'open-colorimeter-utils',
    'version': '0.1.0.post1',
    'description': "Utilities for iorodeo's open colorimeter",
    'long_description': '# Utilities for IO Rodeo\'s Open Colorimeter \n\n\n## Installing\nInstall using pip \n\n```bash\n$ pip install open-colorimeter-utils\n```\n\n## Installinng from source\n\nThis package uses the [poetry](https://python-poetry.org/) dependency manager.\nThe installation instructions for poetry can be found\n[here](https://python-poetry.org/docs/#installation)\n\nOnce poetry is installed the open-colorimeter-utils package can be installed using\n\n```bash\n$ poetry install\n```\n\nAdditional documentation on using poetry can be found\n[here](https://python-poetry.org/docs/)\n\n\n## Using the Open Colorimeter calibration tool\n\nThe Open Colorimeter calibration tool "oc-cal" is a command line program which can fit\ncalibratin data and generate the calibration.json used by the Open Colorimeter.\n\n```console\nUsage: oc-cal [OPTIONS] [INPUT_FILES]...\n\n  Generates an Open Colorimeter calibration .json file from the .toml input\n  files\n\n  .toml file format \n  -----------------\n  name = "TestName"          # Name of the test\n  led = 630                  # Led wavelength\n  units = "ppm"              # Measurement units\n  fit_type = "polynomial"    # Fit type, polynomial or linear\n  fit_order = 2              # Order of the fit\n  values = [                 # Array of measurements\n      [c0, c1, .... , cn],   # Measurements in units\n      [a1, a1, .... , an]    # Corresponding absorbances\n      ]\n\nOptions:\n  -o, --output-file FILENAME  output file\n  --help                      Show this message and exit.\n```\n\nThe input calibration data is provided in the from of one of more .toml files\nwith the following format\n\n```toml\nname = "Nitrite API"\nled = 520 \nunits = "ppm" \nfit_type = "polynomial"\nfit_order = 2\nvalues = [ \n    [0.00, 0.40, 0.80, 1.20, 1.60, 2.00], # concentration\n    [0.00, 0.30, 0.59, 0.88, 1.14, 1.39], # absorbance\n    ]\n```\n\nIn order to generate the calibrations simple run\n\n```bash\n$ oc-cal nitrite.toml\n```\nThe oc-cal program will generate the calibrations.json file used by the open\ncolorimeter. An alternative name can be given to this file using the -o of\n--output options.  \n\nAn example of the calibrations.json file generated using the data from the .toml\nfile above is shown below\n\n```json\n{\n  "Nitrite API": {\n    "units": "ppm",\n    "led": "520",\n    "fit_type": "polynomial",\n    "fit_coef": [\n      0.11543984594053638,\n      1.2747960322708907,\n      0.0\n    ],\n    "range": {\n      "min": 0.0,\n      "max": 1.39\n    }\n  }\n}\n```\n\nIn addtion the oc-cal program will fit the data and plots the results as shown below.\n\n![example plot](images/nitrite_calibration_example.png)\n\n\nAn example of calibrations.json file made using multiple .toml input files is shown below\n```json\n{\n  "Ammonia API": {\n    "units": "ppm",\n    "led": "630",\n    "fit_type": "polynomial",\n    "fit_coef": [\n      1.0128521350438369,\n      1.890930808804952,\n      0.0\n    ],\n    "range": {\n      "min": 0.0,\n      "max": 2.0\n    }\n  },\n  "Nitrate API": {\n    "units": "ppm",\n    "led": "520",\n    "fit_type": "polynomial",\n    "fit_coef": [\n      0.32039213453320625,\n      34.032597696304,\n      0.0\n    ],\n    "range": {\n      "min": 0.0,\n      "max": 1.47\n    }\n  },\n  "Nitrite API": {\n    "units": "ppm",\n    "led": "520",\n    "fit_type": "polynomial",\n    "fit_coef": [\n      0.13111937060865314,\n      1.2591439203550079,\n      0.0\n    ],\n    "range": {\n      "min": 0.0,\n      "max": 1.4\n    }\n  }\n}\n```\n\n\n\n',
    'author': 'Will Dickson',
    'author_email': 'will@iorodeo.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/iorodeo/open-colorimeter-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
