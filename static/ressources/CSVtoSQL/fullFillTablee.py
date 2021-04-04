import pandas
import os
import sys
import numbers
#file = open("fullfill.sql", "w")

#df = pandas.read_csv(os.path.join(sys.argv[1], 'campaign_vaccines_cleaned.csv'), header =0, names = ['pays','vaccin'])
print(os.path.join(sys.argv[1], 'campaign_vaccines_cleaned.csv'))
def write_insert_statement(table_name, df, file):
    for i in range(len(df)):
        file.write(f"INSERT INTO {table_name} VALUES(")
        for j in range(len(df.columns)):

            value = str(df.iloc[i,j]) if str(df.iloc[i,j]).replace('.','',1).isdigit() else "$$" + str(df.iloc[i, j]) + "$$"
            if value=="$$nan$$" :
                value="NULL"
            file.write(value)
            if j < len(df.columns) - 1:
                file.write(",")
        file.write(");\n")


def fullfill_cv():
    with open("fullfill_cv.sql", "w") as file:
        df = pandas.read_csv(os.path.join(directory, 'campaign_vaccines_cleaned.csv'), header =0, names = ['pays','vaccin'])
        write_insert_statement("campagne_vaccin", df, file)

def fullfill_sj():
    with open("fullfill_sj.sql", "w") as file:
        df = pandas.read_csv(os.path.join(directory, 'cleaned_daily_stats.csv'), header=0, names=['id_stat','pays','date','epidemiologist'])
        write_insert_statement("statsjournalieres", df, file)
    

def fullfill_hs():
    with open("fullfill_hs.sql", "w") as file:
        df = pandas.read_csv(os.path.join(directory,'cleaned_hospitalisation_stats.csv'), header=0, names=["id_stat","icu_patients","hosp_patients"])
        write_insert_statement('hospitalisations_stats', df, file)
  

def fullfill_vs():
    with open("fullfill_vc.sql", "w") as file:
        df = pandas.read_csv(os.path.join(directory, 'cleaned_vaccinations_stats.csv'), header=0,
                         names=["id_stat","nb_tests","nb_vaccinations"])
        write_insert_statement('vaccinations_stats', df, file)

def fullfill_cont():
    with open("fullfill_cont.sql", "w") as file:
        df = pandas.read_csv(os.path.join(sys.argv[1],'continent_cleaned.csv'), header=0,
                         names=["name"])
        write_insert_statement("continent", df, file)

def fullfill_country():
    with open("fullfill_country.sql", "w") as file:
        df = pandas.read_csv(os.path.join(directory, 'country_cleaned.csv'), header=0,
                         names=["iso_code","region","name","hdi","population","area_sq_ml","climate","vaccination_campaign_start"])
        write_insert_statement("pays", df, file)

def fullfill_region():
    with open("fullfill_region.sql", "w") as file:
        df = pandas.read_csv(os.path.join(directory, 'region_cleaned.csv'), header=0,
                         names=["name","continent"])
        write_insert_statement("region", df, file)

def fullfill_vacc():
    with open("fullfill_vacc.sql", "w") as file:
        df = pandas.read_csv(os.path.join(directory, 'vaccines_cleaned.csv'), header=0,
                         names=["name"])
        write_insert_statement("vaccins", df, file)

def fullfill_climate():
    with open("fullfill_climate.sql", "w") as file:
        df = pandas.read_csv(os.path.join(directory, 'climate.csv'), sep=';')
        write_insert_statement("climat", df, file)

def fullfill_epidemiologist():
    with open("fullfill_epidemiologist.sql", "w") as file:
        df = pandas.read_csv(os.path.join(directory, 'cleaned_epidemiologists.csv'), sep=';')
        write_insert_statement("epidemiologist(uuid)", df, file)
directory = sys.argv[1]
fullfill_cv()
fullfill_sj()
fullfill_hs()
fullfill_vs()
fullfill_cont()
fullfill_country()
fullfill_region()
fullfill_vacc()
fullfill_climate()
fullfill_epidemiologist()
