# Lab 8 - Docker, containers and images

Images are named with my AUB username, `mia67`. Docker image names must be
lowercase, so the image is `mia67/lab8-muhammad_natour`.

Docker Desktop must be running before any `docker` command works.

```
lab8/
  activity1/          hello world Flask app (flask_docker)
  activity2/
    v0.0.1/           Lab 5 user API on port 5000
    v0.0.2/           Lab 5 user API + GET /get_users on port 3000
```

---

## Activity 1 - first container

```bash
cd activity1
docker image build -t flask_docker .
docker run -p 5000:5000 -d --name flask_docker flask_docker
```

Open http://localhost:5000 to see `Hello, World!`.

Run these and take a screenshot after each one:

```bash
docker ps -a
docker logs flask_docker
docker stop flask_docker
```

Explanations for the Word document:

- **`docker ps -a`** lists all containers on the machine, both running and stopped
  (without `-a` it only shows running ones). For each container it shows the
  container ID, the image it was created from, the command it runs, when it was
  created, its status, the port mappings and its name.
- **`docker logs <container>`** prints everything the container has written to its
  standard output and error. Here it shows the Flask startup messages
  (`Running on http://0.0.0.0:5000`) and a line for every request sent to the app.
- **`docker stop <container>`** stops a running container gracefully: Docker sends
  it a SIGTERM signal and, if it has not exited after 10 seconds, a SIGKILL. The
  container is not deleted; `docker ps -a` now shows it as `Exited`, and it can be
  started again with `docker start <container>`.

Note: these commands take a *container* name or ID, not an image name. The
`--name flask_docker` in `docker run` gives the container the same name as the
image so the commands above work. Without it, use the ID from `docker ps -a`.

---

## Activity 2 - two images

### v0.0.1 - Lab 5 API on port 5000

```bash
cd activity2/v0.0.1
docker image build -t mia67/lab8-muhammad_natour:0.0.1.RELEASE .
docker run -p 5000:5000 -d --name lab8-v1 mia67/lab8-muhammad_natour:0.0.1.RELEASE
```

Test: http://localhost:5000/api/users

Endpoints (same as Lab 5):

| Endpoint | Method |
|----------|--------|
| `/api/users` | GET |
| `/api/users/<user_id>` | GET |
| `/api/users/add` | POST |
| `/api/users/update` | PUT |
| `/api/users/delete/<user_id>` | DELETE |

### v0.0.2 - names of all users on port 3000

```bash
cd activity2/v0.0.2
docker image build -t mia67/lab8-muhammad_natour:0.0.2.RELEASE .
docker run -p 3000:3000 -d --name lab8-v2 mia67/lab8-muhammad_natour:0.0.2.RELEASE
```

Test: http://localhost:3000/get_users returns a list of names, for example
`["John Doe", "Jane Smith", "Ali Hassan"]`. All the Lab 5 endpoints also work on port 3000.

Then open **Docker Desktop -> Images** and take a screenshot showing both images.

---

## Notes

- The database (`database.db`) is created inside the container when it starts,
  with three default users, so every new container starts with the same data.
- The apps run with `host='0.0.0.0'`. With Flask's default (`127.0.0.1`) the app
  would only accept connections from inside the container, and the port mapping
  would not work.
- The Dockerfiles use `python:3.12-alpine` instead of the handout's
  `python:3.8-alpine`, because the current Flask (3.1) needs Python 3.9 or newer.
