#!/usr/bin/env python
"""  COPYRIGHT (c) 2016 UNIVERSITY OF NEBRASKA NIMBUS LAB - JOHN-PAUL ORE
        PHRIKY-UNITS, THE PHYSICAL UNITS INCONSISTENCY DETECTION TOOL
"""
import argparse
from cps_units_checker import CPSUnitsChecker
from subprocess import Popen
import os
import re
from distutils import spawn
import sys
import pkg_resources

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# COMMAND LINE ARGS 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
parser = argparse.ArgumentParser(description='Detect physical unit inconsistencies in C++ code, especially ROS code.')
parser.add_argument('target_file', type=str,
                   help='target cpp file analyzed for physical units inconsistencies. ')
parser.add_argument('--include', dest='include_dir', 
                   help='include directory for cppcheck')
args = parser.parse_args()
target_file = args.target_file


original_directory = os.getcwd()
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# TEST FOR CPPCHECK
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


if not spawn.find_executable('cppcheck'):
    sys.stderr.write( 'cppcheck not installed...')
    sys.exit(1)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# RUN CPPCHECK
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# EXTRACT DIR

if not os.path.exists(target_file):
    sys.stderr.write( 'file does not exist: %s' % target_file)
    sys.exit(1)

sys.stderr.write( 'Attempting to run cppcheck...')
target_file_dir = os.path.dirname(target_file)
sys.stderr.write( 'Changing directory to %s' % target_file_dir)
os.chdir(target_file_dir)
target_file_base_name = os.path.basename(target_file)

# local_cfg_path = os.path.join(path, 'cfg')
# if not os.path.exists(local_cfg_path):
    # os.symlink(cfg_path, 'cfg')

cppcheck_process = Popen(['cppcheck', '--dump', '-I ../include', target_file_base_name])
cppcheck_process.communicate()
if cppcheck_process.returncode != 0:
    sys.stderr.write( 'cppcheck appears to have failed..exiting with return code %d' % cppcheck_process.returncode)
    sys.exit(1)
dump_filename = os.path.basename(target_file) + '.dump'
sys.stderr.write( "Created cppcheck 'dump' file %s'" % dump_filename)
 

os.chdir(original_directory)

cps_unit_checker = CPSUnitsChecker()
dump_file = os.path.join(os.path.dirname(target_file), dump_filename)
source_file = dump_file.replace('.dump','')
cps_unit_checker.main_run_check(dump_file, source_file)

for e in cps_unit_checker.errors:
    sys.stderr.write( "%s\n" % e.get_error_desc())
    sys.stderr.write( "%s\n" % e.linenr)
    sys.stderr.write( "%s\n" % e.units_at_first_assignment)
    sys.stderr.write( "%s\n" % e.all_units_assigned_to_var)
    sys.stderr.write( "%s\n" % e.units_when_multiple_happened)




