from flask import Flask, render_template, url_for, request, redirect
import datetime
from  youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
from transformers import pipeline
from transformers import T5ForConditionalGeneration, T5Tokenizer
import json

from flask import send_from_directory
import os

#youtube_video = "https://www.youtube.com/watch?v=UF8uR6Z6KLc"
#video_id = youtube_video.split("=")[1]

def getTranscript(video_id):
    YouTubeTranscriptApi.get_transcript(video_id, languages=['de', 'en'])
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['de', 'en'])

    formatter = JSONFormatter()

    # .format_transcript(transcript) turns the transcript into a JSON string.
    json_formatted = formatter.format_transcript(transcript)

    # Now we can write it out to a file.
    # with open('your_filename.json', 'w', encoding='utf-8') as json_file:
    #     json_file.write(json_formatted)

    result = ""
    for i in transcript:
        result += ' ' + i['text']

    print(len(result))
    

    # fetch the actual transcript data
    #print(transcript.fetch())

    return result


def getSummary(article):

    summarizer = pipeline("summarization")
    summary = ""
    num_iter = int(len(article)/1000)
    for i in range(0,num_iter+1):
        start = i*1000
        end = (i+1)*1000

        part = summarizer(article[start:end])[0]['summary_text']
        
        summary = summary + " " + part

    
    return summary



# define a variable to hold the app
app = Flask(__name__)

# define the resource endpoints
@app.route('/', methods=['POST','GET'])
def index_page():
    if request.method == 'POST':
        youtube_video = str(request.form['content'])

        if (youtube_video == ""):
            return redirect('/')

        video_id = youtube_video.split("=")[1]
        
        try:
            transcript = getTranscript(video_id)
        except:
            return "There was a problem getting the Transcript"

        print("running")

        summary = getSummary(transcript)
        return render_template('index.html', summary=summary)

    else:
        return render_template('index.html')

#app.route('/time', methods=['GET'])
#def get_time():

# server the app when this file is run
if __name__ == '__main__':
    app.run(debug = True)