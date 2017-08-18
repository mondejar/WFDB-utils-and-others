# Read data from ediagnostic
from os import listdir, mkdir, system
from os.path import isfile, isdir, join, exists
import json

types = ['II', 'V1']
dataset = 'ediagnostic/'


patients = [f for f in listdir(dataset) if isdir(join(dataset, f))]

print patients

freq = '250'


#Create folder
wfdb_dir = dataset + 'wfdb'
#Create folder

if not exists(wfdb_dir):
	mkdir(wfdb_dir)

for p in patients:
	if p != 'wfdb':
		# Read metadata
		metadata_file = dataset + p + '/metadata.json'
		data_file = open(metadata_file)
		metadata = json.load(data_file)

		window = {}
		for v in metadata['ventanas']:
			tipo = v['tipo']
			window[str(tipo)] = v['inicioVentana']
		print 'Derivation II: ', window['II'], ':', window['III'], ' V1: ', window['V1'], ':', window['V2']

		# 1. Write the desired signal at individual .csv files
		signal_file = dataset + p + '/' + p + '.txt'
		signal_data = open(signal_file, 'r')	
		signal_data = signal_data.read()
		signal_II = signal_data[window['II']:window['III']]

		signal_II_file = dataset + p + '/' + p + '_II.csv'
		file_II = open(signal_II_file, 'w')	
		file_II.write(signal_II)
		file_II.close()


		# 2. Write the signals and headers at WFDB format

		wfdb_filename = wfdb_dir + '/' + p[:-3]
		command = 'wrsamp -F ' + freq + ' -i ' + signal_II_file + ' -o ' + wfdb_filename
		print(command)
		system(command)

		# Edit .hea file... metadata['edad'] .... 
		# header # <age>: 35  <sex>: M  <diagnoses>: (none)



