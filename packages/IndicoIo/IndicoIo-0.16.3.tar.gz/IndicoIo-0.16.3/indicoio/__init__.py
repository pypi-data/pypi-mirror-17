from functools import wraps, partial
import warnings

Version, version, __version__, VERSION = ('0.16.3',) * 4

JSON_HEADERS = {
    'Content-type': 'application/json',
    'Accept': 'application/json',
    'client-lib': 'python',
    'version-number': VERSION
}

from indicoio.text.twitter_engagement import twitter_engagement
from indicoio.text.sentiment import posneg, sentiment_hq
from indicoio.text.sentiment import posneg as sentiment
from indicoio.text.political import political
from indicoio.text.lang import language
from indicoio.text.tagging import text_tags
from indicoio.text.keywords import keywords
from indicoio.text.ner import people, places, organizations
from indicoio.text.personality import personality
from indicoio.text.personas import personas
from indicoio.text.relevance import relevance
from indicoio.text.text_features import text_features
from indicoio.text.emotion import emotion
from indicoio.images.fer import fer
from indicoio.images.features import facial_features, image_features
from indicoio.images.faciallocalization import facial_localization
from indicoio.images.recognition import image_recognition
from indicoio.images.filtering import content_filtering
from indicoio.text.summarization import summarization
from indicoio.utils.multi import analyze_image, analyze_text, intersections
from indicoio.utils.errors import IndicoError
