from distutils.core import setup


setup(name='cdmproto',
      version='0.1',
      description='Python library to work with CDM-4000 dispenser',
      author='Oleg Suharev',
      author_email='gigimon4ik@scalr.com',
      packages=['cdmproto'],
      install_requires=[
          'pySerial'
      ]
      )
