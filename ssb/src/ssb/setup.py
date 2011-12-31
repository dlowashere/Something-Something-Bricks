'''
Script for using py2exe to create Windows binary.

Created on Dec 30, 2011

@author: Dan
'''

from distutils.core import setup
import py2exe
import os

origIsSystemDLL = py2exe.build_exe.isSystemDLL
def isSystemDLL(pathname):
        if os.path.basename(pathname).lower() in ("libfreetype-6.dll", "libogg-0.dll", "sdl_ttf.dll"):
                return 0
        return origIsSystemDLL(pathname)
py2exe.build_exe.isSystemDLL = isSystemDLL

setup(console=["ssb.py"])