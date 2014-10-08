#!/bin/bash

#install pip for installing libraries
sudo apt-get install pip

# install scipy for scientific computations
sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose

# install simplecv library and its dependencies
sudo apt-get install python-pygame
sudo apt-get install libopencv python-opencv
sudo pip install sqlalchemy simplecv
