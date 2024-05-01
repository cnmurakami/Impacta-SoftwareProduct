import os

is_docked = os.environ.get('DOCKED', False)

user = "root"
password = "Unitario123"
db = "rscarautomotive"
if not is_docked:
    host = 'localhost'
else:
    host = 'db'
print ('is_Docked:', is_docked)