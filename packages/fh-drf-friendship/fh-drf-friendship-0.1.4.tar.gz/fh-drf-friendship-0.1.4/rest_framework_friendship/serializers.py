from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import module_loading
from friendship.exceptions import AlreadyFriendsError
from friendship.models import Friend, FriendshipRequest
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import rest_framework_common.validators

User = get_user_model()
UserListSerializer = module_loading.import_string(settings.DRF_FRIENDSHIP['USER_LIST_SERIALIZER'])


class FriendshipRequestReadSerializer(rest_framework_common.serializers.ModelSerializer):
    from_user = UserListSerializer()
    to_user = UserListSerializer()
    created_at = serializers.DateTimeField(source='created')

    class Meta:
        model = FriendshipRequest
        exclude = ('url', 'message', 'viewed', 'rejected', 'created',)


class FriendshipRequestSerializer(rest_framework_common.serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(source='to_user', queryset=User.objects.all())

    class Meta:
        model = FriendshipRequest
        exclude = ('url', 'to_user',)

    def create(self, validated_data):
        try:
            return Friend.objects.add_friend(**validated_data)
        except AlreadyFriendsError as e:
            raise serializers.ValidationError(e.message)


class FriendSerializer(rest_framework_common.serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(source='from_user', queryset=User.objects.all())

    class Meta:
        model = Friend
        exclude = ('url', 'from_user',)

    def create(self, validated_data):
        fr = FriendshipRequest.objects.get(from_user=validated_data['from_user'], to_user=validated_data['to_user'])

        if fr and fr.accept():
            return Friend.objects.get(from_user=validated_data['from_user'], to_user=validated_data['to_user'])

    def is_valid(self, raise_exception=False):
        is_valid = super(FriendSerializer, self).is_valid(raise_exception=raise_exception)

        if not is_valid:
            return is_valid
        else:
            try:
                FriendshipRequest.objects.get(from_user=self._validated_data['from_user'],
                                              to_user=self._validated_data['to_user'])
                is_valid = True
            except FriendshipRequest.DoesNotExist:
                self._errors = {'friendship_request': 'not_found'}
                is_valid = False

            if raise_exception and not is_valid:
                raise ValidationError(self.errors)

            return is_valid


class FriendReadSerializer(rest_framework_common.serializers.ModelSerializer):
    user = UserListSerializer(source='from_user')
    created_at = serializers.DateTimeField(source='created')

    class Meta:
        model = Friend
        exclude = ('url', 'from_user', 'to_user', 'created',)
