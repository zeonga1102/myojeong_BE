from uuid import uuid4
from hashlib import sha256

from django.db.models import Q, F
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from myojeong_be.const import LIST_LMIT
from wish.serializers import WishSerializer, WishListSerializer
from wish.models import Wish
from wish.enum import SortedType, SpType


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

        if not data.get('to_name'):
            data['to_name'] = None

        if data.get('is_open', True):
            password = None
        else:
            password = uuid4().hex
            data['password'] = password

        wish_serializer = WishSerializer(data=data)
        if wish_serializer.is_valid():
            saved_data = wish_serializer.save()

            response = {
                'id': saved_data.id,
                'from_name': data['from_name'],
                'to_name': data['to_name'],
                'content': data['content'],
                'emoji': saved_data.emoji,
                'password': password if password else '',
                'is_myself': False if data['to_name'] else True
            }

            return Response(response, status=status.HTTP_200_OK)
        
        return Response(wish_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WishListView(APIView):
    def get(self, request):
        sorted_type = SortedType.get_sorted_type(request.GET.get('sorted', 'recent'))
        if not sorted_type:
            return Response({'msg': '잘못된 정렬 기준입니다!'}, status=status.HTTP_400_BAD_REQUEST)
        
        page = int(request.GET.get('page', 1))
        start = (page - 1) * LIST_LMIT
        last = page * LIST_LMIT

        keyword = request.GET.get('keyword')

        query = Q(is_open=True)
        if keyword:
            query = query & Q(from_name__istartswith=keyword)
        wish_list = Wish.objects.filter(query).order_by(sorted_type.value)[start:last]
        
        serialized_wish_list_data = WishListSerializer(wish_list, many=True).data
        
        return Response({'wish_list': serialized_wish_list_data}, status=status.HTTP_200_OK)


class WishLikeView(APIView):
    def post(self, request):
        data = request.data.copy()

        wish_id = data.get('id')
        sp_type = SpType.get_sp_type(data.get('songpyeon'))
        if not sp_type:
            return Response({'msg': '잘못된 송편입니다!'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            wish_item = Wish.objects.get(id=wish_id)
        except Wish.DoesNotExist:
            return Response({'msg': '존재하지 않는 소원입니다!'}, status=status.HTTP_400_BAD_REQUEST)
        
        setattr(wish_item, sp_type.value, F(sp_type.value) + 1)
        wish_item.sp_sum = F('sp_sum') + 1

        wish_item.save()

        response = {
            'id': wish_item.id,
            'success': True
        }
        
        return Response(response, status=status.HTTP_200_OK)
    

class WishCountView(APIView):
    def get(self, request):
        wish_count = Wish.objects.all().count()
        return Response({'count': wish_count}, status=status.HTTP_200_OK)

