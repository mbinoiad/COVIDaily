# Final Project Intermediate Python
# Snake Coders 
# Lucas Falivene - Lfaliven
# Fabio Beltran Vasquez - fbeltran
# Muhammad Bin Oiad - mbinoiad


import urllib.request
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import sqlite3

#%%
#This function will obtain the current working directory for download purposes
def workingDirectory():
    working_directory = os.getcwd()
    working_directory = working_directory.replace('\\','/')
    return working_directory


#%%
#This function will verify if the files' URLs are reachable to be downloaded later     
def verifyConnection():

    url_confirmed = 'https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv'
    url_deaths ='https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_deaths_global.csv&filename=time_series_covid19_deaths_global.csv'
    url_recovered = 'https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_recovered_global.csv&filename=time_series_covid19_recovered_global.csv'
    
    #try to reach out to the urls to get http codes i.e. 200, 404
    try:
        a = urllib.request.urlopen(url_confirmed).getcode() 
        b = urllib.request.urlopen(url_deaths).getcode()
        c = urllib.request.urlopen(url_recovered).getcode() 
    
    #if codes aren't obtainable it'll set all to zero
    except:
        print('There must be something wrong with the internet connection')
        a = b = c = 0
    return a, b, c, url_confirmed, url_deaths, url_recovered


#%%
#This function will try to obtain the datasets from the internet
def downloadFiles(a,b,c,url_confirmed, url_deaths,url_recovered, working_directory):

    #verifies if  the codes are OK success    
    if a and b and c == 200: 
        
        #download all three files to the working directory
        urllib.request.urlretrieve(url_confirmed, working_directory+'/time_series_covid19_confirmed_global.csv')
        urllib.request.urlretrieve(url_deaths, working_directory+'/time_series_covid19_deaths_global.csv')
        urllib.request.urlretrieve(url_recovered, working_directory+'/time_series_covid19_recovered_global.csv')
            
        print('updated files are in your working directory')
    
    #the codes are 400, 403, 404...etc.       
    elif a and b and c != 0:
        print('There must be something wrong with the website, will look up the file in the working directory')
        
    else:
        print('There must be something wrong with your internet, will look up the file in the working directory')


#%%
#This function will try to open the files that have been downloaded or pre-downloaded
def openFiles():
    #tries to open the three datasets and load them into dataframes
    try:
        with open('time_series_covid19_confirmed_global.csv', 'r') as c, open('time_series_covid19_deaths_global.csv', 'r') as d, open('time_series_covid19_recovered_global.csv', 'r') as r:
            covid_confirmed = pd.read_csv(c)
            covid_deaths = pd.read_csv(d)
            covid_recovered = pd.read_csv(r)
            
        return covid_confirmed, covid_deaths, covid_recovered
    
    #instructs the user to fetch the files manually, if the internet/website is down and file aren't in his directory
    except FileNotFoundError:
        print('the file weren\'t found, please get the files manually at ')
        print('https://data.humdata.org/dataset/novel-coronavirus-2019-ncov-cases')
        
    
        


#%%
#This function will clean up the values and field in the 3 datasets
def cleanUpDFs(covid_confirmed, covid_deaths, covid_recovered):
    
    #replace any empty fields with NA and cleans up the dataframes
    covid_confirmed = covid_confirmed.replace(np.nan, 'NA')
    covid_deaths = covid_deaths.replace(np.nan, 'NA')
    covid_recovered = covid_recovered.replace(np.nan, 'NA')

    covid_confirmed.drop(['Lat','Long'], axis=1, inplace=True)
    covid_deaths.drop(['Lat','Long'], axis=1, inplace=True)
    covid_recovered.drop(['Lat','Long'], axis=1, inplace=True)
    
    covid_confirmed.rename({'US':'United States of America'}, inplace = True)
    covid_deaths.rename({'US':'United States of America'}, inplace = True)
    covid_recovered.rename({'US':'United States of America'}, inplace = True)

    #Sums up the daily stats based on Country/Region name into three new dataframes
    confirmed_covid_data = covid_confirmed.groupby('Country/Region').aggregate(np.sum)
    deaths_covid_data = covid_deaths.groupby('Country/Region').aggregate(np.sum)
    recovered_covid_data = covid_recovered.groupby('Country/Region').aggregate(np.sum)
    
    return confirmed_covid_data, deaths_covid_data, recovered_covid_data

 
#%%
#This function will create a new dataset that stores the total of active cases by calculating the 3 main dataset parameters
def createActiveCovidDF(confirmed_covid_data, deaths_covid_data, recovered_covid_data):
    
    active_covid_data = confirmed_covid_data.copy()
    
    for i in range(len(active_covid_data)):
        active_covid_data.iloc[i] = confirmed_covid_data.iloc[i] - deaths_covid_data.iloc[i] - recovered_covid_data.iloc[i]
    
    return active_covid_data

 
#%%
#This function will alter user input if needed i.e. united STATES Of America => United States of America
def fixUserInput(country):
    
    exceptions = ['and', 'the', 'of']  
    country_all = re.split(' ', country)
    proper_country = list()
    proper_country += [word if word in exceptions else word.capitalize() for word in country_all]
    proper_country = " ".join(proper_country)

    return proper_country

 
#%%
#This function will plot, and save if requested, the active COVID cases over time for the desired country's data
def getAndSavePlotAndActiveStats(proper_country, active_covid_data):
    
    #checks if the entered country name is in the dataset
    if proper_country in active_covid_data.index:
        x=('Active COVID cases in %s' %proper_country)
        plt.title(x)
        plt.xlabel('Dates')
        plt.ylabel('Active Cases')
        plt.xticks(np.arange(len(active_covid_data.columns), step=(len(active_covid_data.columns)//5)))
        
        plt.plot(active_covid_data.columns,active_covid_data.loc[proper_country],color = 'red', linestyle='--',linewidth=3)
        plt.show()
       
        print('\nThe current active number of cases in %s is: %d' %(proper_country, active_covid_data.loc[proper_country][len(active_covid_data.columns)-1]))

        save_figure = input(str('Do you want to save the figure? type y or n: '))
        
        if save_figure.lower() == 'y':
            plt.title(x)
            plt.xlabel('Dates')
            plt.ylabel('Active Cases')
            plt.xticks(np.arange(len(active_covid_data.columns), step=(len(active_covid_data.columns)//5)))
            plt.plot(active_covid_data.columns,active_covid_data.loc[proper_country],color = 'red', linestyle='--',linewidth=3)
            plt.savefig('%s_Active_Covid.png' %proper_country)  
            plt.clf()
        elif save_figure.lower() == 'n':
            print('\nNo problem')
            
        else:
            print('%s is not a valid option, we will assume that you don\'t want to save the figure' %save_figure)

    else:
        print('it seems that this country hasn\t been infected by COIVD-19 yet')
        

#%%
#This function will create or update the sqlite db in the working directory    
def saveSqliteDB(working_directory, active_covid_data, confirmed_covid_data, deaths_covid_data, recovered_covid_data):
    
    DB_name = input(str('\nPlease enter the name of the sqlite DB you want to create/update: '))

    if '.sqlite3' not in DB_name:
        DB_name = DB_name+'.sqlite3' 
        

    
    #checks if the DB doesn't exists in the working directory, if so it creates the DB
    if os.path.exists(working_directory+'/'+DB_name) == False:

        connection = sqlite3.connect(DB_name)
        cursor = connection.cursor( )
        
        #creates the commands list and adds the DB table creation command to it
        creation_commands = list()
        sqlite_table_creator = 'CREATE TABLE IF NOT EXISTS COVID_DATA (COUNTRY VARCHAR2(20) NOT NULL PRIMARY KEY, CONFIRMED_CASES NUMBER(20), DEATHS NUMBER(20), RECOVERED NUMBER(20), ACTIVE NUMBER(20));'
        creation_commands.append(sqlite_table_creator)
        
        #iterates over the datasets to create the sqlite commands to create the entries (country name, confirmed, deaths recovered and active cases)
        for i in range(len(active_covid_data)):
            total_columns = len(active_covid_data.columns)
            country = active_covid_data.index[i]
            confirmed = confirmed_covid_data.iloc[i][total_columns-1]
            deaths = deaths_covid_data.iloc[i][total_columns-1]
            recovered = recovered_covid_data.iloc[i][total_columns-1]
            active = active_covid_data.iloc[i][total_columns-1]
            data_command = 'INSERT INTO COVID_DATA VALUES ("%s", %d, %d, %d, %d);' %(country,confirmed,deaths,recovered,active)
            creation_commands.append(data_command)
        
        #iterates over the commands list and execute them accordingly. Then, saves the changes
        for command in creation_commands:
            cursor.execute(command)    
        connection.commit()
        connection.close()
    
    #if the DB already exists in the working directory, then it'll update it by updating existing entries, or adding new ones if they don't exist
    else:
        connection = sqlite3.connect(DB_name)
        cursor = connection.cursor( )
        
        update_commands = list()
        for i in range(len(active_covid_data)):
            total_columns = len(active_covid_data.columns)
            country = active_covid_data.index[i]
            confirmed = confirmed_covid_data.iloc[i][total_columns-1]
            deaths = deaths_covid_data.iloc[i][total_columns-1]
            recovered = recovered_covid_data.iloc[i][total_columns-1]
            active = active_covid_data.iloc[i][total_columns-1]
            
            
            countryexists_command = 'SELECT EXISTS(SELECT 1 FROM COVID_DATA WHERE COUNTRY="%s");' %country
            cursor.execute(countryexists_command)
            answer, = cursor.fetchone()
    
            if answer == 0:
                insert_command = 'INSERT INTO COVID_DATA VALUES ("%s", %d, %d, %d, %d);' %(country,confirmed,deaths,recovered,active)    
                update_commands.append(insert_command)
                                    
            elif answer == 1:
                update_command = 'UPDATE COVID_DATA SET CONFIRMED_CASES = %d , DEATHS = %d , RECOVERED = %d , ACTIVE = %d WHERE COUNTRY = "%s"' %(confirmed,deaths,recovered,active,country)
                update_commands.append(update_command)   
        
        for command in update_commands:
            cursor.execute(command)    
        connection.commit()
        connection.close()


#%%        
#This function will create and save the new Dataframe which contains current confirmed, deaths, recovered and active COVID cases per country  
def createandSaveFinalDF (active_covid_data, confirmed_covid_data, deaths_covid_data, recovered_covid_data):
    
    allinfo=list()
    
    for i in range(len(active_covid_data)):
        total_columns = len(active_covid_data.columns)
        
        country = active_covid_data.index[i]
        confirmed = confirmed_covid_data.iloc[i][total_columns-1]        
        deaths = deaths_covid_data.iloc[i][total_columns-1]        
        recovered = recovered_covid_data.iloc[i][total_columns-1]        
        active = active_covid_data.iloc[i][total_columns-1]
        

        countryinfo = list()
        countryinfo.append(country)
        countryinfo.append(confirmed)
        countryinfo.append(deaths)
        countryinfo.append(recovered)
        countryinfo.append(active)
        allinfo.append(countryinfo)
    
    FinalDataFrame = pd.DataFrame(allinfo, columns=['Country','Confirmed','Deaths','Recovered','Active'])
          
    userinput = input(str('please enter the desired file name: '))
    if '.csv' in userinput:
        FinalDataFrame.to_csv(userinput)
    else:
        FinalDataFrame.to_csv(userinput+'.csv')    
