import sqlite3
import random
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
from io import BytesIO
import base64
connection = sqlite3.connect('backup_database.db', check_same_thread=False)

#Prime the pump with initial values that are not Null
#loop through a list of service areas and cities and set count to 0 and total to 0.0

cities = ['wellington','christchurch','dunedin','auckland']
service_areas = ['sales_staff', 'mechanic','customer_service','car_quality','car_price','customer_experience','payment_options','online_services','insurance']
for_individual = ['sales_staff', 'mechanic','customer_service','car_quality','car_price','customer_experience']

def initialise(keyword, sentiment):
    c = connection.cursor()
    c.execute(f"INSERT INTO {keyword}_{sentiment}_general VALUES (0, 0.0)")
    connection.commit()
def init_individual(ls1, ls2):
    for i in ls1:
        for y in ls2:
            c = connection.cursor()
            c.execute(f"UPDATE {i}_pos_{y} SET count = 0, total = 0.0")
            c = connection.cursor()
            c.execute(f"UPDATE {i}_neg_{y} SET count = 0, total = 0.0")
            connection.commit()
init_individual(cities, for_individual)

def fill_values(input):
    number = random.uniform(-1.0, 1.0)
    sentiment = ''
    if number < 0:
        sentiment = 'neg'
    else:
        sentiment = 'pos'
    c = connection.cursor()
    count = c.execute(f"SELECT count FROM {input}_{sentiment}_general")
    count_num = count.fetchone()[0]
    c = connection.cursor()
    total = c.execute(f"SELECT total FROM {input}_{sentiment}_general")
    total_num = total.fetchone()[0]
    count_num += 1 
    total_num += number
    c = connection.cursor()
    c.execute(f"UPDATE {input}_{sentiment}_general SET count = {count_num}, total = {total_num}")
    connection.commit()

def fill_individual_values(ls1, ls2):
    for i in ls1:
        for y in ls2:
            number = random.uniform(0.0, 1.0)
            c = connection.cursor()
            count = c.execute(f"SELECT count FROM {i}_pos_{y}")
            count_num = count.fetchone()[0]
            c = connection.cursor()
            total = c.execute(f"SELECT total FROM {i}_pos_{y}")
            total_num = total.fetchone()[0]
            count_num += 1 
            total_num += number
            c = connection.cursor()
            c.execute(f"UPDATE {i}_pos_{y} SET count = {count_num}, total = {total_num}")

            number = random.uniform(-1.0, 0.0)
            c = connection.cursor()
            count = c.execute(f"SELECT count FROM {i}_neg_{y}")
            count_num = count.fetchone()[0]
            c = connection.cursor()
            total = c.execute(f"SELECT total FROM {i}_neg_{y}")
            total_num = total.fetchone()[0]
            count_num += 1 
            total_num += number
            c = connection.cursor()
            c.execute(f"UPDATE {i}_neg_{y} SET count = {count_num}, total = {total_num}")
    connection.commit()
fill_individual_values(cities, for_individual)

def fill_values_areas(input):
    number = random.uniform(-1.0, 1.0)
    sentiment = ''
    if number < 0:
        sentiment = 'neg'
    else:
        sentiment = 'pos'
    c = connection.cursor()
    count = c.execute(f"SELECT count FROM {input}_{sentiment}_general")
    count_num = count.fetchone()[0]
    total = c.execute(f"SELECT total FROM {input}_{sentiment}_general")
    total_num = count.fetchone()[0]
    count_num += 1
    total_num += number
    c = connection.cursor()
    c.execute(f"UPDATE {input}_{sentiment}_general SET count = {count_num}, total = {total_num}")
    connection.commit()

def get_all_scores_cities():
    scores = {}
    for city in cities:
        c = connection.cursor()
        db_count = c.execute(f"SELECT count FROM {city}_pos_general")
        count = db_count.fetchone()[0]
        c = connection.cursor()
        db_total = c.execute(f"SELECT total FROM {city}_pos_general")
        total = db_total.fetchone()[0]
        score = total/count
        scores[f'{city}'] = [score]
        c = connection.cursor()
        db_count = c.execute(f"SELECT count FROM {city}_neg_general")
        count = db_count.fetchone()[0]
        c = connection.cursor()
        db_total = c.execute(f"SELECT total FROM {city}_neg_general")
        total = db_total.fetchone()[0]
        score = total/count
        scores[f'{city}'].append(score * -1)
    return scores

def new_entry(ls):
    sentiment = ''
    if ls[1] < 0:
        sentiment = 'neg'
    else:
        sentiment = 'pos'
    #update the general city score 
    c = connection.cursor()
    db_count = c.execute(f"SELECT count FROM {ls[0]}_{sentiment}_general")
    print(db_count)
    count_num = db_count.fetchone()[0]
    c = connection.cursor()
    db_total = c.execute(f"SELECT total FROM {ls[0]}_{sentiment}_general")
    total_num = db_total.fetchone()[0]
    count_num += 1 
    total_num += ls[1]
    c = connection.cursor()
    c.execute(f"UPDATE {ls[0]}_{sentiment}_general SET count = {count_num}, total = {total_num}")
    print('DONE 1')
    #update the individual score for the service area(s) mentioned in the comment
    for i in range(3, len(ls)):
        key = list(ls[i].keys())[0]
        val = list(ls[i].values())[0]
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
        count = c.execute(f"SELECT count FROM {ls[0]}_{key}")
        num_count = count.fetchone()[0]
        c = connection.cursor()
        total = c.execute(f"SELECT total FROM {ls[0]}_{key}")
        num_total = total.fetchone()[0]
        num_count += 1 
        num_total += val
        c = connection.cursor()
        c.execute(f"UPDATE {ls[0]}_{key} SET count = {num_count}, total = {num_total}")
    connection.commit()
    print("DONE 2")



def get_all_scores_areas():
    scores = {}
    for area in service_areas:
        c = connection.cursor()
        db_count = c.execute(f"SELECT count FROM {area}_pos_general")
        count = db_count.fetchone()[0]
        c = connection.cursor()
        db_total = c.execute(f"SELECT total FROM {area}_pos_general")
        total = db_total.fetchone()[0]
        score = total/count
        scores[f'{area}'] = [score]
        c = connection.cursor()
        db_count = c.execute(f"SELECT count FROM {area}_neg_general")
        count = db_count.fetchone()[0]
        c = connection.cursor()
        db_total = c.execute(f"SELECT total from {area}_neg_general")
        total = db_total.fetchone()[0]
        score = total/count
        scores[f'{area}'].append(score * -1)
    return scores
def display_gen_cities():
    img = BytesIO()
    data = get_all_scores_cities()

    df = pd.DataFrame.from_dict(data, orient='index', columns = ['positive','negative'])
    pd.set_option("display.max.columns", None)
    df.plot(y=["positive", "negative"], kind="bar", alpha=0.75, rot=0)
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url
    




def display_all_areas():
    img = BytesIO()
    data = get_all_scores_areas()
    df = pd.DataFrame.from_dict(data, orient='index', columns = ['positive', 'negative'])
    pd.set_option("display.max.columns", None)
    df.plot(y = ['positive', 'negative'], kind="bar", alpha=0.70, rot=0, fontsize=5)
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url

city = 'wellington'

def get_all_scores_individual(cit):
    areas = ['sales_staff', 'mechanic','customer_service','car_quality','car_price','customer_experience']
    scores = {}
    for i in areas:
        c = connection.cursor()
        count = c.execute(f"SELECT count FROM {cit}_pos_{i}")
        count_num = count.fetchone()[0]
        total = c.execute(f"SELECT total FROM {cit}_pos_{i}")
        total_num = total.fetchone()[0]
        score = total_num/count_num
        scores[f'{cit}_{i}'] = [score]

        c = connection.cursor()
        count = c.execute(f"SELECT count FROM {cit}_neg_{i}")
        count_num = count.fetchone()[0]
        total = c.execute(f"SELECT total FROM {cit}_neg_{i}")
        total_num = total.fetchone()[0]
        score = total_num/count_num
        scores[f'{cit}_{i}'].append(score * -1)
    return scores

def display_all_scores_indidivual(cit):
    img = BytesIO()
    data = get_all_scores_individual(cit)
    df = pd.DataFrame.from_dict(data, orient='index', columns = ['positive','negative'])
    df.plot(y = ['positive', 'negative'], kind="bar", alpha=0.75, rot=0, fontsize=5)
    plt.savefig(img, aspect = 'auto', format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url
