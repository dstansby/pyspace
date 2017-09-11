from setuptools import setup

setup(name='heliopy',
      version='0.1b4',
      description='Python for space physics',
      url='https://github.com/heliopython/heliopy',
      author='David Stansby',
      author_email='dstansby@gmail.com',
      license='GPL-3.0',
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Intended Audience :: Science/Research',
                   'Natural Language :: English',
                   'Programming Language :: Python :: 3',
                   'Topic :: Scientific/Engineering :: Physics'],
      keywords='physics, space-physics',
      include_package_data=True,
      install_requires=['numpy',
                        'scipy',
                        'matplotlib',
                        'pandas'],
      packages=['pycdf',
                'pycdf.toolbox',
                'pycdf.pycdf',
                'heliopy',
                'heliopy.data',
                'heliopy.plot',
                'heliopy.util'],
      package_data={'heliopy': ['heliopyrc']})
