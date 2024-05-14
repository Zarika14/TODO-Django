from rest_framework import generics
from rest_framework.response import Response
from .serializers import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import  authenticate
from django.urls import reverse
from .models import CustomUser, MailVerificationOTP
from . import service
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseBadRequest
from .service import get_otp_for_mail_verification, send_otp_for_mail_verification

#API for register user
class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            username = request.POST.get('username')

            if CustomUser.objects.filter(email=email).exists():
                raise Exception('This email is already in use for an account')

            user = CustomUser(email=email, username=username)
            user.set_password(password)
            user.save()

            # Additional registration logic (e.g., OTP verification)
            otp = get_otp_for_mail_verification(user)
            send_otp_for_mail_verification(otp=otp, user=user)

            # Redirect to the mail verification page upon successful registration
            return redirect(reverse('Verify-mail'))  

        except Exception as e:
            # Handle exceptions, for example, by rendering the registration form again with an error message
            return HttpResponseBadRequest(str(e))



class ResendOTPForMailVerificationView(generics.CreateAPIView):
    serializer_class= EmailSerializer
    def post(self,request):
        try :
            email = request.data['email']
            
            if not CustomUser.objects.filter(email = email).exists():
                raise Exception('Invalid Email')
    
            user = CustomUser.objects.get(email=email)
    
            if user.is_verified:
                raise Exception('Email already verified')
    
            # get and store otp to verify this email    
            otp = service.get_otp_for_mail_verification(user)
    
            # send this otp to user's mail
            service.send_otp_for_mail_verification(otp = otp, user= user)
            return Response({'message' : 'request succesfull'}, status = 200)    
                
    
        except Exception as e :
            return Response({'message' : str(e)}, status = 400)



class MailVerificationView(generics.CreateAPIView):
    serializer_class = MailAndOTPSerializer
    
    def get(self, request, *args, **kwargs):
        # Render the registration form when the request method is GET
        return render(request, 'mailverification.html')

    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            otp = request.data.get('otp')

            if not CustomUser.objects.filter(email=email).exists():
                raise Exception('Invalid email')

            user = CustomUser.objects.get(email=email)

            if user.is_verified:
                raise Exception('Email already verified')

            if not MailVerificationOTP.objects.filter(user=user).exists():
                raise Exception('Try resending OTP')

            obj = MailVerificationOTP.objects.get(user=user)

            thirty_minutes_ago = timezone.now() - timezone.timedelta(minutes=30)

            if obj.updated_at < thirty_minutes_ago:
                raise Exception('OTP expired')

            if obj.otp != int(otp):
                raise Exception('Incorrect OTP')

            obj.delete()
            user.is_verified = True
            user.save()

            # Redirect to the login page upon successful verification
            return redirect(reverse('login'))

        except Exception as e:
            # If verification fails, return an error response
            return Response({'error': str(e)}, status=400)


        

class LoginView(generics.CreateAPIView):
    serializer_class= LoginSerializer
    def post(self,request):
        try :
            email = request.data['email']
            password = request.data['password']

            user = authenticate(password = password, username = email)

            if not user :
                raise Exception('invalid credentials')

            if not user.is_verified : 
                raise Exception('email not verified')

            token, created = Token.objects.get_or_create(user=user)
            return Response({'message' : token.key}, status = 200)
        

        except Exception as e:
            return Response({'message' : str(e)}, status = 400)
        

class ForgotPasswordView(generics.CreateAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response({'message': 'No user found with this email address'}, status=404)
            # Generate and send password reset link
            service.send_password_reset_link(user)
            return Response({'message': 'Password reset link sent to your email'}, status=200)
        return Response(serializer.errors, status=400)    

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=400)
            # Set new password
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"message": "Password changed successfully."})
        return Response(serializer.errors, status=400)    