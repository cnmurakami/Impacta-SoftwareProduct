#!!! Alterar para True para rodar local
local = False
#local = False

user = "root"
password = "Unitario123"
db = "rscarautomotive"
if local:
    host = 'localhost'
else:
    host = 'db'