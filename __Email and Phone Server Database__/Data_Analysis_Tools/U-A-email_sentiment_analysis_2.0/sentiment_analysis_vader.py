"""
Sentiment Analysis Tool - VADER

(Valence Aware Dictionary for Sentiment Reasoning)

This is the more basic option (Lexicon/Rule based), so the word
polarities it gives are pre-defined, based on its reference dictionary
file. It allegedly doesn’t generalize well, but it's faster, and more
importantly, doesn't require any "training data" at all.

Base code sources:
    https://towardsdatascience.com/sentimental-analysis-using-vader-a3415fef7664
    https://www.thepythoncode.com/article/vaderSentiment-tool-to-extract-sentimental-values-in-texts-using-python
    https://github.com/cjhutto/vaderSentiment
___________________________________________________________________________
Note: This script has been specialized to examine the contents of our
email database for potential differences in language patterns/bias between
male and female gendered ID profiles assigned to the same organizations.
However, since the core behavior is operating on the emails associated
with a pre-filtered list of ID numbers (in id_dict.csv), to make the output
more generalized/customized:
	
	1. Change which metadata fields are included in the input .csv file,
	   and pre-filter to only include the identities being compared
	   
	2. Change which metadata fields are included in the output .xlsx file,
	   via Pandas dataframe labels

Additionally, the Sentiment Analysis scores should already have been 
calculated for all 300 Identities, and included in the "Profile Stats" tab
of the "Main Fake Identities Database" spreadsheet, for more convenient
comparisons.
___________________________________________________________________________
Setup:
    pip install pandas numpy
	pip install xlwt openpyxl
	pip install matplotlib
And:
	pip install nltk
Or:
    pip install vaderSentiment
___________________________________________________________________________
"""
import nltk
#nltk.download('vader_lexicon') # NOTE: This has to be done once in your environment for everything to work
from nltk.sentiment.vader import SentimentIntensityAnalyzer
#from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from pandas import ExcelWriter
from pandas import ExcelFile
import pandas as pd
import numpy as np

from datetime import datetime
import datetime as dt
import operator
import openpyxl # Works with .xlsx files from Excel 2007+
#import xlwt # Only works with .xls files from Excel 2003
import math
import csv
import re

# The SentimentIntensityAnalyzer() module takes in a string
# and returns a dictionary of scores in each of four
# categories:
#
#   1. negative
#   2. neutral
#   3. positive
#   4. compound (computed by normalizing the scores above
#
sia = SentimentIntensityAnalyzer() # Initialize the VADER module

# Set up file I/O
in_list_name = "id_dict_2.csv"
in_sheet_name = "email_data_one_sheet.xlsx"
out_sheet_name = "analyzed_email_data_result.xlsx"

print("")
in_sheet_name = input("Please enter the name of the email data spreadsheet:\n\t>> ") #user_prompt
print("")
in_list_name = input("Please enter the name of the CSV file with the pre-filtered IDs to examine:\n\t>> ") #user_prompt
print("")

dframe_in = pd.read_excel(in_sheet_name)
#dframe_out = pd.DataFrame(
#	{ 'ID#':[], 'Email':[], 'Gender':[], 'Num.Emails':[],
#	  'Avg.Score':[], 'Pos%':[], 'Neu%':[],'Neg%':[]  }
#)

reader = csv.reader(open(in_list_name, 'r'))
#writer = pd.ExcelWriter(out_sheet_name)

#dframe_out.to_excel(writer,'Sheet1',index=True) # Start writing to output file
#writer.save() # Finish writing to output file

# Make Dictionaries for quick look-ups
d_id_to_site = {}
d_id_to_email = {}
d_id_to_gender = {}

for row in reader:
	w, x, y, z = row
	d_id_to_site[x] = w
	d_id_to_email[x] = z
	d_id_to_gender[x] = y
	#print(str(row)) # NOTE: This is here intentionally, for debugging

# Start by cleaning any potentially invalid cells/gaps in data file
dframe_in = dframe_in.dropna(subset=['To'])
dframe_in = dframe_in.dropna(subset=['From'])
dframe_in = dframe_in.dropna(subset=['Subject'])
dframe_in = dframe_in.dropna(subset=['Parsed_Content'])

recipients   = dframe_in['To'].tolist()
senders      = dframe_in['From'].tolist()
all_subjects = dframe_in['Subject'].tolist()
all_emails   = dframe_in['Parsed_Content'].tolist()

u_ids   = list(d_id_to_email.keys())
emails  = list(d_id_to_email.values())
sites   = list(d_id_to_site.values())
genders = list(d_id_to_gender.values())

all_received_emails = [] # The final table to export our processed data in

for k_name in range(len(u_ids)):
	# Make a sub-list of emails for each profile
	id_received_emails = []
	#
	str_out_0 = "\n\n"
	str_out_1 = "=================================================================="
	str_out_2 = "\n [Email SA Test Case]  # " + u_ids[k_name] + "\t( " + genders[k_name] + " )\t" + \
				"Website: " + sites[k_name] + \
				"\n To: " + emails[k_name] + '\n'
	print(str_out_0, str_out_1, str_out_2, str_out_1)
	
	# Fetch all messages for this ID from the spreadsheet
	for row in range(len(recipients)):
		
		### Re-assigning better labels ###
		this_uid = u_ids[k_name] # Convert from an int list index to the OG str ID label from the parser
		this_email = all_emails[row]
		
		# Not doing a direct string comparison because of inconsistent
		# prepended/appended characters to email addresses
		# (i.e. '<' '>' , '\"' '\"' )
		if emails[k_name].lower() in recipients[row]:
			#id_received_emails.append(all_emails[row])
			str_out_3 = " Subject: " + str(all_subjects[row]) + "\n < message content hidden >\n"
			
			### FINALLY DONE: Apply Vader to get SA score ###
			sentence = str(this_email)
			this_score = sia.polarity_scores(sentence)
			
			# Write this to a file later, so my team can access/process it from Google Drive
			str_out_x = " The overall sentiment values of the message are : " + str(this_score) + '\n'
			
			#polarity = score
			pos = round(100*this_score["pos"],2)
			neu = round(100*this_score["neu"],2)
			neg = round(100*this_score["neg"],2)
			
			### Package this Email Row and Results in a Tuple for Storage ###
			id_received_emails.append((this_email , this_score))
			
			str_out_a = " The percentage of positive sentiment in the message is : " + str(pos) + '%'
			str_out_b = " The percentage of neutral  sentiment in the message is : " + str(neu) + '%'
			str_out_c = " The percentage of negative sentiment in the message is : " + str(neg) + '%'
			str_out_d = " ------------------------------------------------------------------"
			'''
			print(str_out_3)
			print(str_out_x)
			#print(str_out_a, str_out_b, str_out_c, str_out_d)
			print(str_out_a)
			print(str_out_b)
			print(str_out_c)
			print(str_out_d)
			'''
			#dframe_out
	# end of loop
	# all_received_emails.append(id_received_emails)
	all_received_emails.append((this_uid , id_received_emails))
	# all_received_emails = list[tuple(str u_id, list[tuple(email, score)] u_id_data)]
# end of loop


writer = pd.ExcelWriter(out_sheet_name)
data_to_write = [] ### The list of miracles ###

# DONE: Track and output total # of emails received (needed for avg SA calculation)
for u_id_results in all_received_emails: # For each fake identity's results
	#
	u_id      = u_id_results[0] ### ~ Retreive the magic key that opens all doors ~ ###
	u_id_data = u_id_results[1]
	#u_id = u_ids[k_name] ### ~ Retreive the magic key that opens all doors ~ ###
	#d_id_to_email.keys()
	#id_emails_rec = u_id_data[1]
	#
	id_num_emails_procd = len(u_id_data)
	# TODO: Loop through results and sum up the individual SA scores
	for e in range(id_num_emails_procd):
		(id_email_rec, id_score_rec) = u_id_data[e] # NOTE: Unpacking the tuples from list
		#print(type(id_email_rec), type(id_score_rec))
		#	
		id_total_score_sum  = {'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0}
		id_total_score_avgs = {'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0}
		#text  = u_id_data[1][1][0][u_id] # I guess we don't actually need this part anymore, but keeping it for completeness
		#score = id_score_rec
		#print(type(u_id), type(u_id_data), type(id_total_score_sum), type(id_score_rec))
		#id_total_score_sum += score # NOTE: Careful, this is vector addition with a scalar
		id_total_score_sum['pos'] += id_score_rec['pos']
		id_total_score_sum['neu'] += id_score_rec['neu']
		id_total_score_sum['neg'] += id_score_rec['neg']
		id_total_score_sum['compound'] += id_score_rec['compound']
	# end of loop
	#
	# NOTE: This is vector division by a scalar
	if id_num_emails_procd > 0:
		id_total_score_avgs['pos'] = id_total_score_sum['pos'] / id_num_emails_procd
		id_total_score_avgs['neu'] = id_total_score_sum['neu'] / id_num_emails_procd
		id_total_score_avgs['neg'] = id_total_score_sum['neg'] / id_num_emails_procd
		id_total_score_avgs['compound'] = id_total_score_sum['compound'] / id_num_emails_procd
	#
	# Write result to data frame for Excel file
	data_to_write.append(
		[ u_id, d_id_to_email[u_id], d_id_to_gender[u_id], id_num_emails_procd, id_total_score_avgs['compound'],
			id_total_score_avgs['pos'], id_total_score_avgs['neu'], id_total_score_avgs['neg']
		]
	)
	#dframe_out.append(dframe_row)
	#dframe_out.to_excel(writer,'Sheet1',index=True) ### Write the frame to output file ###
# end of loop


dframe_out = pd.DataFrame( data_to_write,
columns=['ID#', 'Email', 'Gender', 'Num.Emails',
		 'Avg.Score', 'Pos%', 'Neu%','Neg%'
		]
)

dframe_out.to_excel(writer,'Sheet1',index=True) ### Write the frame to output file ###
#writer.save()
writer.close()# Finish writing to output file

#label_dict = {"Google Business":5, "Health Plan":3, "Free Hotel Stay":5, "Viagra":1, "Vehicle Warranty":102, "SSN Fraud":21, "Chinese Bank Credit":4, "Vegas Casino":1, "iCloud Breach":3, "Utility Rebate":3, "Chase Bank Credit":1}
#sorted_d = dict( sorted(label_dict.items(), key=operator.itemgetter(1),reverse=True))
#keys = list(sorted_d.keys())
#keys = [str(key) for key in sorted_d]
#values = list(sorted_d.values())
#plt.ylabel('Average Score of All Emails Received')
#plt.title('Sentiment Analysis of Potential Gender Bias in Emails')
#plt.bar(keys,values)
#plt.show()
