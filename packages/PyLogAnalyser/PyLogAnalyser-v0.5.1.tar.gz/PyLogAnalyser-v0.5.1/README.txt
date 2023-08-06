#############################################
# PyLogAnalyser README                      #
#############################################

  PyLogAnalyser is a Python tool intended for filtering, colorizing,
columnizing or modifying logs so that their analysis will be easier and
faster.

PREVIOUS REQUIREMENTS:
    Python 2.7.x or Python 3.x

CAUTION: Python 2.6.x parses configuration files without order, so the 
        output result can't be predicted beforehand. Use Python 2.7.x
        at least.

I. Package installation (Windows and Linux)
---------------------------------
To install this Python package, provided as a
  .zip file in Windows and as a .tar.gz file in Linux, which was
  created using 'distutils' Python package, just uncompress it 
  in a temporary folder where you've got permission and write
  from a command line in the right directory:

$> python setup.py install #(Windows)
$> sudo python setup.py install #(Linux)

The setup.py script will automatically install it.

II. Check PyLogAnalyser
-----------------------
In order to check that the package works correctly, follow these steps
  after the package installation finishes with no issues.
In case of issues, contact me and I will help you.

 1. Open a Python console.
 2. Import PyLogAnalyser package:
    >>> import loganalyser
    The instruction should perfectly work.
 3. Print the version of the package:
    >>> print loganalyser.__version__
    The version should print.
 4. Show the help of the package, launching directly from command line:
    $> python -m loganalyser -h
 5. Show the demo option of the package, launching directly from command line::
    $> python -m loganalyser -s
    and follow the instructions written.

TROUBLESHOOT: If the command 'python -m loganalyser -h' does not work, maybe you need to use
    'python -m loganalyser.__main__ --help' instead.

Muchas gracias,

Ignacio.
