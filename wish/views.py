from random import randrange
from uuid import uuid4
from hashlib import sha256

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from myojeong_be.const import emoji_list
from wish.serializers import WishSerializer
from wish.models import Wish


class WishView(APIView):
    def get(self, request):
        wish_id = request.GET.get('id')
        password = request.GET.get('password', '')

        try:
            wish_item = Wish.objects.get(id=wish_id)
        except Wish.DoesNotExist:
            return Response({'msg': '존재하지 않는 소원입니다!'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not wish_item.is_open:
            hashing = sha256()
            hashing.update(password.encode('utf-8'))

            if wish_item.password != hashing.hexdigest():
                return Response({'msg': '비밀번호가 틀립니다!'}, status=status.HTTP_400_BAD_REQUEST)
            
        serialized_wish_data = WishSerializer(wish_item).data
        return Response(serialized_wish_data, status=status.HTTP_200_OK)


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

