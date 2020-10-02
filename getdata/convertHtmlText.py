# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 20:55:13 2020

@author: lawre
"""

from bs4 import BeautifulSoup

def check_if_string_in_file(file_name, string_to_search):
    """ Check if any line in the file contains given string """
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            if string_to_search in line:
                return True
    return False

def search_string_in_file(file_name, string_to_search):
    """Search for the given string in file and return lines containing that string,
    along with line numbers"""
    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            line_number += 1
            if string_to_search in line:
                # If yes, then add the line number & line as a tuple in the list
                list_of_results.append((line_number, line.rstrip()))
    # Return list of tuples containing line numbers and lines where string is found
    return list_of_results

def search_multiple_strings_in_file(file_name, list_of_strings):
    """Get line from the file along with line numbers, which contains any string from the list"""
    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            line_number += 1
            # For each line, check if line contains any string from the list of strings
            for string_to_search in list_of_strings:
                if string_to_search in line:
                    # If any string is found in line, then append that line along with line number in list
                    list_of_results.append((string_to_search, line_number, line.rstrip()))
    # Return list of tuples containing matched string, line numbers and lines where string is found
    return list_of_results

def search_records(file_name):
    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
         # Read all lines in the file one by one
        for line in read_obj:
            line_number += 1
            # For each line, check if line contains any string from the list of strings
            if string_to_search in line:
                # If yes, then add the line number & line as a tuple in the list
                list_of_results.append((line_number, line.rstrip()))
                
                
                
                
    # Return list of tuples containing line numbers and lines where string is found
    return list_of_results
                
            


def convertToText(folder_name, file_name):
    local_file = folder_name + "/" + file_name
    local_newfile = folder_name + "/" + file_name[0:-4]+".txt"      
    with open (local_file,"r") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        newtext = soup.get_text()
        with open(local_newfile,'w') as f1:
            f1.write(newtext)

def findTextinFile(folder_name, file_name):
    #local_file = folder_name + "/" + file_name
    local_newfile = folder_name + "/" + file_name[0:-4]+".txt"
    matched_lines = search_string_in_file(local_newfile, 'CODE  NAME OF STOCK    SALES RECORD')
    #matched_lines = search_string_in_file(local_newfile, 'DAILY QUOTATIONS')
    print('Total Matched lines : ', len(matched_lines))
    for elem in matched_lines:
        print('Line Number = ', elem[0], ' :: Line = ', elem[1])
        
    
    
    
if __name__ == '__main__':
    
    folder = "dailyQuotations"
    file = "d190506e.htm"
    convertToText(folder,file)
    
    findTextinFile(folder,file)
    
    



        