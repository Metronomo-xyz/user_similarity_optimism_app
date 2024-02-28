# user_similarity_optimism_app
Tool to calculate users similarity on Optimism blockchain

It's part of user_similarity_optimism functionality
![architecture](http://dl3.joxi.net/drive/2024/02/25/0016/0232/1081576/76/fcf7b0a8f8.jpg)

This module is an API server which allows 2 functions:
- update similarity data from provided Google Cloud Storage blob
- get list of similar wallets to wallets in the provided `.csv` file

To calculate similarity data and store it into Google Cloud Storage blob you can use user_similarity_optimism_calculator module 

## Prerequisites

### Hardware

### App server
Any kind of Python WSGI server with Flask is sutable for running from source code.
For running in Docker image you can use any preferred machine.

#### MongoDB Server
In [user_similarity_optimism_calculator](https://github.com/Metronomo-xyz/user_similarity_optimism_calculator) you created MongoDB server to store similarities.

If not - please, go to link above and first calculate similarities using module in the link.

## Running from Docker image
It's the easiest way to run the module

### 1. Create .env file

Copy `.env` file from `https://github.com/Metronomo-xyz/user_similarity_optimism_app`

Put it on your machine

Change values in .env file like described [below](#env)

### 2. Pull image from docker

```
sudo docker pull randromtk/user_similarity_optimism_app:dev
```

### 3. Run docker container

```
sudo docker run -it -p <server port>:5000 --env-file <path to .env file> <image tag>
```
- `<server port>` - exposed port of the machine on which you will send request
- `5000` - docker port, which is exposed and listened 
- `<path to .env file>` - path to file, that you created [before](#1createenvfile)
- `<image tag>` - image tag. Might be obtained by running `sudo docker images` command

*To run locally* (but this works only for Linux) 

```
sudo docker run -it -p <server port>:5000 --env-file <path to .env file with host 127.0.0.1> --network=="host" <image tag>
```

More details on [docker options](https://docs.docker.com/engine/reference/commandline/run/#publish)

Example:
```
sudo docker run -it -p 80:5000 --env-file user_similarity_optimism_app/.env 0b3a1a3d7587
```

## Running from the source code

### 0. Provide data source

You have to use your own MongoDB server to store similarity

### 1. Clone repository

`git clone https://github.com/Metronomo-xyz/user_similarity_optimism_app.git`

### 2. Create virtual environment

It's recommended to use virtual environment while using module

If you don't have `venv` installed run (ex. for Ubuntu)
```
sudo apt-get install python3-venv

```
then create and activate virtual environment
```
python3 -m venv sim_app
source sim_app/bin/activate
```

### 3. Install requirements
Run
```
pip install -r user_similarity_optimism_app/requirements.txt
```

### 4. Set environmental variables

env-files:
- [.env](#env) - Need to take file from current repository as example, change it and keep it in module directory (in the same directory as `app.py`).

#### .env

Variables to access MongoDB server. You have to set your own

```
- MONGO_HOST - host of mongodb server to write similarities data to
- MONGO_PORT - port of mongodb server  to write similarities data to
- MONGO_DATABASE  - mongo database name to write similarities data to
- MONGO_COLLECTION  - mongo collection name to write similarities data to
```

### 7. Run the app

```
gunicorn -b 0.0.0.0:<port> --chdir user_similarity_optimism_app app:app --timeout <timeout>
```
- `<port>` - port to listen to requests
- `<timeout>` - requests timeout in seconds

example:

```gunicorn -b 0.0.0.0:5000 --chdir user_similarity_optimism_app app:app --timeout 300```

Options to run gunicorn server with app:

- `-b` - binding of local address and port. User `0.0.0.0` as ip and port that was chosen while creating firewall rule (`8080` in our example) 
- `--timeout` - that loading data into server and also retrieving list of similar users will take a while. So need to set at least `--timeout 300`
- `--chdir` - change directory of unicorn. If you use `cd user_similarity_optimism_app` before running server it's necessary to change modules import in files, so better to use command above.

## Send requests to the server

If you completed previous steps correctly, then you will be able to run scripts with request from another machine (maybe your local machine).

- `send_request_get_similarity` - to receive list of user provided in some file

Note, that both scripts are just example of usage, and you have to rewrite them with your own info:

- server host and port
- list of wallets
- similarity thresholds of your interest
- preferable response format. Possible are csv, json.
