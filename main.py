#########################################################################
#Title: PYTHON Project Scenario - Data Analysis
#Description: This program allows user to analyse.......
#Name: <Asil>
#Group Name: <Coders>
#Class: <PN2004Y>
#Date: <16 July 2021>
#Version: <>
#########################################################################

#########################################################################
#Libraries required
import pandas as pd
#import warnings
#warnings.filterwarnings("ignore")

#for pie chart
import random  
import matplotlib.pyplot as plt   
import matplotlib.colors as mcolors
#sys for exiting the System
import sys

#Below function is used to clean columns
def clean_columns(df):

#Strip() is used to remove space between a column name for e.g. [' HongKong '] = [Hong Kong]
  df.columns = [a.strip() for a in df.columns]          
  
  #replace() is used to replace a specific value with another value for e.g ['Korea, Republic of'] = [Korea Republic of] 
  df.columns = [a.replace(',', '') for a in df.columns] 
  return df

#DataFrame has NaN values, filling with 0  
def fill_missing_values(df):
#filling all the NaN values to 0
  df = df.fillna(0)
 #Except Year and Month all Country names are stored in a variable to convert the data type of those specific columns to int, as  Year and Month is unnessessary So temporary removing these two coolumns
  Countries_list = [ col_i for col_i in df.columns if col_i not in ["Year", "Month"]] 
 #Converting the datatype to int
  df[Countries_list] = df[Countries_list].astype(int) 

  return df.reset_index(drop=True)
 


def process_df(df):
  #removing year and month
    df = df.drop(['Year','Month'], axis=1)

  #converting columns into rows for calculation
    calculate = df.T 

  #Calculating the total Number of Visitors
    Total = pd.DataFrame(calculate.sum(axis=1), columns=['Visitors']) 
       
    #As the final output of Top3 countries below code is used to make only two column as aggregated ones.
    Total['Countries'] = Total.index                               #Reseting the countries rows back to to index     
    Total = Total.reset_index(drop=True)
    #sorting the number of visitors in descending order
    Total = Total.sort_values(by=['Visitors'], ascending=False)    #sorting caused the index to jumble up so reseting the index  
    Total = Total.reset_index(drop=True)                
    return Total

#This function is used to filter region 
def filter_by_region(df, region):
#Making amn empty list
  region_list = [] 

#[region_dict] contains all keys as regions and values as countries 
  region_list = region_dict[region]

#In previous function  ['Year'] and ['Month'] columns were removed. So adding them again using .extend() function to filterout countries as per regions. 
  region_list.extend(['Year','Month'])
  df = df[region_list]
    
 #reset_index is used to avoid duplicating columns  
  return df.reset_index(drop=True)
 

#This function is used to filter date or year 
def filter_by_date(df, start_year, end_year):
   #If the start is greater than end year this code will throw and exception error
  if (start_year > end_year):
    print("Start Year Should be less than End Year")

#This filters out years as per user`s input values 
  df = df[(df["Year"] >=  start_year) & (df["Year"] <= end_year)] 
  
  return df.reset_index(drop = True)

#Apply filter is a combination of two filter_by_date() and filter_by_region()
def apply_filters(df, region, start_year, end_year):
  df = filter_by_region(df, region) #passing two arguments, df = DataFrame and region = Region
  df = filter_by_date(df,start_year, end_year) #passing three arguments df = DataFrame, start year and end year
  return df.reset_index(drop=True)
 
#The Final function is combination all the functions defined above.
def run_data_analysis(df, region, start_year, end_year):
  global region_dict 
  region_dict =   {"Africa":["Africa"], 
                 "Europe":['United Kingdom', 'Germany', 'France','Italy', 'Netherlands', 'Greece', 'Belgium & Luxembourg', 'Switzerland',
                                'Austria', 'Scandinavia', 'CIS & Eastern Europe'], 
                 "South East Asia":['Brunei Darussalam', 'Indonesia', 'Malaysia','Philippines', 'Thailand', 'Viet Nam', 'Myanmar'],
                 "North America":['USA','Canada'],
                 "Middle East":['Saudi Arabia','Kuwait','UAE'],
                 "South Asia Pacific":['India', 'Pakistan','Sri Lanka'],
                 "Australia":['Australia', 'New Zealand'],
                 "Asia Pacific":['Japan', 'Hong Kong', 'China', 'Taiwan', 'Korea, Republic Of']
                }
  #Clean columns
  df = clean_columns(df) 
  #Filling in the missing values
  df = fill_missing_values(df) 
  #applying filters
  df = apply_filters(df, region, start_year, end_year) 
  #Printing statments for the selected coutries
  print("\n The following dataframe for {} Region from {} to {} are read as follows: ".format(region, start_year, end_year))

  #reordering year and month before the country columns
  first_column = df.pop('Month') 
  second_column = df.pop('Year') 
  df.insert(0, 'Month', first_column)
  df.insert(0, 'Year', second_column)
  print(df)
  df = process_df(df)
  #printing the top 3 countries
  print("Top 3 countries {} of Visitors to Singapore from the span of {} years are as follows :".format(region, end_year-start_year))

  print(df.head(3))
  

#Main Function
if __name__ == "__main__":
   #Project Title
  print('######################################')
  print('# Data Analysis App - PYTHON Project #')
  print('######################################')
  
                   
  missing_values = [' na ']
  #reading the file
  df = pd.read_csv("MonthyVisitors.csv", na_values = missing_values)
  
 
  print("There are " + str(len(df)) + " data rows read. \n")

  #display dataframe (rows and columns)
  print("The following dataframe are read as follows: \n")
  print(df)

  
  #displaying europe region from 1997 to 2007
  run_data_analysis(df,region="Europe",start_year=1997,end_year=2007)


 #Generate pie Chart
  clean_columns(df)
  fill_missing_values(df)


  Euro_region = region_dict['Europe']
  df_Euro = df[Euro_region]
  df_Euro=df_Euro[(df_Euro.Year >= 1997) & (df_Euro.Year <= 2007)]
  df_Euro =df_Euro.drop(['Year','Month'],axis=1)
  Europe = df_Euro.T                                              
  X = pd.DataFrame(Europe.sum(axis=1), columns=['Visitors']) 
  X['Countries'] = X.index 
  X = X.sort_values(by=['Visitors'], ascending=False) 

  
  y = X['Visitors']
  mylabels = X['Countries']
  colors = random.choices(list(mcolors.CSS4_COLORS.values()),k = 11)
  #spacing between each countries
  my_explode= [0.2] * X['Countries'].count()
  plt.clf()
  fig = plt.figure(figsize=(5,8))
  plt.pie(y, labels = mylabels, explode=my_explode, colors=colors, shadow=True, startangle=90, autopct='%1.2f%%', pctdistance=0.9, labeldistance=1.4)
  plt.legend(title = "Countrywise Analysis",loc="lower right", bbox_to_anchor=(1.3, 0.6, 1, 1))
  plt.savefig("pie-chart.png", bbox_inches = 'tight')


  while True:
    #Min value from ['Year'] column
    min_year = df["Year"].min() 

    #Max value from ['Year'] column
    max_year = df["Year"].max() 

    #add comma after each value
    all_available_region = ", ".join(list(region_dict.keys()))
    

    #print() the available regions and year range
    print("\nThe available regions are {}. Please pick one of the regions mentioned above. Year ranges from {} to {}.".format(all_available_region, min_year, max_year))
    
   
    while True:
      try:
        #Taking input from user for region as string value
        region = str(input("Please Enter Region : ")) 

        #Code for default region
        if region == "":
          region = "Europe"
          print("No input Region is passed, choosing default region : {}".format(region)) 
         
          break
        #print("Please enter valid region")
        elif region not in list(region_dict.keys()):
          print("Please enter valid region")

        else:
          
          break

          

      except:
        print("Please Enter Valid region")  
        
    while True:
      try:
        #Taking input from user for start year as an integer value
        start_year = input("Enter Year to Start : ") 

        if len(start_year) == 0:
          start_year = 1997 #default year
          print("No input start year is passed, choosing default start year : {}".format(start_year))
        #input as int
        start_year = int(start_year)

        if start_year < min_year or start_year > max_year:
          print("Please enter start_year in range of {} to {}".format(min_year, max_year))
        else:
          break

      except:
        print("Invalid start year, please try again!")
        
    while True:
      try:
        #Taking input from user for end year as an integer value
        end_year = input("Enter Year to End : ") 
        
        if len(end_year) == 0:
          #defualt year if input is blank
          end_year = 2007 
          print("No input end year is passed, choosing defaul end year : {}".format(end_year))
        #input as int
        end_year = int(end_year)
        
        if end_year < min_year or end_year > max_year:
          print("Please enter end_year in range of {} to {}".format(min_year, max_year))
        elif end_year < start_year:
          print("End Year should be greater than Start Year!")

        else:
          break
      
      except:
        print("Invalid end year, please try again!")
    
  
    print("\n You have picked {} Region which consists of {} and have picked {} to {} for its year range.".format(region, ", ".join(region_dict[region]), start_year, end_year))

    #run_data_analysis(df, region, start_year, end_year)
    run_data_analysis(df, region, start_year, end_year)

    print("\n"*2)

    cont = str(input("Do you wish to continue : \n Press 'Y' to continue, 'N or Q' to exit = "))
    
    if cont.lower() == "y":
     pass

    elif cont.lower() == "n" or cont.lower() == "q":
      sys.exit("Exiting..")
      

    else:
      print("Invalid input entered, selecting default choice as Yes")