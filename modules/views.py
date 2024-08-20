from django.shortcuts import render
from rest_framework import generics


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# from .models import UserModule, UserProfile, ActivityModule
from profiles.models import UserProfile

from .models import (
    TrainingModule,
    SpecificObjective,
    SkillAndLearning,
    Activity,
    Video,
    FormatText,
    Lecture,
    Evidence,
    Redaction,
    ForumParticipation,
    CloudForumParticipation,
    SelectionMultipleQuestionary,
    OpenQuestionary,
    ChoiceQuestionary,
    ActivityModule,
    UserActivityModule,
    UserModule,
    SurveyModule,
    UserSurveyModule,
    SatisfactionQuestion,
    OpenQuestionaryOptional,
    Image,
)


from .models import (
    TrainingModule,
    ActivityModule,
    UserActivityModule,
    UserModule,
    SurveyModule,
    UserSurveyModule,
    Activity,
)
from .serializers import (
    TrainingModuleSerializer,
    ActivityModuleSerializer,
    UserActivityModuleSerializer,
    UserModuleSerializer,
    SurveyModuleSerializer,
    UserSurveyModuleSerializer,
)


FIELDS = {
    'video': Video,
    'format_text': FormatText,
    'lecture': Lecture,
    'evidence': Evidence,
    'redaction': Redaction,
    'forum_participation': ForumParticipation,
    'cloud_forum_participation': CloudForumParticipation,
    'selection_multiple_questionary': SelectionMultipleQuestionary,
    'open_questionary': OpenQuestionary,
    'open_questionary_optional': OpenQuestionaryOptional,
    'satisfaction_question': SatisfactionQuestion,
}


class TrainingModuleListCreateView(generics.ListCreateAPIView):
    queryset = TrainingModule.objects.all()
    serializer_class = TrainingModuleSerializer


class TrainingModuleListView(generics.ListAPIView):
    queryset = TrainingModule.objects.all()
    serializer_class = TrainingModuleSerializer


class TrainingModuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TrainingModule.objects.all()
    serializer_class = TrainingModuleSerializer


class ActivityModuleListCreateView(generics.ListCreateAPIView):
    queryset = ActivityModule.objects.all()
    serializer_class = ActivityModuleSerializer


class ActivityModuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ActivityModule.objects.all()
    serializer_class = ActivityModuleSerializer


class UserActivityModuleListCreateView(generics.ListCreateAPIView):
    queryset = UserActivityModule.objects.all()
    serializer_class = UserActivityModuleSerializer


class UserActivityModuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserActivityModule.objects.all()
    serializer_class = UserActivityModuleSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        data = request.data
        relations = ['foundations', 'engage', 'co_create', 'reflection']
        print("DATOS DEL REQUEST: ",data,data.keys());
        lista_llaves = data.keys();
        if('tipo' in lista_llaves):
            ### ARMAMOS EL OBJETO A ACTUALIZAR
            ### objeto actividad 

            activity_object = {
                "id":int(data['id']),
                data['campo']:data['valor_campo']
            }
            data = {
                data['tipo']:[
                    {
                        data['key']:activity_object
                    }
                ]
            }
            print("informacióin: ",data);
            for relation in relations:
                if relation in data:
                    activities = data[relation]
                    for activity in activities:

                        field = list(activity.keys())[0]
                        value = list(activity.values())[0]
                        activity_id = value.pop('id')

                        activity_obj = FIELDS[field].objects.get(id=activity_id)

                        for key, val in value.items():
                            setattr(activity_obj, key, val)
                        activity_obj.save()
        
        else:
            for relation in relations:
                if relation in data:
                    activities = data[relation]
                    for activity in activities:

                        field = list(activity.keys())[0]
                        value = list(activity.values())[0]
                        activity_id = value.pop('id')

                        activity_obj = FIELDS[field].objects.get(id=activity_id)

                        for key, val in value.items():
                            setattr(activity_obj, key, val)
                        activity_obj.save()

        return Response(serializer.data)


class UserModuleListCreateView(generics.ListCreateAPIView):
    queryset = UserModule.objects.all()
    serializer_class = UserModuleSerializer


class UserModuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserModule.objects.all()
    serializer_class = UserModuleSerializer


class SurveyModuleListCreateView(generics.ListCreateAPIView):
    queryset = SurveyModule.objects.all()
    serializer_class = SurveyModuleSerializer


class SurveyModuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SurveyModule.objects.all()
    serializer_class = SurveyModuleSerializer


class UserSurveyModuleListCreateView(generics.ListCreateAPIView):
    queryset = UserSurveyModule.objects.all()
    serializer_class = UserSurveyModuleSerializer


class UserSurveyModuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserSurveyModule.objects.all()
    serializer_class = UserSurveyModuleSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        data = request.data

        activities = data['survey']
        for activity in activities:

            field = list(activity.keys())[0]
            value = list(activity.values())[0]
            activity_id = value.pop('id')

            activity_obj = FIELDS[field].objects.get(id=activity_id)

            for key, val in value.items():
                setattr(activity_obj, key, val)
            activity_obj.save()

        return Response(serializer.data)


class CreateUserModuleView(APIView):
    def post(self, request):
        user_id = request.data.get('user')
        activity_module_master_id = request.data.get(
            'activity_module_master'
        )

        if not user_id or not activity_module_master_id:
            return Response(
                {
                    "error": "user and activity_module_master are required fields"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = UserProfile.objects.get(pk=user_id)
            activity_module_master = ActivityModule.objects.get(
                pk=activity_module_master_id
            )
        except UserProfile.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except ActivityModule.DoesNotExist:
            return Response(
                {"error": "ActivityModule not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        user_module = UserModule.objects.create(
            user=user, activity_module_master=activity_module_master
        )

        return Response(
            {
                "id": user_module.id,
                "user": user_module.user.id,
                "activity_module_master": user_module.activity_module_master.id,
            },
            status=status.HTTP_201_CREATED,
        )


#
# class CreateUserActivityModuleView(APIView):
#     def post(self, request):
#         user_id = request.data.get('user')
#         activity_data = request.data.get('activity_module_data', {})
#
#         if not user_id or not activity_data:
#             return Response(
#                 {
#                     "error": "user and activity_module_data are required fields"
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#
#         try:
#             user = UserProfile.objects.get(pk=user_id)
#             user_activity_module = UserActivityModule.objects.create()
#             for key, activities in activity_data.items():
#                 if hasattr(user_activity_module, key):
#                     activity_objs = Activity.objects.filter(
#                         id__in=activities
#                     )
#                     getattr(user_activity_module, key).set(activity_objs)
#             user_module = UserModule.objects.create(
#                 user=user, activity_module_editable=user_activity_module
#             )
#         except UserProfile.DoesNotExist:
#             return Response(
#                 {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
#             )
#         except Activity.DoesNotExist:
#             return Response(
#                 {"error": "One or more activities not found"},
#                 status=status.HTTP_404_NOT_FOUND,
#             )
#
#         return Response(
#             {
#                 "id": user_module.id,
#                 "user": user_module.user.id,
#                 "activity_module_editable": user_module.activity_module_editable.id,
#             },
#             status=status.HTTP_201_CREATED,
#         )
