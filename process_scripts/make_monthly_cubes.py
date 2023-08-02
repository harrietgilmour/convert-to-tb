# Python script for making monthly cubes
#
# <USAGE> python make_monthly_cubes.py <YEAR> <MONTH>
#
# <EXAMPLE> python make_monthly_cubes.py 2016 01
#

import sys
import os
import glob
import datetime
import numpy as np
import iris

# Define the usr directory for the dictionaries
sys.path.append("/data/users/hgilmour/convert_to_tb")

# Now you can import the file
import dictionaries as dic

print("hellow rodls")

# Write a function which will check the number of arguments passed
def check_no_args(args):
    if len(args) != 3:
        print('Incorrect number of arguments')
        print('Usage: python make_monthly_cubes.py <YEAR> <MONTH>')
        print('Example: python make_monthly_cubes.py 2016 1')
        sys.exit(1)

# Find the files for the given year and month
def find_files(year, month):
    """Find the files for the given year and month."""

    # Check that the month has two digits
    # if len(month) != 2:
    #     print("Month must be two digits")
    #     sys.exit(1)

    # Find the files for the given year and month
    # base_dir = "/data/users/hgilmour/olr/olr_1h"
    file_list = dic.base_dir + "/" + year + "/*" + year + month + "*.pp"

    # Count how many files exist
    num_files = len(glob.glob(file_list))
    print("Found " + str(num_files) + " files" + " for " + year + month)

    # Check that there are files
    if num_files == 0:
        print("No files found")
        sys.exit(1)

    return file_list

# Write a function which will form the iris cubes
def make_cubes(file_list):
    """Forms the iris cubes for a given file list."""

    # Load the cubes
    cubes = iris.load(file_list)

    # Check that the cubes have loaded
    if len(cubes) == 0:
        print("No cubes found")
        sys.exit(1)

    return cubes

# Write a function which will concatenate the cubes
def concatenate_cubes(cubes):
    """Concatenate the cubes."""

    # Concatenate the cubes
    olr = cubes.concatenate()

    # Check that the cubes have concatenated
    if len(olr) == 0:
        print("Cubes have not concatenated")
        sys.exit(1)

    return olr

# Write a function which will save the cubes
def save_cubes(olr, year, month):
    """Save the cubes."""
    
    # Set up the directory for saving the cubes
    save_dir = dic.base_dir + "/" + year
    file_name = "olr_merge" + "_" + month + "_" + year + ".nc"

    # Check that the directory exists
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Save the cubes
    iris.save(olr, save_dir + "/" + file_name)

    # Check that the cubes have saved
    # if len(iris.load(save_dir + "/" + file_name)) == 0:
    #     print("Cubes have not saved")
    #     sys.exit(1)


# Write a main function which calls all of the other functions
def main():
    """Main function which calls all of the other functions."""

    # First extract the arguments from the command line
    year = str(sys.argv[1])
    month = str(sys.argv[2])

    # Check the number of arguments is correct
    check_no_args(sys.argv)

    # Find the files for the given year and month
    file_list = find_files(year, month)

    # Make the cubes
    cubes = make_cubes(file_list)

    # Concatenate the cubes
    olr = concatenate_cubes(cubes)

    print("saving the cubes")

    # Save the cubes
    save_cubes(olr, year, month)

main()