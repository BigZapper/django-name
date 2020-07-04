from rest_framework import serializers 
from names.models import Name, MidName
import random

index = 0
class NameSerializer(serializers.ModelSerializer):
    midname = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Name
        fields = ('id',
                  'fullname',
                  'midname',
                  'menh',
                  'van',
                  'gioitinh',
                  'lastname',
                  'meaning',
                  'likes'
                  )
   


    def get_midname(self, obj):
            # arr = []
            rd = random.randint(1,29)
            gender = obj.gioitinh
            thanh = obj.thanh
            midname = MidName.objects.filter(id=rd, gioitinh=gender).values('tenlot', 'meaning').first()
            midname_test = MidName.objects.filter(gioitinh=gender, thanh=thanh).values('id')
            
            if midname_test:
                rand = random.choice(midname_test)
                midname = MidName.objects.filter(id=rand['id'], gioitinh=gender).values('tenlot','meaning').first()
                # print('result', midname)
            # while not midname:
            #     if gender == 'Nữ':
            #         index = random.randint(1,20)  
            #     else:
            #         index = random.randint(20,28)               
            #     midname = MidName.objects.filter(id=index, gioitinh=gender).values('tenlot','meaning').first()

            if midname:
                # print(midname)
                return {
                    'meaning':midname['meaning'],
                    'name':midname['tenlot']
                }
            else:
                return {}