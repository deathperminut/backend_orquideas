# modules/models.py

import re
from django.db import models
from django.conf import settings


class ActivityName(models.Model):
    label = models.CharField(max_length=500)

    def __str__(self):
        return self.label


class SpecificObjective(models.Model):
    description = models.TextField()

    def __str__(self):
        return self.description


class SkillAndLearning(models.Model):
    description = models.TextField()

    def __str__(self):
        return self.description


class Video(models.Model):
    description = models.TextField()
    video_link = models.URLField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.description


class Lecture(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    link = models.URLField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.title


class ForumParticipation(models.Model):
    question = models.TextField()
    response = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.question


class CloudForumParticipation(models.Model):
    question = models.TextField()
    response = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.question


class Evidence(models.Model):
    description = models.TextField()
    upload = models.FileField(upload_to='evidence/', null=True, blank=True)

    def __str__(self):
        return self.description


class ChoiceQuestionary(models.Model):
    choice_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class SelectionMultipleQuestionary(models.Model):
    question_text = models.TextField()
    choices = models.ManyToManyField(ChoiceQuestionary)

    def __str__(self):
        return self.question_text


class OpenQuestionary(models.Model):
    question = models.TextField()
    response = models.TextField()

    def __str__(self):
        return self.question


class OpenQuestionaryOptional(models.Model):
    question = models.TextField()
    response = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.question


class SatisfactionQuestion(models.Model):
    LEVEL_CHOICES = [
        (1, 'Very Dissatisfied'),
        (2, 'Dissatisfied'),
        (3, 'Neutral'),
        (4, 'Satisfied'),
        (5, 'Very Satisfied'),
    ]
    survey = models.TextField(blank=True, null=True)
    level_of_satisfaction = models.IntegerField(
        choices=LEVEL_CHOICES, blank=True, null=True
    )

    def __str__(self):
        return self.survey


class FormatText(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text


class Redaction(models.Model):
    description = models.TextField()
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.description


class Image(models.Model):
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.description


class Activity(models.Model):
    """"""

    activity_name = format_text = models.ForeignKey(
        ActivityName, on_delete=models.CASCADE, null=True, blank=True
    )
    format_text = models.ForeignKey(
        FormatText, on_delete=models.CASCADE, null=True, blank=True
    )
    lecture = models.ForeignKey(
        Lecture, on_delete=models.CASCADE, null=True, blank=True
    )
    evidence = models.ForeignKey(
        Evidence, on_delete=models.CASCADE, null=True, blank=True
    )
    lecture = models.ForeignKey(
        Lecture, on_delete=models.CASCADE, null=True, blank=True
    )
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, null=True, blank=True
    )
    redaction = models.ForeignKey(
        Redaction, on_delete=models.CASCADE, null=True, blank=True
    )
    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    forum_participation = models.ForeignKey(
        ForumParticipation, on_delete=models.CASCADE, null=True, blank=True
    )
    cloud_forum_participation = models.ForeignKey(
        CloudForumParticipation,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    selection_multiple_questionary = models.ForeignKey(
        SelectionMultipleQuestionary,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    open_questionary = models.ForeignKey(
        OpenQuestionary, on_delete=models.CASCADE, null=True, blank=True
    )
    open_questionary_optional = models.ForeignKey(
        OpenQuestionaryOptional,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    satisfaction_question = models.ForeignKey(
        SatisfactionQuestion, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        import re

        header = (
            self.format_text.text
            if self.format_text
            else (
                self.lecture.title
                if self.lecture
                else (
                    self.evidence.description
                    if self.evidence
                    else (
                        self.video.description
                        if self.video
                        else (
                            self.redaction.description
                            if self.redaction
                            else (
                                self.forum_participation.question
                                if self.forum_participation
                                else (
                                    self.cloud_forum_participation.question
                                    if self.cloud_forum_participation
                                    else (
                                        self.selection_multiple_questionary.question_text
                                        if self.selection_multiple_questionary
                                        else (
                                            self.open_questionary.question
                                            if self.open_questionary
                                            else (
                                                self.open_questionary_optional.question
                                                if self.open_questionary_optional
                                                else (
                                                    self.satisfaction_question.survey
                                                    if self.satisfaction_question
                                                    else (
                                                        self.image.description
                                                        if self.image
                                                        else ''
                                                    )
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )

        header = re.sub('<[^<]+?>', '', header)

        return (
            self.activity_name.label + ": " if self.activity_name else ""
        ) + header


class TrainingModule(models.Model):
    """"""

    module_name = models.CharField(max_length=200, null=True, blank=True)
    tag_line = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    color = models.CharField(max_length=100)
    color_name = models.CharField(max_length=32)
    document = models.FileField(upload_to='modules/', null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    general_objective = models.TextField(blank=True)
    specific_objectives = models.ManyToManyField(
        'SpecificObjective', blank=True
    )
    skills_and_learnings = models.ManyToManyField(
        'SkillAndLearning', blank=True
    )

    def __str__(self):
        return f"{self.color_name}: {self.title}"

    class Meta:
        ordering = ['created_at']


########################################################################
class ActivityModule(models.Model):
    """"""

    training_module = models.ForeignKey(
        'TrainingModule', on_delete=models.CASCADE, null=True, blank=True
    )

    foundations_aproximate_duration = models.IntegerField(default=0)
    foundations = models.ManyToManyField(
        'Activity', blank=True, related_name='master_foundation_modules'
    )
    engage_aproximate_duration = models.IntegerField(default=0)
    engage = models.ManyToManyField(
        'Activity', blank=True, related_name='master_engage_modules'
    )
    co_create_aproximate_duration = models.IntegerField(default=0)
    co_create = models.ManyToManyField(
        'Activity', blank=True, related_name='master_co_create_modules'
    )
    reflection_aproximate_duration = models.IntegerField(default=0)
    reflection = models.ManyToManyField(
        'Activity', blank=True, related_name='master_reflection_modules'
    )

    def __str__(self):
        return f"{self.training_module.color_name}: {self.training_module.title}"


########################################################################
class SurveyModule(models.Model):
    """"""

    survey_aproximate_duration = models.IntegerField(default=0)
    survey = models.ManyToManyField(
        'Activity', blank=True, related_name='master_survey_modules'
    )

    def __str__(self):
        return "Survey"


########################################################################
class UserActivityModule(models.Model):
    """"""

    foundations_aproximate_duration = models.IntegerField(default=0)
    foundations = models.ManyToManyField(
        'Activity', blank=True, related_name='foundation_modules'
    )
    engage_aproximate_duration = models.IntegerField(default=0)
    engage = models.ManyToManyField(
        'Activity', blank=True, related_name='engage_modules'
    )
    co_create_aproximate_duration = models.IntegerField(default=0)
    co_create = models.ManyToManyField(
        'Activity', blank=True, related_name='co_create_modules'
    )
    reflection_aproximate_duration = models.IntegerField(default=0)
    reflection = models.ManyToManyField(
        'Activity', blank=True, related_name='reflection_modules'
    )

    def __str__(self):
        total_activities = (
            self.foundations.count()
            + self.engage.count()
            + self.co_create.count()
            + self.reflection.count()
        )
        total_evidence_activities = (
            self.foundations.filter(evidence__isnull=False).count()
            + self.engage.filter(evidence__isnull=False).count()
            + self.co_create.filter(evidence__isnull=False).count()
            + self.reflection.filter(evidence__isnull=False).count()
        )
        return f"Total activities: {total_activities}, Evidence activities: {total_evidence_activities}"


########################################################################
class UserSurveyModule(models.Model):
    """"""

    survey_aproximate_duration = models.IntegerField(default=0)
    survey = models.ManyToManyField(
        'Activity', blank=True, related_name='survey_modules'
    )

    def __str__(self):
        return f"Total questions: {self.survey.count()}"


########################################################################
class UserModule(models.Model):
    """"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    activity_module_master = models.ForeignKey(
        'ActivityModule',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='user_modules_master',
    )

    activity_module_editable = models.ForeignKey(
        'UserActivityModule',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='user_modules',
    )

    survey_module_editable = models.ForeignKey(
        'UserSurveyModule',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='user_survey_modules',
    )

    def save(self, *args, **kwargs):
        if not self.pk and self.activity_module_master:
            new_activity_module_copy = UserActivityModule.objects.create()
            for foundation in self.activity_module_master.foundations.all():
                foundation_copy = Activity.objects.create(
                    activity_name=foundation.activity_name,
                    format_text=(
                        FormatText.objects.create(
                            text=foundation.format_text.text
                        )
                        if foundation.format_text
                        else None
                    ),
                    lecture=(
                        Lecture.objects.create(
                            title=foundation.lecture.title,
                            content=foundation.lecture.content,
                            link=foundation.lecture.link,
                        )
                        if foundation.lecture
                        else None
                    ),
                    evidence=(
                        Evidence.objects.create(
                            description=foundation.evidence.description,
                            upload=foundation.evidence.upload,
                        )
                        if foundation.evidence
                        else None
                    ),
                    video=(
                        Video.objects.create(
                            description=foundation.video.description,
                            video_link=foundation.video.video_link,
                        )
                        if foundation.video
                        else None
                    ),
                    redaction=(
                        Redaction.objects.create(
                            description=foundation.redaction.description,
                            text=foundation.redaction.text,
                        )
                        if foundation.redaction
                        else None
                    ),
                    image=(
                        Image.objects.create(
                            description=foundation.image.description,
                            image=foundation.image.image,
                        )
                        if foundation.image
                        else None
                    ),
                    forum_participation=(
                        ForumParticipation.objects.create(
                            question=foundation.forum_participation.question,
                            response=foundation.forum_participation.response,
                        )
                        if foundation.forum_participation
                        else None
                    ),
                    cloud_forum_participation=(
                        CloudForumParticipation.objects.create(
                            question=foundation.cloud_forum_participation.question,
                            response=foundation.cloud_forum_participation.response,
                        )
                        if foundation.cloud_forum_participation
                        else None
                    ),
                    selection_multiple_questionary=(
                        SelectionMultipleQuestionary.objects.create(
                            question_text=foundation.selection_multiple_questionary.question_text
                        )
                        if foundation.selection_multiple_questionary
                        else None
                    ),
                    open_questionary=(
                        OpenQuestionary.objects.create(
                            question=foundation.open_questionary.question,
                            response=foundation.open_questionary.response,
                        )
                        if foundation.open_questionary
                        else None
                    ),
                    open_questionary_optional=(
                        OpenQuestionaryOptional.objects.create(
                            question=foundation.open_questionary_optional.question,
                            response=foundation.open_questionary_optional.response,
                        )
                        if foundation.open_questionary_optional
                        else None
                    ),
                    satisfaction_question=(
                        SatisfactionQuestion.objects.create(
                            survey=foundation.satisfaction_question.survey,
                            level_of_satisfaction=foundation.satisfaction_question.level_of_satisfaction,
                        )
                        if foundation.satisfaction_question
                        else None
                    ),
                )
                foundation_copy.save()
                new_activity_module_copy.foundations.add(foundation_copy)

            for engage in self.activity_module_master.engage.all():
                engage_copy = Activity.objects.create(
                    activity_name=engage.activity_name,
                    format_text=(
                        FormatText.objects.create(
                            text=engage.format_text.text
                        )
                        if engage.format_text
                        else None
                    ),
                    lecture=(
                        Lecture.objects.create(
                            title=engage.lecture.title,
                            content=engage.lecture.content,
                            link=engage.lecture.link,
                        )
                        if engage.lecture
                        else None
                    ),
                    evidence=(
                        Evidence.objects.create(
                            description=engage.evidence.description,
                            upload=engage.evidence.upload,
                        )
                        if engage.evidence
                        else None
                    ),
                    video=(
                        Video.objects.create(
                            description=engage.video.description,
                            video_link=engage.video.video_link,
                        )
                        if engage.video
                        else None
                    ),
                    redaction=(
                        Redaction.objects.create(
                            description=engage.redaction.description,
                            text=engage.redaction.text,
                        )
                        if engage.redaction
                        else None
                    ),
                    image=(
                        Image.objects.create(
                            description=engage.image.description,
                            image=engage.image.image,
                        )
                        if engage.image
                        else None
                    ),
                    forum_participation=(
                        ForumParticipation.objects.create(
                            question=engage.forum_participation.question,
                            response=engage.forum_participation.response,
                        )
                        if engage.forum_participation
                        else None
                    ),
                    cloud_forum_participation=(
                        CloudForumParticipation.objects.create(
                            question=engage.cloud_forum_participation.question,
                            response=engage.cloud_forum_participation.response,
                        )
                        if engage.cloud_forum_participation
                        else None
                    ),
                    selection_multiple_questionary=(
                        SelectionMultipleQuestionary.objects.create(
                            question_text=engage.selection_multiple_questionary.question_text
                        )
                        if engage.selection_multiple_questionary
                        else None
                    ),
                    open_questionary=(
                        OpenQuestionary.objects.create(
                            question=engage.open_questionary.question,
                            response=engage.open_questionary.response,
                        )
                        if engage.open_questionary
                        else None
                    ),
                    open_questionary_optional=(
                        OpenQuestionaryOptional.objects.create(
                            question=engage.open_questionary_optional.question,
                            response=engage.open_questionary_optional.response,
                        )
                        if engage.open_questionary_optional
                        else None
                    ),
                    satisfaction_question=(
                        SatisfactionQuestion.objects.create(
                            survey=engage.satisfaction_question.survey,
                            level_of_satisfaction=engage.satisfaction_question.level_of_satisfaction,
                        )
                        if engage.satisfaction_question
                        else None
                    ),
                )
                engage_copy.save()
                new_activity_module_copy.engage.add(engage_copy)

            for co_create in self.activity_module_master.co_create.all():
                co_create_copy = Activity.objects.create(
                    activity_name=co_create.activity_name,
                    format_text=(
                        FormatText.objects.create(
                            text=co_create.format_text.text
                        )
                        if co_create.format_text
                        else None
                    ),
                    lecture=(
                        Lecture.objects.create(
                            title=co_create.lecture.title,
                            content=co_create.lecture.content,
                            link=co_create.lecture.link,
                        )
                        if co_create.lecture
                        else None
                    ),
                    evidence=(
                        Evidence.objects.create(
                            description=co_create.evidence.description,
                            upload=co_create.evidence.upload,
                        )
                        if co_create.evidence
                        else None
                    ),
                    video=(
                        Video.objects.create(
                            description=co_create.video.description,
                            video_link=co_create.video.video_link,
                        )
                        if co_create.video
                        else None
                    ),
                    redaction=(
                        Redaction.objects.create(
                            description=co_create.redaction.description,
                            text=co_create.redaction.text,
                        )
                        if co_create.redaction
                        else None
                    ),
                    image=(
                        Image.objects.create(
                            description=co_create.image.description,
                            image=co_create.image.image,
                        )
                        if co_create.image
                        else None
                    ),
                    forum_participation=(
                        ForumParticipation.objects.create(
                            question=co_create.forum_participation.question,
                            response=co_create.forum_participation.response,
                        )
                        if co_create.forum_participation
                        else None
                    ),
                    cloud_forum_participation=(
                        CloudForumParticipation.objects.create(
                            question=co_create.cloud_forum_participation.question,
                            response=co_create.cloud_forum_participation.response,
                        )
                        if co_create.cloud_forum_participation
                        else None
                    ),
                    selection_multiple_questionary=(
                        SelectionMultipleQuestionary.objects.create(
                            question_text=co_create.selection_multiple_questionary.question_text
                        )
                        if co_create.selection_multiple_questionary
                        else None
                    ),
                    open_questionary=(
                        OpenQuestionary.objects.create(
                            question=co_create.open_questionary.question,
                            response=co_create.open_questionary.response,
                        )
                        if co_create.open_questionary
                        else None
                    ),
                    open_questionary_optional=(
                        OpenQuestionaryOptional.objects.create(
                            question=co_create.open_questionary_optional.question,
                            response=co_create.open_questionary_optional.response,
                        )
                        if co_create.open_questionary_optional
                        else None
                    ),
                    satisfaction_question=(
                        SatisfactionQuestion.objects.create(
                            survey=co_create.satisfaction_question.survey,
                            level_of_satisfaction=co_create.satisfaction_question.level_of_satisfaction,
                        )
                        if co_create.satisfaction_question
                        else None
                    ),
                )
                co_create_copy.save()
                new_activity_module_copy.co_create.add(co_create_copy)

            for reflection in self.activity_module_master.reflection.all():
                reflection_copy = Activity.objects.create(
                    activity_name=reflection.activity_name,
                    format_text=(
                        FormatText.objects.create(
                            text=reflection.format_text.text
                        )
                        if reflection.format_text
                        else None
                    ),
                    lecture=(
                        Lecture.objects.create(
                            title=reflection.lecture.title,
                            content=reflection.lecture.content,
                            link=reflection.lecture.link,
                        )
                        if reflection.lecture
                        else None
                    ),
                    evidence=(
                        Evidence.objects.create(
                            description=reflection.evidence.description,
                            upload=reflection.evidence.upload,
                        )
                        if reflection.evidence
                        else None
                    ),
                    video=(
                        Video.objects.create(
                            description=reflection.video.description,
                            video_link=reflection.video.video_link,
                        )
                        if reflection.video
                        else None
                    ),
                    redaction=(
                        Redaction.objects.create(
                            description=reflection.redaction.description,
                            text=reflection.redaction.text,
                        )
                        if reflection.redaction
                        else None
                    ),
                    image=(
                        Image.objects.create(
                            description=reflection.image.description,
                            image=reflection.image.image,
                        )
                        if reflection.image
                        else None
                    ),
                    forum_participation=(
                        ForumParticipation.objects.create(
                            question=reflection.forum_participation.question,
                            response=reflection.forum_participation.response,
                        )
                        if reflection.forum_participation
                        else None
                    ),
                    cloud_forum_participation=(
                        CloudForumParticipation.objects.create(
                            question=reflection.cloud_forum_participation.question,
                            response=reflection.cloud_forum_participation.response,
                        )
                        if reflection.cloud_forum_participation
                        else None
                    ),
                    selection_multiple_questionary=(
                        SelectionMultipleQuestionary.objects.create(
                            question_text=reflection.selection_multiple_questionary.question_text
                        )
                        if reflection.selection_multiple_questionary
                        else None
                    ),
                    open_questionary=(
                        OpenQuestionary.objects.create(
                            question=reflection.open_questionary.question,
                            response=reflection.open_questionary.response,
                        )
                        if reflection.open_questionary
                        else None
                    ),
                    open_questionary_optional=(
                        OpenQuestionaryOptional.objects.create(
                            question=reflection.open_questionary_optional.question,
                            response=reflection.open_questionary_optional.response,
                        )
                        if reflection.open_questionary_optional
                        else None
                    ),
                    satisfaction_question=(
                        SatisfactionQuestion.objects.create(
                            survey=reflection.satisfaction_question.survey,
                            level_of_satisfaction=reflection.satisfaction_question.level_of_satisfaction,
                        )
                        if reflection.satisfaction_question
                        else None
                    ),
                )
                reflection_copy.save()
                new_activity_module_copy.reflection.add(reflection_copy)

            self.activity_module_editable = new_activity_module_copy

            first_survey_module = SurveyModule.objects.first()

            if first_survey_module:
                new_survey_module_copy = UserSurveyModule.objects.create()
                new_survey_module_copy.survey.set(
                    first_survey_module.survey.all()
                )
                self.survey_module_editable = new_survey_module_copy

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user}: {self.activity_module_master}"
