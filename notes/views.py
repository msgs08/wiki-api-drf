from django.contrib.auth import get_user_model
from rest_framework import generics
# from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny

from notes.models import NoteModel
from .serializers import NoteSerializer

User = get_user_model()


class NoteAddView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = NoteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class NotesListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = NoteSerializer
    queryset = NoteModel.objects.order_by('-created_at').all()


class NoteFetchView(generics.RetrieveAPIView):
    queryset = NoteModel.objects.all()
    serializer_class = NoteSerializer


class NoteEditView(generics.UpdateAPIView):
    permission_classes = (AllowAny,)
    get_serializer = NoteSerializer
    queryset = NoteModel.objects

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class NoteDeleteView(generics.DestroyAPIView):
    permission_classes = (AllowAny,)
    get_serializer = NoteSerializer
    queryset = NoteModel.objects
