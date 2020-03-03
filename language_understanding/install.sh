#rm -rf build dist lutools.egg-info
export CC=g++-4.9

echo $CC
python Setup.py build_ext
python Setup.py install --record files.txt
