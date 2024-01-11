from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django_simple_third_party_jwt.serializers import GoogleLoginSerializer

from django_simple_third_party_jwt.utils.third_party_login import third_party_login

class GoogleLoginSession(TokenObtainPairView):
    permission_classes = (AllowAny,)  # AllowAny for login
    serializer_class = GoogleLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        return third_party_login(serializer, request, session=True)