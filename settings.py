import os
import sys

PROJ_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJ_DIR)

LIB_DIR = os.path.join(PROJ_DIR, 'libs')
sys.path.insert(0, LIB_DIR)

UPLOAD_DIR = os.path.join(PROJ_DIR, 'uploads')
