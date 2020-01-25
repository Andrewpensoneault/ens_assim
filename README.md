# Ens_Assim

Ens_Assim provides a simple framework to perform ensemble data assimilation for a generic model.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
To install, you will first need to install Python >= 3.0. This can be found below:
* [Download](https://www.python.org/downloads/)

Additionally you will need to install pip. Look at the pip documentation for how to install if you do not already have it:
* [Installation](https://pip.pypa.io/en/stable/installing.html)

You will need the following packages:
* numpy >= 1.17.4
* scipy >= 1.4.1
```
pip install numpy
pip install scipy
```

### Installing

To install Ens_Assim, run the following command

```
pip install git+git://github.com/Andrewpensoneault/ens_assim.git
```
### Example

To see an example of a scipt using Ens_Assim, look at the lorenz_63.py script

* [Lorenz 63](https://github.com/Andrewpensoneault/ens_assim/blob/master/bin/lorenz_63.py)

## Running the tests

To run the unit tests, run the following command within the ens_assim directory:

```
python -m unittest discover -s ./ens_assim/test/ -p "*_test.py"
```

## Contributing

Please read [CONTRIBUTING.md](https://github.com/Andrewpensoneault/ens_assim/blob/master/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Andrew Pensoneault** - *Initial work*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
