import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, KeywordsOptions
import os
from settings import auth, service_url
    

authenticator = IAMAuthenticator(auth)
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2020-08-01',
    authenticator=authenticator
)
def extract(data):
    natural_language_understanding.set_service_url(service_url)
    response = natural_language_understanding.analyze(
    text=data,
    features=Features(keywords=KeywordsOptions(sentiment=True,emotion=False,limit=25))).get_result()
    return response
