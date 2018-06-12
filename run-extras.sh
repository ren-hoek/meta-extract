docker run --network jupyterhub --name redis -d redis
docker run --network jupyterhub --name mongo -d mongo
docker run --network jupyterhub --link mongo:mongo --name mongo-express -p 8081:8081 mongo-express

