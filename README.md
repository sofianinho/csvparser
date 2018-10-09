# A small utility to convert cartoradio data from csv to csv and extract data
This is a small utility that extracts data from cartoradio CSV dataset 

The idea is that you have a global dataset having all the operators and technologies. And if you want to have just a certain operator and a certain technology, you can use this program to have the appropriate CSV.

Example of commands:
```sh
python2 csvparser.py -i examples/test.csv -o /tmp/out.csv -n "SFR" -t "LTE 800"
python2 csvparser.py -i examples/test.csv -o /tmp/out.csv -n "ORANGE" -t "UMTS 900"
```

## Tricks before you begin (very important)

- Go to cartoradio and have them email the dataset you want to you
- In the CSV, rename the columns "Exploitant" to simply Exploitant (remove the quotes) and "Système" to Systeme (remove the accent)
- Install the dependencies (in a python virtualenv preferably).
```sh
pip install -r requirements.txt
```
You can now execute the commands above.

```sh
python2 csvparser.py -i examples/test.csv -o /tmp/out.csv -n "SFR" -t "LTE 800"
python2 csvparser.py -i examples/test.csv -o /tmp/out.csv -n "ORANGE" -t "UMTS 900"
```
And then have a look at the generated /tmp/out.csv. If no output file argument is given, a local "out.csv" is created.

# Usage

```sh
Usage:  csvparser.py -h
 csvparser.py [-i INPUT] [-o OUTPUT] [-n NETWORK] [-t TECHNOLOGY]
 csvparser.py --version
 csvparser.py --help | -h

Options:
 -i INPUT, --input INPUT       The CSV file to be parsed
 -o OUTPUT, --output OUTPUT      The CSV file to write    [default: out.csv]
 -n NETWORK, --network NETWORK      The Mobile Network Operator to extract information. Column "Exploitant".    [default: ORANGE]
 -t TECHNOLOGY, --technology TECHNOLOGY      The Radio technology to extract for. Column "Systeme".    [default: LTE]
 -h --help   Prints this help
 --version   Programme version
```

# Context
You might want to transform the data downloaded from Cartoradio in a csv format to extract specific data. This is what I wanted, and made this modest utility that serves the purpose. If it's not the case for you, please put an issue, I will try to fix it if possible.

This utility takes advantage of the multiprocessing library in python to dispatch the conversion job among the available cores. If the number of threads is not enough for you, feel free to tweak the `MAX_NB_PROCESS` constant. This comes especially handy when the dataset is huge.

# License
The MIT License (MIT)

Copyright (c) 2018 sofianinho

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



