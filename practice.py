from flask import Flask, render_template, request, session, redirect, url_for
from key_generator.key_generator import generate
import random
import extractor
import condense
import sqlite3
import data_graphs
from io import BytesIO
import base64
connection = sqlite3.connect('backup_database.db', check_same_thread=False)

app = Flask(__name__)
feedbacks = set()


@app.route('/', methods = ["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("form.html")
    else:
        feed_in = (request.form['feed'])
        raw = extractor.extract(feed_in)
        results_raw = raw['keywords']
        clean = []
        for d in results_raw:
            clean.append({d['text']:d['sentiment']['score']})
        count = len(clean)
        #Get overall score as an average
        total = 0 
        for i in clean:
            total += sum(i.values())
        average = total/count
        clean.insert(0, count)
        clean.insert(0, request.form['branch'])
        clean.insert(1, average)
        sanitized = condense.main(clean)
        print(sanitized)
      
    sentiment = ''
    if sanitized[1] < 0:
        sentiment = 'neg'
    else:
        sentiment = 'pos'
    #update the general city score 
    c = connection.cursor()
    db_count = c.execute(f"SELECT count FROM {sanitized[0]}_{sentiment}_general")
    print(db_count)
    count_num = db_count.fetchone()[0]
    c = connection.cursor()
    db_total = c.execute(f"SELECT total FROM {sanitized[0]}_{sentiment}_general")
    total_num = db_total.fetchone()[0]
    count_num += 1 
    total_num += sanitized[1]
    c = connection.cursor()
    c.execute(f"UPDATE {sanitized[0]}_{sentiment}_general SET count = {count_num}, total = {total_num}")
    print('DONE 1')
    #update the individual score for the service area(s) mentioned in the comment
    for i in range(3, len(sanitized)):
        key = list(sanitized[i].keys())[0]
        val = list(sanitized[i].values())[0]
        c = connection.cursor()
        count = c.execute(f"SELECT count FROM {key}_{sentiment}_general")
        num_count = count.fetchone()[0]
        c = connection.cursor()
        total = c.execute(f"SELECT total FROM {key}_{sentiment}_general")
        total_num = total.fetchone()[0]
        num_count += 1 
        total_num += val
        c = connection.cursor()
        c.execute(f"UPDATE {key}_{sentiment}_general SET count = {num_count}, total = {total_num}")
        #then do the same for service areas in individual cities
        c = connection.cursor()
        count = c.execute(f"SELECT count FROM {sanitized[0]}_{sentiment}_{key}")
        num_count = count.fetchone()[0]
        c = connection.cursor()
        total = c.execute(f"SELECT total FROM {sanitized[0]}_{sentiment}_{key}")
        num_total = total.fetchone()[0]
        num_count += 1 
        num_total += val
        c = connection.cursor()
        c.execute(f"UPDATE {sanitized[0]}_{sentiment}_{key} SET count = {num_count}, total = {num_total}")
    connection.commit()
    print("DONE 2")
    pic = data_graphs.display_all_scores_indidivual('christchurch')
    return render_template('thanks.html', result = sanitized)




@app.route('/thanks', methods = ["GET", "POST"])
def thanks(result):
    return render_template("thanks.html", result=result)

@app.route('/cities_general', methods = ['GET','POST'])
def cities_general():
    pic = data_graphs.display_gen_cities()
    return render_template('cities_general.html', pic=pic)

@app.route('/service_areas_general', methods = ["GET","POST"])
def service_areas_general():
    pic = data_graphs.display_all_areas()
    return render_template('service_areas_general.html', pic=pic)

@app.route('/cities_individual', methods = ["POST"])
def cities_individual():
    city_name = request.form['city_name']
    pic = data_graphs.display_all_scores_indidivual(city_name)
    return render_template('cities_individual.html', pic = pic, city = city_name)



if __name__ == '__main__':
    app.run(debug=True)