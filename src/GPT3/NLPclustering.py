import numpy as np
import re
import openai
openai.api_key = ""      # enter your API for GPT-3 here
import json


def nlpSearchResult(query, file_ID="file-bYJxrP1Z2BrEeHWVgxmx2z5T"):
    """
    use GPT-3 model online-application to get the semantic search

    :param query: the search content, such as: query = "grasp object"
    :param file_ID: pre-defined file library () "file-bYJxrP1Z2BrEeHWVgxmx2z5T"
    :return: search response of GPT-3
    """
    searchReponse = openai.Engine("davinci").search(
        search_model="davinci",
        query=query,
        max_rerank=5,                                   # number of documents
        file=file_ID,
        return_metadata=False
    )
    # print(search_response)
    return searchReponse


def bestScore(search_response):
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


def bestCommand(search_response):
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


search_response = nlpSearchResult("drilling", "file-bYJxrP1Z2BrEeHWVgxmx2z5T")



