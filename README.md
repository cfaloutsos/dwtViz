# Haar DWT visualization
## by Christos Faloutsos, Nov. 2025

## Goal
The `scalogram.py` script computes the DWT of the given input file and plots its scalogram.
If no file is given, it creates a few waveforms and plots their scalograms.

## Installation - recommended
With [uv](https://docs.astral.sh/uv/getting-started/installation/)
installed:
```
git clone ....
chmod u+x scalogram.py
```
## Installation - alternative
Without 'uv'
```
git clone ...
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 scalogram.py 
```


## USAGE - basic
We assume 'uv' is installed - then

a) To see a demo of several waveforms (square, sine, flip-flop, e.t.c.):
```
uv run scalogram.py
```
or just
```
  ./scalogram.py
```

b) To apply it on **your_file_name.csv**
(which should have one number per line, no header):
```
uv run scalogram.py -f your_file_name.csv
```
or
```
./scalogram.py -f your_file_name.csv
```

## USAGE - more details
A) To see the available flags
```
uv run scalogram.py --help
```
B) for more examples
```
git clone  ....
make demo_all
```

## USAGE - flags
```
   --help                       # obvious
-d --duration INT               # creates signals of that length (power of 2)
-f --file_name FILENAME         # operates on filename.csv
-v --verbose                    # verbose: prints diagnostics
-a --abs_flag                   # uses the absolute value 
                                #    of the DWT coefficients
-p --print_flag                 # prints the plots into png
```

## Sample output
![example_plot](FIG/example_slow_sine.png)


