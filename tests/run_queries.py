
import requests

filename_fullform_queries = "mockdata/queries_to_test.queries"

prometheus_url_to_get = "http://localhost:8900/api/v1/query"

def query_prom_using_get( p_query):
    http_response = requests.get(prometheus_url_to_get, params={'query': p_query})    
    data = http_response.json()["data"]
    result = data["result"]
    print( data)
    print(" \t\t ", result)

def read_queries_and_fire():
    fd_queries = open( filename_fullform_queries, "r")   
    
    while True:
        line = fd_queries.readline()
 
        if not line:
            break
        # from key=value pair, split
        parts = line.split(  "=", 1)
        print( parts[0])
        print( parts[1])
        # post request to prometheus-server
        cleaned_str = parts[1].strip()
        if  "No Expression" in cleaned_str:
            query_prom_using_get( parts[1])

if __name__ == "__main__":
    read_queries_and_fire()

