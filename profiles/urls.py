from django.urls import path
from .views import CreateUserView, UserListView,CreateInstitutionView,LoginView, InstitutionDetailView, InstitutionListView,RoleListView,UserDetailView,GetUserInfo
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('register/', CreateUserView.as_view(), name='register'),
    path('roles/',RoleListView.as_view(),name="roles-list"),
    path('login/', LoginView.as_view(), name='login'),
    path('createInstitution/',CreateInstitutionView.as_view(),name='create-institution'),
    path('get-user-info/', GetUserInfo.as_view(), name='get_user_info'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('institutions/', InstitutionListView.as_view(), name='institution-list'),
    path('institutions/<int:pk>/', InstitutionDetailView.as_view(), name='institution-detail'),
    # Otras rutas
]
