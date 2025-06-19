from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotFound
from .models import Todo, User
from .serializers import TodoSerializer

class Todos(APIView):

    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("유저를 찾을 수 없습니다.")
        return user

    # todolist 조회
    def get(self,request,user_id):
        # 유저 가져오기
        user = self.get_user(user_id)

        # 기본 -> 전체 todolist 조회
        todos = Todo.objects.get(user=user)
        
        # 쿼리 파라미터에서 month, day 가져오기
        month = request.query_params.get("month")
        day = request.query_params.get("day")

        # month, day 가 제공된 경우에만 필터링해서 제공
        if month is not None and day is not None:
            try:
                month = int(month)
                day = int(day)
                todos = todos.filter(date_month=month, date_day=day)
            except ValueError:
                raise ParseError("month와 day는 정수여야 합니다.")
        
        # 정렬, 추가 필터링을 위한 sort_by 파라미터
        sort_by = request.query_params.get('sort_by','created_at')
        if sort_by not in ['created_at','updated_at']:
            sort_by = 'created_at'
        
        # 직렬화
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)
    
