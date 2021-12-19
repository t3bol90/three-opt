from setuptools import setup, find_packages
from os import path as os_path
import opt

this_directory = os_path.abspath(os_path.dirname(__file__))


def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]


setup(name='3-opt',
      python_requires='>=3.5',
      version='1.0.0',
      description='3-otp TSP in Python',
      long_description=read_file('README.md'),
      long_description_content_type="text/markdown",
      url='https://github.com/t3bol90/three-opt',
      author='Toan Doan',
      author_email='t3bol90@gmail.com',
      license='MIT',
      packages=find_packages(),
      platforms=['linux', 'windows', 'macos'],
      install_requires=['numpy', 'scipy'],
      zip_safe=False)
