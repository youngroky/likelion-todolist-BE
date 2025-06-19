from django.urls import path
from . import views

urlpatterns = [
    # 이렇게만 해도 쿼리 알아서 받아냄, 안받을 수도 있고
    path('<int:user_id>/',views.Todos.as_view()),
]
