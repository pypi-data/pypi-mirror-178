import sys
import tomli
import json
import click
import numpy as np
import matplotlib.pyplot as plt
from .data_fitting import polyfit_thru_zero

@click.command()
@click.argument('input_files', nargs=-1) 
@click.option('-o', '--output-file', 'output_file', type=click.File('w'), default='calibrations.json', help='output file')
def app_main(input_files, output_file):
    """Generates an Open Colorimeter calibration .json file from the .toml input files 

    \b
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
    
    
    """

    click.echo()
    click.echo(f'processing {len(input_files)} files')

    # Loop over all input files, fit and populate calibrations dict 
    calibrations_dict = {}
    for toml_input_file in input_files:

        click.echo(f'{toml_input_file}')

        # Load and parse toml file
        try:
            with open(toml_input_file, 'rb') as f:
                input_data = tomli.load(f)
        except Exception as error:
            error_msg = f'{toml_input_file} unable to load file. {error}'
            raise click.exceptions.UsageError(error_msg)

        # Exactact values
        try:
            name = str(input_data['name'])
            units = str(input_data['units'])
            fit_type = str(input_data['fit_type'])
            led = str(input_data['led'])
            vals = input_data['values']
        except Exception as error:
            error_msg = f'{toml_input_file}, missing {error}'
            raise click.exceptions.UsageError(error_msg)

        # Convert concetraton and absorbance values to numpy arrays
        try:
            conc = np.array(vals[0])
            abso = np.array(vals[1])
        except Exception as error:
            error_msg = f'{toml_input_file}, values incorrect format {error}'
            raise click.exceptoins.UsageError(error_msg)

        # Fit data, constrained to go through zero
        if fit_type not in ('linear', 'polynomial'):
            error_msg = f'{toml_input_file} unsupported fit type {fit_type}'
            raise click.exceptions.UsageError(error_msg)
        if fit_type == 'linear':
            fit_order = 1
        else:
            try:
                fit_order = int(input_data['fit_order'])
            except Exception as error:
                error_msg = f'{toml_input_file}, missing {error}'
                raise click.exceptions.UsageError(error_msg)
        fit_coef, abso_fit, conc_fit = polyfit_thru_zero(abso, conc, fit_order, 1000)
        conc_fit_polyval = np.polyval(fit_coef, abso_fit)

        # Add data to calibrations
        cal = {
            'units'    :  units, 
            'led'      :  led,
            'fit_type' :  fit_type, 
            'fit_coef' :  fit_coef.tolist(),
            'range'    :  {'min': abso.min(), 'max': abso.max()},
            }
        calibrations_dict[name] = cal

        # Plot result
        fig, ax = plt.subplots(1,1)
        ax.plot(abso_fit, conc_fit, 'r')
        ax.plot(abso_fit, conc_fit_polyval, 'r')
        ax.plot(abso, conc, 'ob')
        ax.grid(True)
        ax.set_xlabel('absorbance')
        ax.set_ylabel(f'concentration ({units})')
        ax.set_title(f'file: {toml_input_file}, name: {input_data["name"]}' )

    if calibrations_dict:
        json.dump(calibrations_dict, output_file, indent=2)
        print(f'calibrations written to {output_file.name}')
        plt.show()

    click.echo()







