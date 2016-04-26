#!/usr/bin/env python

"""
Sequence.py module
author: Bulteau Romain

This Class is a simplified version of the BioPython class manipulating sequences.

Attributes:
	ID		-> Sequence ID (str)
	SEQUENCE	-> Sequence (DNA alphabet, str)
	LENGTH	-> Sequence length (int)
	QUALITY	-> Sequence quality (array of quality score per base, array(int))

Declaring a Sequence object:
	from Sequence import Sequence
	
		my_newSeq = Sequence(bioSeqRecord_obj)
Methods:
	get_ID(self)
	get_SEQUENCE(self)
	get_LENGTH(self)
	get_QUALITY(self)
	set_SEQUENCE(self, newSeq)
	set_QUALITY(self,newQual)
	
"""
from Bio.SeqRecord import SeqRecord


class Sequence (object):

	
	def __init__(self, bioSeqRecord_obj):
		
		self.ID=bioSeqRecord_obj.id
		self.SEQUENCE=bioSeqRecord_obj.seq
		self.LENGTH=len(bioSeqRecord_obj.seq)
		self.QUALITY=bioSeqRecord_obj.letter_annotations['phred_quality']
	
	def get_ID(self):
		"""->Returns ID"""
		return self.ID
		
	def get_SEQUENCE(self):
		"""->Returns SEQUENCE"""
		return self.SEQUENCE
		
	def get_LENGTH(self):
		"""->Returns LENGTH"""
		return self.LENGTH
		
	def get_QUALITY(self):
		"""->Returns QUALITY"""
		return self.QUALITY
	
	def set_SEQUENCE(self, newSeq):
		"""->Sets SEQUENCE and LENGTH attributes accordingly, inputs a str (DNA alphabet)"""
		self.SEQUENCE = newSeq
		self.LENGTH = len(newSeq)
	
	def set_QUALITY(self,newQual):
		"""->Sets QUALITY attribute from array of quality scores, inputs array(int)"""
		self.QUALITY = newQual
