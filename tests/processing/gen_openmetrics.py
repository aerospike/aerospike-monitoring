from datetime import datetime, timezone
import time


def generate_openmetrics_data(p_orig_csv_file_name, p_output_csv_file_name, p_utc_timestamp):
    inpput_csv_file = open( p_orig_csv_file_name, "r")    
    output_csv_file = open( p_output_csv_file_name, "w")
    
    while True:
        line = inpput_csv_file.readline()
 
        if not line:
            break
        # append this line to output file along with timestamp in UTC format
        output_line = line.strip()
        if not line.startswith("#"):
           output_line = (line.strip() + " " + str(p_utc_timestamp) )
           output_line = output_line.replace("cluster_name","job=\""+"aerospike"+"\""+",cluster_name")
        
        output_csv_file.write( output_line+ "\n")
    output_csv_file.write("# EOF")


# print( utc_timestamp )
# print( round(time.time()) )
if __name__ == "__main__":
    from globals import fn_mock_metrics_data, fn_modified_mock_metrics_data
    utc_timestamp = round(time.time())
    generate_openmetrics_data( fn_mock_metrics_data, fn_modified_mock_metrics_data, utc_timestamp)
