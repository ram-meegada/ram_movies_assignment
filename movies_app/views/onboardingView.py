from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from movies_app.services.User.onboardingService import OnboardingService

onboarding_obj = OnboardingService()

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        result = onboarding_obj.user_registration(request)
        return Response(result, status=result["status"])
