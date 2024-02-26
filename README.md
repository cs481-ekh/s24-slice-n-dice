# GoVizzy

![Build and Test](https://github.com/cs481-ekh/s24-slice-n-dice/actions/workflows/ci.yml/badge.svg?branch=main)

## Usage
GoVizzy will work on any system with a supported version on Python and Pip installed.

Simply run the build.sh script, which will install all dependencies in a virtual environment, and launch GoVizzy.

## Documentation
All of the documentation for GoVizzy can be found in the docs directory. See the [intro page](docs/intro.md).

## Testing

In order to run tests, the test script expects the `.venv` folder to have been
created by the `build.sh` script. Otherwise the test will throw an error.

To execute the test script perform:
```bash
$ ./test.sh
```
