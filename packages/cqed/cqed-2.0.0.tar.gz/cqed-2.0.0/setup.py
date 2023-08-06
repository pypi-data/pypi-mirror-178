from setuptools import setup, find_packages

setup(
    name='cqed',
    version='2.0.0', # 1-new module, 2-big change, 3-small change
    description='Modules for CQED experiments',
    author='Guodong Cui',
    author_email='guodong.cui@stonybrook.edu',
    packages=find_packages('src'),
    package_dir={'':'src'},
    install_requires=['numpy',
                      'pandas',
                      'scipy', 
                      'h5py',
                      'easygui',
                      'matplotlib'], # external packages as dependencies
  )