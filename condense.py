'''ATTENTION: This is a janky solution that I will eventually clean up. For the purpose of having a little prototype/demo of my solution
I basically just created a bunch of keyword 'sets' (so that homogenous keywords can go into the database). Eventually I will implement some kind 
of NLP to recognise synonyms.
'''

'''UPDATE: Having run the function with loops, it was finickity and produced unreliable results. 
Also, the best performance I could get was cubic efficiency, which means it was slow and inefficient. 
A big if-else ladder may be cumbersome to write, but at least it's more or less linear'''

sales_staff = {'staff', 'crew', 'guy', 'salesman', 'sales staff', 'team', 'employee'}
mechanic = {'mechanic', 'mechanics'}
customer_service = {'customer service', 'service', 'rude','friendly','helpful'}
car_quality = {'car'}
car_price = {'price', 'cost', 'cheap', 'expensive'}
customer_experience = {'experience','time'} 
payment_options = {'pay', 'payment'} 
online_services = {'site', 'website', 'online', 'app'}
insurance = {'insurance', 'policy', 'premiums'}

#A function to create a new list with the 
#first three (location, overall score and count) entries INTACT. 

def fresh_list(ls):
    new_list = []
    for i in range(0,3):
        new_list.append(ls[i])
    return new_list

def traverse(raw, collection):
    raw = set(raw.split(' '))
    result = raw & collection
    if result:
        return True
    return False



#A function which creates all remaining entries in the new_list
#with proper names that can be stored in a database

def update(old_list, new_list):
    for i in range(3, len(old_list)):
        key = list(old_list[i].keys())[0]
        value = list(old_list[i].values())[0]
        print(key, value)
        #If key in sales_staff
        if traverse(key, sales_staff):
            new_list.append({'sales_staff':value})
        #if key in mechanic
        elif traverse(key, mechanic):
            new_list.append({'mechanic':value})
        #if key in customer_service
        elif traverse(key, customer_service):
            new_list.append({'customer_service':value})
        #if key in car_price
        elif traverse(key, car_price):
            new_list.append({'car_price':value})
        #if key in car_quality
        elif traverse(key, car_quality):
            new_list.append({'car_quality':value})
        #if key in customer_experience
        elif traverse(key, customer_experience):
            new_list.append({'customer_experience':value})
        #if key in payment_options
        elif traverse(key, payment_options):
            new_list.append({'payment_options':value})
        #if key in online_services
        elif traverse(key, online_services):
            new_list.append({'online_services':value})
        elif traverse(key, insurance):
            new_list.append({'insurance':value})
        else:
            pass
    return new_list

#main method which takes the old list, calls the fresh_list function on it to 
#create a new list, then calls update on new/old list to create a new list of updated values

def main(lst):
    empty = fresh_list(lst)
    updated = update(lst, empty)
    return updated

