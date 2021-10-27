from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from twilio.rest import Client

import pandas as pd
import time
import datetime
import sys
import os


browser = webdriver.Chrome(executable_path=r'C:/Users/jpnts/Downloads/chromedriver_win32/chromedriver.exe')

# options = Options()
# options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
# options.add_argument('--disable-gpu')
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# options.add_argument('--no-sandbox')

# browser = webdriver.Chrome(executable_path='/app/.chromedriver/bin/chromedriver', options=options)

# browser.maximize_window()
# time.sleep(30)

return_ticket = "//label[@id='flight-type-roundtrip-label-hp-flight']"
one_way_ticket = "//label[@id='flight-type-one-way-label-hp-flight']"

def choose_ticket(ticket):

    try:
        ticket_type = browser.find_element_by_xpath(ticket)
        ticket_type.click()
    except Exception as e:
        pass

def dep_country_chooser(dep_country):
    from_src = browser.find_element_by_xpath("//input[@id='flight-origin-hp-flight']")
    time.sleep(1)
    from_src.clear()
    time.sleep(1.5)
    from_src.send_keys('  ' + dep_country)
    time.sleep(1.5)
    first_choice = browser.find_element_by_xpath("//a[@id='aria-option-0']")
    time.sleep(1.5)
    first_choice.click()

def arrival_country_chooser(arr_country):
    to_dst = browser.find_element_by_xpath("//input[@id='flight-destination-hp-flight']")
    time.sleep(1)
    to_dst.clear()
    time.sleep(1.5)
    to_dst.send_keys('  ' + arr_country)
    time.sleep(1.5)
    first_choice = browser.find_element_by_xpath("//a[@id='aria-option-0']")
    time.sleep(1.5)
    first_choice.click()

def date_chooser(month,day,year):

    dep_date = browser.find_element_by_xpath("//input[@id='flight-departing-hp-flight']")
    dep_date.clear()
    dep_date.send_keys(month+ '/'+day+'/'+year)

def return_chooser(month,day,year):

    return_date = browser.find_element_by_xpath("//input[@id='flight-returning-hp-flight']")
    for i in range(11):
        return_date.send_keys(Keys.BACKSPACE)
    return_date.send_keys(month + '/' + day + '/' + year)

def search():
    search = browser.find_element_by_xpath("//button[@class='btn-primary btn-action gcw-submit']")
    search.click()
    time.sleep(15)
    bags = browser.find_elements_by_xpath("//span[@class='show-flight-details']")
    for i in bags:
        i.click()
        time.sleep(2)
    time.sleep(15)

    print("results ready!")
    print("You will recieve message alerts when the price drops!!")


df = pd.DataFrame()

def compile_data():
    global df
    global dep_times_list
    global arr_times_list
    global airlines_list
    global price_list
    global durations_list
    global stops_list
    global layovers_list

    
    #departure times
    let index = []
    dep_times = browser.find_elements_by_xpath("//span[@data-test-id='departure-time']")
    dep_times_list = [value.text for value in dep_times]
    #arrival times
    arr_times = browser.find_elements_by_xpath("//span[@data-test-id='arrival-time']")
    arr_times_list = [value.text for value in arr_times]
    #airline name
    airlines = browser.find_elements_by_xpath("//span[@data-test-id='airline-name']")
    airlines_list = [value.text for value in airlines]
    #prices
    prices = browser.find_elements_by_xpath("//span[@data-test-id='listing-price-dollars']")
    price_list = [value.text for value in prices]
    #durations
    durations = browser.find_elements_by_xpath("//span[@data-test-id='duration']")
    durations_list = [value.text for value in durations]
    #stops
    stops = browser.find_elements_by_xpath("//span[@class='number-stops']")
    stops_list = [value.text for value in stops]
    #baggage info 
    carry_on = browser.find_elements_by_xpath("//*[@id='section-offer-leg0-details']/div/div[4]/dl/dd[2]/table/tbody/tr[1]/td[2]")
    bag_1 = browser.find_elements_by_xpath("//*[@id='section-offer-leg0-details']/div/div[4]/dl/dd[2]/table/tbody/tr[2]/td[2]")
    bag_2 = browser.find_elements_by_xpath("//*[@id='section-offer-leg0-details']/div/div[4]/dl/dd[2]/table/tbody/tr[3]/td[2]")
    carry_list = [value.text for value in carry_on]
    bag1_list = [value.text for value in bag_1]
    bag2_list = [value.text for value in bag_2]
    print(bag1_list)
    #layovers
    layovers = browser.find_elements_by_xpath("//span[@data-test-id='layover-airport-stops']")
    layovers_list = [value.text for value in layovers]
    now = datetime.datetime.now()
    current_date = (str(now.year) + '-' + str(now.month) + '-' + str(now.day))
    current_time = (str(now.hour) + ':' + str(now.minute))
    current_price = 'price' + '(' + current_date + '---' + current_time + ')'
    for i in range(len(dep_times_list)):
        try:
            df.loc[i, 'departure_time'] = dep_times_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'arrival_time'] = arr_times_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'airline'] = airlines_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'duration'] = durations_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'stops'] = stops_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'layovers'] = layovers_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, str(current_price)] = price_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'carryon'] = carry_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'bag_1'] = bag1_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'bag_2'] = bag2_list[i]
        except Exception as e:
            pass

    print('Excel Sheet Created!')

def main():
    for i in range(8):    
        print("Welcome Mr. Singh! Tickets are on me!")
        time.sleep(1)
        print("Connecting to Expediaaaa dum dum!!")
        link = 'https://www.expedia.com/'
        browser.get(link)
        time.sleep(5)
        #choose flights only
        flights_only = browser.find_element_by_xpath("//button[@id='tab-flight-tab-hp']")
        flights_only.click()
        print("switching to flights coz you not homeless")
        choose_ticket(return_ticket)
        dep_country_chooser('hou')
        print("going from DC huh niiice!")
        arrival_country_chooser('abq')
        print("going to dilllli aaye!")
        date_chooser('01', '17', '2020')
        print("setting your date")
        return_chooser('01', '20', '2020')
        print("sort let me get some results for you chill back and relax!")
        search()
        compile_data()
        #save values for email
        
        # option 1
        current_values_1 = df.iloc[0]
        cheapest_dep_time_1 = current_values_1[0]
        cheapest_arrival_time_1 = current_values_1[1]
        cheapest_airline_1 = current_values_1[2]
        cheapest_duration_1 = current_values_1[3]
        cheapest_stops_1 = current_values_1[4]
        cheapest_price_1 = current_values_1[6]
        carry_on_1 = current_values_1[-1]
        bag_1 = current_values_1[7]
        bag_2_1 = current_values_1[8]
        # option 2
        current_values_2 = df.iloc[1]
        cheapest_dep_time_2 = current_values_2[0]
        cheapest_arrival_time_2 = current_values_2[1]
        cheapest_airline_2 = current_values_2[2]
        cheapest_duration_2 = current_values_2[3]
        cheapest_stops_2 = current_values_2[4]
        cheapest_price_2 = current_values_2[6]
        carry_on_2 = current_values_2[-1]
        bag_2 = current_values_2[7]
        bag_2_2 = current_values_2[8]

        # option 3
        current_values_3 = df.iloc[2]
        cheapest_dep_time_3 = current_values_3[0]
        cheapest_arrival_time_3 = current_values_3[1]
        cheapest_airline_3 = current_values_3[2]
        cheapest_duration_3 = current_values_3[3]
        cheapest_stops_3 = current_values_3[4]
        cheapest_price_3 = current_values_3[6]
        carry_on_3 = current_values_3[-1]
        bag_3 = current_values_3[7]
        bag_2_3 = current_values_3[8]

        print('run {} completed!'.format(i))
        # create_msg()
        # connect_mail(username,password)
        # send_email(msg)
        # print('Email sent!')
        # account_sid = 'AC55ded024cf2a4d908a229b5d57541789'
        # auth_token = '992e11b7142215812c67daba56539bb2'
        client = Client(account_sid, auth_token)
        msg = '\nCurrent Cheapest flights:\n\n Option 1 \n\n Departure time: {}\nArrival time: {}\nAirline: {}\nFlight duration: {}\nNo. of stops: {}\nPrice: {}\nCarry_On: {}\nCheck-In1: {}\nCheck-In2: {} \n \n Option 2 \n\n Departure time: {}\nArrival time: {}\nAirline: {}\nFlight duration: {}\nNo. of stops: {}\nPrice: {}\nCarry_On: {}\nCheck-In1: {}\nCheck-In2: {}\n \nOption 3 \n\n Departure time: {}\nArrival time: {}\nAirline: {}\nFlight duration: {}\nNo. of stops: {}\nPrice: {}\nCarry_On: {}\nCheck-In1: {}\nCheck-In2: {}\n End of messages, Server going to Sleep'.format(cheapest_dep_time_1,
                       cheapest_arrival_time_1,
                       cheapest_airline_1,
                       cheapest_duration_1,
                       cheapest_stops_1,
                       cheapest_price_1,
                       carry_on_1,
                       bag_1,
                       bag_2_1,
                       cheapest_dep_time_2,
                       cheapest_arrival_time_2,
                       cheapest_airline_2,
                       cheapest_duration_2,
                       cheapest_stops_2,
                       cheapest_price_2,
                       carry_on_2,
                       bag_2,
                       bag_2_2,
                       cheapest_dep_time_3,
                       cheapest_arrival_time_3,
                       cheapest_airline_3,
                       cheapest_duration_3,
                       cheapest_stops_3,
                       cheapest_price_3,
                       carry_on_3,
                       bag_3,
                       bag_2_3
                       )

        message = client.messages \
                .create(
                     body=msg,
                     from_='+12028757729',
                     to='+12036902147'
                 )

        print(message.sid)
        df.to_excel('flights.xlsx')
        time.sleep(3600)

main()