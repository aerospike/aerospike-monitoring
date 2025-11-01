echo Downloading and installing OLM
echo

# Create the namespace (harmless if it exists)
kubectl create namespace cert-manager --dry-run=client -o yaml | kubectl apply -f -

# Install the latest stable cert-manager (manifests include CRDs)
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.19.1/cert-manager.yaml

# Wait for it to be ready
kubectl -n cert-manager rollout status deploy/cert-manager --timeout=120s
kubectl -n cert-manager rollout status deploy/cert-manager-webhook --timeout=120s
kubectl -n cert-manager rollout status deploy/cert-manager-cainjector --timeout=120s

echo 
echo Installed cert-manager and verifed they are available
echo 
echo now installing OLM operator

echo curl -L https://github.com/operator-framework/operator-lifecycle-manager/releases/download/v0.36.0/install.sh -o /tmp/olm36_install.sh

curl -L https://github.com/operator-framework/operator-lifecycle-manager/releases/download/v0.36.0/install.sh -o /tmp/olm36_install.sh
chmod +x /tmp/olm36_install.sh
/tmp/olm36_install.sh v0.36.0
