```
docker-machine create -d azure \
    --azure-subscription-id="c280f806-099e-4a81-9e6e-f0a3829ef605" \
    --azure-subscription-cert ~/.azure/mycert.pem \
    --azure-location="West Europe" 
    --azure-size="Medium" 
  os-master
```