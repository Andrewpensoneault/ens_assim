from distutils.core import setup

setup(
    name='Ens_Assim',
    version='0.0.1',
    author='A. Pensoneault',
    author_email='apensoneaultl@gmail.com',
    packages=['ens_assim', 'ens_assim.test','ens_assim.assimilate','ens_assim.measure','ens_assim.model'],
    scripts=['bin/lorenz_63.py'],
    url='http://pypi.python.org/pypi/Ens_Assim/',
    license='LICENSE.txt',
    description='Ensemble Data Assimilation framework.',
    long_description=open('README.txt').read(),
    install_requires=[
        "numpy >= 1.17.4",
        "scipy >= 1.4.1",
    ],
)
