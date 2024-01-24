from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from gensim.summarization import summarize
from googletrans import Translator

app = Flask(__name__)

@app.route('/summary', methods=['GET'])
def summary_api():
    try:
        url = request.args.get('url', '')
        lang = request.args.get('lang', '')
        
        if not url:
            return jsonify({'error': 'Please provide a YouTube video URL'}), 400

        video_id = url.split('=')[1]

        try:
            transcript = get_transcript(video_id)+'.'
            print(transcript)
        except Exception as e:
            return jsonify({'error': f'Error getting transcript: {str(e)}'}), 500

        translator = Translator()

        try:
            translated_summary = translator.translate(summarize(transcript), dest=lang).text
        except Exception as e:
            return jsonify({'error': f'Error translating summary: {str(e)}'}), 500

        return translated_summary,200

    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

def get_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ' '.join([d['text'] for d in transcript_list])
        return transcript
    except Exception as e:
        raise Exception(f'Error getting transcript: {str(e)}')

if __name__ == '__main__':
    app.run(debug=True)
