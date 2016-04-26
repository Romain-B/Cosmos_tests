#!/usr/bin/env python
"""
tools.py module
author: Bulteau Romain

Collection of tools developped for a simple Quality and Length treatment of a raw fastq file.

Tools:
	Quality Treatment Tool
		quality_treatment(path2file, path2output, threshold)	-> Quality treatment according to threshold
		
	Length Treatment Tool
		length_treatment(path2file, path2output, threshold)	-> Length treatment according to threshold
		
	Graph Generation Tool
		format_files(path2input, path2output, ftype)		-> File formating according to ftype
		r_call(path2script, path2input, path2output)		-> Graph generation from formated files
	
	Misc Functions
		max_length(sequences)				
		write_fastq(path2output,seqs)			
		fastq2fasta(path2input,path2output)	
		fastq2Sequence(path2file)			
		sequence2SeqRecord(seq_obj)				
"""
import subprocess
import Sequence
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

#--------------------------
# QUALITY TREATMENT TOOL
#--------------------------
	#Allows for 1 base to be bad if the next is over the treshold
	
def quality_treatment(path2file,path2output,threshold):
	"""
	Quality Treatment Tool
		quality_treatment(path2file, path2output, threshold)
		
	This function inputs a fastq file, an output file and a threshold for minimum acceptable quality.
	The algorithm allows for one base to be of 'bad' score if the next is above the threshold.
	The results are written in the output file under a fastq format
	"""
	sequences = fastq2Sequence(path2file)
    	
    	for ind_seq in sequences :
    		i=0
    		j=0
    		newQual = []
    		
    		for qual_pb in ind_seq.get_QUALITY():
    											
    			if i+1 < len(ind_seq.get_QUALITY()):
	    			if qual_pb >= threshold or ind_seq.get_QUALITY()[i+1]>=threshold: 
	    				newQual.append(qual_pb)
	    				j += 1
	    			elif j > 0 :
	    				break
	    			
	    			i += 1
    		if i == j:
    			newSeq = ind_seq.get_SEQUENCE()[:i] 		    			
    		elif j != 0:
    			newSeq = ind_seq.get_SEQUENCE()[i-j-1:i]
    			
    		ind_seq.set_SEQUENCE(newSeq)
    		ind_seq.set_QUALITY(newQual)
    		
    	write_fastq(path2output, sequences)

#--------------------------
# LENGTH TREATMENT TOOL
#--------------------------

def length_treatment(path2file, path2output, threshold):
	"""
	Length Treatment Tool
		length_treatment(path2file, path2output, threshold)
	
	This function inputs a fastq file, an output file and a treshold.
	The threshold is the minimum length authorized for a sequence to be kept.
	The algorithm removes all sequences with a length inferior to the threshold and writes the outcome in the ouput file under a fastq format.
	"""
		
	sequences = fastq2Sequence(path2file)
	newSeqs = []
	for ind_seq in sequences:
		if ind_seq.get_LENGTH()>=threshold:
			newSeqs.append(ind_seq)			
	write_fastq(path2output, newSeqs)

#--------------------------
# R GRAPH GEN TOOL
#--------------------------

def format_files(path2input, path2output, ftype):
	"""
	File formater
		format_files(path2input, path2output, ftype)
	
	This function formats the input (fastq) file according to the ftype referenced. The ftype can be either 'length' or 'quality' and the formating will output a file under TSV format usable for the called R scripts in r_call(path2script, path2input, path2output).
	"""
	
	sequences = fastq2Sequence(path2input)
	
	if ftype == 'length':
		path2output+='_length.txt'
		OUT=open(path2output,'w')
		fwrite=""
		for ind_seq in sequences:
			fwrite+=ind_seq.get_ID()+"\t"+str(ind_seq.get_LENGTH())+"\n"
		OUT.write(fwrite)
	elif ftype == 'quality':
		path2output+='_quality.txt'
		OUT=open(path2output,'w')
		ml=max_length(sequences)
		
		for ind_seq in sequences:
			fQual = ind_seq.get_QUALITY()
			while len(fQual) < ml:
				fQual.append('NA')
				#print str(len(fQual))+" / "+str(ml)
			fwrite=""
			for ind_qual in fQual:
				fwrite+=str(ind_qual)+"\t"
			fwrite+="\n"
			OUT.write(fwrite)
	
	OUT.close()	
	
def r_call(path2script, path2input, path2output):
	"""
	R call
		r_call(path2script, path2input, path2output)
		
	This function calls the Rscript according to the arguments and the input files.
	"""
	
	subprocess.call(['Rscript', path2script, path2input, path2output])

#--------------------------
# MISC FUNCTIONS
#--------------------------

def max_length(sequences):
	"""-> Returns max length from Sequence object array
	"""	
	ml=0
	for ind_seq in sequences:
		if ind_seq.get_LENGTH() >= ml:
			ml = ind_seq.get_LENGTH()
	return ml

def write_fastq(path2output,seqs):
	"""-> Writes a fastq file from Sequence object array
	"""
	sequences_rec = []
	for ind_seq in seqs :
    		sequences_rec.append(sequence2SeqRecord(ind_seq))
    	SeqIO.write(sequences_rec, path2output, "fastq")

def fastq2fasta(path2input,path2output):
	"""-> Writes a fasta file from a fastq file	
	"""
	sequences_rec = []
	for seqrec_obj in SeqIO.parse(path2input,"fastq") :
    		sequences_rec.append(seqrec_obj)
    	SeqIO.write(sequences_rec, path2output, "fasta")

def fastq2Sequence(path2file):
	"""-> Loads a fastq file into a Sequence object array
	"""
	sequences = []
	for bioSeqRecord_obj in SeqIO.parse(path2file,"fastq"):
    		sequences.append(Sequence.Sequence(bioSeqRecord_obj))
    	return sequences
	    		
def sequence2SeqRecord(seq_obj):
	"""-> loads a SeqRecord object array from a Sequence object array
	"""
	seqRecord_obj = SeqRecord(seq_obj.get_SEQUENCE(),
						id = seq_obj.get_ID())
	seqRecord_obj.letter_annotations['phred_quality'] = seq_obj.get_QUALITY()
	return seqRecord_obj	
