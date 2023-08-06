apt-deps
========
Recursively resolve package dependencies using apt.

Usage
~~~~~


Features
~~~~~~~~
It works 60% of the time, every time.


Build
~~~~~
On Ubuntu and Debian systems, you can apt-get install python-apt

If you want to build in a virtualenv, you need to do one of the following:
1) Initiate your virtualenv using site-packages
virtualenv --site-packages

2) Install required system libs and install python-apt from source.
apt-get install g++ gcc libapt-pkg-dev
pip install git+git://anonscm.debian.org/apt/python-apt.git@1.1.0_beta1
