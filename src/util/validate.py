import re

def is_valid_sgrna(sgrna):
	sgrna = sgrna.upper()

	if len(sgrna) != 23:
		raise ValueError('sgRNA string should be of length 23 (sequence of length 20 and 3 character PAM)')

	chars_sgrna = re.search('[^ATGC]', sgrna)
	if chars_sgrna is not None:
		raise ValueError('sgRNA string should contain only DNA nucleotides {A, C, G, T}')

	pam = sgrna[-3:]
	if not pam.endswith('GG'):
		raise ValueError('PAM should be of the form NGG (SP CAS9)')

	return True
