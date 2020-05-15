# Final Project Intermediate Python
# Snake Coders 
# Lucas Falivene - Lfaliven
# Fabio Beltran Vasquez - fbeltran
# Muhammad Bin Oiad - mbinoiad

import API as API
import Scrap as S
import CSV as CSV



def main():
    option = '1'
    print('\n----------------------------Welcome To COVIDaily-------------------------------')
    print('\nThis program aims to provide daily updates about COVID-19 pandemic')
    
    while option != '0':
        
        print('\n\n\n------------------------------- MAIN MENU ----------------------------------\n')
        print('1- Updated statistics for any county in the United States')
        print('2- Travel Restrections from Pennsylvania Government or instructions from CDC')
        print('3- Live statistics for all countries in the world')
        
                  
        print('\n\nNOTE:\nIf you wish to exit the program enter option 0 when on the main menu')

        option = input(str('Please enter your selected option: '))
        options = ['0','1','2','3']
        while option not in options:
            option = input(str('Incorrect optoin chosen, please enter an option from the menu above: '))
        
        if option == '1':
            print('''
       ---------------- MENU-1 ----------------
        1. Obtain qucik real time data from API
        2. Obtain real time US counties data
        3. Compare US counties data
        0. Return to main menu
        ''')
        
            useropt = input(str('Please input your option number: '))
            useropttions = ['0','1','2','3']
            while useropt not in useropttions:
                useropt = input(str('Incorrect optoin chosen, please enter an option from the sub-menu above: '))
        
            if useropt == '1':
                API.QUICK_INFO()
                
            elif useropt == '2':
                state = input('Enter the state where the county is located: ')
                state = API.CHECK_INPUT(state, 1, 0)
                county = input('Enter the US county you want to obatin data from: ')
                county = API.CHECK_INPUT(county, 0, 1)
                print('\nDo you want to obtain yesterday\'s data?')
                today = input('Input yes or no: ')
                date_option = API.CHECK_OPTION(today)
                comparee = 0
                API.API_CITY(county,state,date_option,comparee)
                
            elif useropt == '3':
                state1 = input('Enter the state where the county is located: ')
                state1 = API.CHECK_INPUT(state1, 1, 0)
                county1 = input('Enter the first US county you want to compare: ')
                county1 = API.CHECK_INPUT(county1, 0, 1)
                state2 = input('Enter the state where the county is located: ')
                state2 = API.CHECK_INPUT(state2, 1, 0)
                county2 = input('Enter the second US county you want to compare: ')
                county2 = API.CHECK_INPUT(county2, 0, 1)
                today = 1
                comparee = 1
                county1_conf, county1_dead, county1 = API.API_CITY(county1,state1,today,comparee)
                county2_conf, county2_dead, county2 = API.API_CITY(county2,state2,today,comparee)
                API.GRAPHS(county1_conf, county1_dead, county2_conf, county2_dead, county1, county2)            

        if option == '2':
            print("""
        -------------- MENU-2 ----------------
        1. Information for Travelers PA Gov
        2. Information from CDC Site
        0. Return to main menu
        """)
            useropt = input(str('Please input your option number: '))
            useropttions = ['0','1','2']
            while useropt not in useropttions:
                useropt = input(str('Incorrect option chosen, please enter an option from the sub-menu above: '))
            
            # Get common info for travelers from Pennsylvania 
            # Department of Health website
            if useropt=='1':
                travelq1=S.gettravel()
                print('\n\n---------------------------- MENU-2 SUB-MENU-1 ------------------------------')  
                
                for i in travelq1:                    
                    print('%d.  %s'%(i,travelq1[i][0]))
                    
                useropt=input('Please enter your option: ')
                while useropt.isdigit() != True:
                    useropt = input('please make sure that you enter a valid option: ')
                useropttions = list(travelq1.keys())
                while int(useropt) not in useropttions:
                    useropt = input('Incorrect option chosen, please enter an option from the sub-menu above: ')
                                
                print(travelq1[int(useropt)][1])
            # Get Frequently Asked Questions about COVID  from the CDC Site.
            elif useropt=='2':
                covidcdc=S.getcovidcdc()
                print('\n\n---------------------------- MENU-2 SUB-MENU-2 ------------------------------')
                covid_keys=list(covidcdc.keys())
                for i in range(len(covid_keys)):
                    print('\t%d.  %s'%(i,covid_keys[i]))
                               
                useropt1=input('Please enter your option: ')
                while useropt1.isdigit() != True:
                    useropt1 = input('Incorrect option chosen, please make sure that you enter a valid option: ')
                
                while int(useropt1) not in range(len(covid_keys)):
                    useropt1 = input('Incorrect option chosen, please enter an option from the sub-menu above: ')
                       
                covid_subkeys=list(covidcdc[covid_keys[int(useropt1)]].keys())
                
                for i in range(len(covid_subkeys)):
                    print('%d.  %s'%(i,covid_subkeys[i]))
                               
                useropt2=input('Please enter your option: ')
                
                while useropt2.isdigit() != True:
                    useropt2 = input('Incorrect option chosen, please make sure that you enter a valid option: ')      
                while int(useropt2) not in range(len(covid_subkeys)):
                    useropt2 = input('Incorrect option chosen, please enter an option from the sub-menu above: ')
                           
                print(covidcdc[covid_keys[int(useropt1)]][covid_subkeys[int(useropt2)]])
        
        elif option == '3':
            print('First, we will obtain the updated datasets from the internet or from your computer')
            working_directory = CSV.workingDirectory()
            a, b, c, url_confirmed, url_deaths, url_recovered = CSV.verifyConnection()
            CSV.downloadFiles(a,b,c,url_confirmed, url_deaths,url_recovered, working_directory)
            
            if CSV.openFiles() is not None:
                covid_confirmed, covid_deaths, covid_recovered = CSV.openFiles()
                confirmed_covid_data, deaths_covid_data, recovered_covid_data = CSV.cleanUpDFs(covid_confirmed, covid_deaths, covid_recovered)
                active_covid_data = CSV.createActiveCovidDF(confirmed_covid_data, deaths_covid_data, recovered_covid_data)
    
                print('Great, now let\'s take you to the sub-menu')
                print('\n------------------------------------ MAIN-3 ---------------------------------------')
                print('''
        1. Get active COVID-19 cases in a specific country with timeline plot
        2. Create a database for confirmed/deaths/recoveries/active cases in all countires
        3. Create a dataset for confirmed/deaths/recoveries/active cases in all countires
        0. Return to main menu''')   
                        
                useropt = input(str('Please input your option number: '))
                useropttions = ['0','1','2','3']
                while useropt not in useropttions:
                    useropt = input('Incorrect optoin chosen, please enter an option from the sub-menu above: ')
                
                if useropt == '1':
                    country = input('Please enter the coutnry name to view the confirmed cases stas and plots: ')
                    proper_country = CSV.fixUserInput(country)
                    CSV.getAndSavePlotAndActiveStats(proper_country, active_covid_data)
                
                elif useropt == '2':
                    CSV.saveSqliteDB(working_directory, active_covid_data, confirmed_covid_data, deaths_covid_data, recovered_covid_data)
                    
                elif useropt == '3':
                    CSV.createandSaveFinalDF(active_covid_data, confirmed_covid_data, deaths_covid_data, recovered_covid_data)

# calling main
if __name__ == '__main__':
    main()