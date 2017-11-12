from flask import Flask, request, render_template, make_response
from io import StringIO
import urllib
import csv

import sys
sys.path.insert(0, './site_sleuth/')
import getResults

sys.path.insert(0, './spellbook/')
import spellGetter

sys.path.insert(0, './scory_story_v1')
import mainStoryScory

sys.path.insert(0, './scory_story_v2')
import mainStoryScory_v2


app = Flask(__name__)
requiredInfo=[]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home_template/home.html', 
                           css_source='../static/home_static/app.css', 
                           activeTab='home')

#Site Sleuth App
@app.route('/site_sleuth_search')
def site_sleuth_search():
    return render_template('site_sleuth_templates/search.html', 
                           css_source='../static/site_sleuth_static/app.css', 
                           repoLink='https://github.com/lamar133/siteSleuth',
                           activeTab='site_sleuth')

@app.route('/site_sleuth_result', methods=['POST'])
def site_sleuth_result():
    try:
        websites = request.form['website']
        reqInfo = getResults.run(websites)
        requiredInfo.append(reqInfo)
        return render_template('site_sleuth_templates/result.html', 
                           css_source='../static/site_sleuth_static/app.css', 
                           activeTab='site_sleuth',
                           repoLink='https://github.com/lamar133/siteSleuth',
                           requiredInfo=reqInfo)        
    except urllib.error.HTTPError:
        return render_template('site_sleuth_templates/error.html', 
                           css_source='../static/site_sleuth_static/app.css', 
                           repoLink='https://github.com/lamar133/siteSleuth',
                           activeTab='site_sleuth')
    except urllib.error.URLError:
        return render_template('site_sleuth_templates/search.html', 
                           css_source='../static/site_sleuth_static/app.css', 
                           repoLink='https://github.com/lamar133/siteSleuth',
                           activeTab='site_sleuth')
    except UnicodeDecodeError:
        return render_template('site_sleuth_templates/error.html', 
                           css_source='../static/site_sleuth_static/app.css', 
                           repoLink='https://github.com/lamar133/siteSleuth',
                           activeTab='site_sleuth')

@app.route("/site_sleuth_downloadCSV")
def site_sleuth_downloadCSV():
        
    si = StringIO()
    w = csv.DictWriter(si, requiredInfo[0].keys())
    w.writeheader()
    w.writerows(requiredInfo)
    
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=siteSleuth.csv"
    output.headers["Content-type"] = "text/csv"
    
    return output


#Spellbook App
@app.route('/spellbook_search')
def spellbook_search():
    return render_template('/spellbook_templates/search.html', 
                           css_source='../static/spellbook_static/app.css', 
                           repoLink='https://github.com/lamar133/spellbook',
                           activeTab='spellbook')

@app.route('/spellbook_result', methods=['POST'])
def spellbook_result():
    inputDesire = request.form['desire']    
    resultSpells = spellGetter.search(inputDesire)
    return render_template('/spellbook_templates/searchResultSpellbook.html', 
                           spellInfo=resultSpells, 
                           css_source='../static/spellbook_static/app.css', 
                           repoLink='https://github.com/lamar133/spellbook',
                           activeTab='spellbook')

#Scory Story App 1.0
@app.route('/scory_story_v1')
def scory_story_v1_search():
    return render_template('/scory_story_v1_templates/searchScoryStoryV1.html', 
                           css_source='../static/scory_story_v1_static/app.css',  
                           repoLink='https://github.com/lamar133/scoryStory1.0',
                           activeTab='scory_story_v1')

@app.route('/scory_story_v1_result', methods=['POST'])
def scory_story_v1_result():
    story = request.form['sent']
    classification, songGenre, vidId = mainStoryScory.runProgram(story)
    
    return render_template('/scory_story_v1_templates/resultScoryStoryV1.html',
                           sent=story, genre=classification, musicGenre=songGenre, youtube_id=vidId, 
                           css_source='../static/scory_story_v1_static/app.css',  
                           repoLink='https://github.com/lamar133/scoryStory1.0',
                           activeTab='scory_story_v1')

#Scory Story App 2.0
@app.route('/scory_story_v2')
def scory_story_v2_search():
    return render_template('/scory_story_v2_templates/searchScoryStoryV2.html', 
                           css_source='../static/scory_story_v2_static/app.css', 
                           activeTab='scory_story_v2')

@app.route('/scory_story_v2_result', methods=['POST'])
def scory_story_v2_result():
    story = request.form['sent']
    storyParagraphs, combinedGenreList = mainStoryScory_v2.v2_runProgram(story)
    return render_template('/scory_story_v2_templates/resultScoryStoryV2.html',
                           paragraphs=storyParagraphs, combinedGenres=combinedGenreList,
                           css_source='../static/scory_story_v2_static/app.css', 
                           activeTab='scory_story_v2')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)