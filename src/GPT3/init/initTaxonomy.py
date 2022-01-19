import openai

# enter your API
openai.api_key = ""

# upload your file library
response = openai.File.create(file=open("D:/1. Papers/4. MyPapers/6_(20210609) Skill taxonomy/skill-taxonomy-extraction/src/GPT3/init/primitiveDef.jsonl"), purpose="search")
# file saved for search is: ile-uw4IRrLna23zoYBCHjANqkg5
# file saved for classification is: file-1rS01Nz1T5ggS7NAUfV24JZd
# file saved for primitive search: file-Q6xMsNk5O101Mp8NmKeG4Fc3

# get your file ID as response
print(response)

# then your can use this ID in the main.py

# "file-aVmfougPtrAX3RA40qSufHqQ"
