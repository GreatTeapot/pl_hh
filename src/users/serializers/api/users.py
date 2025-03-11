from crum import get_current_user
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from djoser import serializers as djoser_serializers
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegistrationSerializer(djoser_serializers.UserCreateSerializer):
    """
    User registration serializer.
    """

    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
    )

    confirm_password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
    )
    role = serializers.ChoiceField(choices=[User.Role.EMPLOYER, User.Role.EMPLOYEE])

    class Meta(djoser_serializers.UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'role', 'password', 'confirm_password')

    @staticmethod
    def validate_email(value: str) -> str:
        """Ensure email uniqueness."""
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise ParseError('A user with this email is already registered.')
        return email

    def validate(self, attrs: dict[str, str]) -> dict[str, str]:
        """Validate that passwords match and meet security requirements."""
        password = attrs.get("password")
        confirm_password = attrs.pop("confirm_password", None)

        if password != confirm_password:
            raise ParseError("Passwords do not match.")

        return attrs


    def create(self, validated_data):
        password = validated_data.pop("password")  
        user = User.objects.create(**validated_data)
        user.set_password(password)  
        user.save()  

        tokens = TokenObtainPairSerializer().get_token(user)
        access_token = str(tokens.access_token)
        refresh_token = str(tokens)

        return {
            "user": user.id,
            "access": access_token,
            "refresh": refresh_token
        }



class UserSerializer(serializers.ModelSerializer):
    """
    User serializer with profile information.
    """

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'username',
            'date_joined',
            'role'
        )



class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    Change password serializer.
    
    Attributes:
        * `old_password` (CharField): old password.
        * `new_password` (CharField): new password.
    """

    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password')

    def validate(self, attrs: dict[str, str]) -> dict[str, str]:
        """Validation for correctness."""
        user = get_current_user()
        old_password = attrs.pop('old_password')
        if not user.check_password(raw_password=old_password):
            raise ParseError('Check the correctness of the current password!')
        return attrs

    @staticmethod
    def validate_new_password(password: str) -> str:
        """Validation for the correctness of the new password."""
        validate_password(password=password)
        return password

    def update(self, instance: User, validated_data: dict[str, str]) -> User:
        """Updating the password in the User model."""
        password = validated_data.pop('new_password')
        # Hash the password
        instance.set_password(raw_password=password)
        instance.save()
        return instance


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user information.
    """
    role = serializers.ChoiceField(choices=[User.Role.EMPLOYER, User.Role.EMPLOYEE])

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'role'
        )

    def update(self, instance: User, validated_data: dict[str, str]) -> User:
        """Update user model and related profile."""

        with transaction.atomic():
            instance = super().update(
                instance=instance, validated_data=validated_data
            )
        return instance


class UserListSearchSerializer(serializers.ModelSerializer):
    """Serializer for user search."""

    class Meta:
        model = User
        fields = ('id',
                  'first_name',
                  'last_name',
                  'email',
                  'username',
                  'role')
