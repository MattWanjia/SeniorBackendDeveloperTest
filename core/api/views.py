from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.response import Response
import urllib
import json
from django.http import HttpResponse
import requests
import operator
import time


unwanted_characters = ['-', '.', ',', '–']


def get_user_karma(id):
    url = f'https://hacker-news.firebaseio.com/v0/user/{id}.json'
    data = requests.get(url)
    data = data.json()

    # print(data)

    return data["karma"]


def word_count(str):
    counts = dict()
    words = str.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts


class Last25StoriesApiView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        new_stories_url = 'https://hacker-news.firebaseio.com/v0/newstories.json'

        new_stories_data = requests.get(new_stories_url)

        new_stories_list = new_stories_data.json()

        new_stories_list = new_stories_list[0:25]

        all_titles = ""

        for new_story in new_stories_list:
            story_object = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{new_story}.json')

            story = story_object.json()

            if story["type"] == "story":
                all_titles += f' {story["title"]}'

        for char in all_titles:
            if char in unwanted_characters:
                all_titles.replace(char, "")

        counts = word_count(all_titles)
        counts = sorted(counts.items(), key=operator.itemgetter(1), reverse=True)
        wanted = counts[0:10]
        words = []

        for one in wanted:
            last_word = one[0]
            words.append(last_word)

        response = Response()
        response.data = {
            'status': 200,
            'words': words
        }

        return response


class LastWeekWords(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        current_time = int(time.time())

        last_week_timestamp = current_time - 604800

        new_stories_url = 'https://hacker-news.firebaseio.com/v0/newstories.json'

        new_stories_data = requests.get(new_stories_url)

        new_stories_list = new_stories_data.json()

        max_id = requests.get('https://hacker-news.firebaseio.com/v0/maxitem.json?print=pretty')

        #print(max_id.json())

        max_id = max_id.json()

        all_titles = ""

        for story_id in range(max_id, 0, -1):
            story_object = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json')

            story = story_object.json()

            #while story["time"] > last_week_timestamp:
            # print(story["time"])
            if story["type"] == "poll" and story["time"] > last_week_timestamp:
                all_titles += f' {story["title"]}'
            else:
                break

        for char in all_titles:
            if char in unwanted_characters:
                all_titles.replace(char, "")

        counts = word_count(all_titles)
        counts = sorted(counts.items(), key=operator.itemgetter(1), reverse=True)
        wanted = counts[0:10]
        words = []

        for one in wanted:
            last_word = one[0]
            words.append(last_word)

        response = Response()
        response.data = {
            'status': 200,
            'words': words
        }

        return response


class UserKarmaStoryCount(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        max_id = requests.get('https://hacker-news.firebaseio.com/v0/maxitem.json?print=pretty')

        max_id = max_id.json()

        count = 0

        all_titles = ""

        for story_id in range(max_id, 0, -1):
            print(count)
            if count >= 600:
                break

            story_object = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json')
            story = story_object.json()

            print(story)

            try:
                if story["type"] == "story" and get_user_karma(story["by"]) > 10:
                    all_titles += f' {story["title"]}'
                    count += 1
            except:
                pass

        for char in all_titles:
            if char in unwanted_characters:
                all_titles.replace(char, "")

        counts = word_count(all_titles)
        counts = sorted(counts.items(), key=operator.itemgetter(1), reverse=True)
        wanted = counts[0:10]
        words = []

        for one in wanted:
            last_word = one[0]
            words.append(last_word)

        response = Response()
        response.data = {
            'status': 200,
            'words': words
        }

        return response



