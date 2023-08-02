# Python script for converting from OLR to TB
#
# <USAGE> python convert_olr_to_tb.py <YEAR> <MONTH>
#
# <EXAMPLE> python convert_olr_to_tb.py 2016 01
#

# Local imports
import sys
import os
import glob
import datetime

# Third party imports
import numpy as np
import iris

# Define the usr directory for the dictionaries
sys.path.append("/data/users/hgilmour/convert-to-tb")

# Import the dictionaries
import dictionaries as dic

# Write a function which will check the number of arguments passed
def check_no_args(args):
    """Check the number of arguments passed."""
    if len(args) != 3:
        print('Incorrect number of arguments')
        print('Usage: python convert_olr_to_tb.py <YEAR> <MONTH>')
        print('Example: python convert_olr_to_tb.py 2016 1')
        sys.exit(1)

# Find the files for the given year and month
def find_files(year, month):
    """Find the files for the given year and month."""

    # Find the file for the given year and month
    file = dic.base_dir + "/" + year + "/" + "olr_merge_" + month + "_" + year + ".nc"

    # Check that the file exists
    if not os.path.exists(file):
        print("File does not exist:", file)
        sys.exit(1)

    return file

# Write a function which loads the file as an iris cube
def load_file(file):
    """Load the file as an iris cube."""

    # Load the file as an iris cube
    olr = iris.load_cube(file)

    # Print the data type of the cube
    # print("Data type of the cube:", olr.dtype)

    return olr


# Write a function which will calculate the brightness temperature
# from the OLR
def convert_olr_to_tb(olr):
    """Convert the OLR to brightness temperature."""

    # Calculate the equivalent temp flux
    tf = (olr.data / dic.sigma) ** 0.25

    # Calculate the brightness temperature
    tb_var =(-dic.a + np.sqrt(dic.a ** 2 + 4 * dic.b * tf.data)) / (2 * dic.b)

    return tb_var

# Write a function which will save the brightness temperature
# as a netcdf file
def append_data(olr, tb_var, year, month):
    """Copies the original OLR cube to later append the new data to."""

    # Copy the original cube
    tb = olr.copy()

    # Replace the data with the brightness temperature
    tb.data = tb_var.data

    # Change the units
    tb.units = "K"

    return tb

# Write a function which will save the brightness temperature
def save_file(tb, year, month):
    """Saves the file."""

    # Set up the directory for saving
    save_dir = dic.cubes_dir + "/" + year

    # If this directory does not exist, create it
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Set up the file name for saving
    filename = "tb_merge_" + month + "_" + year + ".nc"

    # Save the file
    iris.save(tb, save_dir + "/" + filename)

    return

# Define the main function
def main():
    """Main function."""

    # First extract the arguments
    year = str(sys.argv[1])
    month = str(sys.argv[2])

    # Check the number of arguments
    check_no_args(sys.argv)

    # first find the file
    file = find_files(year, month)

    # Load the file as an iris cube
    olr = load_file(file)

    # Convert the OLR to brightness temperature
    tb_var = convert_olr_to_tb(olr)

    # Append the brightness temperature to the original cube
    tb = append_data(olr, tb_var, year, month)

    # Save the brightness temperature
    save_file(tb, year, month)

# Run the main function
if __name__ == "__main__":
    main()