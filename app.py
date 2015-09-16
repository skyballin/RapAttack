from flask import Flask
from flask import Flask, render_template, request
import jinja2
from lyricextractor import lyrics_extractor

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index2.html')

# My word counter app
@app.route('/rap_lyrics', methods=['POST'] )
def rap_output():
    text = str(request.form['user_input'])
    word_counts = 10
    page = lyrics_extractor(text, 'http://www.azlyrics.com/j/johndenver.html')
    lyrics = page[0]
    count = page[1]
    output = []
    for line in lyrics:
         line2 = []
         for word in line.split():
             word = ''.join(ch for ch in word if ord(ch)<128)
             line2.append(word)
         output.append(' '.join(line2))

    context_dict = {}

    context_dict['lyrics'] = '<br>'.join(output)
    context_dict['count'] = count
        
    return render_template('rap_output.html', data = '<br>'.join(output), object = count)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 3030, debug = True)








