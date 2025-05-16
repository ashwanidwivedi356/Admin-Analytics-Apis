from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from .models import User

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.urls import reverse

class PasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            token = PasswordResetTokenGenerator().make_token(user)
            reset_url = request.build_absolute_uri(
                reverse('password-reset-confirm', kwargs={'uid': user.pk, 'token': token})
            )
            send_mail(
                subject="Password Reset",
                message=f"Reset your password here: {reset_url}",
                from_email="admin@ecommerce.com",
                recipient_list=[email],
            )
        return Response({'msg': 'Check your email for reset instructions'}, status=200)
