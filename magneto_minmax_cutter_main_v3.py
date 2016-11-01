import os
import datetime

print("Welcome to Magneto Min/Max Cutter v1.1!")
print("Please ensure that the file is in a root folder!")

#This block asks for the information on file location - name, extension, and the drive where the file is located.
filename = input("What is the name of your file? (Only the name, without extension!)")
extension = input("What is the extension of your file?")
if extension[0] == ".":
    extension = extension[1:]
filename_full = filename + "." + extension.lower()
location = input("What is the letter code of the drive the file is on? Please only input the letter itself.")
location = location.upper() + ":"
location_correct = 0
#An examination to see if the filename + location input by the user is correct and the file can be located
while location_correct == 0:
    try:
        input_file = open(os.path.join(location, filename_full), "r")
        input_file.close()
        location_correct = 1
    except:
        location_correct = 0
        print("No such file has been found at the specified location. Please try again.")
        filename = input("What is the name of your file? (Only the name, without extension!)")
        extension = input("What is the extension of your file?")
        if extension[0] == ".":
            extension = extension[1:]
        filename_full = filename + "." + extension.lower()
        location = input("What is the letter code of the drive the file is on? Please only input the letter itself.")
        location = location.upper() + ":"
#Setting up processing of the dataset by asking for the delimiter and the min/max value to be cut
delimiter_question = input("Is the delimiter of your dataset TAB? (y/n)")
delimiter = ""
if delimiter_question == "y":
    delimiter = "\t"
else:
    delimiter = input("Please specify the delimiter of your dataset:")
nanotesla_max = float(input("What is the min/max value you want to cut? Input a positive number here!"))
nanotesla_min = float(0 - nanotesla_max)

#Generating an output and a log filename by adding "processed and "log" to the original filename.
output_file_name = filename + "_processed" + "." + extension.lower()
log_file_name = filename + "_log" + "." + "txt"
#Opening  the input file in read mode + generating (and opening) the output and log files in write mode
input_file = open(os.path.join(location, filename_full), "r")
output_file = open(os.path.join(location, output_file_name), "w")
log_file = open(os.path.join(location, log_file_name), "w")

#Setting up the counters for the logs.
processed_lines = 0
output_lines = 0
deleted_lines = 0
invalid_lines = 0
valid_lines = 0
processing_time_start = datetime.datetime.now()

input_lines = input_file.readlines() #Reading the file line by line into a new list.
for line in input_lines:
    split_values = line.split(delimiter) #Split every line with the delimiter
    try: #Exception check to see if the line has values in it, or is and invalid (empty) line
        coord_x = float(split_values[0])
        coord_y = float(split_values[1])
        nanotesla = float(split_values[2])
        if nanotesla >= nanotesla_min and nanotesla <= nanotesla_max: #If the line has values and is within limits -> output
            output_file.write(str(line))
            output_lines += 1
            processed_lines += 1
            valid_lines += 1
        elif nanotesla < nanotesla_min or nanotesla > nanotesla_max: #Else -> do nothing, just add to the counters
            deleted_lines += 1
            processed_lines += 1
            valid_lines += 1
    except ValueError: #If the line did not contain data, add to the processed and invalid counter, print and add the fact to the logs
        print("Invalid (empty) data detected in line %s!" %(processed_lines))
        log_file.write("Invalid (empty) data detected in line %s! \n" %(processed_lines))
        invalid_lines += 1
        processed_lines += 1

#Close the timer on the processing and calculate elapsed time.
processing_time_end = datetime.datetime.now()
processing_time_elapsed = processing_time_end - processing_time_start

#Write out processing data into the log file.
log_file.write("Processing Finished \n\nProcessed file: %s \n \n" %(filename_full))
log_file.write("Processing started at: %s \n \n" % (processing_time_start))
log_file.write("Number of lines processed: %s \n" %(processed_lines))
log_file.write("Number of valid lines in dataset: %s \n" %(valid_lines))
log_file.write("Number of lines remaining after processing: %s \n" %(output_lines))
log_file.write("Number of lines deleted: %s \n" %(deleted_lines))
log_file.write("Number of invalid (empty) lines: %s \n \n" %(invalid_lines))
log_file.write("Processing ended at: %s \n" %(processing_time_end))
log_file.write("Elapsed time: %s \n" %(processing_time_elapsed))

#Close down the files.
input_file.close()
output_file.close()
log_file.close()

print("Number of processed lines: %s" %(processed_lines))
print("Number of valid lines in dataset: %s" %(valid_lines))
print("Number of lines remaining after processing: %s" %(output_lines))
print("Number of deleted lines: %s" %(deleted_lines))
print("Processing started: %s" %(processing_time_start))
print("Processing ended: %s" %(processing_time_end))
print("Elapsed time: %s" %(processing_time_elapsed))