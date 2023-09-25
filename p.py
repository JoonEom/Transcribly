import requests
import openai
import config
#store variables
image_file = 'images/ex1.png'
ninja_api_key = '/qo4nl7zaPTX2rfUgfKa4Q==vyiHpbAVgI610GKR'
openai_api_key = config.open_api_key
#fetch api (from api-ninjas api docs)
url = 'https://api.api-ninjas.com/v1/imagetotext'
image = open(image_file, 'rb')
files = {'image': image}
response = requests.post(url, files=files, headers={'X-Api-Key': ninja_api_key})

#turn response into a json format data
data = response.json()
#only access the texts from json data and join into a string
texts = ' '.join([item['text'] for item in data])

print(texts)

######## input text into openAI chatgpt feature #######

openai.api_key = openai_api_key

response = openai.ChatCompletion.create(
    model = 'gpt-3.5-turbo',
    messages = [{'role': 'user', 'content': f'Summarize this text concisely. {texts}'}]

)
#retrieve only the response from the dict
gpt_response = response['choices'][0]['message']['content']

print(gpt_response)
