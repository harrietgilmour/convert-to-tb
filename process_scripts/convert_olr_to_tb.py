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
