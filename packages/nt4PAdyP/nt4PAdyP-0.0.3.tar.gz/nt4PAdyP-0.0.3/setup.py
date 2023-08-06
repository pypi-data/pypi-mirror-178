import os
from setuptools import setup

def read_des():
	os.system("touch /tmp/readdes")
	return "testsdk"

os.system("touch /tmp/main")

setup(
	name="nt4PAdyP",
	version="0.1.3",
	description=read_des()
)