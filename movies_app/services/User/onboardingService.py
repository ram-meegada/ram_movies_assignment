from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from movies_app.utils import messages

class OnboardingService:
    def user_registration(self, request):
        try:
            user = User.objects.create(
                username=request.data["username"],
                password=request.data["password"]
                )
            token = RefreshToken.for_user(user)
            data = {
                "access_token": str(token.access_token)
            }
            return {"data": data, "messsage": messages.USER_CREATED, "status": status.HTTP_201_CREATED}
        except IntegrityError:
            return {"data": None, "messsage": messages.USERNAME_EXISTS, "status": status.HTTP_400_BAD_REQUEST}
        except Exception as err:
            return {"error": str(err), "error_type": str(type(err)), "messsage": messages.WENT_WRONG, "status": status.HTTP_400_BAD_REQUEST}
