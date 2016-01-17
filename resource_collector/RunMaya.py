import os
import subprocess

cwd = os.getcwd()
maya_exec = 'C:/Program Files/Autodesk/Maya2015/bin/maya.exe'
# mayaa_exec = '/Applications/Autodesk/maya2014/Maya.app/Contents/bin/maya'


cmd = maya_exec

# Set up environmental variables
os.environ['MAYA_PROJECT'] = cwd
os.environ['PYTHONPATH'] = os.path.join(cwd, 'scripts')
os.environ['MAYA_SCRIPT_PATH'] = os.path.join(cwd, 'Scripts')
os.environ['MAYA_APP_DIR'] = 'H:/Code/Python/kk-maya-launcher/config/user_prefs/maya'

subprocess.Popen(cmd)