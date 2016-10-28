import os
import datetime

print("Welcome to Magneto Min/Max Cutter v1.0!")
print("Please ensure that the file is in a root folder!")

filename = input("What is the name of your file? (Only the name, without extension!)")
extension = input("What is the extension of your file?")
if extension[0] == ".":
    extension = extension[1:]
filename_full = filename + "." + extension.lower()
location = input("What is the letter code of the drive the file is on? Please only input the letter itself.")
location = location.upper() + ":"
delimiter_question = input("Is the delimiter of your dataset TAB? (y/n)")
delimiter = ""
if delimiter_question == "y":
    delimiter = "\t"
else:
    delimiter = input("Please specify the delimiter of your dataset:")
print(delimiter)
nanotesla_max = float(input("What is the min/max value you want to cut? Input a positive number here!"))
nanotesla_min = float(0 - nanotesla_max)

output_file_name = filename + "_processed" + "." + extension.lower()
log_file_name = filename + "_log" + "." + "txt"
input_file = open(os.path.join(location, filename_full), "r")
output_file = open(os.path.join(location, output_file_name), "w")
log_file = open(os.path.join(location, log_file_name), "w")

processed_lines = 0
output_lines = 0
deleted_lines = 0
invalid_lines = 0
processing_time_start = datetime.datetime.now()

input_lines = input_file.readlines()
for line in input_lines:
    split_values = line.split(delimiter)
    try:
        coord_x = float(split_values[0])
        coord_y = float(split_values[1])
        nanotesla = float(split_values[2])
    except ValueError:
        invalid_lines += 1
    if nanotesla >= nanotesla_min and nanotesla <= nanotesla_max:
        output_file.write(str(line))
        output_lines += 1
        processed_lines += 1
    else:
        deleted_lines += 1
        processed_lines += 1

processing_time_end = datetime.datetime.now()
processing_time_elapsed = processing_time_end - processing_time_start

log_file.write("Processing Finished \n\nProcessed file: %s \n \n" %(filename_full))
log_file.write("Processing started at: %s \n \n" %(processing_time_start))
log_file.write("Number of lines processed: %s \n" %(processed_lines))
log_file.write("Number of lines remaining after processing: %s \n" %(output_lines))
log_file.write("Number of lines deleted: %s \n" %(deleted_lines))
log_file.write("Number of invalid (empty) lines: %s \n \n" %(invalid_lines))
log_file.write("Processing ended at: %s \n" %(processing_time_end))
log_file.write("Elapsed time: %s \n" %(processing_time_elapsed))

input_file.close()
output_file.close()
log_file.close()

print("\nNumber of processed lines: %s" %(processed_lines))
print("Number of lines remaining after processing: %s" %(output_lines))
print("Number of deleted lines: %s" %(deleted_lines))
print("Processing started: %s" %(processing_time_start))
print("Processing ended: %s" %(processing_time_end))
print("Elapsed time: %s" %(processing_time_elapsed))