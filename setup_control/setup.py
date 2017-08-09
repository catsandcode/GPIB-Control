from setuptools import setup

setup(name='setup_control',
      version=1.0,
      description='For use controling the microwave transmission setup',
      url='https://github.com/catsandcode/Microwave-Transmission-Experiment',
      packages=['setup_control'],
      install_requires=['numpy', 'pyserial'],
      zip_safe=False)
