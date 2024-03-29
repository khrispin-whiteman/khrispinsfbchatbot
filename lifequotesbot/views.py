import json
import random
import re
from pprint import pprint

import requests

from django.http import HttpResponse

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from lifequotesbot.models import Answers, Questions, ChatRecord, NoRecordFoundResponse

PAGE_ACCESS_TOKEN = 'EAAKj7aa5t4UBAGuGl9ZAasCCFczvKsFJ4zqmkNIFZBwVEVPC87GOwucjo2eKsuCvPZCGe4i8ZAysDQrHY1KCuZBZA2M4iWH5sC4Gu0TVlsZCA3WvcBa50TZBK677obRjZCy3h0ZCuznlqIGkQo9tqc7eBYO7rOgVwClaU75iVuQpONWZAh1KhinZCInI'
VERIFY_TOKEN = 'LIFEQUOTES_VERIFY_TOKEN'


# Helper function
def post_facebook_message(fbid, recevied_message):
    # Remove all punctuations, lower case the text and split it based on space
    #tokens = re.sub(r"[^a-zA-Z0-9\s]", ' ', recevied_message).lower().split()
    tokens = recevied_message.lower()
    print('The Tokens Received: ', recevied_message)
    joke_text = ''
    que = ''

    answers = Answers.objects.all()
    questions = Questions.objects.all()

    #for token in tokens:
    #answers = answers.filter(question_keyword__question_keyword__endswith=tokens).order_by('?')

    for answer in answers:
        question = answer.question_keyword.question_keyword
        if question.lower() in tokens:
            answers = answers.filter(question_keyword__question_keyword__icontains=question).order_by('?')
            if answers:
                for a in answers:
                    print('THE QUESTION: ', tokens)
                    print('THE ANSWER: ', a.answer)
                    joke_text = a.answer
                    break
    if not joke_text:
        #pick a rondom response if bot does not understand
        erroressages = ["'{}' what?".format(tokens), ]
        response_txt = list(NoRecordFoundResponse.objects.values_list('responsetext', flat=True))
        joined_list = erroressages + response_txt
        joke_text = random.choice(joined_list)

    user_details_url = "https://graph.facebook.com/v3.2/%s" % fbid
    user_details_params = {'fields': 'first_name,last_name,profile_pic', 'access_token': PAGE_ACCESS_TOKEN}
    user_details = requests.get(user_details_url, user_details_params).json()
    #joke_text = 'Yo ' + user_details['first_name'] + '..! ' + joke_text

    print('ID: ', user_details)
    chatrecord = ChatRecord()
    # chatrecord = ChatRecord(fb_user=user_details.get(['first_name']), message=tokens, response=joke_text)
    # chatrecord.objects.create(fb_user=user_details['first_name'], message=tokens, response=joke_text)
    # chatrecord.fb_user = user_details.get(['name',] )
    # chatrecord.message = tokens
    # chatrecord.response = joke_text
    # chatrecord.save()

    post_message_url = 'https://graph.facebook.com/v3.2/me/messages?access_token=%s' % PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"text": joke_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    #pprint(status.json())


# Create your views here.
class MyBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly.
                    print('The message is: ', message['message']['text'])
                    print('Sender Details: ', message['sender']['id'])
                    post_facebook_message(message['sender']['id'], message['message']['text'])
        return HttpResponse()
