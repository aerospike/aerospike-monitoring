source elk_docker_variables.sh 
#docker-compose -f docker-compose.yml up (not working) 

#docker compose -f docker-compose.yml up  
#docker compose -f with-fluentbit-docker-compose.yml up 
docker compose -f docker-compose-aerospike-log-analysis.yml up
