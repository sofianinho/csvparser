#!/usr/bin/env python2
# -*- coding: ISO-8859-1 -*-
"""
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
"""

from docopt import docopt, printable_usage
from tqdm import tqdm
import csv
from json import dumps
from multiprocessing import Process, cpu_count
import os, shutil, subprocess, time

# I choose to have 3 times the number of cores as a basis for the max 
# number of processes to run the conversion task if the file size is important
# if the file is relatively small the min number is take. Small file is under 
# 10000 lines
FILE_SIZE_THRESHOLD = 10000
MAX_NB_PROCESS = cpu_count()*2
MIN_NB_PROCESS = 2

def nb_processes(nb_file_lines):
  """
  Returns MAX_NB_PROCESS if files_size > FILE_SIZE_THRESHOLD, MIN_NB_PROCESS otherwise

  :param nb_file_lines: number of lines in the file
  :param nb_file_lines: Integer
  :return: the number of processes to run to process the file
  :rtype: Integer
  """
  if nb_file_lines > MIN_NB_PROCESS*2 and nb_file_lines <= FILE_SIZE_THRESHOLD:
    return MIN_NB_PROCESS
  elif nb_file_lines <= MIN_NB_PROCESS*2:
    return 1
  return MAX_NB_PROCESS

def unitary_extraction(infile, start, stop, subOutFile, pb_pos, **features):
  """
  Actually extracts the csv entries to a geojson format
  
  :param infile: the input file (the CSV)
  :param start: line number to start conversion
  :param stop: line number where to stop conversion
  :param subOutFile: output file (part of the resulting csv)
  :param pb_pos: Progress bar position for tqdm
  :param features: the columns to reduce the csv to
  :param infile: String
  :param start: Integer
  :param stop: Integer
  :param subOutFile: String
  :param pb_pos: Integer
  :param features: Dict
  """
  with open(subOutFile, 'a') as dst:
    with open(infile, 'r') as src:
      reader = csv.DictReader(src, delimiter=';')
      for i, row in tqdm(enumerate(reader), desc="Partial processing", unit="lines", total=((stop-start)+1), position=pb_pos):
        if i >= start and i <= stop:
          if row['Exploitant'] == features['Exploitant'] and row['Systeme'] == features['Systeme']:
            stringdict = ''
            for ky in row.keys():
              stringdict = stringdict + row[ky] + ';'
            stringdict = stringdict[0:-1]
            dst.write(stringdict+'\n')
    src.close()
  dst.close()

def merge_results(listfiles, outfile,  pb_pos):
  """
  Merge a set of files into one 

  :param listFiles: The list of files to merge
  :param outfile: The output file
  :param pb_pos: Progress bar position for tqdm
  :param listFiles: list
  :param outfile: String
  :param pb_pos: Integer
  """
  with open(outfile, 'a') as dst:
    for k, v in tqdm(enumerate(listfiles), desc="Merging results", unit="files", position=pb_pos):
      with open(v, 'r') as src:
        shutil.copyfileobj(src, dst)
      src.close()
    dst.close()


def whole_convert(infile, outfile, **features):
  """
  Converts the CSV entry into csv using only the features

  :param infile: input file (the CSV)
  :param outfile: output file (the geojson)
  :param features: the columns to reduce the csv to
  :type infile: String
  :type outfile: String
  :param features: Dict
  """
  # In order to process the file among different processes, we will divide it
  # Total number of lines
  nb_lines = sum(1 for line in open(infile))
  # Total number of processes that will handle the file
  processes = nb_processes(nb_lines)
  # size of the processed portion per process
  step = (nb_lines/processes)
  start = 0
  # output files (one per subprocess)
  list_out_files = list()
  list_processes = list()
  try:
    # dispatch the job
    for i in range(processes):
      stop = start + step
      list_out_files.append(outfile+'.'+str(i))
      p = Process(target=unitary_extraction, args=[infile, start, stop, outfile+'.'+str(i), i], kwargs=features)
      start = stop + 1
      list_processes.append(p)
      p.start()
    # wait for completion
    for p in list_processes:
      p.join()
    # merge the results
    # 0- clear the terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    # 1- the csv header
    with open(outfile, 'a') as dst:
      dst.write('Exploitant;Systeme;Type d\'antenne;Dimension de l\'antenne;Numero d\'antenne;Debut;Azimut;Numero de support;Unite;Directivite;Numero Cartoradio;Fin;Hauteur / sol\n')
    dst.close()
    # 2- the subparts of the converted source file
    merge_results(list_out_files, outfile, 0) 
    #3- closing the geojson FeatureCollection property
    dst.close()
    #4- deleting the sub files
    for f in list_out_files:
      os.remove(f)    
  except IOError as e:
    print "Error when handling the files. Details: "+str(e)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='csvparser utility v0.1, Author: Sofiane Imadali <sofianinho@gmail.com>')
    if arguments["--input"] is not None:
     print "Converting "+arguments["--input"]+" to geojson in the file: "+arguments["--output"]
     features = {"Systeme": arguments["--technology"], "Exploitant": arguments["--network"]}
     whole_convert(arguments["--input"], arguments["--output"], **features)
     print "All done! Your output is in: "+arguments["--output"]
    else:
     print "\nYou must give an input file to convert. Try -h or --help option for help.\n"
     print(printable_usage(__doc__))
