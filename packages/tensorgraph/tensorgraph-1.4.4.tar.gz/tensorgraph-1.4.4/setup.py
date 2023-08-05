from distutils.core import setup
from setuptools import find_packages


setup(
    name='tensorgraph',
    version='1.4.4',
    author=u'Wu Zhen Zhou',
    author_email='hyciswu@gmail.com',
    install_requires=['numpy>=1.7.1',
                      'scipy>=0.11',
                      'six>=1.9.0',
                      'scikit-learn>=0.17',
                      'pandas>=0.17',
                      'matplotlib>=1.5',
                      'scipy>=0.17'],
    url='https://github.com/hycis/TensorGraph',
    download_url = 'https://github.com/hycis/TensorGraph/tarball/1.4.4',
    license='Apache 2.0, see LICENCE',
    description='A tensorflow library for building all kinds of models',
    long_description=open('README.md').read(),
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True
)
