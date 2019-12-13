from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from rest_framework.reverse import reverse as api_reverse

User = get_user_model()

from status.api.serializers import StatusInlineUserSerializer

# display user info serializer
class UserDetailSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    # getting a status links belonging to this user using relation not serializers like above
    # status_links = serializers.HyperlinkedRelatedField(
    #                 source = 'status_set', # Status.objects.filter(user=user)
    #                 many=True,                    
    #                 read_only=True,
    #                 lookup_field = 'id',
    #                 view_name='api-status:detail',
    #             )

    # getting all status details linked to this user using relation not serializer
    # statuses = StatusInlineUserSerializer(source='status_set',many=True,read_only=True)

    class Meta:
        model = User
        fields = [
            'id', #remove it later
            # 'status_links',
            # 'statuses',
            'username',
            'email',
            'uri',
            'status',
        ]
    
    def get_uri(self,obj):
        request = self.context.get('request')
        return api_reverse("api-user:detail",kwargs={"username":obj.username}, request=request)

    def get_status(self,obj):
        request = self.context.get('request')
        limit = 10
        if request:
            limit_query = request.GET.get('limit')
            try:
                limit = int(limit_query)
            except:
                pass
            
        qs = obj.status_set.all().order_by("-timestamp")
        data = {
            'uri': self.get_uri(obj) + "status/",
            'last': StatusInlineUserSerializer(qs.first(),context={'request':request}).data,
            'recent': StatusInlineUserSerializer(qs[:limit], many=True,context={'request':request}).data 
        }
        return data
