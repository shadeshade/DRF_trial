from rest_framework.generics import \
    (
    ListAPIView,
)

from core.serializers import UserSerializer


# Users
class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]
    # filter_backends = [SearchFilter]
    queryset = User.objects.all()
    # search_fields = ['']

