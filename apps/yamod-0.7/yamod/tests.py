import datetime
import json

from django.test import Client
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db.utils import IntegrityError
from django.test import TestCase

from rest_framework.test import APIClient

from . import models

class YamodBaseTest(TestCase):

    def setUp(self):
        self.genres=["Action","Horror","Scifi","Drama","Comedy"]
        self.movies = [
            ("Blade Runner", datetime.date(year=1982,month=6,day=25),"Scifi",100),
            ("Blade Runner 2049", datetime.date(year=2017,month=10,day=6),"Scifi",150),
            ("Nomadland", datetime.date(year=2020,month=9,day=11),"Drama",110),
            ("The French Dispatch", datetime.date(year=2021,month=7,day=12),"Comedy",100),
            ("Rushmoore", datetime.date(year=1998,month=9,day=17),"Comedy",95)
        ]
        # Setup database
        # Next line has been adapted in contrast to version 0.5
        # (replace models.Genre.objects.create by models.Genre.objects.get_or_create)
        [models.Genre.objects.get_or_create(name=name) for name in self.genres]
        [models.RoleType.objects.create(name=name) for name in ["Actor","Producer","Director"]]
        [models.Movie.objects.create(movie_title=movie_title,
                                     released=released,
                                     original_title=movie_title,
                                     runtime=runtime) for movie_title,released, genre,runtime in self.movies]    
        # Updates
        for movie_title,released, genre,runtime in self.movies:
            models.Movie.objects.get(movie_title=movie_title).genre.add(models.Genre.objects.get(name=genre))


class YamodModelTest(YamodBaseTest):

    def test_create_genre(self):
        # Create a new model instance for model "Genre" with name "Comedy"
        # YOUR CODE HERE:
        genre = models.Genre.objects.create(name="Comedy")
        # /ENDYOURCODE
        self.assertEqual(genre.name,"Comedy")

    def test_delete_genre(self):
        # YOUR CODE HERE: Delete Genre instance with name "Action"
        models.Genre.objects.filter(name="Action").delete()
        # /ENDYOURCODE
        self.assertEqual(models.Genre.objects.count(),4)

    def test_filter_movie_by_year(self):
        # Filter all movies, that were released after 2000 (store results of query in variable movies_2000)
        # YOUR CODE HERE:
        movies_2000 = models.Movie.objects.filter(released__year__gte=2000)
        # /ENDYOURCODE        
        self.assertEqual(movies_2000.count(),3)

    def test_filter_movie_by_runtime(self):
        # Filter all movies with a runtime <= 100 (FIXED: runtime < 100)
        # YOUR CODE HERE:
        movies_90 = models.Movie.objects.filter(runtime__lte=100)
        # /ENDYOURCODE
        self.assertEqual(movies_90.count(),3)

    def test_filter_movie_starting_with_b(self):
        # Filter all movies that start with letter B
        # YOUR CODE HERE:
        movies_with_b = models.Movie.objects.filter(movie_title__startswith="B")
        # /ENDYOURCODE
        self.assertEqual(movies_with_b.count(),2)

    def test_filter_movie_containing_blade(self):
        # Filter all movies that contain "Blade" in its title
        # YOUR CODE HERE:
        movies_containing_blade = models.Movie.objects.filter(movie_title__contains="Blade")
        # /ENDYOURCODE
        self.assertEqual(movies_containing_blade.count(),2)

    def test_genre_to_str(self):        
        # Implement the __str__ method of model class Genre and Movie
        # Genre should return the name and Movie should return the movie_title
        # (Implementation is done in models.py)
        for movie_title,released,genre,runtime in self.movies:
            self.assertEqual(str(models.Movie.objects.get(movie_title=movie_title)),movie_title)


    def test_update_role_type(self):
        # Load the model instance "Actor" of model "RoleType"
        # and update the name of the RoleType to "Actor/Actress"
        # YOUR CODE HERE:
        actor = models.RoleType.objects.get(name="Actor")
        actor.name="Actor/Actress"
        actor.save()
        # /ENDYOURCODE
        self.assertEqual(models.RoleType.objects.filter(name="Actor/Actress").count(),1)

    def test_get_or_create_role_type(self):
        # The following call results in an error, as a role type "Producer"
        # already exists. Modify the "create" method accordingly, so this 
        # test can pass
        # MODIFY CODE HERE
        models.RoleType.objects.get_or_create(name="Producer")
        # /ENDYOURCODE
        self.assertEqual(models.RoleType.objects.count(),3)
        len(models.RoleType.objects.all())
        models.RoleType.objects.count()
        self.assertEqual(models.RoleType.objects.filter(name="Producer").count(),1)

class ExtendedQueryTests(YamodBaseTest):

    def test_and_query(self):
        # Filter all movies where the name starts with a B
        # AND that were released after 1980
        # YOUR CODE HERE:
        movies_with_b_after_1980 = models.Movie.objects.filter(movie_title__startswith="B",
                                                               released__year__gt=1980)
        # /ENDYOURCODE
        self.assertEqual(movies_with_b_after_1980.count(),2)

    def test_or_query(self):
        # Filter all movies that were released after 2020 OR have genre comedy
        # YOUR CODE HERE:
        movies = models.Movie.objects.filter(Q(released__year__gt=2020) | Q(genre__name="Comedy") )
        # /ENDYOURCODE
        self.assertEqual(movies.count(),2)

    def test_filter_relation(self):
        # Filter all movies where the genre ends with character "y"
        # YOUR CODE HERE:
        results = models.Movie.objects.filter(genre__name__endswith="y")
        # /ENDYOURCODE
        self.assertEquals(results.count(),2)

    def test_add_persons_to_movie(self):
        # Go to Wikipedia and select (a) the director and (b) 
        # the lead actor of "Blade runner 2049".
        # Create two person model instances and add them to the 
        # movie "Blade runner 2049"
        #
        # Note: the model class "Person" has a many-to-many relation 
        # with model class "Movie"; Unlike the many-to-many relation 
        # Movie --> Genre, it uses an intermediate relation "Role".
        # The reason is: we need to provide more information on what
        # a person has actually done in a movie which is expressed through
        # the intermediate model "Role" - the intermediate role is provided 
        # through the "through" argument in
        #
        # participates_in = models.ManyToManyField(Movie,through="Role")
        #
        # In this case, you cannot use the person.participates_in.add method 
        # as we have seen on the slides in the genre case. You have to create 
        # the model instances using their respective .objects.create method.
        #
        # YOUR CODE HERE:
        director = models.Person.objects.create(credited_name="Denis Villeneuve",
                                                year_of_birth=1967,
                                                gender="m")
        lead_actor = models.Person.objects.create(credited_name="Ryan Gosling",
                                                  year_of_birth=1980,
                                                  gender="m")
        
     
        models.Role.objects.create(
            person=director,
            role=models.RoleType.objects.get(name="Director"),
            movie=models.Movie.objects.get(movie_title="Blade Runner 2049")
        )
        models.Role.objects.create(
            person=lead_actor,
            role=models.RoleType.objects.get(name="Actor"),
            movie=models.Movie.objects.get(movie_title="Blade Runner 2049")
        ) 
        # /ENDYOURCODE      
        self.assertEqual(director.participates_in.all().count(),1)
        self.assertEqual(lead_actor.participates_in.all().count(),1)

class MigrationTests(YamodBaseTest):
    '''
    The goal of these tests, is to practice the use of the migrations 
    concept of Django. 
    
    Extend the data model of models.py to include the concept of 
    TV shows. The data model should at least provide models for 

    - TV shows (should have at least a title and a release date)
    - Seasons (should provide the possibility to add a regular cast referencing the Person model)
    - Episodes (should have at least a title and a length in minutes)

    and appropriate relations between them. Develop iterativley, 
    thus extend the data model one by one (always running 
    migrations between them) and implement the following test. 

    You can add further relations (e.g. tv shows and seasons 
    might have a link to genres) as you see fit.

    Optional: try to write a custom data migration (see slides)
    that populates the development databases with following pre-defined 
    list of genres:

    ["Action","Horror","Scifi","Drama","Comedy"]    

    Optional: add custom django admin classes for the newly generated 
    models TV shows, seasons and episodes.

    '''

    def _create_tv_show(self):
        created_by = models.Person.objects.create(
            credited_name="David S. Goyer",
            gender="m",
            year_of_birth=1965
        )
        return models.TVShow.objects.create(
            name="Foundation",
            released_year=2021,
            created_by=created_by
        )

    def test_tv_show(self):
        '''
        Go to models.py and create a new model "TVShow". 
        Write appropriate tests that show case how a new 
        model instance ist created, updated and deleted.
        '''
        tv_show = self._create_tv_show()
        self.assertEqual(tv_show.name,"Foundation")

    def test_tv_show_season(self):
        '''
        Go to models.py and create a new model "Season".
        Write appropriate tests that show case how a new 
        model instance ist created, updated and deleted.        
        '''
        tv_show = self._create_tv_show()
        season = models.Season.objects.create(season_no=1,tv_show=tv_show)
        actor = models.Person.objects.create(credited_name="Ryan Gosling",
                                                  year_of_birth=1980,
                                                  gender="m")        
        season.cast.add(actor)
        self.assertEqual(season.cast.all().count(),1)
        # or (shorter):
        self.assertEqual(season.cast.count(),1)
        # try to create the same season again, this should fail due to 
        # the unique constraint
        with self.assertRaises(IntegrityError):
            models.Season.objects.create(season_no=1,tv_show=tv_show)
        # Season tv show name should be "Foundation"
        self.assertEquals(season.tv_show.name,"Foundation")

    def test_tv_show_episode(self):
        '''
        Go to models.py and create a new model "Episode".
        Write appropriate tests that show case how a new 
        model instance ist created, updated and deleted.        
        '''
        tv_show = self._create_tv_show()
        season_1 = models.Season.objects.create(season_no=1,tv_show=tv_show)
        season_2 = models.Season.objects.create(season_no=2,tv_show=tv_show)
        e1 = models.Episode.objects.create(
            name="The Emperor's Peace",
            season=season_1
        )

class YamodGenreAPITest(YamodBaseTest):

    def get_token(self,is_superuser=False):
        password="api_user"
        # Create us an API user:
        api_user , created = get_user_model().objects.get_or_create(
            username="api_user",
            is_active=True,
            is_superuser=is_superuser
        )
        api_user.set_password(password)
        api_user.save()
        # Now, request a token for this user:
        # for more details
        client = APIClient()
        # Provide credentials
        response = client.post("/api-token-auth/",{"username":"api_user","password":password})
        # Assure, we get a valid response
        self.assertEqual(response.status_code,200)
        # Extract token.
        return response.json().get("token")

    def test_list_genres(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="JWT %s" % self.get_token())
        response = client.get("/genres/")
        # We expect 5 entries in the genre list:
        self.assertEqual(len(response.json()),5)

    def test_list_genres_order_by_desc(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="JWT %s" % self.get_token())
        response = client.get("/genres/?order_by=-name")
        # We expect 5 entries in the genre list:
        results = response.json()
        self.assertEqual(results[0][1],"Scifi")   
        self.assertEqual(results[1][1],"Horror")
        self.assertEqual(results[2][1],"Drama")
        self.assertEqual(results[3][1],"Comedy")
        self.assertEqual(results[4][1],"Action")

    def test_list_genres_order_by_asc(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="JWT %s" % self.get_token())
        response = client.get("/genres/?order_by=name")
        # We expect 5 entries in the genre list:
        results = response.json()
        self.assertEqual(results[0][1],"Action")   
        self.assertEqual(results[1][1],"Comedy")
        self.assertEqual(results[2][1],"Drama")
        self.assertEqual(results[3][1],"Horror")
        self.assertEqual(results[4][1],"Scifi")

    def test_create_thriller_genre(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="JWT %s" % self.get_token())
        response = client.post("/genres/",{"name":"Thriller"})
        self.assertEquals(response.status_code,201)

    def test_create_thriller_genre_empty_payload(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="JWT %s" % self.get_token())
        response = client.post("/genres/",{})
        self.assertEquals(response.status_code,400)        

    def test_update_thriller_genre_empty_payload(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="JWT %s" % self.get_token())
        # Create thriller genre
        client.post("/genres/",{"name":"Thriller"})
        # Filter genre with that name
        response = client.get("/genres/?name=Thriller")
        results = response.json()
        # Now update with empty representation        
        response = client.put("/genres/%s/" % results[0][0] , {})
        # Should result in a HTTP 400 Bad request
        self.assertEquals(response.status_code,400)

    def test_update_thriller_genre(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="JWT %s" % self.get_token())
        # Create thriller genre
        client.post("/genres/",{"name":"Thriller"})
        # Filter genre with that name
        response = client.get("/genres/?name=Thriller")
        results = response.json()
        # Update result and change name to "Scifi/Thriller"
        # (Extract id/pk from object from the result of the previous API call)
        client.put("/genres/%s/" % results[0][0],{"name":"Scifi/Thriller"})
        self.assertEqual(response.status_code,200)  
        # For tests, retrieve the genre again via the API
        response = client.get("/genres/%s/" % results[0][0])  
        self.assertEqual(response.json().get("name"),"Scifi/Thriller")

    def test_delete_not_existing_genre(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="JWT %s" % self.get_token())
        response = client.delete("/genres/23746/")
        self.assertEquals(response.status_code,404)             

    def test_delete_thriller_genre(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="JWT %s" % self.get_token(is_superuser=True))
        # Create thriller genre
        response = client.post("/genres/",{"name":"Thriller"})
        thriller_id = response.json().get("id")      
        response = client.delete("/genres/%s/" % thriller_id)
        self.assertEqual(response.status_code,204)
        # try to load it again, should result in a 404 error
        response = client.get("/genres/%s/" % thriller_id)
        self.assertEqual(response.status_code,404)

    def test_delete_thriller_genre_not_authorized(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="JWT %s" % self.get_token(is_superuser=False))
        # Create thriller genre
        response = client.post("/genres/",{"name":"Thriller"})
        thriller_id = response.json().get("id")      
        response = client.delete("/genres/%s/" % thriller_id)
        # We expect a HTTP code 403 (FORBIDDEN) as we are not a superuser:
        self.assertEqual(response.status_code,403)                  
