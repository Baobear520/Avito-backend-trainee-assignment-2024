
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from banners.models import Banner, BannerTagFeature, UserBanner
from banners.serializers import BannerContentSerializer, BannerSerializer, BannerTagFeatureSerializer,UserSerializer


class BannerList(APIView):
    """
    List all banners, or create a new banner.
    """
    def get(self, request):
        banners = Banner.objects.all()
        serializer = BannerSerializer(banners, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = BannerSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        banner = serializer.save()
        print(banner.id)

        # Process tags and create BannerTagFeature instances
        tags = request.data.get('tags', [])
        for tag_id in tags:
            tag_feature_data = {
                'tag': tag_id,
                'banner': banner.id,
                'feature': request.data.get('feature')
            }
            banner_tag_feature_serializer = BannerTagFeatureSerializer(data=tag_feature_data)
            banner_tag_feature_serializer.is_valid(raise_exception=True)
            banner_tag_feature_serializer.save()
            
        return Response(data={'banner_id': serializer.data['id']}, status=status.HTTP_201_CREATED)
        
        
    

class User(APIView):
    """
    Show current user's banner
    
    """
    def get(self, request):
        tag_id = request.query_params.get('tag_id')
        feature_id = request.query_params.get('feature_id')
        use_last_revision = request.query_params.get('use_last_revision', False)

        if not tag_id or not feature_id:
            return Response({"error": "Incorrect data. Please provide both tag_id and feature_id"}, status=status.HTTP_400_BAD_REQUEST)

        # Filter banners based on tag_id and feature_id
        filtered_banners = BannerTagFeature.objects.filter(tag=tag_id, feature=feature_id)
        banner = get_object_or_404(filtered_banners)

        #Serializing only the content field
        serializer = BannerTagFeatureSerializer(banner)
        return Response(serializer.data)
        
