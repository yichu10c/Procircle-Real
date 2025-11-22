# procircle-be-api-main

## HOW TO DEPLOY BACKEND APP
```
serve [environment] [action]
```
Example
```
serve dev start
serve prod stop
serve prod restart
serve prod cleanstop
serve dev cleanstart
serve dev log
```

### Notes
1. It is important to execute below code for the first deployment
```
serve prod cleanstart
```

## How to run test
1. go to `backend` directory
2. run
```
pytest
```
3. or with coverage
```
pytest --cov=app
pytest --cov=job_worker
pytest --cov=rpc
```

## How to SSH
```
ssh <user>@<host> -i <pem file>
```

## How to setup tunnel
```
ssh <user>@<host> -i <pem file> -L
ssh -i "./pem/mms-pgm-procircle-sg-dev.pem" -f -N -L \
    5432:procircle-dev-main-db.c504y6w4qp4k.ap-southeast-1.rds.amazonaws.com:5432\
    ubuntu@ec2-52-221-221-213.ap-southeast-1.compute.amazonaws.com
```

## How to check active port listener
```
lsof -nP -iTCP -sTCP:LISTEN | grep .
```

## Deploy ASGI
```
gunicorn main:app --workers 3 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --log-level critical
uvicorn main:app --workers 3 --log-level critical
uvicorn main:app --workers 3 --log-level critical --loop uvloop --interface asgi3
python3 -m socketify main:app -w 3 -p 8000
```