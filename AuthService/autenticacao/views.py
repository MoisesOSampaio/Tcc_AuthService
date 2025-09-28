from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework.response import Response
from rest_framework import status

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            data = response.data
            access_token = data.get("access")
            refresh_token = data.get("refresh")

            # Configura o cookie HttpOnly
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,          # Segurança: não acessível via JS
                secure=False,            # Apenas HTTPS
                samesite="Strict",
                max_age=14400       
            )

            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite="Strict",
                max_age=14400
            )

        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({"detail": "Refresh token não encontrado."}, status=status.HTTP_401_UNAUTHORIZED)
        request.data._mutable = True
        request.data["refresh"] = refresh_token
        request.data._mutable = False
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            data = response.data
            access_token = data.get("access")
            

            # Configura o cookie HttpOnly
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,          # Segurança: não acessível via JS
                secure=False,            # Apenas HTTPS
                samesite="Strict",
                max_age=14400       # Protege contra CSRF básico
            )
            return response
        return Response({"mensagem: Erro no refresh do Token"}, status=status.HTTP_400_BAD_REQUEST)
    
class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        acess_token = request.COOKIES.get("access_token")
        if not acess_token:
            return Response({"detail": "Refresh token não encontrado."}, status=status.HTTP_401_UNAUTHORIZED)
        request.data._mutable = True
        request.data["token"] = acess_token
        print(acess_token)
        request.data._mutable = False
        print(request.data)
        return super().post(request, *args, **kwargs)
        

        