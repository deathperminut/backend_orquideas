from rest_framework import serializers
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


class OpenQuestionaryOptionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenQuestionaryOptional
        fields = ['id', 'question', 'response']


class SatisfactionQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SatisfactionQuestion
        fields = ['id', 'survey', 'level_of_satisfaction']


class SpecificObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificObjective
        fields = ['id', 'description']


class SkillAndLearningSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillAndLearning
        fields = ['id', 'description']


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'description', 'video_link']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'description', 'image']


class FormatTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormatText
        fields = ['id', 'text']


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['id', 'title', 'content', 'link']


class EvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evidence
        fields = ['id', 'description', 'upload']


class RedactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Redaction
        fields = ['id', 'description', 'text']


class ForumParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumParticipation
        fields = ['id', 'question', 'response']


class CloudForumParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudForumParticipation
        fields = ['id', 'question', 'response']


class ChoiceQuestionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoiceQuestionary
        fields = ['id', 'choice_text', 'is_correct']


class SelectionMultipleQuestionarySerializer(serializers.ModelSerializer):
    choices = ChoiceQuestionarySerializer(many=True)

    class Meta:
        model = SelectionMultipleQuestionary
        fields = ['id', 'question_text', 'choices']


class OpenQuestionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenQuestionary
        fields = ['id', 'question', 'response']


class ActivitySerializer(serializers.ModelSerializer):

    format_text = FormatTextSerializer()
    lecture = LectureSerializer()
    evidence = EvidenceSerializer()
    video = VideoSerializer()
    image = ImageSerializer()
    redaction = RedactionSerializer()
    forum_participation = ForumParticipationSerializer()
    cloud_forum_participation = CloudForumParticipationSerializer()
    selection_multiple_questionary = SelectionMultipleQuestionarySerializer()
    open_questionary = OpenQuestionarySerializer()
    open_questionary_optional = OpenQuestionaryOptionalSerializer()
    satisfaction_question = SatisfactionQuestionSerializer()

    class Meta:
        model = Activity
        fields = [
            'format_text',
            'lecture',
            'evidence',
            'video',
            'image',
            'redaction',
            'forum_participation',
            'cloud_forum_participation',
            'selection_multiple_questionary',
            'open_questionary',
            'open_questionary_optional',
            'satisfaction_question',
        ]
        extra_kwargs = {
            'format_text': {'allow_null': False},
            'lecture': {'allow_null': False},
            'evidence': {'allow_null': False},
            'video': {'allow_null': False},
            'image': {'allow_null': False},
            'redaction': {'allow_null': False},
            'forum_participation': {'allow_null': False},
            'cloud_forum_participation': {'allow_null': False},
            'selection_multiple_questionary': {'allow_null': False},
            'open_questionary': {'allow_null': False},
        }

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return {
            key: value for key, value in ret.items() if value is not None
        }


class TrainingModuleSerializer(serializers.ModelSerializer):
    specific_objectives = SpecificObjectiveSerializer(
        many=True, read_only=True
    )
    skills_and_learnings = SkillAndLearningSerializer(
        many=True, read_only=True
    )

    class Meta:
        model = TrainingModule
        fields = [
            'id',
            'module_name',
            'tag_line',
            'title',
            'description',
            'document',
            'created_at',
            'updated_at',
            'color',
            'general_objective',
            'specific_objectives',
            'skills_and_learnings',
        ]


class ActivityModuleSerializer(serializers.ModelSerializer):
    foundations = ActivitySerializer(many=True, read_only=True)
    engage = ActivitySerializer(many=True, read_only=True)
    co_create = ActivitySerializer(many=True, read_only=True)
    reflection = ActivitySerializer(many=True, read_only=True)
    training_module = TrainingModuleSerializer(read_only=True)

    class Meta:
        model = ActivityModule
        fields = [
            'id',
            'training_module',
            'foundations',
            'engage',
            'co_create',
            'reflection',
        ]


class UserActivityModuleSerializer(serializers.ModelSerializer):
    foundations = ActivitySerializer(many=True, read_only=True)
    engage = ActivitySerializer(many=True, read_only=True)
    co_create = ActivitySerializer(many=True, read_only=True)
    reflection = ActivitySerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='useractivitymodule-detail', lookup_field='pk'
    )

    class Meta:
        model = UserActivityModule
        fields = [
            'url',
            'foundations',
            'engage',
            'co_create',
            'reflection',
        ]


class SurveyModuleSerializer(serializers.ModelSerializer):
    survey = ActivitySerializer(many=True, read_only=True)

    class Meta:
        model = SurveyModule
        fields = ['id', 'survey']


class UserSurveyModuleSerializer(serializers.ModelSerializer):
    survey = ActivitySerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='usersurveymodule-detail', lookup_field='pk'
    )

    class Meta:
        model = UserSurveyModule
        fields = [
            'url',
            'survey',
        ]


class UserModuleSerializer(serializers.ModelSerializer):
    #     activity_module_master = ActivityModuleSerializer(read_only=True)
    user = serializers.CharField(source='user.email', read_only=True)
    number_of_activities = serializers.SerializerMethodField()
    number_of_evidence_activities = serializers.SerializerMethodField()
    activity_module_editable = UserActivityModuleSerializer(read_only=True)
    survey_module_editable = UserSurveyModuleSerializer(read_only=True)
    module_name = serializers.CharField(
        source='activity_module_master.training_module.module_name',
        read_only=True,
    )

    class Meta:
        model = UserModule
        fields = [
            'module_name',
            'user',
            'number_of_activities',
            'number_of_evidence_activities',
            'activity_module_editable',
            'survey_module_editable',
        ]

    def get_number_of_activities(self, obj):
        return (
            obj.activity_module_editable.foundations.count()
            + obj.activity_module_editable.engage.count()
            + obj.activity_module_editable.co_create.count()
            + obj.activity_module_editable.reflection.count()
        )

    def get_number_of_evidence_activities(self, obj):
        return (
            obj.activity_module_editable.foundations.filter(
                evidence__isnull=False
            ).count()
            + obj.activity_module_editable.engage.filter(
                evidence__isnull=False
            ).count()
            + obj.activity_module_editable.co_create.filter(
                evidence__isnull=False
            ).count()
            + obj.activity_module_editable.reflection.filter(
                evidence__isnull=False
            ).count()
        )
