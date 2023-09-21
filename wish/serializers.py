from hashlib import sha256

from rest_framework import serializers

from wish.models import Wish


class WishSerializer(serializers.ModelSerializer):
    is_myself = serializers.SerializerMethodField(read_only=True)

    def get_is_myself(self, obj):
        return True if obj.to_name else False

    def validate(self, data):
        if not data.get('is_open') and data.get('password'):
            raise serializers.ValidationError(
                detail={
                    'msg': 'not valid attribute'
                }
            )        
        
        return data
    

    def create(self, validated_data):
        validated_data['sp1'] = 0
        validated_data['sp2'] = 0
        validated_data['sp3'] = 0
        validated_data['sp_sum'] = 0

        if not validated_data.get('to_name'):
            validated_data['to_name'] = None

        if not validated_data.get('password'):
            validated_data['password'] = None
        else:
            hashing = sha256()
            hashing.update(validated_data.get('password').encode('utf-8'))

            validated_data['password'] = hashing.hexdigest()

        wish = Wish(**validated_data)
        wish.save()

        return wish
    

    class Meta:
        model = Wish
        fields = [
            'from_name',
            'to_name',
            'content',
            'emoji',
            'is_open',
            'password',
            'sp1',
            'sp2',
            'sp3',
            'is_myself'
        ]

        extra_kwargs = {
            'password': { 'write_only': True },
            'sp1': { 'required': False },
            'sp2': { 'required': False },
            'sp3': { 'required': False }
        }
        