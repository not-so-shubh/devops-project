"""Apply external Grafana credentials without a password in argv or on disk."""
import getpass
import json
import subprocess

password=getpass.getpass('Grafana admin password (at least 16 characters): ')
if len(password)<16:
    raise SystemExit('Use at least 16 characters')
secret={'apiVersion':'v1','kind':'Secret','metadata':{'name':'stockpilot-grafana','namespace':'monitoring'},'type':'Opaque','stringData':{'admin-user':'admin','admin-password':password}}
subprocess.run(['kubectl','apply','--server-side','-f','-'],input=json.dumps(secret),text=True,check=True)
print('Grafana credentials applied without saving a password file.')
