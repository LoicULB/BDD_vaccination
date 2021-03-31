import pandas

file = open("fullfill.sql", "w")

df = pandas.read_csv('campaign_vaccines_cleaned.csv', header =0, names = ['pays','vaccin'])
#df = pandas.read_csv('cleaned_daily_stats.csv', index_col='id_stat')
#df = pandas.read_csv('cleaned_hospitalisation_stats.csv', index_col='id_stat')
#df = pandas.read_csv('cleaned_vaccinations_stats.csv', index_col='id_stat')
#df = pandas.read_csv('continent_cleaned.csv')
#df = pandas.read_csv('country_cleaned.csv', index_col='iso_code')
#df = pandas.read_csv('region_cleaned.csv', index_col='name')
#df = pandas.read_csv('vaccines_cleaned.csv')

#df.loc("pays")
#vaccin = df["vaccin"]
#pays = df["pays"]
#pays_vaccin = df[["pays","vaccin"]]
#print(df.iloc[0,0])
#print(pays_vaccin)

"""
for i in range(len(df)):
    file.write("INSERT INTO campagnevaccination VALUES(")
    for j in range(len(df.columns)):
        file.write(df.iloc[i,j])
        if j < len(df.columns)-1:
            file.write(",")
    file.write(");\n")
"""

def fullfill_cv():
    file = open("fullfill_cv.sql", "w")
    df = pandas.read_csv('campaign_vaccines_cleaned.csv', header =0, names = ['pays','vaccin'])
    for i in range(len(df)):
        file.write("INSERT INTO campagnevaccination VALUES(")
        for j in range(len(df.columns)):
            file.write("'" + df.iloc[i, j] + "'")
            if j < len(df.columns) - 1:
                file.write(",")
        file.write(");\n")
    file.close()

def fullfill_sj():
    file = open("fullfill_sj.sql", "w")
    df = pandas.read_csv('cleaned_daily_stats.csv', header=0, names=["id_stat","pays","date","epidemiologist"])
    for i in range(len(df)):
        file.write("INSERT INTO stats_journalieres VALUES(")
        for j in range(len(df.columns)):
            file.write("'" + str(df.iloc[i, j]) + "'")
            if j < len(df.columns) - 1:
                file.write(",")
        file.write(");\n")
    file.close()

def fullfill_hs():
    file = open("fullfill_hs.sql", "w")
    df = pandas.read_csv('cleaned_hospitalisation_stats.csv', header=0, names=["id_stat","icu_patients","hosp_patients"])
    for i in range(len(df)):
        file.write("INSERT INTO hospitalisations_stats VALUES(")
        for j in range(len(df.columns)):
            file.write("'" + str(df.iloc[i, j]) + "'")
            if j < len(df.columns) - 1:
                file.write(",")
        file.write(");\n")
    file.close()

def fullfill_vs():
    file = open("fullfill_vc.sql", "w")
    df = pandas.read_csv('cleaned_vaccinations_stats.csv', header=0,
                         names=["id_stat","nb_tests","nb_vaccinations"])
    for i in range(len(df)):
        file.write("INSERT INTO vaccinations_stats VALUES(")
        for j in range(len(df.columns)):
            file.write("'" + str(df.iloc[i, j]) + "'")
            if j < len(df.columns) - 1:
                file.write(",")
        file.write(");\n")
    file.close()

def fullfill_cont():
    file = open("fullfill_cont.sql", "w")
    df = pandas.read_csv('continent_cleaned.csv', header=0,
                         names=["name"])
    for i in range(len(df)):
        file.write("INSERT INTO continent VALUES(")
        for j in range(len(df.columns)):
            file.write("'" + str(df.iloc[i, j]) + "'")
            if j < len(df.columns) - 1:
                file.write(",")
        file.write(");\n")
    file.close()

def fullfill_country():
    file = open("fullfill_country.sql", "w")
    df = pandas.read_csv('country_cleaned.csv', header=0,
                         names=["iso_code","region","name","hdi","population","area_sq_ml","climate","vaccination_campaign_start"])
    for i in range(len(df)):
        file.write("INSERT INTO pays VALUES(")
        for j in range(len(df.columns)):
            file.write("'" + str(df.iloc[i, j]) + "'")
            if j < len(df.columns) - 1:
                file.write(",")
        file.write(");\n")
    file.close()

def fullfill_region():
    file = open("fullfill_region.sql", "w")
    df = pandas.read_csv('region_cleaned.csv', header=0,
                         names=["name","continent"])
    for i in range(len(df)):
        file.write("INSERT INTO region VALUES(")
        for j in range(len(df.columns)):
            file.write("'" + str(df.iloc[i, j]) + "'")
            if j < len(df.columns) - 1:
                file.write(",")
        file.write(");\n")
    file.close()

def fullfill_vacc():
    file = open("fullfill_vacc.sql", "w")
    df = pandas.read_csv('vaccines_cleaned.csv', header=0,
                         names=["name"])
    for i in range(len(df)):
        file.write("INSERT INTO vaccins VALUES(")
        for j in range(len(df.columns)):
            file.write("'" + str(df.iloc[i, j]) + "'")
            if j < len(df.columns) - 1:
                file.write(",")
        file.write(");\n")
    file.close()

def fullfill_climate():
    file = open("fullfill_climate.sql", "w")
    df = pandas.read_csv('climate.csv', sep=';')
    for i in range(len(df)):
        file.write("INSERT INTO climat VALUES(")
        for j in range(len(df.columns)):
            file.write("'" + str(df.iloc[i, j]) + "'")
            if j < len(df.columns) - 1:
                file.write(",")
        file.write(");\n")
    file.close()

fullfill_cv()
fullfill_sj()
fullfill_hs()
fullfill_vs()
fullfill_cont()
fullfill_country()
fullfill_region()
fullfill_vacc()
fullfill_climate()
