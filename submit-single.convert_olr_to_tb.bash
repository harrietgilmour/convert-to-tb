#!/bin/bash -l
#SBATCH --mem=10000
#SBATCH --ntasks=4
#SBATCH --time=5

# Check that the correct number of arguments were provided
if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters"
    echo "Usage: submit-single.convert_olr_to_tb.bash year month"
    exit 1
fi

# Extract args from the command line
year=$1
month=$2

echo "$year"
echo "$month"

python process_scripts/convert_olr_to_tb.py ${year} ${month}