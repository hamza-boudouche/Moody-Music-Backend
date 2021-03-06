# **Moody-Music-Backend**

## **_Description_**

Moody Music is an AI powered music player based on Spotify embeds and mood detection using deep learning.

Moody Music changes the way we listen and perceive music. As a user, you will no longer have to interact with the music player in the traditionnal way, looking up playlists by name and picking music manually. All you have to do is give the app access to your webcame and let it do its magic.

Using deep learning algorithms, the system will automatically recognize your mood and based on that it will give you suggestions of playlists that are compatible with your current mood.

## **_Demo_**

The project is not yet publicly hosted. If you want to test it you will have to set it up locally.

## **_Setup_**

### **_Requirements_**

In order to to setup this project and run it locally you need to have [`docker`](https://docs.docker.com/get-docker/) installed on your machine.

All you need to do is change your working directory to the root of the project, and the following command:

```
docker-compose up
```

This will start the server on `http://localhost:5000` . Head over there to start using the app.

To shut down the server, run the following command:

```
docker-compose down
```

To apply the changes you made, shut down the server and execute the following command:

```
docker-compose build
```

And then turn it back on using the first command.

## **_API Documentation_**

The full documentation of the API is provided in the [moodyMusic.yaml](./moodyMusic.yaml) file and can be viewed using Github pages [here](https://hamza-boudouche.github.io/Moody-Music-Backend/).

It is written following the [OpenAPI 3.0 specification](https://swagger.io/specification/). You can render its contents in a clear interactive format using the [Swagger Viewer](https://marketplace.visualstudio.com/items?itemName=Arjun.swagger-viewer) vs code extention or using the [Swagger Editor](https://editor.swagger.io/) website.
