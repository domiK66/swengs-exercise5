import json
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
# Note: Django in general allows the exchange 
# of its standard user model through your own. 
# The "get_user_model" function is a helper function 
# that returns the user model class defined in your 
# project settings. Even if you do not change 
# the user model, it is generally better to use 
# the get_user_model function, as it is much more 
# generic. 
# Equivalent: from django.contrib.auth.models import User

from . import models

class GenreViewSet(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, format = None):
        if request.GET.get("name") is None:
            queryset = models.Genre.objects.all()
        else:
            queryset = models.Genre.objects.filter(name=request.GET.get("name"))

        # Django Model manager's have not only a .filter method, but also 
        # an order_by method - 
        # see https://docs.djangoproject.com/en/3.2/ref/models/querysets/#django.db.models.query.QuerySet.order_by
        # for more details: 
        # The given API should be changed in a way that following calls should be possible:
        # GET /genres/?order_by=name
        # GET /genres/?order_by=name uses ascending order
        # GET /genres/?order_by=-name uses descending order
        # The GET parameter order_by should be optional, thus
        # whereas "name" represents the field name that should by which the list should be ordered.
        # GET /genres/ should be still possible
        # Note: tested by test_list_genres_order_by_desc and test_list_genres_order_by_asc in tests.py
        # your code here
        if request.GET.get("order_by") is not None:
            queryset = queryset.order_by(request.GET.get("order_by"))
        # your code here
        return Response(
            [(genre.pk, genre.name) for genre in queryset],
            status = 200
        )

    def create(self ,request, format = None):
        # request.data contains a dictionary 
        # looking like this:
        # {"name":"Scifi"}
        # The code does not check, if dictionary key 
        # "name" really exists. Change the code in a way, 
        # that if the key DOES NOT EXIST, a HTTP response 
        # with status 400 (BAD REQUEST) is returned.
        # tests.py->test_create_thriller_genre_empty_payload is the 
        # test that should pass, after this has been changed.
        # your code here
        if not("name" in request.data):
            return Response(
                {"error": "No name given."},
                status = 400
            )
        # your code here
        genre = models.Genre.objects.create(name = request.data["name"])
        return Response(
            {"name": genre.name, "id": genre.pk},
            status = 201
        ) 

    def retrieve(self, request, pk=None, format=None):
        try:
            genre = models.Genre.objects.get(pk = pk)
            return Response(
                {"name": genre.name,"pk": genre.pk},
                status = 200
            )
        except models.Genre.DoesNotExist:
            return Response(
                status = 404
            )
        

    def update(self, request, pk=None, format=None):
        try:
            genre = models.Genre.objects.get(
                pk = pk
            )
            # TODO: same as in method "create"
            # make this more robust
            # your code here
            if not("name" in request.data):
                return Response(
                    status = 400
                )
            # your code here
            genre.name = request.data["name"]
            genre.save()
            return Response(
                {"name": genre.name,"pk": genre.pk},
                status = 200                
            )
        except models.Genre.DoesNotExist:
            return Response(
                status = 404
            )

    def partial_update(self, request, pk=None, format=None):
        # We do not allow partial updates here
        # So we return a 405 instead.
        return Response( 
            status= 405
        )

    def destroy(self, request, pk=None, format=None):
        # first check, if the genre with the given 
        # primary key really exists. If not, return a 
        # response with status code 404 (Not found).
        
        # 2: Check the currently logged in user, 
        # and change it in a way that only superusers 
        # are able to delete genres. If the currently logged in 
        # user is not a superuser, return a HTTP 403 (FORBIDDEN)
        # response
        # Note: test covered by YamodGenreAPITest.test_delete_not_existing_genre
        # your code here
        try:
            models.Genre.objects.get(pk = pk)
        except models.Genre.DoesNotExist:
            return Response(
                status = 404
            )
        if not(request.user.is_superuser):
            return Response(
                status = 403
            )
        # your code here
        genre = models.Genre.objects.filter(
            pk = pk
        ).delete()
        return Response(
            status=204
        )







