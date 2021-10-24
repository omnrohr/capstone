import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Movie, Actor, setup_db


MANAGER_TOKEN = os.environ.get('MANAGER_TOKEN', 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1KUnctNEpnWEw5V253bU1HN2FrdSJ9.eyJpc3MiOiJodHRwczovL2Rldi11aXc1MXJ4OC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE1YmU4ZWRmZTM5YmIwMDY5MjA2NzRiIiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo1MDAwIiwiaWF0IjoxNjM1MDkyMzcxLCJleHAiOjE2MzUwOTk1NzEsImF6cCI6IldVbTY2bHExSmtqTnlHZVNLeXZvendHYWlpMXRlNVZKIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJlZGl0OmFsbF9kYXRhIiwicmVhZDphbGxfZGF0YSJdfQ.SVZqZ95B3lwkHdClqpRf2fDsrtOGt36jzC8eo21aFa56I0ADODsIx-AYtwCunMY3j8fW8982vIx-SxXVY5kl3BELKVh-AKPgFfyQ7rEOJS2baAQBxqrstdxx44TRsasatlHY2Ssk_oV-kand5kRHs6p9o0dc62QKKirIx2P-lnqFY3whMBQoPmwpAYHu8p5U6xAvgXaOm3pJ4qRpN-KW5ySAJMhXPy66TZHj_PIdTiQ1wup684Eskd0AKfutITTvXQrllv8a5zctI0_0HX7RnPTfFK2jYbN93Msm9FHzmIvchLERq1qpTnliV-WUa_F51vCOfV0Ub5baXWPmkMQ6Sg')
USER_TOKEN = os.environ.get('USER_TOKEN', 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1KUnctNEpnWEw5V253bU1HN2FrdSJ9.eyJpc3MiOiJodHRwczovL2Rldi11aXc1MXJ4OC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE1YzE2NmVjYWMzN2YwMDY4NDU4MDI0IiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo1MDAwIiwiaWF0IjoxNjM1MDkyNDk3LCJleHAiOjE2MzUwOTk2OTcsImF6cCI6IldVbTY2bHExSmtqTnlHZVNLeXZvendHYWlpMXRlNVZKIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJyZWFkOmFsbF9kYXRhIl19.p2Nf-oJo_dcPQ1NboUX1YW2fmQtEkDrD4pEgcx6RmaKmIVYOFAhAkKII57GrDGqPQFocWFfT2UbX5N2veiz8EeEuoSWW4Zwf2bAfn34e0yoRUfdrdRHEuKG5dsLV3Fbt9BBPF21604BB7vgJZJtXaBuvGWUKWL0et33NATdGqa2oQs81DuYkkvQI4lEMp_HzLPfgYcooHi-sZxZ7TVpfqhXno38xe8hlygm5GUNDBPV1qNgSBd0vppI9xaO1cPsrlGY1vyQpIfXU-LYGnwTsAFxwP8B5x_2_dKrrIcjolE4C3cmSHUteE7TvDwztYx_Hc6sDYqKC5TSar9uej42OXw')


class CastingAgencyTestCase(unittest.TestCase):

    # this function to add some values to the test database

    def insert_data(self):
        """Insert test database with initial data"""

        actor1 = Actor(name='Matt Ryan')
        actor2 = Actor(name='Jerry O\'Connell')
        actor3 = Actor(name=' Jamie Foxx')
        actor4 = Actor(name='Vishwak Sen')

        movie1 = Movie(title='Justice League Dark', release_date='2020-7-19',
                       description='https://en.wikipedia.org/wiki/Justice_League_Dark:_Apokolips_War')
        movie2 = Movie(title='Soul', release_date='2020-9-1',
                       description='https://en.wikipedia.org/wiki/Soul_(2020_film)')
        movie3 = Movie(title='The Three', release_date='2020-02-28',
                       description='https://en.wikipedia.org/wiki/Vishwak_Sen')

        movie1.actors.append(actor1)
        movie1.actors.append(actor2)
        movie2.actors.append(actor3)
        movie3.actors.append(actor4)

        self.db.session.add(actor1)
        self.db.session.add(actor2)
        self.db.session.add(actor3)
        self.db.session.add(actor4)

        self.db.session.add(movie1)
        self.db.session.add(movie2)
        self.db.session.add(movie3)
        self.db.session.commit()
        self.db.session.close()

# ---------------------------------------------------------------------------------
# SETUP TESTS
# ---------------------------------------------------------------------------------

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        self.manager_header = {
            "Authorization": "Bearer {}".format(MANAGER_TOKEN)}
        self.user_header = {
            "Authorization": "Bearer {}".format(USER_TOKEN)}

        self.client = self.app.test_client
        self.DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
        self.DB_USER = os.getenv('DB_USER', 'admin')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', 'Opadah12')
        self.DB_NAME = os.getenv('DB_NAME', 'casting_agency')
        self.DB_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
            self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_NAME)
        setup_db(self.app, self.DB_PATH)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.drop_all()
            self.db.create_all()
            self.insert_data()

    def tearDown(self):
        """Runs cleanup after each test"""
        pass

# ---------------------------------------------------------------------------------
# MOVIES
# ---------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------
    # Without headers

    def test_get_movies_with_NO_HEADERS(self):
        res = self.client().get('/movies')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['message'], 'authorization_header_missing')

    def test_post_movies_with_NO_HEADERS(self):
        res = self.client().post('/movies', json={
            'title': 'Added movie',
            'release_date': '2020-7-19'
        })

        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['message'], 'authorization_header_missing')

    def test_patch_movies_with_NO_HEADERS(self):
        res = self.client().patch('/movies/4', json={
            'title': 'edited movie',
            'release_date': '2020-7-19'
        })

        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['message'], 'authorization_header_missing')

    def test_delete_movies_with_NO_HEADERS(self):
        res = self.client().delete('/movies/4')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['message'], 'authorization_header_missing')

    # -----------------------------------------------------------------------------
    # Test Manager header role
    # -----------------------------------------------------------------------------

    def test_get_movies(self):
        res = self.client().get(
            '/movies', headers=self.manager_header)

        body = json.loads(res.data)
        movies = body['movies']

        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(movies, list), True)

    def test_post_movies(self):
        res = self.client().post('/movies', headers=self.manager_header, json={
            'title': 'The Movie 4',
            'release_date': '2020-7-19'
        })

        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_patch_movies(self):
        res = self.client().patch('/movies/2', headers=self.manager_header, json={
            'title': 'The Movie 4',
            'release_date': '2020-7-19'
        })
        body = json.loads(res.data)
        movies = body['movies']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(movies, list), True)

    def test_delete_movies(self):
        res = self.client().delete('/movies/2', headers=self.manager_header)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    # -----------------------------------------------------------------------------
    # Test user header role
    # -----------------------------------------------------------------------------

    def test_get_movies(self):
        res = self.client().get(
            '/movies', headers=self.user_header)

        body = json.loads(res.data)
        movies = body['movies']

        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(movies, list), True)

    def test_post_movies(self):
        """ FAILS: 403 - Forbidden """
        res = self.client().post('/movies', headers=self.user_header, json={
            'title': 'The Movie 4',
            'release_date': '2020-7-19',
            'description': 'test description'
        })

        self.assertEqual(res.status_code, 403)

    def test_patch_movies(self):
        """ FAILS: 403 - Forbidden """
        res = self.client().patch('/movies/2', headers=self.user_header, json={
            'title': 'The Movie 4',
            'release_date': '2020-7-19',
            'description': 'test description'
        })

        self.assertEqual(res.status_code, 403)

    def test_delete_movies(self):
        """ FAILS: 403 - Forbidden """
        res = self.client().delete('/movies/2', headers=self.user_header)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 403)

# ---------------------------------------------------------------------------------
# MOVIE_ACTORS
# ---------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------
    # Test Without headers

    def test_get_ators_by_movie_with_NO_HEADERS(self):
        res = self.client().get('/movies/2/actors')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['message'], 'authorization_header_missing')

    def test_assgin_ators_by_movie_with_NO_HEADERS(self):
        res = self.client().post('/movies/2/actors', json={
            'actor_id': '1'
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(body['message'], 'method not allowed')

    def test_remove_ators_by_movie_with_NO_HEADERS(self):
        res = self.client().delete('/movies/2/actors', json={
            'actor_id': '1'
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(body['message'], 'method not allowed')

    # -----------------------------------------------------------------------------
    # Test Manager header role

    def test_get_ators_by_movie(self):
        res = self.client().get(
            '/movies/2/actors', headers=self.manager_header)

        body = json.loads(res.data)
        actors = body['2']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(actors, list), True)

    # -----------------------------------------------------------------------------
    # Test user header role

    def test_get_ators_by_movie(self):
        res = self.client().get(
            '/movies/2/actors', headers=self.user_header)

        body = json.loads(res.data)
        actors = body['actors']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(actors, list), True)


# ---------------------------------------------------------------------------------
# ACTORS.
# ---------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------
    # Test Without headers


    def test_get_actors_with_NO_HEADERS(self):
        res = self.client().get('/actors')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['message'], 'authorization_header_missing')

    def test_post_actors_with_NO_HEADERS(self):
        res = self.client().post('/actors', json={
            'name': 'Test Actor1'
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(body['message'], 'method not allowed')

    def test_delete_actors_with_NO_HEADERS(self):
        res = self.client().delete('/actors/4')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['message'], 'authorization_header_missing')

    # -----------------------------------------------------------------------------
    # Test Manager header roll

    def test_get_actors(self):
        res = self.client().get(
            '/actors', headers=self.manager_header)
        body = json.loads(res.data)
        actors = body['actors']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(actors, list), True)

    def test_patch_actors(self):
        res = self.client().patch('/actors/2', headers=self.manager_header, json={
            'name': 'patch test'
        })
        body = json.loads(res.data)
        actors = body['actor']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(actors, list), True)

    def test_delete_actors(self):
        res = self.client().delete('/actors/2', headers=self.manager_header)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    # -----------------------------------------------------------------------------
    # Test user header role

    def test_get_actors(self):
        res = self.client().get(
            '/actors', headers=self.user_header)
        body = json.loads(res.data)
        actors = body['actors']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(actors, list), True)

    def test_patch_actors(self):
        """ FAILS: 403 - Forbidden """
        res = self.client().patch('/actors/2', headers=self.user_header, json={
            'name': 'test pacth name'
        })

        self.assertEqual(res.status_code, 403)

    def test_delete_actors(self):
        """ FAILS: 403 - Forbidden """
        res = self.client().delete('/actors/2', headers=self.user_header)

        self.assertEqual(res.status_code, 403)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
