from flask import Flask,render_template,request
from flask_cors import cross_origin
import downloader as dl
import mysql_db as mydb
import config_parser as cp

application: Flask = Flask(__name__)


@application.route('/', methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")


@application.route('/ytvdownload', methods=['POST', 'GET'])  # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            channel_url = request.form['content'].replace(" ", "")
            cp.init()
            channel = dl.init(channel_url)
            video_data = mydb.fetchData(channel.channel_id)
            if len(video_data) > 0:
                return render_template('results.html', video_data=video_data[0:(len(video_data))])
            else:
                dl.process_url()
                video_data = mydb.fetchData(channel.channel_id)
                return render_template('results.html', video_data=video_data[0:(len(video_data))])

        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'
        finally:
            dl.close()

    # return render_template('results.html')

    else:
        return render_template('index.html')


if __name__ == "__main__":
    # application.run(host='127.0.0.1', port=8001, debug=True
    application.run()



