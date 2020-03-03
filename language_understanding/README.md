## Get started

CFGParser is in C. To compile it, install its prerequisites **with right version**:

1.gcc 4.9.0 or higher (with C++11 regex support)

    // In case you are using ubuntu 14.04, here is an instruction:
    sudo add-apt-repository ppa:ubuntu-toolchain-r/test
    sudo apt-get update
    sudo apt-get install gcc-4.9 g++-4.9

2.cython

    sudo apt-get install cython
    export CC=g++-4.9  # This is to make sure you are using the right gcc version(>4.9.0)

Installation:

    python Setup.py build_ext
    sudo python Setup.py install

