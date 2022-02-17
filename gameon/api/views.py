from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
# from rest_framework import mixins
from.throttle import ReviewListThrottle, ReviewCreateThrottle
from .permissions import IsReviewUserOrReadOnly, IsAdminOrReadOnly
from .pagination import WatchListPagination
from gameon.models import WatchList, StreamPlatform, Review
from .serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer

class UserReview(generics.ListAPIView):

    serializer_class = ReviewSerializer
    # queryset = Review.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    # throttle_classes = [ReviewListThrottle]

    # def get_queryset(self):
    #     usernames = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=usernames)

    def get_queryset(self):
        usernames = self.request.query_params.get('username',None)
        return Review.objects.filter(review_user__username=usernames)

class ReviewCreate(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReviewSerializer
    throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self,serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)

        review_user = self.request.user 
        review_check = Review.objects.filter(watchlist=watchlist,review_user=review_user)
        if review_check.exists():
            raise ValidationError('You reviewed this watchlist already')
            
        if watchlist.number_rating == 0:
            watchlist.avg_review = serializer.validated_data['rating']
        else:
            watchlist.avg_review = (watchlist.avg_review + serializer.validated_data['rating'])/2
            
        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()

        serializer.save(watchlist=watchlist,review_user=review_user,status=status.HTTP_201_CREATED)


class ReviewList(generics.ListAPIView):

    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [ReviewListThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active', 'review_user__username','watchlist']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]


class StreamPlatformView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self,request):
        streamplatforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(streamplatforms, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        else:
            return Response(serializer.errors)

class StreamPlatformDetail(APIView):    
    permission_classes = [IsAdminOrReadOnly]    
    def get(self,request, pk):
        try:
            streamplatform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            content = {
                'error': 'Stream Platform does not exist'
            }
            return Response(content,status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(streamplatform)
        return Response(serializer.data)
    
    def put(self,request,pk):
        try:
            streamplatform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            content = {
                'error': 'Stream Platform does not exist'
            }
            return Response(content,status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(streamplatform,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    def delete(self,request,pk):
        try:
            streamplatform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            content = {
                'error': 'Stream Platform does not exist'
            }
            return Response(content,status.HTTP_404_NOT_FOUND)
        streamplatform.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


class WatchListSearch(generics.ListAPIView):

    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'storyline','platform__name']
    pagination_class = WatchListPagination

    '''
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'storyline','platform__name']
    for filtering

     filter_backends = [filter.OrderingFilter]
     would work on ordering for us based on a specified filedsz
    '''
    

class WatchListView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request):
        watchlist = WatchList.objects.all()
        serializer = WatchListSerializer(watchlist,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer =WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    
class WatchListDetail(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request,pk):
        try:
            watchlist = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            content = {
                'error': 'Watch list not found'
            }
            return Response(content,status.HTTP_404_NOT_FOUND)


        serializer = WatchListSerializer(watchlist)
        return Response(serializer.data)

    def put(self,request,pk):
        try:
            watchlist = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            content = {
                'error': 'Watch list not found'
            }
            return Response(content,status.HTTP_404_NOT_FOUND)
        
        serializer = WatchListSerializer(watchlist,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self,request,pk):
        try:
            watchlist = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            content = {
                'error': 'Watch list not found'
            }
            return Response(content,status.HTTP_404_NOT_FOUND)
        watchlist.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


# class ReviewDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request,*args, **kwargs)

# class ReviewList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer 

#     def get(self, request, *args, **kwargs):
#         return self.list(request,*args,**kwargs)

#     def post(self,request,*args, **kwargs):
#         return self.create(request,*args, **kwargs)
