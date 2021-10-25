# Casting Agency

Site live at : [afternoon-earth-48253.herokuapp.com](https://afternoon-earth-48253.herokuapp.com/)

This project is my capstone project for Udacity's Fullstack Nanodegree program.
It models a company that is responsible for creating movies and managing and assigning actors to those movies.
Authorized users can interact with the API to view,add,update,delete Movies and Actors details.

## API

In order to use the API users need to be authenticated. Jwt tokens can be generated by logging in with the provided credentials on the hosted site.

### Endpoints

#### GET /movies

- General:

  - Returns all the movies.
  - Roles authorized : Casting Assistant,Casting Director,Executive Producer.

- Sample: `curl http://127.0.0.1:5000/movies`

```json
{
  "movies": [
    {
      "id": 1,
      "release_date": "2020-7-19",
      "title": "Justice League Dark",
      "discription": "https://en.wikipedia.org/wiki/Justice_League_Dark:_Apokolips_War"
    },
    {
      "id": 2,
      "release_date": "2020-9-1",
      "title": "Soul",
      "discription": "https://en.wikipedia.org/wiki/Soul_(2020_film)"
    }
    ......
  ],
  "success": true
}
```

#### GET /movies/\<int:id\>

- General:

  - Route for getting a specific movie.
  - Roles authorized : Casting Assistant,Casting Director,Executive Producer.

- Sample: `curl http://127.0.0.1:5000/movies/1`

```json
{
  "movie": {
      "release_date": "2020-7-19",
      "title": "Justice League Dark",
      "discription": "https://en.wikipedia.org/wiki/Justice_League_Dark:_Apokolips_War"
  },
  "success": true
}
```

#### POST /movies

- General:

  - Creates a new movie based on a payload.
  - Roles authorized : Executive Producer.

- Sample: `curl http://127.0.0.1:5000/movies -X POST -H "Content-Type: application/json" -d '{ "title": "Natasha romanov", "release_date": "2020-05-06" }'`

```json
{
  "movie": {
    "id": 3,
      "release_date": "2020-7-19",
      "title": "Justice League Dark",
      "discription": "https://en.wikipedia.org/wiki/Justice_League_Dark:_Apokolips_War"
  },
  "success": true
}
```

#### PATCH /movies/\<int:id\>

- General:

  - Patches a movie based on a payload.
  - Roles authorized : Casting Director, Executive Producer.

- Sample: `curl http://127.0.0.1:5000/movies/3 -X POST -H "Content-Type: application/json" -d '{ "title": "Natasha romanov patched", "release_date": "2020-05-06" }'`

```json
{
  "movie": {
    "id": 3,
      "release_date": "2020-7-19",
      "title": "Justice League Dark",
      "discription": "https://en.wikipedia.org/wiki/Justice_League_Dark:_Apokolips_War"
  },
  "success": true
}
```

#### DELETE /movies/<int:id\>

- General:

  - Deletes a movies by id form the url parameter.
  - Roles authorized : Executive Producer.

- Sample: `curl http://127.0.0.1:5000/movies/3 -X DELETE`

```json
{
  "message": "movie id 3, titled Natasha romanov patched was deleted",
  "success": true
}
```

#### GET /actors

- General:

  - Returns all the actors.
  - Roles authorized : Casting Assistant,Casting Director,Executive Producer.

- Sample: `curl http://127.0.0.1:5000/actors`

```json
{
  "actors": [
    {
      "id": 1,
      "name": "Will Smith"
    },
    {
      "id": 2,
      "name": "Bruce Wills"
    }
    ......
  ],
  "success": true
}
```

#### GET /actors/\<int:id\>

- General:

  - Route for getting a specific actor.
  - Roles authorized : Casting Assistant,Casting Director,Executive Producer.

- Sample: `curl http://127.0.0.1:5000/actors/1`

```json
{
  "actor": {
    "id": 1,
    "name": "Will Smith"
  },
  "success": true
}
```

#### POST /actors

- General:

  - Creates a new actor based on a payload.
  - Roles authorized : Casting Director,Executive Producer.

- Sample: `curl http://127.0.0.1:5000/actors -X POST -H "Content-Type: application/json" -d '{ "name": "Mary", "age": 22, "gender": "female" }'`

```json
{
  "actor": {
    "id": 3,
    "name": "Mary"
  },
  "success": true
}
```

#### PATCH /actors/\<int:id\>

- General:

  - Patches an actor based on a payload.
  - Roles authorized : Casting Director, Executive Producer.

- Sample: `curl http://127.0.0.1:5000/actors/3 -X POST -H "Content-Type: application/json" -d '{ "name": "John"}'`

```json
{
    
    "id": 3,
    "name": "John"
  },
  {
  "success": true
}
```

#### DELETE /actors/<int:id\>

- General:

  - Deletes an actor by id form the url parameter.
  - Roles authorized : Casting Director,Executive Producer.

- Sample: `curl http://127.0.0.1:5000/actors/3 -X DELETE`

```json
{
  "delete": "3",
  "success": true
}
```

## Project dependencies

## Getting Started

### Installing Dependencies

#### Python 3.9

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

To setup vurtual environment run the following command

```bash
pipenv shell
```

#### Installing Dependencies

```bash
pipenv install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Database Setup

The project uses Postgresql as its database, you would need to create one locally and reflect it in setup.sh.
To update the database and seed run the following :

```bash
python manage.py db upgrade
python manage.py seed
```

- you may need to change the database url in setup.sh after which you can run

```bash
source setup.sh
```

- Start server by running

```bash
flask run
```

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

- [Pycodestyle](https://pypi.org/project/pycodestyle/) - pycodestyle is a tool to check your Python code against some of the style conventions in PEP 8.

## Testing

Replace the jwt tokens in app_test.py with the ones generated on the website.

For testing locally, we need to reset database.


### Error Handling

- 401 errors due to RBAC are returned as

```json
{
  "code": "unauthorized",
  "description": "Permission not found."
}
```

Other Errors are returned in the following json format:

```json
{
  "success": "False",
  "error": 422,
  "message": "Unprocessable entity"
}
```

The error codes currently returned are:

- 400 – bad request
- 401 – unauthorized
- 404 – resource not found
- 422 – unprocessable
- 500 – internal server error
