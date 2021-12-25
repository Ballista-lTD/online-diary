from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.models import Tokens
from user.models import Group
from user.serializers import GroupSerializer


class GroupApiViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete']


@login_required()
@api_view(http_method_names=["POST"])
def promote(request):
    if not request.data["access_level"]:
        return Response({"access_level": "Required field"}, status=status.HTTP_400_BAD_REQUEST)

    if not request.data["uid"]:
        return Response({"uid": "Required field"}, status=status.HTTP_400_BAD_REQUEST)

    if request.user.tokens.access_code == "*" or \
            not request.data["access_level"].startswith(request.user.tokens.access_code):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    try:
        token = Tokens.objects.get(user__pk=request.data["uid"])
    except User.DoesNotExist:
        return Response({"uid": "Invalid uid"}, status=status.HTTP_400_BAD_REQUEST)

    if request.user.tokens.access_code.startswith(token.access_code):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    token.access_code = f'{request.data["access_level"]}-{request.user.tokens.users_under}'
    token.save()
