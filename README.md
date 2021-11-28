# **Moody-Music-Backend**

## **_Description_**

Moody Music is an AI powered music player based on Spotify embeds and mood detection using deep learning.

Moody Music changes the way we listen and perceive music. As a user, you will no longer have to interact with the music player in the traditionnal way, looking up playlists by name and picking music manually. All you have to do is give the app access to your webcame and let it do its magic.

Using deep learning algorithms, the system will automatically recognize your mood and based on that it will give you suggestions of playlists that are compatible with your current mood.

## **_Demo_**

The project is not yet publicly hosted. If you want to test it you will have to set it up locally.

## **_Setup_**

### **_Requirements_**

In order to to setup this project and run it locally you need to have [`python3`](https://www.python.org/downloads/) and [`pipenv`](https://pypi.org/project/pipenv/) installed on your machine.

### **_Setup and populate the database_**

This projects uses a PostgreSQL database. You will need to [install it](https://www.postgresqltutorial.com/install-postgresql/) before proceeding with the rest of the steps. Alternatively, you can use a remotely hosted PostreSQL database using the ip adress of the server on which it is hosted.

Navigate to the root folder of this project and run the following command:

```
psql -U postgres_username -f setup.sql
```

Where `postgres_username` is the username of the PostgreSQL user you wish to create the database with.
Or, if you're using a remote database:

```
psql -U postgres_username -h xxx.xxx.xxx.xxx -f setup.sql
```

Where `xxx.xxx.xxx.xxx` is the ip adress of the PostgreSQL database you want to work with.

Next, you will need to create a `database.ini` file in the root of the project, in which you will provide the required credentials for the app to connect to your database in the following format:

```
[postgresql]
host=ipadress
database=moodymusic
user=postgres_username
password=dbpass
```

Where `ipadress` is the ip address of the database you want to connect to, `dbpass` is its password, and `postgres_username` is the username.

### **_Install dependencies_**

This project is based on pipenv. This means that tracking dependencies becomes far easier compared to using a `requirements.txt` file.

In order to install the required dependencies all you need to do is navigate to the root folder and run the following command:

```
pipenv install
```

Or

```
python -m pipenv install
```

### **_Start the server_**

The next and final step is starting the server.

Before doing that, you will need to activate the project's virtualenv using the following command:

```
pipenv shell
```

Or

```
python -m pipenv shell
```

Next, start the server by running one of the following commands:

- On bash:
  ```
  $ export FLASK_APP=moodymusic
  ```
- On CMD:
  ```
  > set FLASK_APP=moodymusic
  ```
- On PowerShell:
  ````
  > $env:FLASK_APP = "moodymusic"
  	```
  And then run the command (independently from your environnement):
  ````

```
flask run
```

This will start the server on `http://localhost:5000` . Head over there to start using the app.

## **_API Documentation_**

The full documentation of the API is provided in the [moodyMusic.yaml](./moodyMusic.yaml) file.

It is written following the [OpenAPI 3.0 specification](https://swagger.io/specification/). You can render its contents in a clear interactive format using the [Swagger Viewer](https://marketplace.visualstudio.com/items?itemName=Arjun.swagger-viewer) vs code extention or using the [Swagger Editor](https://editor.swagger.io/) website.
