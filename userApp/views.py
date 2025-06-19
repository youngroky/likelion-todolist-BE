from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotFound
from .serializers import UserSerializer
from .models import User
from rest_framework import status

class Register(APIView):
    def post(self,request):
            #1. 사용자 요청으로 데이터 받기

            #2. 요청된 데이터로 Serializer 객체 만들기
            serializer = UserSerializer(data = request.data)
            #3. 데이터가 유효한지 확인
            if serializer.is_valid():
                  #3-1. 유효하면 저장
                  serializer.save()
                  return Response({"detail":"회원가입 요청이 성공적으로 처리되었습니다."},status=status.HTTP_200_OK)
            else :
                  #3-2. 유효하지 않으면 에러 처리 넘김
                  return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            

class Login(APIView):
    def get_user(self,username, password):
        try:
            user = User.objects.get(username=username, password=password)
            return user 
        except User.DoesNotExist:
            raise NotFound("유저를 찾을 수 없습니다.")
    
    def post(self, request): #로그인 요청은 보안을 위해서 POST
        # requset -> username, password 로 구성
        username = request.data.get("username") # 키 값이 username
        password = request.data.get("password")

        if not username or not password:
            raise ParseError("username 또는 password가 필요합니다.")
        
        # 유저 객체를 가져옴
        user = self.get_user(username,password)
        return Response({"user_id": user.id},status=status.HTTP_200_OK)
