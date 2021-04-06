import csv
country_fields_name = ["iso_code", "region", "name", "hdi", "population", "area_sq_ml", "climate", "vaccination_campaign_start"]
country_result_list = []
def is_key_value_in_dict_list(dict_result, dict_result_list, key):
    for dict_ele in dict_result_list:
        if dict_result[key] == dict_ele[key]:
            return True
    return False   

def write_dict_into_file(result_list, file_path, fields_name): 
    with open(file_path, mode='w',  newline='') as file:

        writer = csv.DictWriter(file, fieldnames=fields_name)
        writer.writeheader()

        for result in result_list:
            writer.writerow(result)
def return_null_if_none(row, column):

    if row[column] is None or row[column] == "":
        return "NULL"
    else :
        return row[column]

def convert_countries_row_to_result(country_result, row):
    country_result["iso_code"]= row["iso_code"]
    country_result["region"]= row["region"]
    country_result["name"]= row["country"]
    country_result["hdi"]= row["hdi"]
    country_result["population"]= row["population"]
    country_result["area_sq_ml"]= row["area_sq_ml"]
    country_result["climate"]= return_null_if_none(row, "climate")
    country_result["vaccination_campaign_start"]= "NULL"

def convert_continent_row_to_result(continent_result, row):   
    continent_result["name"] = row["continent"]  

def convert_region_row_to_result(region_result, row): 
    region_result["name"] = row["region"]
    region_result["continent"] = row["continent"]

def create_countries_tables(country_CSV_path):
    
    region_fields_name = ["name", "continent"]
    continent_fields_name = ["name"]
    with open('country.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        line_count = 0
        countryResultList= []
        regionResultList = []
        continentResultList = []
        for row in csv_reader:
            countryResult= dict.fromkeys(country_fields_name)
            regionResult = dict.fromkeys(region_fields_name)
            continentResult = dict.fromkeys(continent_fields_name)

            convert_countries_row_to_result(countryResult, row)
            convert_region_row_to_result(regionResult, row)
            convert_continent_row_to_result(continentResult, row)
            
            countryResultList.append(countryResult)
            if not is_key_value_in_dict_list(regionResult, regionResultList, "name"):
                regionResultList.append(regionResult)
            
            if not is_key_value_in_dict_list(continentResult, continentResultList, "name"):
                continentResultList.append(continentResult)

        write_dict_into_file(regionResultList, 'CleanedCSV/region_cleaned.csv', region_fields_name)
        write_dict_into_file(countryResultList, 'CleanedCSV/country_cleaned.csv', country_fields_name)
        write_dict_into_file(continentResultList, 'CleanedCSV/continent_cleaned.csv', continent_fields_name)
        
        global country_result_list
        country_result_list = countryResultList
      
        
def clean_producers_file(producers_csv_path):

    with open(producers_csv_path) as csv_file:
        vaccines_fields_name = ["name"]
        campaign_vaccines_fields_name = ["pays","vaccin"]
        
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        line_count = 0
        vaccines_result_list = []
        campaign_vaccines_result_list = []
        for row in csv_reader:
            
            campaign_vaccines_result  = dict.fromkeys(campaign_vaccines_fields_name)
            vaccines = row["vaccines"].split(", ")
            country = row["iso_code"]
            add_vacines_to_list(vaccines_result_list, vaccines_fields_name, vaccines)
            add_campaign_vaccines_to_list(campaign_vaccines_result_list, campaign_vaccines_fields_name, vaccines, country )
            add_vaccination_campaign_start_to_countries(country_result_list, row)

        write_dict_into_file(vaccines_result_list, 'CleanedCSV/vaccines_cleaned.csv', vaccines_fields_name)
        write_dict_into_file(campaign_vaccines_result_list, 'CleanedCSV/campaign_vaccines_cleaned.csv', campaign_vaccines_fields_name)
        write_dict_into_file(country_result_list, 'CleanedCSV/country_cleaned.csv', country_fields_name)

def add_vaccination_campaign_start_to_countries(country_result_list, campaign_vaccine):
    start_founded = False
    for country_result in country_result_list:
        if country_result["iso_code"] == campaign_vaccine["iso_code"]:
            country_result["vaccination_campaign_start"] = convert_ugly_date_to_pretty_date(campaign_vaccine["date"])
            break
def add_campaign_vaccines_to_list(campaign_vaccines_result_list, campaign_vaccines_fields_name, vaccines, country):
    for vaccine in vaccines: 
        campaign_vaccines_result= dict.fromkeys(campaign_vaccines_fields_name)
        campaign_vaccines_result["vaccin"] = vaccine
        campaign_vaccines_result["pays"] = country
        campaign_vaccines_result_list.append(campaign_vaccines_result) 
    
def add_vacines_to_list(vaccines_result_list, vaccines_fields_name, vaccines):
    
    for vaccine in vaccines: 
        vaccines_result= dict.fromkeys(vaccines_fields_name)
        vaccines_result["name"] = vaccine
        if not is_key_value_in_dict_list(vaccines_result, vaccines_result_list, "name"):
            vaccines_result_list.append(vaccines_result)        

daily_stats_index=0
def clean_hospitals_vaccinations_fileV2(vaccinations_csv_path, hospitals_csv_path):
    daily_stats_fields_name = ["id_stat", "pays", "date", "epidemiologist"]
    hospitalisation_stats_fields_name = ["id_stat","icu_patients", "hosp_patients" ]
    vaccinations_stats_fields_name = ["id_stat",  "nb_tests", "nb_vaccinations"  ]
    
    daily_stats_result_list = []
    hospitalisation_stats_result_list = []
    vaccinations_stats_result_list = []
    epidemiologists_list = []


    epidemiologists_result_list = []
    with open(hospitals_csv_path) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        counter = 0
        for row in csv_reader:
            
            daily_stats_result = dict.fromkeys(daily_stats_fields_name)
            hospitalisation_stats_result = dict.fromkeys(hospitalisation_stats_fields_name)
            vaccinations_stats_result = dict.fromkeys(vaccinations_stats_fields_name)
            
            global daily_stats_index
            daily_stats_index+=1
            daily_stats_result["id_stat"] = daily_stats_index
            daily_stats_result["pays"] = row["iso_code"]
            daily_stats_result["date"] = convert_ugly_date_to_pretty_date(row["date"])
            daily_stats_result["epidemiologist"] = row["source_epidemiologiste"]

            if not row["source_epidemiologiste"] in epidemiologists_list:
                epidemiologists_list.append(row["source_epidemiologiste"])

            hospitalisation_stats_result["id_stat"] = daily_stats_index
            hospitalisation_stats_result["icu_patients"] = row["icu_patients"]
            hospitalisation_stats_result["hosp_patients"] = row["hosp_patients"]
            
            daily_stats_result_list.append(daily_stats_result)
            hospitalisation_stats_result_list.append(hospitalisation_stats_result)
            counter+=1
    
    for epi in epidemiologists_list:
        epidemiologists_result = dict.fromkeys(["id"])
        epidemiologists_result["id"] = epi
        epidemiologists_result_list.append(epidemiologists_result)
    with open(vaccinations_csv_path) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        counter = 0
        for row in csv_reader:
            if row["tests"] or row["vaccinations"] :
                check_if_pays_date_already_used(row, daily_stats_result_list, vaccinations_stats_result_list)
         
    write_dict_into_file(daily_stats_result_list, "CleanedCSV/cleaned_daily_stats.csv", daily_stats_fields_name)
    write_dict_into_file(vaccinations_stats_result_list, "CleanedCSV/cleaned_vaccinations_stats.csv", vaccinations_stats_fields_name)
    write_dict_into_file(hospitalisation_stats_result_list, "CleanedCSV/cleaned_hospitalisation_stats.csv", hospitalisation_stats_fields_name)
    write_dict_into_file(epidemiologists_result_list, 'CleanedCSV/cleaned_epidemiologists.csv', ["id"])

def check_if_pays_date_already_used(vaccinations , daily_stats_result_list, vaccinations_result_list):
    is_founded = False
    vaccinations_stats_fields_name = ["id_stat",  "nb_tests", "nb_vaccinations"  ]
    vaccinations_stats_result = dict.fromkeys(vaccinations_stats_fields_name)
    global daily_stats_index
    vaccination_daily_stat = daily_stats_index
    good_date =  convert_ugly_date_to_pretty_date (vaccinations["date"])
    
    for daily_stats_result in daily_stats_result_list:
        
        if daily_stats_result["pays"] == vaccinations["iso_code"] and daily_stats_result["date"] == good_date:
            vaccinations_stats_result["id_stat"] = daily_stats_result["id_stat"]
            
            is_founded = True
            break
    if is_founded == False:
        daily_stats_index+=1
        vaccinations_stats_result["id_stat"] = vaccination_daily_stat
        
        daily_stats_result["id_stat"] = daily_stats_index
        daily_stats_result["epidemiologist"] = "NULL"
        daily_stats_result["pays"] =vaccinations["iso_code"]
        daily_stats_result["date"] = convert_ugly_date_to_pretty_date (vaccinations["date"])
    
    
    vaccinations_stats_result["nb_tests"] = return_null_if_none(vaccinations,"tests")
    vaccinations_stats_result["nb_vaccinations"] = return_null_if_none(vaccinations,"vaccinations")
    vaccinations_result_list.append(vaccinations_stats_result)

    daily_stats_result_list.append(daily_stats_result)
      

from dateutil import parser
def convert_ugly_date_to_pretty_date(ugly_date_string):
    
    dto = parser.parse(ugly_date_string)
    return dto.strftime("%d/%m/%Y")

    
create_countries_tables("country.csv")
clean_producers_file("producers.csv")
clean_hospitals_vaccinations_fileV2('vaccinations.csv', 'hospitals.csv')


