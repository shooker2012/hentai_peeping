# setup.py
from distutils.core import setup
import py2exe      
 
setup(
        windows=['main_frame.py'],
        options={
                "py2exe":{
                        "unbuffered": True,
                        "optimize": 2,
                        "packages": ["lxml", "cssselect"],
                        "bundle_files": 2,
                        # "excludes": ["email"],
                }
        }
)
