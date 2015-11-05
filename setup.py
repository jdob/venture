from distutils.core import setup

setup(name='Venture Society',
      version='1.0',
      description='Venture Society Roguelike',
      author='Jay Dobies',
      packages=['venture'],
      entry_points={
          'console_scripts': [
              'vs = venture.main:main'
          ]
      },
     )
