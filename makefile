# Christos Faloutsos, Nov. 2024
# demo of Haar wavelets

ALL= README.md makefile $(SRC) DATA pyproject.toml
SRC=scalogram.py

demo_main: demo_file demo 

demo_all: demo_file demo_irregular demo_wrong demo demo_abs \
  demo_long demo_wrong2

demo: scalogram.py
	uv run scalogram.py --duration 64

demo_long: scalogram.py
	uv run scalogram.py -d 128

demo_abs: scalogram.py
	uv run scalogram.py --duration 64 --abs_flag

demo_file: scalogram.py
	uv run scalogram.py -f DATA/mixed_square_wave.csv
	uv run scalogram.py -a -f DATA/mixed_square_wave.csv

demo_irregular: scalogram.py
	uv run scalogram.py -f DATA/mixed_square_wave_irregular.csv

demo_wrong: scalogram.py
	uv run scalogram.py -f DATA/wave_wrong.csv

demo_wrong2: scalogram.py
	uv run scalogram.py -d 10

clean:
	\rm -f all.tar
	\rm -rf TST
	\rm -f *.png
	\rm -f DATA/*.png

spotless: clean

all.tar: $(ALL)
	tar cvf all.tar $(ALL)

