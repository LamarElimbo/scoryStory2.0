from flask import Flask, request, render_template, make_response
from io import StringIO
import urllib
import csv
import mainStoryScory_v2


app = Flask(__name__)
requiredInfo=[]

@app.route('/')
@app.route('/scory_story_v2')
def scory_story_v2_search():
    return render_template('/searchScoryStoryV2.html', 
                           css_source='../static/app.css', 
                           activeTab='scory_story_v2')

@app.route('/scory_story_v2_result', methods=['POST'])
def scory_story_v2_result():
    story = request.form['sent']
    storyParagraphs, combinedGenreList = mainStoryScory_v2.v2_runProgram(story)
    return render_template('/resultScoryStoryV2.html',
                           paragraphs=storyParagraphs, combinedGenres=combinedGenreList,
                           css_source='../static/app.css', 
                           activeTab='scory_story_v2')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)