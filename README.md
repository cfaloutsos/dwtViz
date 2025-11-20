# Haar DWT visualization
## by Christos Faloutsos, Nov. 2025

## Goal
Computes the DWT of the given input file and plots its scalogram.
If no file is given, it create a few waveforms and plots their scalograms.

## USAGE
a) To see a demo of several waveforms (square, sine, flip-flop, etc):
```commandline
uv run scalogram.py
```

b) To apply it on **your_file_name**
(which should have one number per line, no header):
```commandline
uv run scalogram.py -f your_file_name
```

c) To see the available flags
```commandline
uv run scalogram.py --help
```