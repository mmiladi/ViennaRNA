import RNApath

RNApath.addSwigInterfacePath(3)

import RNA
import unittest

seq1  =  	"CGCAGGGAUACCCGCG"
struct1=	"(((.(((...))))))"
seq1Dimer = 	"CGCAGGGA&ACCCGCG"
struct1Dimer=	"(((.(((..))))))"

struct11 = 	"(((.((.....)))))"
seq2  =		"GCGCCCAUAGGGACGC"
struct2=	"((((((...))).)))"
seq3  =		"GCGCACAUAGUGACGC"
struct3=	"(..(((...)))...)"
align=[seq1,seq2,seq3]

struct1_pt =	 [len(struct1),16,15,14,0,13,12,11,0,0,0,7,6,5,3,2,1]
seq_con  =  	"CCCAAAAGGGCCCAAAAGGG"
str_con_def=	"(((....)))(((....)))"
str_con=	"..........(((....)))"



def getShapeDataFromFile(filepath):
	
	retVec = []
	with open(filepath, 'r') as f:
		lines = f.readlines()
		
		for line in lines:
			retVec.append(float(line.split(' ')[1]))
	return retVec



class FoldCompoundTest(unittest.TestCase):
	def test_create_fold_compound_Single(self):
		print ("test_create_fold_compound_Single\n")
		
		fc = RNA.fold_compound(seq1)
		self.assertEqual(fc.type(),0)
		
	def test_create_fold_compound_Align(self):
		print ("test_create_fold_compound_Align\n")
		fc= RNA.fold_compound(align)
		self.assertEqual(fc.type(),1)
		
	def test_create_fold_compound_2D(self):
		print ("test_create_fold_compound_2D\n")
		fc= RNA.fold_compound(seq1,seq2,seq3)
		self.assertTrue(fc)
	
	def test_mfe(self):
		print ("test_mfe\n")
		fc= RNA.fold_compound(seq1)
		(ss,mfe) = fc.mfe()
		print (ss, "[ %6.2f" %mfe ,"]\n")
		self.assertEqual(ss,struct1)
	def test_mfe_Dimer(self):
		print ("test_mfe_Dimer\n")
		fc=RNA.fold_compound(seq1Dimer)
		(ss,mfe) = fc.mfe_dimer()
		print(ss, "[ %6.2f" %mfe ,"]\n")
		self.assertEqual(ss,struct1Dimer)
	def test_mfe_window(self):
		print("test_mfe_window\n")
		fc= RNA.fold_compound(seq1)
		(ss,mfe) = fc.mfe()
		print(ss, "[ %6.2f" %mfe ,"]\n")
		self.assertEqual(ss,struct1)
	
	def test_eval_structure(self):	
		print("test_eval_structure\n")
		fc = RNA.fold_compound(seq1)
		energy= fc.eval_structure(struct1)
		self.assertEqual("%6.2f" % energy, "%6.2f" % -5.60)
		print("\n", struct1, "[%6.2f" % energy,"]\n")
		
	def test_eval_structure_pt(self):
		print("test_eval_structure_pt\n")
		fc=RNA.fold_compound(seq1)
		energy= fc.eval_structure_pt(struct1_pt) /100; #/100 for dcal
		
		self.assertEqual("%6.2f" % energy, "%6.2f" % -5.60)
		print( struct1, "[%6.2f" % energy,"]\n")
	
	# Testing with filehandler and with stdout	
	#def test_eval_structure_verbose(self):
		#print("test_eval_structure_verbose")
		#fc = RNA.fold_compound(seq1)
		#filename= 'data/output_test.txt'
		#try:
			
			#with open(filename,'w') as f: 
				#print(filename ," is opened for writing\n")
				#energy = fc.eval_structure_verbose(struct1,f)
				#energy2 = fc.eval_structure_verbose(struct1,None)
			
			#self.assertEqual("%6.2f" % energy, "%6.2f" % -5.60)
			#print( struct1, "[%6.2f" % energy,"]\n")
			#f.close()
		#except IOError:
			#print("Could not open ",filename)
	
	
	
	##def test_eval_structure_pt_verbose(self):
		#print("test_eval_structure_pt_verbose\n")
		#filename= "data/output_test.txt"
		#try:
			#with open(filename,'w') as f: 
				#print(filename ," is opened for writing\n")
				#fc=RNA.fold_compound(seq1)
			
				#energy = fc.eval_structure_pt_verbose(struct1_pt,f)/100;  # / 100 for dcal
				#energy2 = fc.eval_structure_pt_verbose(struct1_pt,None)/100;  # / 100 for dcal
			
			#self.assertEqual("%6.2f" % energy, "%6.2f" % -5.6)
			#print( struct1, "[%6.2f" % energy,"]\n")
			#f.close()
		#except IOError:
			#print("Could not open ",filename)
	
	def test_eval_covar_structure(self):
		print("test_eval_covar_structure\n")
		s1="CCCCAAAACGGG"
		s2="CCCGAAAAGGGG"
		s3="CCCCAAAAGGGG"
		ali = [s1,s2,s3]
		covarStructure = "((((....))))"
		

		fc = RNA.fold_compound(ali)
		pseudoEScore=fc.eval_covar_structure2(covarStructure)
		print(covarStructure, "[ %6.2f" %pseudoEScore ,"]\n")
		self.assertTrue(pseudoEScore)
		
if __name__ == '__main__':
	unittest.main()
