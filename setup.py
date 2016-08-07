import os
from setuptools import setup


# def read(fname):
# 	return open(os.path.join(os.path.dirname(__file__), fname)).read()

readme = open('README.rst').read()

setup(
	name="chi",
	version="0.1",
	author="Kevin Walchko",
	keywords=['framework', 'robotic', 'robot', 'vision', 'ros', 'distributed'],
	author_email="kevin.walchko@outlook.com",
	description="A python robotic framework and tools",
	license="MIT",
	classifiers=[
		'Development Status :: 4 - Beta',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 2 :: Only',
		'Operating System :: Unix',
		'Operating System :: POSIX :: Linux',
		'Operating System :: MacOS :: MacOS X',
		'Operating System :: POSIX',
		'Topic :: Scientific/Engineering',
		'Topic :: Scientific/Engineering :: Artificial Intelligence',
		'Topic :: Scientific/Engineering :: Image Recognition',
		'Topic :: Software Development :: Libraries :: Python Modules',
	],
	install_requires=['pyzmq', 'simplejson', 'pyyaml', 'pyserial', 'PySDL', 'numpy', 'nose', 'adafruit-io', 'pyaudio'],
	url="https://github.com/walchko/soccer2",
	long_description=readme,
	packages=["chi"],
	scripts=[
		'chi/tools/mjpeg-server.py'
	]
	# entry_points={
	# 	'console_scripts': [
	# 		# 'pyarchey=pyarchey.pyarchey:main',
	# 	],
	# },
)
