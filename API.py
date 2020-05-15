# Final Project Intermediate Python
# Lfaliven - fbeltran - mbinoiad
# Lucas Falivene
# Fabio Beltran Vasquez
# Muhammad Bin Oiad

#imports
import requests
import os
import matplotlib.pyplot as plt
import re
import sqlite3
from datetime import datetime

# API patterns listing
P_LISTn = ['P_CONFIRMED', 'P_DEATHS','P_LAST_UPDATE']
P_LISTv = [r'confirmed": ',r'deaths": ',r'last_update": ']

 #%%

# functions definitions
    
# Checks user input related to states and counties
# Retries for user input until a valid state is entered
# Retries for user input until a probable valid county is entered (we will check later if county is valid by cheking if API reply is or not null)
# As parameters we entered the user input (state and county)
# Retunrs user input clean (after being checked)
def CHECK_INPUT(user_input, state, county):
    states = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','District of Columbia','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming']
    if state == 1:
        user_input = user_input.title()
        while user_input not in states: # Checks user input against state list
            user_input = input("*** ERROR *** Wrong input. \nPlease enter a US state: ")
            user_input = user_input.title()
        return user_input
    elif state == 0 and county == 1:
        pattern = r"[0-9]|\&|\!|\*|\(|\)|\#|\$|\%"
        while re.search(pattern, user_input) != None: # Checks for probable bad county input
            user_input = input("*** ERROR *** Wrong input. \nPlease enter a US county: ")
            # Convert only first letter capital and the rest non capital letters
        user_input = user_input.title()
        clean_input = user_input
        return clean_input
 #%%
# Checks user option for yes or no instances
# If option is not similar to yes or no, iterates until getting a good input
# A parameter today is entered to the function, that is the user input for the no/yes question
# Returns yes or no option but after validating user inmput
def CHECK_OPTION(today):
    option = -1
    while option == -1:
        if today.lower() in ['yes','y','ye']:
            option = 1
        elif today.lower() in ['no','n']:
            option = 0
        else:
            print("*** INVALID OPTION ENTERERED ***")
            today = input('Input yes or no: ')
    return option
 #%%
# Checks if current year is or not leap
# When looking on the first of march for data we will need to know if the previous day was 28 or 29
# Returns 1 if leap year or 0 if not
def CHECK_LEAP_YEAR(year):
    year = int(year)
    if year % 4 == 0 and year % 100 !=0:
        return 1
    elif year % 400 == 0:
        return 1
    else:
        return 0
 #%%
# When looking for the last update data we must search for yesterdays info
# As info is generally updated over night at GMT timezone
#Todays date (or date input by user) is input as parameter of this function
#Returns yesterday's date
def GET_YESTERDAY(date):
    day = date[8:]
    month = date[5:7]
    year = date[:4]
    if day == '01':
        if month in ['01','02','04','06','08','09','11']: # Only their previous months have 31 days
            date = date[:8] + '31'
        elif month == '02':
            if CHECK_LEAP_YEAR(year) == 1:
                date = date[:8] + '29' # Only if leap year february has 29 days
            else:
                date = date[:8] + '28'
        else:
            date = date[:8] + '30' #The rest of the months will have 30 days
    else:
        day = str(int(day)-1) # We are looking for yesterday's day number
        if len(day) == 1:
            day = '0' + day
        date = date[:8] + day
    return date
 #%%
#Month and day input as entered as parameters of the function
#Checks user month and day input to be valid
# Returns date clean of user errors
def DATE_CHECK(month,day):
    #Checks month
    if len(month) > 2 or len(month) == 0:
        while len(month) > 2 or len(month) == 0:
            print('*** you entered an invalid month value ***')
            month = input('Input month in numbers: ')
    elif len(month) == 1:
        montht = datetime.today().strftime('%m')
        while int(month) > int(montht) and (len(month) > 2 or len(month) == 0)or not isinstance(int(month), int) or int(month) < 1 or int(month) > 12: # the scope of this app is until december 2020, after that we should include the input of the year by the user and check to input be greater than jan 2020 and less than today
            month = input('Data is only available since January 2020 up to present.\nInput a valid month number: ')
        month = '0' + str(month)
    #Checks day input
    if len(day) > 2 or len(day) == 0 or int(day) > 31 or int(day) < 1 or not isinstance(int(day), int):
        while len(day) > 2 or len(day) == 0:
            print('**** you entered an invalid day value ****')
            day = input('Input day: ')
    elif len(day) == 1:
        day = '0' + str(day)
    date = '2020' + '-' + month + '-' + day
    return date
 #%%
#Searches for a defined set of patterns within the API reply
# The idea is to  retrieve the relevant data form the API
#Patterns and API reply as entered as parameters of the function
# Returns the lines wheer a match is found
def PATTERN_SEARCH(pattern,text): 
    lines = list()
    text_split = text.split(',')
    for line in text_split:
        if re.search(pattern,line) != None:
            lines.append(line)
    return lines
 #%%
#Splits the API response in order to only store the number of cases or deths (or last update) as a variable
#The lines from the API reply that we are interested and a counter of them reply as entered as parameters of the function
# Returns values for state (first) and for county (Second) of each relevant API reply
def SPLITT(lines,counter):
    #Searches for state info
    search = lines[0].split('": ')
    i = search[1]
    if counter == 0 or counter == 1:
        first = int(i)
    else: 
        first = i
    #Searches for county info
    search2 = lines[1].split('": ')
    j = search2[1]
    if counter == 0 or counter == 1:
        second = int(j)
    else:
        second = j
    return first, second
 #%%
# Stores graphs in the current directory
# Has aprameters with all the necesary data to build the graph (z,xlabel,ylabel, x data, y data, graph name)
# Does not reutn any values
def STORE_GRAPH(z,xlabel,ylabel, x, y, name):
    plt.title(z)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.bar(x,y)
    plt.savefig(name)
    plt.clf()
 #%%
# Stores all data related to the US county query through the API in the database
# Creates database if not exists and stores interesting replies from the API
#All data to be stored as entered as parameters of the  (all the data relevant that was extracted from the API reply)
# No return values by the function
def STORE_DB(county, state, county_confirmed, state_confirmed, county_deaths, state_deaths, county_lastup, state_lastup):
    county = county.title()
    state = state.title()
    working_directory = os.getcwd()
    working_directory = working_directory.replace('\\','/')
    #Check if database exist
    if os.path.exists(working_directory+'/us_covid_db.sqlite3') == False:
        print('\nCreating database...')
        connection = sqlite3.connect('us_covid_db.sqlite3')
        cursor = connection.cursor( )
        creation_commands = list()
        sqlite_table_creator = 'CREATE TABLE IF NOT EXISTS COUNTY (COUNTY VARCHAR2(30), STATE VARCHAR2(30),  CONFIRMED_CASES NUMBER(20), DEATHS NUMBER(20), DATE_UPDATE VARCHAR2(12));'
        creation_commands.append(sqlite_table_creator)
        sqlite_table_creator = 'CREATE TABLE IF NOT EXISTS STATE (STATE VARCHAR2(30),  CONFIRMED_CASES NUMBER(20), DEATHS NUMBER(20), DATE_UPDATE VARCHAR2(12));'
        creation_commands.append(sqlite_table_creator)
        for command in creation_commands:
            cursor.execute(command)    
        connection.commit()
    else:
        print('\nAccesing database...')
        connection = sqlite3.connect('us_covid_db.sqlite3')
        cursor = connection.cursor( )
    update_commands = list()
    insert_command = 'INSERT INTO COUNTY VALUES ("%s", "%s", %d, %d, "%s");' %(county,state,county_confirmed, county_deaths, county_lastup)    
    update_commands.append(insert_command)
    insert_command2 = 'INSERT INTO STATE VALUES ("%s", %d, %d, "%s");' %(state,state_confirmed, state_deaths, state_lastup)    
    update_commands.append(insert_command2)
    for command in update_commands:
        cursor.execute(command)    
    connection.commit()
    connection.close()
    print('\nAll data stored in database')
 #%%
# Calls API, gets reply and process it 
# Prints API reply data and creates graphs for county vs state comparisson
# Gets entered as parameters the county, state, taody's date and if we are or not comparying two states (boolean)
# Returns value for county (Cases, death and last update date)    
def API_CITY(county,state,today,comparee):
    if today == 1: #If we want to search for yesterdays info
        date = datetime.today().strftime('%Y-%m-%d')
        date1 = GET_YESTERDAY(date)
    else: # User wants to search for specific date
        print('\nWhat is the date you want to search for?')
        month = input('Input month in numbers: ')
        day = input('Input day: ')
        date1 = DATE_CHECK(month,day)
    print("\nObtaining " + county + " data from API...")
    url = "https://covid-19-statistics.p.rapidapi.com/reports"
    q_state = "US " + state
    querystring = {"region_province":state,"iso":"USA","region_name":"US","city_name":county,"date":date1,"q":q_state}
    headers = {'x-rapidapi-host': "covid-19-statistics.p.rapidapi.com", 'x-rapidapi-key': "faa4db15d0msh471f8c6026d4b5bp1992c2jsn16ad20733bfe"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    text = response.text
    #Checks if county inputed by user is or not valid (API response will be short <20 if county is not valid)
    out = 0
    while text == None or len(text) < 20:
        print('\n*** ERROR *** You either input an invalid county name or there is no data available for that county at your specified date')
        out = 1
        break
    if out != 1:
        counter = -1
        for pattern in P_LISTv: #Processes API reply
            counter = counter + 1
            lines = PATTERN_SEARCH(pattern,text)
            first, second = SPLITT(lines,counter)
            if counter == 0:
                state_confirmed = int(first)
                county_confirmed = int(second)
            elif counter == 1:
                state_deaths = int(first)
                county_deaths = int(second)
            else:
                state_lastup = first
                county_lastup = second
        # Prints county and state info
        print()
        print('COVIDaily for ' + county + ' in the state of ' + state)
        print('Confirmed cases in ' + county + ': ' + str(county_confirmed))
        print('Deaths in ' + county + ': ' + str(county_deaths))
        print('Last updated: ' + county_lastup[1:20] + ' GMT')
        print()
        print('State information')
        print('Confirmed cases in ' + state + ': ' + str(state_confirmed))
        print('Deaths in ' + state + ': ' + str(state_deaths))
        print('Last updated: ' + state_lastup[1:20] + ' GMT')
        
        # Only returns values if we are comparying two counties
        if comparee == 1:
            return county_confirmed, county_deaths, county
        else: # If not comparing create graphs
            print("\nPrinting graphs....")
            z = 'COVID confirmed cases in ' + county + ' and ' + state
            plt.title(z)
            plt.xlabel(str(county_confirmed)+' County vs '+ str(state_confirmed) +' State')
            plt.ylabel('Confirmed cases')
            x = [county,state]
            y = [county_confirmed, state_confirmed]
            plt.bar(x,y)
            plt.show()
            save_figure = input(str('Do you want to save the confirmed cases graph? type y or n: '))
            option = CHECK_OPTION(save_figure)
            if option == 1:
                name = county + '_COVID_confirmed_cases.png'
                x = [county,state]
                y = [county_confirmed, state_confirmed]
                xlabel = str(county_confirmed)+' County vs '+ str(state_confirmed) +' State'
                ylabel = 'Confirmed cases'
                STORE_GRAPH(z,xlabel,ylabel, x, y, name)    
            elif option == 0:
                print('no problem')
            z = 'COVID related deaths in ' + county + ' and ' + state
            plt.title(z)
            plt.xlabel(str(county_deaths)+' County vs '+ str(state_deaths) +' State')
            plt.ylabel('Confirmed deaths')
            x = [county,state]
            y = [county_deaths, state_deaths]
            plt.bar(x,y)
            plt.show()
            save_figure = input(str('Do you want to save the confirmed deaths grpah? type y or n: '))
            option = CHECK_OPTION(save_figure)
            if option == 1:
                name = county +'_COVID_deaths.png'
                x = [county,state]
                y = [county_deaths, state_deaths]
                xlabel = str(county_deaths)+' County vs '+ str(state_deaths) +' State'
                ylabel = 'Confirmed deaths'
                STORE_GRAPH(z,xlabel,ylabel, x, y, name)  
            elif option == 0:
                print('no problem')
            save_db = input(str('Do you want to save the info in the database? type y or n: '))
            option = CHECK_OPTION(save_db)
            if option == 1:
                county_lastup = county_lastup[1:20]
                state_lastup = state_lastup[1:20]
                STORE_DB(county, state, county_confirmed, state_confirmed, county_deaths, state_deaths, county_lastup, state_lastup)
            elif option == 0:
                print('no problem')
         #%%
# Creates grpahs for the comparison of cases and deaths of two US counties
# Parameters related to counties compared and their data are entered to the function
# No returns values for the function
def GRAPHS(county1_conf, county1_dead, county2_conf, county2_dead, county1, county2):
    print("\nPrinting graphs....")
    z = 'Comparison confirmed cases in ' + county1 + ' and ' + county2
    plt.title(z)
    plt.xlabel(str(county1_conf)+ ' ' + county1 + ' vs ' + str(county2_conf) + ' ' + county2 )
    plt.ylabel('Confirmed cases')
    x = [county1,county2]
    y = [county1_conf, county2_conf]
    plt.bar(x,y)
    plt.show()
    save_figure = input(str('Do you want to save the confirmed cases graph? type y or n: '))
    if save_figure.lower() == 'y':
        xlabel = str(county1_conf)+ ' ' + county1 + ' vs ' + str(county2_conf) + ' ' + county2 
        ylabel = 'Confirmed cases'
        x = [county1,county2]
        y = [county1_conf, county2_conf]
        name = county1 + ' vs ' + county2 + '_confirmed_cases.png'
        STORE_GRAPH(z,xlabel,ylabel, x, y, name) 
    elif save_figure.lower() == 'n':
        print('no problem')
    z = 'Comparison deaths in ' + county1 + ' and ' + county2
    plt.title(z)
    plt.xlabel(str(county1_dead)+ ' ' + county1 + ' vs ' + str(county2_dead) + ' ' + county2 )
    plt.ylabel('Confirmed deaths')
    x = [county1,county2]
    y = [county1_dead, county2_dead]
    plt.bar(x,y)
    plt.show()
    save_figure = input(str('Do you want to save the confirmed deaths grpah? type y or n: '))
    if save_figure.lower() == 'y':
        xlabel = str(county1_dead)+ ' ' + county1 + ' vs ' + str(county2_dead) + ' ' + county2 
        ylabel = 'Confirmed deaths'
        x = [county1,county2]
        y = [county1_dead, county2_dead]
        name = county1 + ' vs ' + county2 + '_COVID_deaths.png'
        STORE_GRAPH(z,xlabel,ylabel, x, y, name)
    elif save_figure.lower() == 'n':
        print('no problem')
 #%%
# Shows the quick global info that can be obtained form the API (toatl confirmed cases, deaths, recovered and last update of this info)
# No parameters entered for this function
# No returns values for the function
def QUICK_INFO():
    print("\nObtaining data from API...")
    #Calls API
    url = "https://covid-19-statistics.p.rapidapi.com/reports/total"
    date = datetime.today().strftime('%Y-%m-%d')
    date1 = GET_YESTERDAY(date)
    querystring = {"date":date1}
    headers = {'x-rapidapi-host': "covid-19-statistics.p.rapidapi.com",'x-rapidapi-key': "faa4db15d0msh471f8c6026d4b5bp1992c2jsn16ad20733bfe"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    text = response.text
    texts = text.split('confirmed": ')
    confs = texts[1].split(',')
    confirmed = confs[0]
    print('\nTotal confirmed cases globally: ' + confirmed)
    # Gets total deaths number
    texts = text.split('deaths": ')
    confs = texts[1].split(',')
    deaths = confs[0]
    print('\nTotal deaths globally: ' + deaths)
    # Gets total recovered cases number
    texts = text.split('recovered": ')
    confs = texts[1].split(',')
    recover = confs[0]
    print('\nTotal recoveries globally: ' + recover)
    # Gets total active cases number
    texts = text.split('active": ')
    confs = texts[1].split(',')
    active = confs[0]
    print('\nTotal active cases globally: ' + active)
    # Gets fatality ratee\ number
    texts = text.split('fatality_rate": ')
    confs = texts[1].split(',')
    fatality = confs[0]
    print('\nGlobal fatality rate: ' + fatality[:6])
    # Gets last update date of the previous information
    texts = text.split('last_update": ')
    confs = texts[1].split(',')
    last_up = confs[0]
    print('\nLast update: ' + last_up[1:20] + ' GMT')