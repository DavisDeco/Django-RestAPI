
from rest_framework import serializers

from status.models import Status
from accounts.api.serializers import UserPublicSerializer
from rest_framework.reverse import reverse as api_reverse

# 
class StatusSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    # user = serializers.SerializerMethodField(read_only=True)
    user = UserPublicSerializer(read_only=True)
    # getting a user/owner belonging to this status using relation not serializers
    # user_link = serializers.HyperlinkedRelatedField(
    #                 source='user', #user foreign key
    #                 lookup_field = 'username',
    #                 view_name='api-user:detail',
    #                 read_only=True
    #             )

    # getting a user/owner's username/email/etc belonging to this status using relation not serializers
    # username = serializers.SlugRelatedField(source='user',read_only=True, slug_field='username')

    class Meta:
        model = Status
        fields = [            
            'id', # remove later
            # 'user_link',
            # 'username',
            'user',
            'context',
            'image',
            'uri', 
            
        ]
        read_only_fields = ['user']

    # def get_user(self,obj):
    #     request = self.context.get('request')
    #     user = obj.user
    #     return UserPublicSerializer(user,read_only=True, context={"request":request}).data


    def get_uri(self,obj):
        request = self.context.get('request')
        return api_reverse('api-status:detail',kwargs={"id":obj.id}, request=request)


    # serializers handle validation differently from forms
    # lets validate all fields in the model
    def validate(self,data):
        context = data.get("context",None)
        if context == "":
            context = None
        
        image = data.get("image", None)
        if context is None and image is None:
            raise serializers.ValidationError("Status content or image is required")
        return data

    # lets validate length of context
    def validate_context(self,value):
        if len(value) > 100:
            raise serializers.ValidationError("Status content is too long")
        return value

# this class extends the above class of StatusSerializer
class StatusInlineUserSerializer(StatusSerializer):
    class Meta:
        model = Status
        fields = [            
            'id', # remove later
            'context',
            'image',
            'uri', 
        ]
  
# this class achieves the above without extending StatusSerializer
# class StatusInlineUserSerializer(serializers.ModelSerializer):
#     uri = serializers.SerializerMethodField(read_only=True)
    
 
#     class Meta:
#         model = Status
#         fields = [            
#             'id', # remove later
#             'context',
#             'image',
#             'uri', 
#         ]
    
#     def get_uri(self,obj):
#         return "/api/Status/{id}/".format(id=obj.id)
