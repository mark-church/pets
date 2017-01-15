#The Pets Application
Pets is a simple application that's useful for testing out features of Docker.

Pets is comprised of two images:

- `web` is a front-end Python Flask container that serves up random images of housepets, depending on the given configuration
- `db` is a back-end consul KV store that stores the number of visits that each `web` service recieves. It's configured to bootstrap itself with 3 replicas so that we have fault tolerant persistence.


###Running Pets on Swarm in Development
Docker Swarm can easily be set up to run applications on a single developer laptop. The full app can be brought up to run in the same way it would run in production. We use a compose v3 file to deploy a fully fault tolerant frontend and backend, along with the configurations, secrets, and networks required for the application to run.

This is the full architecture that is deployed when using [pets-dev-compose.yml]().

```
$ docker stack deploy -c pets-dev-compose.yml pets
Creating network pets_backend
Creating service pets_db
Creating service pets_web
```

![](images/pets-dev-arch.png) 


####web
The `web` container has several required inputs.

- `-e ROLE` - this environment variable must be the value `cat` or `dog`. This will determine what type of animations are served.
- `-e DB` - this environment variable is the service name or `IP:port` location of the backend `db` container
- `-p <external port>:5000` determines the external port that content is served on. `web` runs internally on port `5000`

####db
The `db` container has no required inputs. It may require a service name if a service name is provided to `web` instead of an IP address.


####admin



###Single Tenant Deployment
In a single tenant deployment Pets deploys as a single `web` and a single `db` container. The `ROLE` can be either `cat` or `dog` depending on your preference and what kind of person you are. The Pets app will be externally reachable on port `8000`.

####Local Deployment

```
$ docker network create -d bridge petnet
$ docker run -d --net petnet --name db redis
$ docker run -d --net petnet -p 8000:5000 -e 'DB=db' -e 'ROLE=cat' chrch/web 
```
####Swarm Deployment
```
$ docker network create -d overlay petnet
$ docker service create --network petnet --name db redis
$ docker service create --network petnet -p 8000:5000 -e 'DB=db' --name web chrch/web
```

docker service create --restart-condition on-failure:3 --network petnet -p 8000:5000 -e 'DB=db' --name web chrch/web

<br>
<p align="center">
<img src="./images/singletenant.png" width=40%>
</p>
<br>

Additional `web` containers can be added to achieve more front-end scale. 


###Multi Tenant Deployment
In a multi-tenant deployment Pets deploys as multiple independent services. You can instantiate a multi-tenant deployment by running `docker-compose up -f multi-tenant-compose.yml`. The service will be externally reachable on the following ports:

- Dogs on port `8000`
- Cats on port `8001`
- Admin on port `8002`

<br>
<p align="center">
<img src="./images/multitenant.png" width=90%>
</p>
<br>