# Don't call this flask.py!
# Documentation for Flask can be found at:
# https://flask.palletsprojects.com/en/1.1.x/quickstart/


from flask import Flask, render_template, request, session, redirect, url_for, jsonify 
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import time

from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher


from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy_instagram.scrapy_instagram.spiders.hashtag import InstagramSpider


app = Flask(__name__)
app.secret_key = b'_2_#pi*CO0@^z'

crawl_runner = CrawlerRunner()
output_data = []

UPLOADS_DIR = 'static/img/display'


#@app.route("/index")
@app.route("/")
def index():
    return render_template("app.html") # templatesフォルダ内のindex.htmlを表示する

@app.route('/loc_input', methods=['POST', 'GET'])
def test():
    info_dict = {}
    if request.method == 'POST':
        data = request.json
    
        
        today_time = time.strftime("%d-%m-%Y_%H")
        today_date = time.strftime("%d-%m-%Y")
        # example showing
        if data['location'] == 'unitedstatesofamerica' or data['location'] == 'japan' or data['location'] == 'paris' or data['location'] == 'kyoto' or data['location'] == 'newyork':
            today_time = "25-03-2022_17"
            today_date = "25-03-2022"
        output_dir = './scraped/hashtag/'+data['location']
        output_path = output_dir+'/'+today_time
        outputs = []
        try: 
            outputs = os.listdir(output_dir)
        except:
            pass
        run_scrapy = True
        folder_name = today_time
        for file in outputs:
            if today_date in file:
                run_scrapy = False
                output_path = output_dir+'/'+file
                folder_name = file

        if run_scrapy:
            process = CrawlerProcess(get_project_settings())
            process.crawl(InstagramSpider, hashtag=data['location'])
            process.start()
        info_dict = fetch_info(output_path, folder_name, data['location'])
        
    return jsonify(info_dict)


def _crawler_result(item, response, spider):
    output_data.append(dict(item))


def fetch_info(file_path, folder, location):
    infos = {}
    with open(file_path, 'r') as f:
        post_list = f.read().splitlines()
        count = 1
        for num in range(0, len(post_list)):
            content = {}
            content['timestamp'] = folder;
            _id = str(count)
            values = post_list[num].split(', ')
            for value in values:
                if 'shortcode' in value:
                    shortcode = value.strip('"shortcode": ')
                    content['shortcode'] = shortcode
                if 'loc_lat' in value:
                    lat = value.strip('"loc_lat": ')
                    content['lat'] = lat
                if 'loc_lon' in value:
                    lon = value.strip('"loc_lon": ')
                    content['lon'] = lon
            image_path = './static/img/'+location+'/'+folder+'/'+content['shortcode']+'.jpg'
            if content['lat']=='Nothing' or content['lon']=='Nothing':
                print("No Info on Post")
            elif not os.path.exists(image_path):
                print("No Image on Post")
            else:
                infos[_id] = content
                count += 1
                print('found')
                # if found 5 posts, stop web scraping
                if count == 5:
                    break
    return infos


if __name__=="__main__":
    app.run(debug=True, port=5005, use_reloader=False, threaded=False)
