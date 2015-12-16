#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

from cache import cache


YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


@cache.memoize(timeout=7200)
def youtube_search(key, q="Google", type="video", part="id,snippet",
                   maxResults=25, channelId=None, location=None, locationRadius=None,
                   order=None, pageToken=None, publishedAfter=None, publishedBefore=None,
                   regionCode=None, topicId=None, videoCategoryId=None, videoDefinition=None,
                   videoDimension=None, videoDuration=None, videoEmbeddable=None,
                   videoLicense=None, videoSyndicated=None, videoType=None):
    kwargs = {}
    if q is not None:
        kwargs["q"] = q
    if type is not None:
        kwargs["type"] = type
    if part is not None:
        kwargs["part"] = part
    if maxResults is not None:
        kwargs["maxResults"] = maxResults
    if channelId is not None:
        kwargs["channelId"] = channelId
    if location is not None:
        kwargs["location"] = location
    if locationRadius is not None:
        kwargs["locationRadius"] = locationRadius
    if order is not None:
        kwargs["order"] = order
    if pageToken is not None:
        kwargs["pageToken"] = pageToken
    if publishedAfter is not None:
        kwargs["publishedAfter"] = publishedAfter
    if publishedBefore is not None:
        kwargs["publishedBefore"] = publishedBefore
    if regionCode is not None:
        kwargs["regionCode"] = regionCode
    if topicId is not None:
        kwargs["topicId"] = topicId
    if videoCategoryId is not None:
        kwargs["videoCategoryId"] = videoCategoryId
    if videoDefinition is not None:
        kwargs["videoDefinition"] = videoDefinition
    if videoDimension is not None:
        kwargs["videoDimension"] = videoDimension
    if videoDuration is not None:
        kwargs["videoDuration"] = videoDuration
    if videoEmbeddable is not None:
        kwargs["videoEmbeddable"] = videoEmbeddable
    if videoLicense is not None:
        kwargs["videoLicense"] = videoLicense
    if videoSyndicated is not None:
        kwargs["videoSyndicated"] = videoSyndicated
    if videoType is not None:
        kwargs["videoType"] = videoType
    return _youtube_search(key, **kwargs)


def _youtube_search(key, **kwargs):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=key)
    return youtube.search().list(**kwargs).execute()
