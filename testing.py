import pkg_resources
import os

# Get the package installation path
pkg_path = pkg_resources.resource_filename('saft_data_mgmt', 'SQLTables')

# Verify core SQL files exist
core_path = os.path.join(pkg_path, 'Core')
expected_core_files = [
    'securities_info.sql',
    'security_exchange.sql', 
    'security_types.sql'
]

for sql_file in expected_core_files:
    full_path = os.path.join(core_path, sql_file)
    print(f"Checking {full_path}: {os.path.exists(full_path)}")