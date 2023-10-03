from flask import Flask, render_template, url_for, send_file, request
import requests
import openai
import config


app = Flask(__name__)

user_image = ""

@app.route('/')
def index():
    return render_template('index.html')


# get uploaded image and upload it to local directory 
@app.route('/upload', methods=["POST"])
def upload_file():
    global user_image
    uploaded_file = request.files['file']
    user_image = uploaded_file.filename
    if uploaded_file.filename != '':
        uploaded_file.save(f'static/uploads/{uploaded_file.filename}')
        return render_template('index.html', filename = uploaded_file.filename)
    else:
        return 'File Upload Error'
    
@app.route('/upload/summary', methods=["POST"])
def upload_summary():
    image_file = 'static/uploads/' + user_image
    ninja_api_key = config.ninja_api_key
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

    ######## input text into openAI chatgpt feature #######

    openai.api_key = openai_api_key

    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = [{'role': 'user', 'content': f'Summarize this text concisely. {texts}'}]

    )
    #retrieve only the response from the dict
    gpt_response = response['choices'][0]['message']['content']

    return render_template('index.html', response = gpt_response)



if __name__ == '__main__':
    app.run(debug=True)