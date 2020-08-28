from django.db import models

# Create your models here.
from django.db import models


# Create your models here.
from django_random_queryset import RandomManager


class Questions(models.Model):
    question_keyword = models.CharField('Keyword', max_length=1000, )

    class Meta:
        verbose_name = 'Questions Or Keywords'
        verbose_name_plural = 'Questions Or Keywords'

    def __str__(self):
        return self.question_keyword


class Answers(models.Model):
    question_keyword = models.ForeignKey('Questions', verbose_name='Key', null=True, blank=True, on_delete=models.CASCADE)
    answer = models.CharField('Values', max_length=10000)

    objects = RandomManager()

    class Meta:
        verbose_name = 'Answers'
        verbose_name_plural = 'Answers'

    def __str__(self):
        return str(self.question_keyword.question_keyword + ' - ' + self.answer)


class NoRecordFoundResponse(models.Model):
    responsetext = models.CharField(max_length=200, verbose_name='Response Text')


    class Meta:
        verbose_name = 'No Record Found Response'
        verbose_name_plural = 'No Record Found Responses'

    def __str__(self):
        return self.responsetext


class ChatRecord(models.Model):
    fb_user = models.CharField('Recipients FB name', max_length=200)
    message = models.CharField('Message Received', max_length=200)
    response = models.CharField('Recipients FB name', max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Chat Records'
        verbose_name = 'Chat Records'

    def __str__(self):
        return str(self.fb_user + ' - ' + self.message + ' - ' + str(self.timestamp))