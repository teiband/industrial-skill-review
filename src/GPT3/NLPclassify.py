import numpy as np
import re
import openai
openai.api_key = ""      # enter your API for GPT-3 here
import json


def nlpClassifyResult(query, file_ID):
    """
    use GPT-3 model online-application to get the semantic classification

    :param query: the search content, such as: query = "grasp object"
    :param file_ID: pre-defined file library () "file-aVmfougPtrAX3RA40qSufHqQ"
    :return: search response of GPT-3
    """
    classificationResponse = openai.Classification.create(
        file="file-1rS01Nz1T5ggS7NAUfV24JZd",
        query=query,
        search_model="ada", 
        model="curie", 
        max_examples=3
    )
    # print(search_response)
    return classificationResponse


def best_score(search_response):
    """
    output the best score in search response

    :param search_response: search result of GPT-3
    :return: the max score of content similarity
    """
    score = re.findall(r"(?<=\"score\": )\d+", search_response)      # extract number after "score"
    max_score = None
    for num in score:
        if max_score is None or num > max_score:
            max_score = num
    # print('best score：', max_score)
    return max_score


def best_command(search_response):
    """
    output the pre-defined content that get the best score in search response

    :param search_response: search result of GPT-3
    :return: the corresponding command text in pre-defined files
    """

    score = re.findall(r"(?<=\"score\": )\d+", search_response)      # extract number after "score"
    max_score = None
    for num in score:
        if max_score is None or num > max_score:
            max_score = num
    text = re.findall(r'\"score\": '+max_score+',\n\"text\": (.*?)}', search_response)      # extract the text
    return text


search_response = nlpClassifyResult("elemental actions", "file-1rS01Nz1T5ggS7NAUfV24JZd")

print(search_response)

