from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer

class BookListView(APIView):
    
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetailView(APIView):
    
    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return None
    
    def get(self, request, pk):
        book = self.get_object(pk)
        if not book:
            return Response({"error": "Book not found"}, status=404)
        
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
    def delete(self, request, pk):
        book = self.get_object(pk)
        if not book:
            return Response({"error": "Book not found"}, status=404)
        
        book.delete()
        return Response({"message": "Book deleted successfully"})