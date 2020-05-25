from rest_framework import serializers 
from names.models import Name
 
 
class NameSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Name
        fields = ('id',
                  'fullname',
                  'menh',
                  'van',
                  'gioitinh',
                  'lastname',
                  'meaning'
                  )
