from setuptools import setup, find_packages

setup(name='zirc',
      version='1.2.3',
      description="Python IRCP Library",
      url='https://github.com/itslukej/zirc',
      author='Luke J.',
      author_email='me+zirc@lukej.me',
      license='GNU',
      packages=find_packages(),
      install_requires=['six', 'pysocks'],
      include_package_data=True,
      zip_safe=False)
