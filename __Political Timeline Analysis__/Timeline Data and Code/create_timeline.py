#==========================================================================#
'''
Use and Abuse of Personal Information - Summer 2021
	Creating the Timeline for the Entire Research Project's Database
	Author: Joshua Lyons - josh13@vt.edu

Setup Library Dependencies:
	pip3 install openpyxl
	pip3 install pandas	
	pip3 install xlwt
'''
#==========================================================================#
from datetime import datetime as dt
import operator
import math
import csv
import re
import os

from pandas import ExcelWriter
from pandas import ExcelFile
import pandas as pd
import numpy as np
import openpyxl # Works with .xlsx files from Excel 2007+
#import xlwt # Only works with .xls files from Excel 2003

#import matplotlib.dates as mdates
#import matplotlib.pyplot as plt

is_test_mode = False # Pseudo-macro to toggle code blocks for print debugging
#==========================================================================#

'''
===========================================================================
 TODO: Timeline Data Extraction and Processing Plan
===========================================================================
#0. Open the spreadsheet(s) to read and clean out unneeded/empty columns
#
#1a.Create a list/Series for the 300 ID# labels, from the 'ID_List' column
#   in the spreadsheet
#		
#		id_label_list = []
#
#1b.Create a list/Series for all the potential calendar dates (stored as
#   formatted strings), from the 'Calendar_Dates' column
#		
#		timeline_cal_dates = []
#   
#2. For each of the 300 IDs, create a lookup table/dict/map with a date
#   string for the keys and a 3-element vector/tuple/series for the values:
#
#		timeline_map = {}
#		
#3. Fill in the timeline mapping for each ID by nested looping through the
#   lists of all 3 (or 4?) data types, checking the related `To_ID` entries
#   for the current ID, and add values to the 3-tuple mapped to the date key
#		
#		map[i_date] = (i_emails, i_vmails, i_sms)
#
#4. Create a dataframe for each entry in the list of ID labels?
#		
#		pd.DataFrame(timeline_map, index = id_label_list[i_entry])
#			or
#		pd.DataFrame(timeline_map, rows = timeline_cal_dates)
#
#5. Reasonably organize/format the data results, and write it out to a new
#   spreadsheet, from which I can easily copy/paste into the Google Drive one
===========================================================================
'''

print()
print("Starting database file pre-processing, please wait...")
print()

#--------------------------------------------------------------------------#
#0. Open the spreadsheet(s) to read and clean out unneeded/empty columns
#--------------------------------------------------------------------------#
in_sheet_name = "Database_Summary_for_Timelines.xlsx"
out_sheet_name = "Timeline_from_Database.xlsx"
dframe_in = pd.read_excel(in_sheet_name)

#email_date_list = dframe_in.dropna(subset=['Email_Date']).tolist()
#call_date_list = dframe_in.dropna(subset=['Call_Date']).tolist()
#sms_date_list = dframe_in.dropna(subset=['SMS_Date']).tolist()
#vm_date_list = dframe_in.dropna(subset=['VM_Date']).tolist()

# Start by cleaning any potentially invalid cells/gaps in data file (and skip the less reliable non-Zadarma call logs)
#dframe_in = dframe_in.dropna(axis=0, subset=[
#	'Email_To_ID', 'VM_To_ID', 'Z-Call_To_ID', 'SMS_To_ID',
#	'Email_Date', 'VM_Date', 'Z-Call_Date', 'SMS_Date',  'ID_List'
#	]
#)
#dframe_in = dframe_in.dropna(subset=['Email_To_ID'])
#dframe_in = dframe_in.dropna(subset=['Email_Date'])
#dframe_in = dframe_in.dropna(subset=['Z-Call_Date'])
#dframe_in = dframe_in.dropna(subset=['Z-Call_To_ID'])
#dframe_in = dframe_in.dropna(subset=['SMS_Date'])
#dframe_in = dframe_in.dropna(subset=['SMS_To_ID'])
#dframe_in = dframe_in.dropna(subset=['VM_Date'])
#dframe_in = dframe_in.dropna(subset=['VM_To_ID'])

email_date_col = dframe_in.dropna(subset=['Email_Date'])
email_date_series = email_date_col['Email_Date']

call_date_col = dframe_in.dropna(subset=['Z-Call_Date'])
call_date_series = call_date_col['Z-Call_Date']

sms_date_col = dframe_in.dropna(subset=['SMS_Date'])
sms_date_series = sms_date_col['SMS_Date']

vmail_date_col = dframe_in.dropna(subset=['VM_Date'])
vmail_date_series = vmail_date_col['VM_Date']

email_to_id_col = dframe_in.dropna(subset=['Email_To_ID'])
email_to_id_series = email_to_id_col['Email_To_ID']

call_to_id_col = dframe_in.dropna(subset=['Z-Call_To_ID'])
call_to_id_series = call_to_id_col['Z-Call_To_ID']

sms_to_id_col = dframe_in.dropna(subset=['SMS_To_ID'])
sms_to_id_series = sms_to_id_col['SMS_To_ID']

vmail_to_id_col = dframe_in.dropna(subset=['VM_To_ID'])
vmail_to_id_series = vmail_to_id_col['VM_To_ID']

#print(type(email_date_col))
#print(type(email_date_series))

#email_date_col = dframe_in['Email_Date'].tolist()
#call_date_col = dframe_in['Z-Call_Date'].tolist()
#sms_date_col = dframe_in['SMS_Date'].tolist()
#vm_date_col = dframe_in['VM_Date'].tolist()
#
#email_to_id_col = dframe_in['Email_To_ID'].tolist()
#call_to_id_col = dframe_in['Z-Call_To_ID'].tolist()
#sms_to_id_col = dframe_in['SMS_To_ID'].tolist()
#vm_to_id_col = dframe_in['VM_To_ID'].tolist()


#--------------------------------------------------------------------------#
#1a.Create a list/Series for the 300 ID# labels, from the 'ID_List' column
#	in the spreadsheet
#		
#		id_label_list = []
#--------------------------------------------------------------------------#
#id_label_list = []
id_label_col = dframe_in.dropna(subset=['ID_List'])
id_label_list = id_label_col['ID_List'].tolist()
#id_label_list = dframe_in['ID_List'].values()
field_labels = [
	'Emails: ',
	'Vmails: ',
	'Calls: ',
	'SMS: '
]
print("Length of ID labels list: ", len(id_label_list))

#--------------------------------------------------------------------------#
#1b.Create a list/Series for all the potential calendar dates (stored as
#	formatted strings), from the 'Calendar_Dates' column
#		
#		timeline_cal_dates = []
#--------------------------------------------------------------------------#
#timeline_cal_dates = []
timeline_cal_col = dframe_in.dropna(subset=['Calendar_Dates'])
timeline_cal_dates = timeline_cal_col['Calendar_Dates'].tolist()
print("Length of Calendar dates list: ", len(timeline_cal_dates))

#--------------------------------------------------------------------------#
#2. For each of the 300 IDs, create a lookup table/dict/map with a date
#	string for the keys and a 3-element vector/tuple/series for the values:
#
#		timeline_map = {}
#--------------------------------------------------------------------------#
#timeline_map = {}
timeline_maps = []

#--------------------------------------------------------------------------#
#3. Fill in the timeline mapping for each ID by nested looping through the
#	lists of all 3 (or 4?) data types, checking the related `To_ID` entries
#	for the current ID, and add values to the 3-tuple mapped to the date key
#		
#		map[i_date] = (i_emails, i_vmails, i_sms)
#--------------------------------------------------------------------------#
def count_and_map_ids(num_ids):
	#num_emails_procd = len(u_id_data)
	#num_emails = len(email_date_col.tolist())
	#num_vms    = len(vm_date_col.tolist())
	#num_calls  = len(call_date_col.tolist())
	#num_sms    = len(sms_date_col.tolist())
	num_emails = len(email_date_col)
	num_vmails = len(vmail_date_col)
	num_calls  = len(call_date_col)
	num_sms    = len(sms_date_col)
	
	print("Total number of emails:\t", num_emails)
	print("Total number of vmails:\t", num_vmails)
	print("Total number of calls:\t", num_calls)
	print("Total number of SMS:\t", num_sms)
	print()
	
	id_count = 0 ### My convenience counter <3 ###
	
	for ID in id_label_list:
		
		if id_count >= num_ids:
			break
		
		id_timeline_map = {}
		
		email_total = 0
		vmail_total = 0
		call_total  = 0
		sms_total   = 0
		
		print("Begin timeline creation for:\t", ID, "\n")
		
		for date in timeline_cal_dates:
			# Get the data for that day from the columns
			data_entry = []
			
			email_count = 0
			vmail_count = 0
			call_count  = 0
			sms_count   = 0
			
			# NOTE: Doing it like this in 1 line is probably the most succient and "Pythonic" way
			#email_count = len(dframe_in[dframe_in['Email_Dates'].str.contains(date)==True])
			
			for e_date in range(num_emails): # Forces integer index values for cross-referencing
				#if dframe_in['Email_Date'][e_date].contains(date) and dframe_in['Email_to_ID'][e_date].contains(ID):
				#if (str(date) in dframe_in['Email_Date'][e_date]) and (str(ID) in dframe_in['Email_To_ID'][e_date]):
				if str(date) in email_date_series.values[e_date]:
					if str(ID) in email_to_id_series.values[e_date]:
						email_count += 1 ### Only count emails for this ID if they were received on this current date ###
					pass
				pass
			data_entry.append(email_count)
			email_total += email_count
			
			for v_date in range(num_vmails): # Forces integer index values for cross-referencing
				#if ( str(date) in dframe_in['VM_Date'][v_date] ) and ( str(ID) in dframe_in['VM_To_ID'][v_date] ):
				if str(date) in vmail_date_series.values[v_date]:
					if str(ID) in vmail_to_id_series.values[v_date]:
						vmail_count += 1 ### Only count voicemails for this ID if they were received on this current date ###
					pass
				pass
			data_entry.append(vmail_count)
			vmail_total += vmail_count
			
			for c_date in range(num_calls): # Forces integer index values for cross-referencing
				#if dframe_in['Z-Call_Date'][c_date].contains(date) and dframe_in['Z-Call_To_ID'][c_date].contains(str(ID)):
				#if ( str(date) in dframe_in['Z-Call_Date'][c_date] ) and ( str(ID) in dframe_in['Z-Call_To_ID'][c_date] ):
				if str(date) in call_date_series.values[c_date]:
					if str(ID) in call_to_id_series.values[c_date]:
						call_count += 1 ### Only count calls for this ID if they were received on this current date ###
					pass
				pass
			data_entry.append(call_count)
			call_total += call_count
				
			for s_date in range(num_sms): # Forces integer index values for cross-referencing
				#if dframe_in['SMS_Date'][s_date].contains(date) and dframe_in['SMS_To_ID'][s_date].contains(str(ID)):
				#if ( str(date) in dframe_in['SMS_Date'][s_date] ) and ( str(ID) in dframe_in['SMS_To_ID'][s_date] ):
				if str(date) in sms_date_series.values[s_date]:
					if str(ID) in sms_to_id_series.values[s_date]:
						sms_count += 1 ### Only count sms texts for this ID if they were received on this current date ###
					pass
				pass
			data_entry.append(sms_count)
			sms_total += sms_count
			
			#data_entry = [call_count, sms_count, email_count, voicemail_count]
			print("\tData entry for ", str(ID), " on ", str(date), " is ", data_entry)
			
			# Wrap a list as a Series to label the index values of the entry (like using enums in C)
			timeline_entry = pd.Series(data_entry, index=field_labels).values
			id_timeline_map[date] = timeline_entry
			
		# End for
		
		
		id_timeline_map["Totals"] = [email_total, vmail_total, call_total, sms_total]
		
		# Wrap a map as a Series to label the index values of the entry (like using enums in C)
		#series_out = pd.Series(id_timeline_map, index=id_label_list)
		
		#dframe_out = pd.DataFrame(id_timeline_map, index=id_label_list, columns=timeline_cal_dates)
		#timeline_maps.append(dframe_out)
		
		timeline_maps.append(id_timeline_map)
		
		#timeline_maps.append(series_out)
		print()
		print("\tTotal Stats:", id_timeline_map["Totals"], "\n")
		print("\tProcessing ", str(ID), " is complete!\n")
		print()
		
		id_count += 1 # Don't forget to increment the convenience counter
		pass
	# End for
# End of def


#def output_spreadsheet_results(df_entries_to_write, out_sheet_name):
def output_spreadsheet_results(index_labels, id_entries_to_write, out_sheet_name):
	
	print("")
	if len(id_entries_to_write) == 0:
		print("No writeable data was produced")
		return
		
	print("Note: Output data entry syntax convention is in the following form\n\t[ num_emails, num_vmails, num_calls, num_sms ]\n")
	
	print("Writing to spreadsheet...\n")
	
	writer = pd.ExcelWriter(out_sheet_name) # Ignore this irrelevant warning
	
	# Wrap result in a labeled Pandas data frame for the Excel file
	
	dframe_out = pd.DataFrame( id_entries_to_write,	index=index_labels, columns=timeline_cal_dates)
	
	dframe_out.to_excel(writer, out_sheet_name, index=True) ### Write the frame to output file ###
	
	writer.close()
# End of def

#timeline_map =  pd.Series()


#==========================================================================#
def main():
	#---------------------------------------------------#
	#  Setup the Input/Output Files to Read/Write to
	#---------------------------------------------------#
	#in_sheet_name = "Database_Summary_for_Timelines.xlsx"
	#out_sheet_name = "Timeline_from_Database.xlsx"
	#dframe_in = pd.read_excel(in_sheet_name)
	id_label_list = []
	
	print()
	num_ids = input("\tHow many IDs would you like to process today? (Note: each one can take up to 10 seconds)\n\n\t>> ") #user_prompt
	print()
	
	if int(num_ids) <= 0:
		print("\tOops! Nevermind, see you later then\n\nUser exited timeline creation\n")
		return
	elif int(num_ids) < 300:
		loc_id_label_list = id_label_col['ID_List'].tolist()[0:int(num_ids)] # Hopefully this allows the convenience feature to work as intended
	else:
		loc_id_label_list = id_label_col['ID_List'].tolist()
	
	print("Starting main database processing, please wait...")
	print()
	
	#---------------------------------------------------#
	#  Process Database to Create Timeline Data
	#---------------------------------------------------#
	count_and_map_ids(int(num_ids))
	
	#---------------------------------------------------#
	#  Write Analysis Result Data to Excel Spreadsheet
	#---------------------------------------------------#
	output_spreadsheet_results(loc_id_label_list, timeline_maps, out_sheet_name)
	
	print()
	print("Timeline data processing is now complete. Have a nice day! =]")
	print()
	
# End of def
#==========================================================================#

if __name__ == '__main__':
	if is_test_mode:
		pass
	else:
		main()

# End of execution
