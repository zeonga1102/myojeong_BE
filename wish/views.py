from random import randrange
from uuid import uuid4

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from myojeong_be.const import emoji_list
from wish.serializers import WishSerializer


class WishView(APIView):
    def get(self, request):
        pass

    def post(self, request):
        data = request.data.copy()

        emoji = emoji_list(randrange(10)[0])
        data['emoji'] = emoji

        if not data.get('is_open'):
            password = uuid4().hex
            data['password'] = password

        wish_serializer = WishSerializer(data=data)
        if wish_serializer.is_valid():
            saved_data = wish_serializer.save()
            response = saved_data.__dict__
            response['is_myself'] = True if saved_data.to_name else False
            response['to_name'] = saved_data.to_name if saved_data.to_name else ''
            response['password'] = password if saved_data.password else ''

            return Response(response, status=status.HTTP_200_OK)
        
        return Response(wish_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WishListView(APIView):
    def get(self, request):
        pass


class WishLikeView(APIView):
    def post(self, request):
        pass

