#!/bin/sh -l
#
# This script submits a job to the queue to make monthly cubes
#
# Usage: submit.make_monthly_cubes.bash <year>
#
# For example: bash submit.make_monthly_cubes.bash 1998
#

# Check that the year has been provided
if [ $# -ne 1 ]; then
    echo "Usage: submit.make_monthly_cubes.bash <year>"
    exit 1
fi

# Set the year
year=$1

# Set up the months
months=(01 02 03 04 05 06 07 08 09 10 11 12)

# Set up the extractor script
EXTRACTOR="/data/users/hgilmour/convert-to-tb/submit-single-job-test.sh"

# Set up the output directory for the LOTUS job
OUTPUT_DIR="/data/users/hgilmour/convert-to-tb/lotus_output"
mkdir -p $OUTPUT_DIR

# Activate the conda environment
# conda activate myclone

# Loop over the months
for month in ${months[@]}; do

    # Echo the year and month
    echo "Year: $year"
    echo "Month: $month"

    # Set up the output files
    OUTPUT_FILE="$OUTPUT_DIR/make_monthly_cubes.$year.$month.out"
    ERROR_FILE="$OUTPUT_DIR/make_monthly_cubes.$year.$month.err"

    # Submit the batch job
    sbatch --mem=1000 --ntasks=4 --time=5 --output=$OUTPUT_FILE --error=$ERROR_FILE $EXTRACTOR $year $month

done
