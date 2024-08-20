from django.contrib import admin
from .models import (
    TrainingModule,
    SpecificObjective,
    SkillAndLearning,
    Video,
    Lecture,
    ForumParticipation,
    CloudForumParticipation,
    Evidence,
    Activity,
    ChoiceQuestionary,
    SelectionMultipleQuestionary,
    OpenQuestionary,
    FormatText,
    Redaction,
    ActivityModule,
    UserModule,
    UserActivityModule,
    SurveyModule,
    UserSurveyModule,
    SatisfactionQuestion,
    OpenQuestionaryOptional,
    ActivityName,
    Image,
)


class SpecificObjectiveInline(admin.TabularInline):
    model = TrainingModule.specific_objectives.through
    extra = 1
    verbose_name_plural = "Specific Objectives"


class SkillAndLearningInline(admin.TabularInline):
    model = TrainingModule.skills_and_learnings.through
    extra = 1
    verbose_name_plural = "Skills and Learnings"


class FoundationsInline(admin.TabularInline):
    model = ActivityModule.foundations.through
    extra = 1
    verbose_name_plural = "Foundations"


class EngageInline(admin.TabularInline):
    model = ActivityModule.engage.through
    extra = 1
    verbose_name_plural = "Engage Activities"


class CoCreateInline(admin.TabularInline):
    model = ActivityModule.co_create.through
    extra = 1
    verbose_name_plural = "Co-Create Activities"


class ReflectionInline(admin.TabularInline):
    model = ActivityModule.reflection.through
    extra = 1
    verbose_name_plural = "Reflections activities"


class SurveyModuleInline(admin.TabularInline):
    model = SurveyModule.survey.through
    extra = 1
    verbose_name_plural = "Survey Activities"


class TrainingModuleAdmin(admin.ModelAdmin):
    inlines = [
        SpecificObjectiveInline,
        SkillAndLearningInline,
    ]
    exclude = (
        'specific_objectives',
        'skills_and_learnings',
    )


class ActivityModuleAdmin(admin.ModelAdmin):
    inlines = [
        FoundationsInline,
        EngageInline,
        CoCreateInline,
        ReflectionInline,
    ]
    exclude = (
        'foundations',
        'engage',
        'co_create',
        'reflection',
    )


class UserModuleAdmin(admin.ModelAdmin):
    readonly_fields = ('activity_module_editable', 'survey_module_editable')


class SurveyModuleAdmin(admin.ModelAdmin):
    inlines = [
        SurveyModuleInline,
    ]
    exclude = ('survey',)


admin.site.register(UserModule, UserModuleAdmin)

# admin.site.register(UserModule)

admin.site.register(TrainingModule, TrainingModuleAdmin)
admin.site.register(ActivityModule, ActivityModuleAdmin)
admin.site.register(UserActivityModule)
admin.site.register(SurveyModule, SurveyModuleAdmin)
admin.site.register(UserSurveyModule)

admin.site.register(SpecificObjective)
admin.site.register(SkillAndLearning)
admin.site.register(Video)
admin.site.register(Lecture)
admin.site.register(ForumParticipation)
admin.site.register(CloudForumParticipation)
admin.site.register(Evidence)
admin.site.register(ChoiceQuestionary)
admin.site.register(SelectionMultipleQuestionary)
admin.site.register(OpenQuestionary)
admin.site.register(Activity)
admin.site.register(FormatText)
admin.site.register(Redaction)
admin.site.register(SatisfactionQuestion)
admin.site.register(OpenQuestionaryOptional)
admin.site.register(ActivityName)
admin.site.register(Image)
