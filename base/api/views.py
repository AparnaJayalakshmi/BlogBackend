from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from  rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import BlogSerializer,RegisterSerializer
from base.models import Blog
from rest_framework import status
from rest_framework.pagination import PageNumberPagination



@api_view(['GET'])
def getRoutes(request):
    routes = [
        'api/register',
        '/api/token',
        '/api/token/refresh',
        'api/blog/'
    ]
    return Response(routes)

class RegisterView(APIView):

    def post(self,request):
        try:
            data = request.data 
            serializer = RegisterSerializer(data = data)

            if not serializer.is_valid():
                return Response({
                    'data' : serializer.errors ,
                    'message' : 'Something went wrong' 
                }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response({
                'data' : {},
                'message': "Account is created"
            },status=status.HTTP_201_CREATED)
            
        except Exception as e:
            
            print(e)
            return Response({
                    'data' : {} ,
                    'message' : 'Something went wrong' 
                }, status=status.HTTP_400_BAD_REQUEST)
        
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

 

class BlogView(APIView):
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    pagination_class = PageNumberPagination
    pagination_class.page_size = 10 

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        try:
            print(request.user)
            blogs = Blog.objects.all()
            paginator = self.pagination_class()
            result_page = paginator.paginate_queryset(blogs, request)
            serializer = BlogSerializer(result_page, many=True)
            num_pages = paginator.page.paginator.num_pages  # Total number of pages
            return paginator.get_paginated_response({
                'data': serializer.data,
                'message': 'Blogs retrieved successfully',
                'num_pages': num_pages
            })

        except Exception as e:
            return Response({
                'data': {},
                'message': 'Something went wrong',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            data = request.data
            print(request.user)
            data['user'] = request.user.id
            serializer = BlogSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({
                'data': serializer.data,
                'message': "Blog is created"
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'Something went wrong',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            blog_instance = Blog.objects.get(pk=pk)
            data = request.data
            data['user'] = request.user.id
            serializer = BlogSerializer(blog_instance, data=data)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({
                'data': serializer.data,
                'message': 'Blog is updated'
            }, status=status.HTTP_200_OK)

        except Blog.DoesNotExist:
            return Response({
                'message': 'Blog does not exist'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'data': {},
                'message': 'Something went wrong',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            blog_instance = Blog.objects.get(pk=pk)
            blog_instance.delete()
            return Response({
                'message': 'Blog is deleted successfully'
            }, status=status.HTTP_200_OK)
        except Blog.DoesNotExist:
            return Response({
                'message': 'Blog does not exist'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'data': {},
                'message': 'Something went wrong',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


