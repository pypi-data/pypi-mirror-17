pyopenbr
========

An alternative Python wrapper for OpenBR which uses the Command Line Tool.

Simple Usage:
-------------

.. code:: python

    import pyopenbr
    result = pyopenbr.run(algorithm="FaceRecognition", compare="image1.jpg model.gal")
    print(result)

Documentation:
==============

Parameters:
-----------

The parameters and the algorithms are exactly the same as the OpenBR
Command-Line tool. The official documentation can be found at:
http://openbiometrics.org/docs/api\_docs/cl\_api/

Syntax:
-------

These are valid syntax examples for doing the same thing:

.. code:: python

    # [1st Option] --> RECOMMENDED
    result = pyopenbr.run("output.csv", algorithm="FaceRecognition", compare="image1.jpg model.gal")

    # [2nd Option - Splitting the parameter-option pairs]
    result = pyopenbr.run("output.csv", "-algorithm FaceRecognition", "-compare image1.jpg model.gal")

    # [3rd Option - Copying the Command Line Tool's parameters as a second argument of the `run` function]
    result = pyopenbr.run("output.csv", "-algorithm FaceRecognition -compare image1.jpg model.gal")

Notes:
------

-  The ``output`` parameter is *optional*.

-  The argument names for the 1st option are **not** hard-coded. This means that any argument is translated to the format whic the OpenBR tool uses.

-  The command always returns the content of the output of the OpenBR
   tool. (even if it is an unreadable format - *e.g. raw format*)

-  If the output parameter is omitted, or it ends in ``.csv``, then the
   returned value will be a Dictionary with the result of the OpenBR
   tool.

Example - Face Recognition:
---------------------------

.. code:: python

    # You can read the official tutorial with the Command Line tool here: http://openbiometrics.org/docs/tutorials/#face-recognition
    # and see the similarities in the usage.
    import pyopenbr

    # Train the model with images in the `train` directory and store it in `model.gal`:
    pyopenbr.run("model.gal", "-enrollAll -enroll train/", algorithm="FaceRecognition")

    # Run a test of the trained model:
    result = pyopenbr.run(algorithm="FaceRecognition", compare="model.gal testImage.jpg")

Options to Configure:
---------------------

You can configure two things in the module:

-  Disable error printing in the Terminal: ``pyopenbr.disableErrors()``

-  Provide your Path for the OpenBR Command-Line tool:
   ``pyopenbr.setExecutable(path)``. By default, the module will try to
   find the executable in your system.

Requirements:
=============

You need to have OpenBR installed on your system. For installation
instructions please visit: http://openbiometrics.org/docs/install/

Compatibility:
==============

The module is compatible with Windows, Mac OS X and \*nix Systems. It
has been tested under Mac OS X El Capitan. Both Python 2.7
and Python 3 are supported.

Advantages/Disadvantages:
-------------------------

Using this Wrapper has many advantages that the official Python wrapper
doesn't: - Solves many Memory Issues (e.g. when handling a lot of
images), and it is simpler to use. - Won't throw any Segmentation Faults
or other C/C++ related errors, which are common in the official wrapper.
- Doesn't need special parameters when you run ``cmake`` in order to be
installed. - Simple usage, because it is similar to the OpenBR Command
Line tool. (Which is also the most well-documented in the OpenBR
Website, including Tutorials).

However, there is one **disadvantage**: It is **slower** than the
official python wrapper. The official wrapper doesn't
initialize/finalize the OpenBR object when used for many sequential
processeses. This one, however, does. This is unavoidable since we
essentially call the OpenBR command line tool.

Speed Test:
~~~~~~~~~~~

I did a quick experiment to see the time difference between the official
Python wrapper and this module. The test was about recognizing a face of
the same image, against a trained model:

-  The official Wrapper timing: ``0.182754993439``
-  Our timing: ``0.663321971893``

So, there is a huge difference between the speed performance of the two
wrappers. Probably this is the trade-off between speed and stability.

Notice:
=======

This is a rather simple wrapper which uses basic ways to communicate
with the OpenBR executable. However, it is stable and easy to use, which
is the reason why I publish it as open-source.

Contact:
========

You can contact me via e-mail at: antonis.katzourakis{AT}gmail{DOT}com

Twitter: `@ant0nisktz <https://www.twitter.com/ant0nisktz>`_

License:
========

    | Copyright 2016 Antonios Katzourakis
    |  Licensed under the Apache License, Version 2.0 (the "License");
      you may not use this file except in compliance with the License.
      You may obtain a copy of the License at
    |  http://www.apache.org/licenses/LICENSE-2.0
    |  Unless required by applicable law or agreed to in writing,
      software distributed under the License is distributed on an "AS
      IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
      express or implied. See the License for the specific language
      governing permissions and limitations under the License.

