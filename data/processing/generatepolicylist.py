import csv
import os
import pycountry
import codecs
import pandas

#Enable prints and write non-valid survey responses
DEBUG = False

#Policy Counts
WORK_EXCEP = 0
SPECIFIC_COUNTRY = 0
CITIZEN_EXCEP = 0 
ESSENTIAL_ONLY = 0
VISA_BAN = 0
CITIZENSHIP_BAN = 0
HISTORY_BAN = 0
BORDER_CLOSURE = 0
CITIZENSHIP_BAN_AND_HISTORY_BAN = 0

def decode_policy(complete,visa,citizen,history,refugee,citException,workerException,countryException,air,land,sea):
    global WORK_EXCEP 
    global SPECIFIC_COUNTRY
    global CITIZEN_EXCEP 
    global ESSENTIAL_ONLY
    global VISA_BAN
    global CITIZENSHIP_BAN
    global HISTORY_BAN
    global BORDER_CLOSURE
    global CITIZENSHIP_BAN_AND_HISTORY_BAN
    if (complete and workerException):
        WORK_EXCEP = WORK_EXCEP + 1
    elif (complete and countryException):
        SPECIFIC_COUNTRY = SPECIFIC_COUNTRY + 1
    elif (complete and citException):
        CITIZEN_EXCEP = CITIZEN_EXCEP + 1
    elif (complete):
        ESSENTIAL_ONLY = ESSENTIAL_ONLY + 1
    if (visa):
        VISA_BAN = VISA_BAN + 1
    if (citizen):
        CITIZENSHIP_BAN = CITIZENSHIP_BAN + 1
    if (history):
        HISTORY_BAN = HISTORY_BAN + 1
    if (citizen and history):
        CITIZENSHIP_BAN_AND_HISTORY_BAN = CITIZENSHIP_BAN_AND_HISTORY_BAN + 1
    if (air or land or sea):
        BORDER_CLOSURE = BORDER_CLOSURE + 1
    if (complete and workerException):
        return "WORK_EXCEP"
    elif (complete and countryException):
        return "SPECIFIC_COUNTRY"
    elif (complete and citException):
        return "CITIZEN_EXCEP"
    elif (complete):
        return "ESSENTIAL_ONLY"
    elif (visa):
        return "VISA_BAN"
    elif (citizen):
        return "CITIZENSHIP_BAN"
    elif (history):
        return "HISTORY_BAN"
    elif (refugee):
        return "REFUGEE"
    elif (air or land or sea):
        return "BORDER_CLOSURE"
    return "NONE"


def month_to_num(month):
    if (month == 'Jan'):
        return "01"
    elif (month == 'Feb'):
        return "02"
    elif (month == 'Mar'):
        return "03"
    elif (month == 'Apr'):
        return "04"
    elif (month == 'May'):
        return "05"
    elif (month == 'Jun'):
        return "06"
    elif (month == 'Jul'):
        return "07"
    elif (month == 'Aug'):
        return "08"
    elif (month == 'Sept'):
        return "09"
    elif (month == 'Oct'):
        return "10"
    elif (month == 'Nov'):
        return "11"
    elif (month == 'Dec'):
        return "12"
    else:
        print "INVALID_DATE: " + month
        return "00"

#create output file for writing
outputfile = codecs.open("policy_list.csv", 'w', 'utf-8')

#create empty list to gather policies we want to look at
policyList = []

#open input files and error out if not found
#main survey of policy data
try:
    mainSurvey = pandas.read_csv('main_survey_raw.csv',keep_default_na=False, encoding='utf-8', dtype=str, quotechar='"', delimiter=',',header=0)
except OSError:
    print "Could not open/read file:", 'masterdata1017.csv'
    os.system("pause")
    sys.exit()

#survey to add end dates to policies and link policies that supersede others
try:
    endDatesSurvey = pandas.read_csv('end_dates_survey_raw.csv',keep_default_na=False,encoding='utf-8', dtype=str, quotechar='"', delimiter=',',header=0)
except OSError:
    print "Could not open/read file:", 'end_dates.csv'
    os.system("pause")
    sys.exit()

#list of policies with targeted country lists normalized
try:
    targetsFixed = pandas.read_csv('countrylistsclean.csv',keep_default_na=False, encoding='utf-8',dtype=str, quotechar='"', delimiter=',',header=1)
except OSError:
    print "Could not open/read file:", 'countylistsclean.csv'
    os.system("pause")
    sys.exit()

#policies from acaps when a better source is not available
#from: https://www.acaps.org/covid-19-government-measures-dataset
try:
    acapsLinks = pandas.read_csv('acaps_covid19_government_measures_dataset.csv',keep_default_na=False, encoding='latin-1', dtype=str, quotechar='"', delimiter=',',header=1)
except OSError:
    print "Could not open/read file:", 'acaps_covid19_government_measures_dataset.csv'
    os.system("pause")
    sys.exit()

outputfile.write("ID|COUNTRY_NAME|ISO3|ISO2|POLICY_TYPE|POLICY_SUBTYPE|START_DATE|END_DATE|AIR|AIR_TYPE|TARGETS_AIR|LAND|LAND_TYPE|TARGETS_LAND|SEA|SEA_TYPE|TARGETS_SEA|CITIZEN|CITIZEN_LIST|HISTORY_BAN|HISTORY_BAN_LIST|REFUGEE|REFUGEE_LIST|VISA_BAN|VISA_BAN_TYPE|VISA_BAN_LIST|CITIZEN_EXCEP|CITIZEN_EXCEP_LIST|COUNTRY_EXCEP|COUNTRY_EXCEP_LIST|WORK_EXCEP|SOURCE0|SOURCE1|SOURCE2|SOURCE3|SOURCE4\n")

for index,row in mainSurvey.iterrows():
    if(DEBUG):
        print ("Policy: %s Country: %s "%(row['Q1_5_TEXT'],row['Q1_4_TEXT']))
    #handle country code irregularities
    if(row['ISO3']=="EUR"):
        countryName = "European Union"
        iso2 = "EU"
    elif(row['ISO3']=="ESH"):
        countryName = "Sahrawi Arab Democratic Republic"
        iso2 = "EH"
    elif(row['ISO3']=="XKX"):
        countryName = "Republic of Kosovo"
        iso2 = "XK"
    elif(row['ISO3']=="SOL"):
        countryName = "Somaliland"
        iso2 = "XS"
    #ignore country name in survey, regenerate from country code
    elif(pycountry.countries.get(alpha_3=row['ISO3'])):
        countryName = pycountry.countries.get(alpha_3=row['ISO3']).name
        iso2 = pycountry.countries.get(alpha_3=row['ISO3']).alpha_2
    else:
        if(DEBUG):
            print("COUNTRYCODENOTFOUND: %s %s"%(row['Q1_4_TEXT'],row['Q1_5_TEXT']))
    if(row['Q24'] == 'No, it is none of the above.'):
        if(DEBUG):
            print("NOPOLICY, %s policy %s not recorded"%(row['Q1_4_TEXT'],row['Q1_5_TEXT']))
            outputfile.write(row['Q1_5_TEXT']+"|"+countryName+"|"+row['ISO3']+"|"+iso2+"|NONE\n")
    elif(row['Q5']==''):
        if(DEBUG):
            print("OUTGOING, %s policy %s not recorded"%(row['Q1_4_TEXT'],row['Q1_5_TEXT']))
            outputfile.write(row['Q1_5_TEXT']+"|"+countryName+"|"+row['ISO3']+"|"+iso2+"|OUTGOING\n")
    elif(row['Q3']=='25'):
        if(DEBUG):
            print("NOSTARTDATE, %s"%(row['Q1_5_TEXT']))
            outputfile.write(row['Q1_5_TEXT']+"|"+countryName+"|"+row['ISO3']+"|"+iso2+"|NOSTARTDATE\n")
    
    elif(row['Q5'] == "I did a full contextual search and found that there was no national-level policy enacted (paste wayback link here to justify this choice, and select a start date of Jan 1, 2020 and today's date as the end date)"):
        source = row['Q5_3_TEXT']
        endDate = row['Q4'].split()[1].strip('()').rjust(2,'0') + "_" + row['Q22_1_TEXT'].rjust(2,'0') + "_20"
        outputfile.write(row['Q1_5_TEXT']+"|"+countryName+"|"+row['ISO3']+"|"+iso2+"|NOPOLICYIMPLEMENTED|NONE|NONE|"+endDate+"|0|NA|NA|0|NA|NA|0|NA|NA|0|NA|0|NA|0|NA|0|NA|NA|0|NA|0|NA|0|"+source+"\n")
    
    elif(row['Q5'].split()[0]=='Partial' and row['Q3'].split()[0] != 'No' and row['Q21'].split()[0] != 'No'):
        if ((row['Q32'] == '2020') or (row['Q32'] == '')):
            startDate = row['Q3'].split()[1].strip('()').rjust(2,'0') + "_" + row['Q21_1_TEXT'].rjust(2,'0') + "_20"
        else:
            startDate = row['Q3'].split()[1].strip('()').rjust(2,'0') + "_" + row['Q21_1_TEXT'].rjust(2,'0') + "_21"

        if(row['Q4'].split()[0] != 'No' and row['Q22'].split()[0] != 'No'):
            if ((row['Q31'] == '2020') or (row['Q31'] == '')):
                endDate = row['Q4'].split()[1].strip('()').rjust(2,'0') + "_" + row['Q22_1_TEXT'].rjust(2,'0') + "_20"
            else:
                endDate = row['Q4'].split()[1].strip('()').rjust(2,'0') + "_" + row['Q22_1_TEXT'].rjust(2,'0') + "_21"
        else:
            endDate = "NONE"
        
        for indexEndDates,rowEndDates in endDatesSurvey.iterrows():  
            if (rowEndDates['Q1_2_TEXT'] == row['Q1_5_TEXT']):
                if(rowEndDates['Q5']=='2020' or rowEndDates['Q5']==''):
                    endDate = month_to_num(rowEndDates['Q3']).rjust(2,'0') + '_' + rowEndDates['Q4_1_TEXT'].rjust(2,'0')+'_20'
                else:
                    endDate = month_to_num(rowEndDates['Q3']).rjust(2,'0') + '_' + rowEndDates['Q4_1_TEXT'].rjust(2,'0')+'_21'
        
        source=""
        if (row['Q28_1_TEXT']!=""):
            source = source = source + row['Q28_1_TEXT'] +  "|"; 
        if (row['Q27_1_TEXT'] != ""):
            source = source = source + row['Q27_1_TEXT'] +  "|"; 
        if (row['Q27_2_TEXT'] != ""):
            source = source = source + row['Q27_2_TEXT'] +  "|"; 
        if (row['Q27_3_TEXT'] != ""):
            source = source = source + row['Q27_3_TEXT'] +  "|"; 
        if (row['Q27_4_TEXT'] != ""):
            source = source = source + row['Q27_4_TEXT'] +  "|"; 
        if (row['Q20_1_TEXT'] != ""):
            source = source = source + row['Q20_1_TEXT'] +  "|"; 
        if (row['Q20_2_TEXT'] != ""):
            source = source = source + row['Q20_2_TEXT'] +  "|"; 
        if (row['Q20_3_TEXT'] != ""):
            source = source = source + row['Q20_3_TEXT'] +  "|"; 
        if (row['Q20_4_TEXT'] != ""):
            source = source = source + row['Q20_4_TEXT'] +  "|";
        if (row['Q20_5_TEXT'] != ""):
            source = source = source + row['Q20_5_TEXT'] +  "|"; 
        if (row['Q20_6_TEXT'] != ""):
            source = source = source + row['Q20_6_TEXT'] +  "|"; 
        if (row['Q20_14_TEXT'] != ""):
            source = source = source + row['Q20_14_TEXT'] +  "|";
        if (row['Q20_16_TEXT'] != ""):
            source = source = source + row['Q20_16_TEXT'] +  "|"; 

        #grab source from acaps if no better source was found
        if (source == ""): #and row[13].split()[0] == "Unable"):
            for indexAcaps,acaps in acapsLinks.iterrows():  
                if (acaps[0] == row['Q1_5_TEXT']):
                    source =  acaps[15] 
        
        sea = 1 if "Sea" in row['Q10'] else 0
        air = 1 if "Air" in row['Q10'] else 0
        land = 1 if "Land" in row['Q10'] else 0
        airType = "All" if "Air, all" in row['Q10'] else "Specific" if "Air (specific)," in row['Q10'] else "NA"
        seaType = "All" if "Sea, all" in row['Q10'] else "Specific" if "Sea (specific)," in row['Q10'] else "NA"
        landType = "All" if "Land, all" in row['Q10'] else "Specific" if "Land (specific)," in row['Q10'] else "NA"
        targetsAir = row['Q10_6_TEXT'] if (row['Q10_6_TEXT'] != "") else "NA"
        targetsLand = row['Q10_3_TEXT'] if (row['Q10_3_TEXT'] != "") else "NA"
        targetsSea = row['Q10_8_TEXT'] if (row['Q10_8_TEXT'] != "") else "NA"

        citizen = 1 if "citizenship" in row['Q7']else 0
        citizenshipList = row['Q7_1_TEXT'] if (row['Q7_1_TEXT'] != "") else "NA"

        history = 1 if "history" in row['Q7'] else 0
        historyList = row['Q7_2_TEXT'] if (row['Q7_2_TEXT'] != "") else "NA"

        refugee = 1 if "refugee" in row['Q7'] else 0
        refugeeList = row['Q7_18_TEXT'] if (row['Q7_18_TEXT'] != "") else "NA"
        
        visa = 1 if "Yes" in row['Q17'] else 0 
        visaType = "All" if "all" in row['Q17'] else "specific" if "specific" in row['Q17'] else "NA"
        visaList = row['Q17_3_TEXT'] if (row['Q17_3_TEXT'] != "") else "NA"

        #COMPLETE fields
        citExceptionList = "NA"
        countryExceptionList = "NA"
        permitException = "NA"

        citException = 0
        countryException = 0
        workerException = 0

        for indexCountryLists,rowCountryLists in targetsFixed.iterrows():  
            if (rowCountryLists[0] == row['Q1_5_TEXT']):
                historyList = rowCountryLists[1] if (rowCountryLists[1] != "") else "NA"
                visaList = rowCountryLists[2] if (rowCountryLists[2] != "") else "NA"
        policyList.append({'name' :countryName, 'id': row['Q1_5_TEXT'], 'ISO3': row['ISO3'], 'partialfull': 'PARTIAL', 'air' : airType, 'land' : land, 'sea' : sea, 'policy_start' : startDate, 'policy_end': endDate, 'source':source})
        if (decode_policy(0,visa,citizen,history,refugee,citException,workerException,countryException,air,land,sea) != 'NONE' or DEBUG):
            outputfile.write(row['Q1_5_TEXT']+"|"+countryName+"|"+row['ISO3']+"|"+iso2+"|PARTIAL|"+decode_policy(0,visa,citizen,history,refugee,citException,workerException,countryException,air,land,sea)+"|"+startDate+"|"+endDate+"|"+str(air)+"|"+str(airType)+"|"+targetsAir+"|"+str(land)+"|"+str(landType)+"|"+targetsLand+"|"+str(sea)+"|"+str(seaType)+"|"+targetsSea+"|"+str(citizen)+"|"+citizenshipList+"|"+str(history)+"|"+historyList+"|"+str(refugee)+"|"+refugeeList+"|"+str(visa)+"|"+visaType+"|"+visaList+"|"+str(citException)+"|"+citExceptionList+"|"+str(countryException)+"|"+countryExceptionList+"|"+str(workerException)+"|"+source+"\n")

    elif(row['Q5'].split()[0]=='Complete' and row['Q3'].split()[0] != 'No' and row['Q21'].split()[0] != 'No'):
        if ((row['Q32'] == '2020') or (row['Q32'] == '')):
            startDate = row['Q3'].split()[1].strip('()').rjust(2,'0') + "_" + row['Q21_1_TEXT'].rjust(2,'0') + "_20"
        else:
            startDate = row['Q3'].split()[1].strip('()').rjust(2,'0') + "_" + row['Q21_1_TEXT'].rjust(2,'0') + "_21"

        if(row['Q4'].split()[0] != 'No' and row['Q22'].split()[0] != 'No'):
            if ((row['Q31'] == '2020') or (row['Q31'] == '')):
                endDate = row['Q4'].split()[1].strip('()').rjust(2,'0') + "_" + row['Q22_1_TEXT'].rjust(2,'0') + "_20"
            else:
                endDate = row['Q4'].split()[1].strip('()').rjust(2,'0') + "_" + row['Q22_1_TEXT'].rjust(2,'0') + "_21"
        else:
            endDate = "NONE"
        for indexEndDates,rowEndDates in endDatesSurvey.iterrows():  
            if (rowEndDates['Q1_2_TEXT'] == row['Q1_5_TEXT']):
                if(rowEndDates['Q5']=='2020' or rowEndDates['Q5']==''):
                    endDate = month_to_num(rowEndDates['Q3']).rjust(2,'0') + '_' + rowEndDates['Q4_1_TEXT'].rjust(2,'0')+'_20'
                else:
                    endDate = month_to_num(rowEndDates['Q3']).rjust(2,'0') + '_' + rowEndDates['Q4_1_TEXT'].rjust(2,'0')+'_21'
        
        source=""
        if (row['Q28_1_TEXT']!=""):
            source = source = source + row['Q28_1_TEXT'] +  "|"; 
        if (row['Q27_1_TEXT'] != ""):
            source = source = source + row['Q27_1_TEXT'] +  "|"; 
        if (row['Q27_2_TEXT'] != ""):
            source = source = source + row['Q27_2_TEXT'] +  "|"; 
        if (row['Q27_3_TEXT'] != ""):
            source = source = source + row['Q27_3_TEXT'] +  "|"; 
        if (row['Q27_4_TEXT'] != ""):
            source = source = source + row['Q27_4_TEXT'] +  "|"; 
        if (row['Q20_1_TEXT'] != ""):
            source = source = source + row['Q20_1_TEXT'] +  "|"; 
        if (row['Q20_2_TEXT'] != ""):
            source = source = source + row['Q20_2_TEXT'] +  "|"; 
        if (row['Q20_3_TEXT'] != ""):
            source = source = source + row['Q20_3_TEXT'] +  "|"; 
        if (row['Q20_4_TEXT'] != ""):
            source = source = source + row['Q20_4_TEXT'] +  "|";
        if (row['Q20_5_TEXT'] != ""):
            source = source = source + row['Q20_5_TEXT'] +  "|"; 
        if (row['Q20_6_TEXT'] != ""):
            source = source = source + row['Q20_6_TEXT'] +  "|"; 
        if (row['Q20_14_TEXT'] != ""):
            source = source = source + row['Q20_14_TEXT'] +  "|";
        if (row['Q20_16_TEXT'] != ""):
            source = source = source + row['Q20_16_TEXT'] +  "|"; 

        #grab source from acaps if no better source was found
        if (source == ""): #and row[13].split()[0] == "Unable"):
            for indexAcaps,acaps in acapsLinks.iterrows():  
                if (acaps[0] == row['Q1_5_TEXT']):
                    source =  acaps[15] 
        
        citException = 1 if  "Yes" in row['Q6'] else 0 
        countryException = 1 if  "Yes" in row['Q9'] else 0
        workerException = 1 if "Yes" in row['Q8'] else 0

        citExceptionList = row['Q6_1_TEXT'] if "Yes" in row['Q6'] else "NA" 
        countryExceptionList = row['Q9_1_TEXT'] if "Yes" in row['Q9'] else "NA"

        #Partial fields
        air = 0
        land = 0
        sea = 0
        airType = "NA"
        seaType = "NA"
        landType = "NA"
        targetsAir = "NA"
        targetsLand = "NA"
        targetsSea = "NA"
        visa = 0
        visaType="NA"
        visaList = "NA"
        citizen = 0
        citizenshipList = "NA"
        history = 0
        historyList = "NA"
        refugee = 0
        refugeeList = "NA"

        for indexCountryLists,rowCountryLists in targetsFixed.iterrows():  
            if (rowCountryLists[0] == row['Q1_5_TEXT']):
                if (rowCountryLists[3] != "Unclear" and rowCountryLists[3] != "" and rowCountryLists[3] != "No" and rowCountryLists[3] != "NA"):
                    countryExceptionList = rowCountryLists[3]
        policyList.append({'name' :countryName, 'id': row['Q1_5_TEXT'], 'ISO3': row['ISO3'], 'partialfull': 'COMPLETE', 'air' : air, 'land' : land, 'sea' : sea, 'policy_start' : startDate, 'policy_end': endDate, 'source':source})
        if (decode_policy(1,visa,citizen,history,refugee,citException,workerException,countryException,air,land,sea) != 'NONE' or DEBUG):
            outputfile.write(row['Q1_5_TEXT']+"|"+countryName+"|"+row['ISO3']+"|"+iso2+"|COMPLETE|"+decode_policy(1,visa,citizen,history,refugee,citException,workerException,countryException,air,land,sea)+"|"+startDate+"|"+endDate+"|"+str(air)+"|"+airType+"|"+targetsAir+"|"+str(land)+"|"+landType+"|"+targetsLand+"|"+str(sea)+"|"+seaType+"|"+targetsSea+"|"+str(citizen)+"|"+citizenshipList+"|"+str(history)+"|"+historyList+"|"+str(refugee)+"|"+refugeeList+"|"+str(visa)+"|"+visaType+"|"+visaList+"|"+str(citException)+"|"+citExceptionList+"|"+str(countryException)+"|"+countryExceptionList+"|"+str(workerException)+"|"+source+"\n")

print "\nPOLICY_SUMMARY:\n"
print "WORK_EXCEP " + str(WORK_EXCEP/2)
print "SPECIFIC_COUNTRY " + str(SPECIFIC_COUNTRY/2)
print "CITIZEN_EXCEP " + str(CITIZEN_EXCEP/2)
print "ESSENTIAL_ONLY " + str(ESSENTIAL_ONLY/2)
print "VISA_BAN " + str(VISA_BAN/2)
print "CITIZENSHIP_BAN " + str(CITIZENSHIP_BAN/2)
print "HISTORY_BAN " + str(HISTORY_BAN/2)
print "BORDER_CLOSURE " + str(BORDER_CLOSURE/2)
print "CITIZENSHIP_BAN_AND_HISTORY_BAN " + str(CITIZENSHIP_BAN_AND_HISTORY_BAN/2)