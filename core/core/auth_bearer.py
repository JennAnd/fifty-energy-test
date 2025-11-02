#from ninja.security import HttpBearer
#from rest_framework.authtoken.models import Token

# Checks if the token belongs to a real user
#class TokenAuth(HttpBearer):
 #   def authenticate(self, request, token): # Runs when someone sends a request with a token
  #      try:
   #         user = Token.objects.get(key=token).user
    #        return user # If correct token return the user
    #   except Token.DoesNotExist:
     #       return None
    