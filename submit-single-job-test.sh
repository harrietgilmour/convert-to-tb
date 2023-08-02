#!/bin/bash -l
#SBATCH --mem=10000
#SBATCH --ntasks=4
#SBATCH --time=5

# conda init bash

# conda activate myclone

# Extract args from the command line
year=$1
month=$2

echo "$year"
echo "$month"

python process_scripts/make_monthly_cubes.py ${year} ${month}