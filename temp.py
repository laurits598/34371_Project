import csv

infile = "ip_data_files/results.csv"
output_file = "ip_data_files/filtered_results.csv"


with open(infile, newline="", encoding="utf-8") as infile, \
    open(output_file, "w", newline="", encoding="utf-8") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    # Read and write header
    header = next(reader)
    writer.writerow(header)
    # Filter rows where login_prompt_found is True
    for row in reader:
        if len(row) > 1 and row[1] == "True":
            writer.writerow(row)
    
    print(f"Filtered results written to {output_file}")
