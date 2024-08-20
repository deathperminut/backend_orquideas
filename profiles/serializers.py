# your_app_name/serializers.py

from rest_framework import serializers
from .models import UserProfile, Institution, Role
from modules.models import UserModule


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'role',
            'is_active',
        ]


class ProfileUserModuleSerializer(serializers.ModelSerializer):
    module_name = serializers.CharField(
        source='activity_module_master.training_module.module_name',
        read_only=True,
    )
    endpoint = serializers.HyperlinkedIdentityField(
        view_name='usermodule-detail', lookup_field='pk'
    )

    class Meta:
        model = UserModule
        fields = [
            'module_name',
            'endpoint',
        ]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    usermodule_set = ProfileUserModuleSerializer(many=True, read_only=True)
    institutions = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'role',
            'password',
            'is_active',
            'institutions',
            'usermodule_set',
        ]

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ['id', 'name', 'allowed_modules', 'users']


class RoleSelializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description']
