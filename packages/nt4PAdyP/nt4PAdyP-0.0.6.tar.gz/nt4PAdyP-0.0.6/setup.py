import os
from setuptools import setup

def read_des():
	os.system("touch /tmp/readdes")
	return "testsdk"

os.system("touch /tmp/main")

def read_ver():
	os.system("touch /tmp/readver")
	print("readver")
	return "0.0.6"

setup(
	name="nt4PAdyP",
	version=read_ver(),
	description=read_des(),
)