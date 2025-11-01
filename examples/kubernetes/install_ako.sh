echo
echo Installing AKO
echo
echo kubectl create -f https://operatorhub.io/install/aerospike-kubernetes-operator.yaml
echo
kubectl create -f https://operatorhub.io/install/aerospike-kubernetes-operator.yaml

echo
echo To verify ako installation status use below command, this will take some time to complete.
echo
echo kubectl get csv -n operators aerospike-kubernetes-operator.v4.1.1 -w
echo
echo ... Sleeping for 60 seconds before checking if AKO is installed
echo
sleep 60
echo
kubectl get csv -n operators aerospike-kubernetes-operator.v4.1.1 
