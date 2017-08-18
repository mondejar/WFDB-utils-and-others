This repository contains a few examples to use WFDB intended to be 
as simple as possible. 

To obtain more info visit: https://www.physionet.org/physiotools/wag/wag.htm

The examples cover the next functionalities:

1. Convert signals to *WFDB format*
2. Convert annotations files in *WFDB format* to *text* file
3. 3 Using ECGPUWAVE: to detect P-QRS-T on/off waves

# 1 Convert signals to *WFDB format*

## Creating signal and header files
If you don't already have PhysioBank-compatible records, an easy way to make them from the data you have is to begin by creating a CSV file containing one sample of each signal per line, as in this example consisting of samples of two ECG signals: 

```
927,998
927,1017
939,1034
958,1048
980,1064
```
If you have written your data in this format to a CSV file named *foo.csv*,create *foo.hea* and *foo.dat* using this command: 
```
wrsamp -F freq -i foo.csv -o foo -s, 0 1
```

replacing *freq* by the sampling frequency of your signals. The final command line arguments (0 and 1 in the example) specify the columns of the input file that should be written as signals to the output; column 0 is the leftmost, 1 the next, etc. Columns can be omitted, reordered, or duplicated as desired. See wrsamp for details and additional options that can be used if your samples are not 16-bit integers.

Edit the .hea file using any text editor of your choice to insert signal names and physical units, and calibration parameters. For records to be contributed to PhysioBank, please add, at the end of the file, an info string (a comment line beginning with '#') that describes (at a minimum) the age, gender, diagnoses, and medications of the subject (other information that does not identify the subject is also welcome). Example: 

```
# <age>: 35  <sex>: M  <diagnoses>: (none)  <medications>: (none)
```

Please use this format to permit indexing software to parse this information reliably. This string may extend over multiple lines if necessary, but begin each such line with '#'.

# RUN
```
python convert_ediagnostic_2_wfdb.py
```

This script will read the data from *ediagnostic/* and will save the data in WFDB format at *ediagnostic_wfdb/* 

### Creating a data collection from a set of records

To create a PhysioBank-style data collection (repository), given a set of PhysioBank-compatible records, is a very simple process:

More info in: https://physionet.org/tutorials/creating-records.shtml#creating-signal-files-from-physical-signals


# 2 Convert annotations files in *WFDB format* to *text* file
## rdann
To convert whatever annotation file from WDFB use *rdann*

Code:
```
rdann -r record -f 0 -a atr -v > output_dir/name_record_atr.txt
rdann -r record -f 0 -a qrs -v > output_dir/name_record_qrs.txt
```

# RUN
```
python convert_wfdb_data_2_csv.py
```
This script will read the data from *mitdb/* and will save the data and annotations in .txt format at *mitdb/csv/* 


# 3 Using ECGPUWAVE: to detect P-QRS-T on/off waves
https://physionet.org/physiotools/ecgpuwave/

## Exporting results on annotation files

```
ecgpuwave -r record -a annotator 
```

-r record
	filename (.dat) without extension

-a output extension
	output extension like *qrs*

## Loading QRS detections from other files

Read QRS locations from the specified input-annotator (and copy them to the output annotation file). 
: run the built-in QRS detector. 
```
ecgpuwave -r record  -i input-annotator  -a annotator
```
-i input-annotator
	input annotator extension like *atr*


# RUN
```
python ecgpuwave_mitdb.py
```
This script apply ecgpuwave on *mitdb/* and export the output
in text files at *mitdb/qrs/* 

```
python ecgpuwave_mitdb_atr.py
```
This script apply ecgpuwave on *mitdb/* (using its annotations for QRS peak location) and export the output in text files at *mitdb/qrs/* 
