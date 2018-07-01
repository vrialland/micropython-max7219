import sys
# Remove current dir from sys.path, otherwise setuptools will peek up our
# module instead of system's.
sys.path.pop(0)
from setuptools import setup
sys.path.append("..")
import sdist_upip

setup(name='micropython-max7219',
      version='0.1.0',
      description='MAX7219 8x8 matrices driver for Micropython',
      long_description=open('README').read(),
      url='https://github.com/vrialland/micropython-max7219',
      author='Vincent Rialland',
      author_email='vincent.rialland@gmail.com',
      licence='MIT',
      cmdclass={'sdist': sdist_upip.sdist},
      py_modules=['max7219']
)