import subprocess
import sys
from graphviz import Graph


gv_file_path = "D:/github/PythonHub/h2o-work/GBM_ForLoanPredict.gv"
image_file_name = "D:/github/PythonHub/h2o-work/gbm_tree.png"
win_install_graphviz_path = "C:\\Program Files (x86)\\Graphviz2.38\\bin\\"


def generateTreeImage(gv_file_path, image_file_path):
    result = subprocess.call([win_install_graphviz_path + "dot", "-Tpng", gv_file_path, "-o", image_file_path], shell=True)


generateTreeImage(gv_file_path, image_file_name)


