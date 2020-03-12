import requests
import csv
import time
import json
import sys

def iterate(name):
    #search url uses business_name
    search_url = "https://api.carpe.insure/v11/search"
    #match url uses name
    match_url = "https://api.carpe.insure/v11/match"
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'Postman-Token': "fa205d70-adaf-47ae-805f-d1e39295b64d"
        }

    #opens data to be requested
    filename = "%s.csv" % name
    with open (filename,encoding='utf-8') as csvinput:
        with open("business_names_output.csv",'w',encoding='utf-8') as csvoutput:
            writer = csv.writer(csvoutput, lineterminator='\n')
            reader = csv.reader(csvinput)

            all = []
            row = next(reader)
            business_name = row[0]
            address = row[1]
            city = row[2]
            state = row[3]
            country = row[4]
            row.append(business_name)
            all.append(row)
    #builds and sends requests
            for row in reader:
                #row.append(r.text)
                business_name = row[0]
                address = row[1]
                city = row[2]
                state = row[3]
                country = row[4]
      #build request
                #payload = "{\"query\": {\"name\": \"{}\"}}".format(business_name)
                d_pay = dict(name = row[0],
                            full_address = row[1],
                            city = row[2],
                            state = row[3],
                            country = row[4])
                payload = json.dumps(d_pay)
                response = requests.post(match_url.strip('\n'), data=payload, headers=headers)
                results = response.text
                response.close()
                #row.append(results)

        #Test that the query is being sent as intended
                #print(payload)

        #Test results json
                #print (results)
                results_json = response.json().get("result")
                print(results_json)
                #print(type(results_json))
            #    row.append(results_json)


    # Below we begin to add the response from the API back to the csv, parsing each field.
    # Try and except statements are used to avoid failures if a value is null, but this could be done more elegantly.
                
        #Append endpoint version used
                row.append(match_url)
        #Append full results object
                try:
                    row.append(results)
                except Exception as f:
                    row.append("No result")
        #Append biz id
                try:
                    row.append(results_json["id"])
                except Exception as f:
                    row.append("No result")
        #Append biz categories
                try:
                    row.append(results_json["business"]["categories"])
                except Exception as f:
                    row.append("No result")
        #Append biz hours
                try:
                    row.append(results_json["business"]["hours"])
                except Exception as f:
                    row.append("No result")
        #Append sources
                try:
                    row.append(results_json["sources"])
                except Exception as f:
                    row.append("No result")
        #Append risks object
                #if results_json is not None:
                #results_length = (len(results_json))
                    #print("results length is")
                    #print(len(results_json))
                #print(results_length)
                try:
                    row.append(results_json["risks"])
                except Exception as f:
                    row.append("No result")

                #def list_risks():
                #    i = 0
                #    while i < len(results_json):
                #        row.append(results_json["risks"][i])
                #        i +=1

        #Append each risk nested in the risk object
                if results_json is not None:
                    #print(results_json["risks"][0])
                    try:
                        if results_json["risks"] is not None:
                            i = 0
                            while i < len(results_json["risks"]):
                                row.append(results_json["risks"][i])
                                i +=1
                            #list_risks()
                    except Exception as f:
                        print()


    # End loop
            # Here I sleep between requests to avoid overloading the API and append the row
                time.sleep(2)
                all.append(row)
    #writes all data to the csv at once
            writer.writerows(all)

if __name__ == "__main__":
    iterate(sys.argv[1])
