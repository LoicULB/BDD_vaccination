def get_sql_from_file(filepath):
        #read whole file to a string/*
        text_file = open(filepath, "r")
        data = text_file.read()
 
        #close file
        text_file.close()
        #string = ""
        #with open(filepath, "r") as file:
            
        #    for row in file:
        #        print(row)
        print(data)
        return data 

get_sql_from_file("aa2.sql")