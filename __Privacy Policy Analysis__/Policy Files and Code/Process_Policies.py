#==========================================================================#
'''
Original Code Source from:
	Project 4 - Text Analysis - Fall 2020
	Author: Joe Harrison - joeh24

Use and Abuse of Personal Information - Summer 2021
	Quantitative Analysis of Privacy Policies
	Heavily Modified by: Joshua Lyons

Setup Library Dependencies:
	pip3 install pandas
	pip3 install openpyxl
	pip3 install xlwt
	pip3 install nltk
(enter each of these into the command line for your OS)
'''
#==========================================================================#
from datetime import datetime as dt
import operator
import os

from pandas import ExcelWriter
from pandas import ExcelFile
import pandas as pd
import openpyxl # Works with .xlsx files from Excel 2007+
#import xlwt # Only works with .xls files from Excel 2003

#import matplotlib.dates as mdates
#import matplotlib.pyplot as plt

is_test_mode = False # Pseudo-macro to toggle code blocks
dir_path = "C:/Users/JoshT/Documents/UGR/Code/Quantitative_Policy_Analysis/New_Plaintext_Policies_for_Python"
# Feel free to change this default value for copy/paste convenience ^
#==========================================================================#

def read_text(name):
    with open(name, 'r', encoding = 'utf8') as file:
        raw_text = file.read()
    return(raw_text)

def read_easy_text(name):
    with open(name, 'r') as file:
        easy_text = file.read()
    return(easy_text)

### if char in set, strip it away. Then return a lower case version of the text. 
def clean_text(raw_text):
    item_set = {
		'~', '@', '#', '$',  '%', '^',  '&',  '©',  '¶', '§', '™',
		':', ';', ',', '.',  '?', '!',  '\'', '\"', '“', '”', '`',
		'(', ')', '[', ']',  '{', '}',  '<',  '>',  '≤', '≥', '«', '»',
		'+', '-', '±', '*',  '/', '|',  '\\', '_',
		'•', '○', '●', '◌', '◯', '◦',  '◦',
		'▪', '▫', '■', '☐', '◼', '◻', '□','□',  '◇', '◆', '◊'
	}
    raw_list = ["" if char in item_set else char for char in raw_text]
    cleaned_string = ""
    for char in raw_list:
        cleaned_string += char
		# TODO: Add an exception for when the last character of a string is punctuation
    cleaned_text = cleaned_string.lower().strip()
    return(cleaned_text)

def count_characters(raw_text):
	char_list = raw_text.strip()
	num_chars = len(char_list)
	return(num_chars)

### create a dictionary and use it to count word frequencies
def get_word_frequencies(word_list):
    dict_freq = {} #dict = {}
    for word in word_list:
        if word not in dict_freq:
            dict_freq[word] = 1
        else:
            dict_freq[word] += 1
    return(dict_freq)

### provided
def count_syllables(word):
    syllables = 0
    vowels = 'aeiouy'
    word = word.lower().strip(".:;?!")
    if word[0] in vowels:
        syllables += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index-1] not in vowels:
            syllables += 1
    if word.endswith('e'):
        syllables -= 1
    if word.endswith('le'):
        syllables += 1
    if syllables == 0: 
        syllables = 1
    return(syllables)

### for each word in the text, count syllables, and then total the results
def count_all_syllables(cleaned_text):
    num_syllables = 0
    for word in cleaned_text:
        count = count_syllables(word)
        num_syllables += count
    return(num_syllables)

### Presumes all sentances end in a period, question mark, or exclamation mark. 
def count_of_sentences(raw_text): ### TODO: Fix this so it recognizes alpha numbering/bullets
    num_of_sentences = 0
    for char in raw_text:
        if char == '.' or char == '?' or char == '!': # or char == '\n':
            num_of_sentences += 1
    return(num_of_sentences)

def count_sentences_new(word_list): ### TODO: Maybe finish this later for better accuracy?
	num_sentences = 0
	for word in word_list:
		#if str(word).
		#if str(word).endswith(".") and str(word).:
		#	pass
		#if char == "." or char == "?" or char == "!":# or char == "\n":
		#	num_sentences += 1
		pass
	return(num_sentences)

def count_of_easy_words(easy_text, cleaned_text):
    num_easy_words = 0
    for word in cleaned_text:
        if word in str(easy_text):
            num_easy_words += 1
    return(num_easy_words)

def count_complex_words(cleaned_text):
	num_hard_words = 0
	for word in cleaned_text:
		count = count_syllables(word)
		if count >= 3: # Polysyllabic
			num_hard_words += 1
	return(num_hard_words)


def count_hyperlinks(text_file_path):
	num_hyperlinks = 0
	with open(text_file_path, 'r', encoding = 'utf8') as f:
		i = 1 # Line number iterator
		for line in f:
			if i == 1 and "<URL>" in line:
				### CRITICAL ERROR ###
				# Unfinished template file encountered, do NOT continue attempting to process it
				return -1
				
			if i > 3: # List of links always starts after line 3
				clean_line = line.strip()
				
				# Only count nonempty lines
				if str(clean_line).isspace() == False and len(str(clean_line)) > 1:
					num_hyperlinks += 1
				
				# Check for end of hyperlink list condition
				if str(clean_line).endswith(')'):
					break
			# End if
			i += 1
		# End for
	# End open
	return num_hyperlinks # Return the line number to restart parsing from
# End of def

def run_old_code_version():
	print("")
	user_prompt = input("Name of the sample to analyze? ")
	raw_text = read_text(user_prompt)
	easy_text = read_easy_text("Dale-Chall.txt")
	# Replace with readlines
	cleaned_text = clean_text(raw_text)
	word_list = cleaned_text.split() #list = cleaned_text.split() ### Josh: Bug Fixed #1 ###
	dict_freq = get_word_frequencies(word_list) ### Josh: Bug Fixed #1a, #2 ###
	
	num_chars = count_characters(raw_text)
	num_syllables = count_all_syllables(word_list) ### Josh: Bug Fixed #1b ###
	num_sentences = count_of_sentences(raw_text)
	unique_words = len(dict_freq) ### Josh: Bug Fixed #2a ###
	
	num_hyperlinks = count_hyperlinks(user_prompt)
	num_easy_words = count_of_easy_words(easy_text, word_list) ### Josh: Bug Fixed #3 ###
	num_hard_words = count_complex_words(word_list)
	
	### both flesch grade and score did not need dedicated functions. One simple equation for each of them taken from wikipedia. 
	flesch_grade = 0.39 * (len(word_list)/num_sentences) + 11.8 * (num_syllables/len(word_list)) - 15.59 ### Josh: Bug Fixed #1f ###
	flesch_score = 206.835 - 1.015 * (len(word_list)/num_sentences) - 84.6 * (num_syllables/len(word_list)) ### Josh: Bug Fixed #1g ###
	
	print("")
	print("number of words:\t", len(word_list)) ### Josh: Bug Fixed #1c ###
	print("number of characters:\t", num_chars)
	print("number of unique words:\t", unique_words)
	print("number of sentences:\t", num_sentences)	
	print("")
	print("average words per sentence: ", round(len(word_list)/num_sentences, 1)) ### Josh: Bug Fixed #1d ###
	print("average syllables per word: ", round(num_syllables/len(word_list), 1)) ### Josh: Bug Fixed #1e ###
	print("")
	print("Number of easy words:\t", str(num_easy_words))
	print("Number of complex words:", str(num_hard_words))
	print("Number of embedded links:", str(num_hyperlinks))
	
	#flesch_grade = 0.39 * (len(word_list)/num_sentences) + 11.8 * (num_syllables/len(word_list)) - 15.59 ### Josh: Bug Fixed #1f ###
	#flesch_score = 206.835 - 1.015 * (len(word_list)/num_sentences) - 84.6 * (num_syllables/len(word_list)) ### Josh: Bug Fixed #1g ###
	
	print("")
	print("Reading-ease score:\t", round(flesch_score, 2))
	print("U.S. grade level:\t", round(flesch_grade, 2))
	
	#print("DEBUG: Easy words dump: \n", easy_text, "\n")
	
	print("")
	print("The twenty most common words:")
	
	f_dict_sorted = sorted(dict_freq.items(), key=operator.itemgetter(1), reverse=True)
	
	i = 0
	for word in f_dict_sorted: #sorted(dict, key=dict.get, reverse=True): ### Josh: Bug Fixed #2b ###
		if i == 20:
			break
		else:
			print(str(word[1]) + "x\t", "\"" + str(word[0]) + "\"") ### Josh: Bug Fixed #2c ###
			i += 1
	print("\n")
# End of def

#==========================================================================#
################### New Bulk File Processing Code (6/14) ###################
#==========================================================================#

data_to_write = [] # This is a 2D vector to store + export our processed data in (with a lazy global scope)

easy_text = read_easy_text("Dale-Chall.txt") # Only do this once for all files


def read_text_lines(file_name, num_header_lines):
	policy_text_lines = []
	with open(file_name, 'r', encoding = 'utf8') as file:
		raw_text_lines = file.readlines()
		i = 0
		for line in raw_text_lines:
			if i > num_header_lines: # Only start parsing the text lines after the variable-length header
				policy_text_lines.append(line)
			i += 1
	print("\tParsing lines from text file...")
	return(policy_text_lines)
# End of def

# Read text File
def read_text_files(comp_id, comp_name, f_path_terms, f_path_policy):
	
	num_hyperlinks = 0
	company_docs_raw = []
	company_docs_cleaned = []
	
	if (f_path_terms == "Default") and (f_path_policy == "Default"):
		return
		
	#---------------------------------------------------#
	# 			Parse Terms of Service File
	#---------------------------------------------------#
	if f_path_terms != "Default": ### NOTE: The ToS document is required for analysis
		### NOTE: It was such a power move to name my files for this to work ###
		print("\tReading file: " + comp_name + "_Terms_of_Service.txt")
		
		# Do a quick preview of the header text lines
		num_hyperlinks_1 = count_hyperlinks(str(f_path_terms))
		if num_hyperlinks_1 < 0:
			return ### ERROR ###
		
		raw_text_lines_1 = read_text_lines(f_path_terms, num_hyperlinks_1)
		num_hyperlinks += num_hyperlinks_1 # After using the subresult for parsing, can add the link count to the total
		
		company_docs_raw.extend(raw_text_lines_1) # Store each line string from the raw list as an entry in new list
	# End if
	
	#---------------------------------------------------#
	# 			Parse Privacy Policy File
	#---------------------------------------------------#
	if f_path_policy != "Default": ### NOTE: The Privacy Policy is optional
		### NOTE: It was such a power move to name my files for this to work ###
		print("\tReading file: " + comp_name + "_Privacy_Policy.txt")
		
		# Do a quick preview of the header text lines
		num_hyperlinks_2 = count_hyperlinks(f_path_policy)
		if num_hyperlinks_2 < 0:
			return ### ERROR ###
		
		raw_text_lines_2 = read_text_lines(str(f_path_policy), num_hyperlinks_2)
		num_hyperlinks += num_hyperlinks_2 # After using the subresult for parsing, can add the link count to the total
		
		company_docs_raw.extend(raw_text_lines_2) # Store each line string from the raw list as an entry in cumulative list
	# End if
	
	#---------------------------------------------------#
	# 		Process All Document Text from File(s)
	#---------------------------------------------------#
	for raw_line in company_docs_raw:
		company_docs_cleaned.append(clean_text(raw_line))
	
	c_docs_text_raw = '\n'.join(company_docs_raw) # Re-join the long string-format documents for compatibility
	c_docs_text_cleaned = '\n'.join(company_docs_cleaned) # Re-join the long string-format documents for compatibility
	
	word_list = c_docs_text_cleaned.split() # Create a new super-long list of all words in this company's document(s)
	
	dict_freq = get_word_frequencies(word_list)
	unique_words = len(dict_freq)
	
	num_chars = count_characters(c_docs_text_raw) # TODO: Don't count whitespace characters
	num_syllables = count_all_syllables(word_list)
	num_sentences = count_of_sentences(c_docs_text_raw)
	
	num_easy_words = count_of_easy_words(easy_text, word_list)
	num_hard_words = count_complex_words(word_list)
	
	flesch_grade = 0.39 * (len(word_list)/num_sentences) + 11.8 * (num_syllables/len(word_list)) - 15.59
	flesch_score = 206.835 - 1.015 * (len(word_list)/num_sentences) - 84.6 * (num_syllables/len(word_list))
	#---------------------------------------------------#
	
	# Add a row vector entry for this CID's data to the 2D vector result
	data_to_write.append(
		[ comp_id, comp_name, num_sentences, len(word_list), num_chars,
		num_easy_words, num_hard_words, unique_words, num_hyperlinks,
		round(len(word_list)/num_sentences, 2), round(num_syllables/len(word_list), 2),
		round(flesch_score, 2), round(flesch_grade, 2)
		# NOTE: I could probably add other metrics here too, but that can also be easily
		# done anytime in our live spreadsheet based on this core data.
		]
	)
	print("\tAdded data entry for:", comp_name, "\n")
	# End if
# End of def

def output_spreadsheet_results(values_to_write, out_sheet_name):
	
	print("")
	if len(data_to_write) == 0:
		print("No writeable data was produced")
		return
		
	print("Writing to spreadsheet...\n")
	
	writer = pd.ExcelWriter(out_sheet_name) # Ignore this irrelevant warning
	
	# Wrap result in a labeled Pandas data frame for the Excel file
	dframe_out = pd.DataFrame( data_to_write,
	columns=['C-ID#', 'Company Name', 'Sentences', 'Words', 'Characters',
			 '# of Simple Words', '# of Complex Words', '# of Unique Words', '# of Hyperlinks',
			 'Avg. Words/Sentence', 'Avg. Syllables/Word', 'F-K Readability Score', 'F-K Grade Level'
			]
	)
	
	dframe_out.to_excel(writer,'Quantitative Analysis',index=True) ### Write the frame to output file ###
	writer.close()
# End of def


#==========================================================================#
def main():
	#---------------------------------------------------#
	#  Setup the Input/Output Files to Read/Write to
	#---------------------------------------------------#
	out_sheet_name = "_analyzed_data_result.xlsx" # TODO: Append timestamp to filename?
	
	print("")
	dir_path = input("Please enter the FULL path to the plaintext policies folder in the form \"C:/Users/...\":\n\t>> ") #user_prompt
	print("")
	
	# Change the present working directory
	os.chdir(dir_path)
	
	# Temp variables for filenames, so 2 matching files can be read back-to-back
	terms_file  = "Default"
	policy_file = "Default"
	
	comp_name_1 = "Default"
	comp_name_2 = "Default"
	
	#---------------------------------------------------#
	#  Process All Files in Present Working Directory
	#---------------------------------------------------#
	print("List of files in present working directory:")
	c_id = 1 # I'm finally attempting to re-index everything in a sorted list
	f_count = 0 # Tracks how many files for the current company have been found so far
	
	for file in os.listdir(): # Iterate through all files in pwd (assumes pre-sorted alphabetically)
		print(" - ", file)
		
		# Check whether file is in text format or not
		if file.endswith(".txt"):
			input_file_path = f"{dir_path}\{file}"
			#comp_name = (file.split("_")[0]).split(".")[0]
			
			comp_name_2 = file.split("_")[0] # Get the new name input to compare with the stored "state"
			
			### Look for and Flag File Pairs ###
			if   "Terms" in str(file): # Always check for Terms first
				terms_file = input_file_path
				f_count += 1
			elif "Policy" in str(file): # Policy is made optional later
				policy_file = input_file_path
				f_count += 1
			else: # Goodbye Dale-Chall
				f_count = 0
				continue
			# End if
			
			### Check if at Least 1 File (Terms) is Ready for Processing ###
			if (f_count == 2 and comp_name_1 == comp_name_2) or (f_count == 1 and (terms_file != "Default")): # All files found for company
				
				#comp_name = (file.split("_")[0]).split(".")[0] ### NOTE: It was such a power move to name my files for this to work ###
				
				if comp_name_1 == "Default":
					comp_name_1 = comp_name_2 # Quick fix for an awkward little bug
				
				read_text_files(c_id, comp_name_1, terms_file, policy_file)
				
				# Reset company name state data for the next company
				comp_name_1 = "Default"
				comp_name_2 = "Default"
				
				terms_file  = "Default"
				policy_file = "Default"
				
				f_count = 0
				c_id += 1
			else:
				comp_name_1 = file.split("_")[0] # Save the "state" of the previous company name
				f_count = 0
			# End if
		# End if
		
		### Ignore all other non-plaintext files ###
		
	# End for
	
	#---------------------------------------------------#
	#  Write Analysis Result Data to Excel Spreadsheet
	#---------------------------------------------------#
	output_spreadsheet_results(data_to_write, out_sheet_name)
	
	print("Policy processing is now complete. Have a nice day! =]\n")
	
# End of def
#==========================================================================#

if __name__ == '__main__':
	if is_test_mode:
		run_old_code_version()
	else:
		main()

# End of execution
