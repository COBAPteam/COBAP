import csv
import os
import pycountry
import codecs
import pandas
from datetime import datetime, date, timedelta

#Enable prints and write non-valid survey responses
DEBUG = False
WEBSITE_FILES = True
TIME_SERIES = True

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
#ESSENTIAL_ONLY
#CITIZEN_EXCEP
#SPECIFIC_COUNTRY
#WORK_EXCEP 
#VISA_BAN
#CITIZENSHIP_BAN
#HISTORY_BAN
#REFUGEE_BAN
#BORDER_CLOSURE

def decode_policy(complete,visa,citizen,history,refugee,citException,workerException,countryException,air,land,sea,unclear):
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
    if (unclear):
        if(DEBUG):
            return "UNCLEAR"
        else:
            return "NONE"
    elif (complete and workerException):
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
        return "REFUGEE_BAN"
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

#create list to gather policies for website files
policyList = []

policyId = {}

acapsSource = {}

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

for indexAcaps,acaps in acapsLinks.iterrows():  
    acapsSource[acaps[0]] = acaps[15] 

outputfile.write("ID|COUNTRY_NAME|ISO3|ISO2|POLICY_TYPE|POLICY_SUBTYPE|START_DATE|END_DATE|AIR|AIR_TYPE|TARGETS_AIR|LAND|LAND_TYPE|TARGETS_LAND|SEA|SEA_TYPE|TARGETS_SEA|CITIZEN|CITIZEN_LIST|HISTORY_BAN|HISTORY_BAN_LIST|REFUGEE|REFUGEE_LIST|VISA_BAN|VISA_BAN_TYPE|VISA_BAN_LIST|CITIZEN_EXCEP|CITIZEN_EXCEP_LIST|COUNTRY_EXCEP|COUNTRY_EXCEP_LIST|WORK_EXCEP|SOURCE_QUALITY|SOURCE_TYPE|INTERNAL_GOVT_SOURCE|AIRLINE_SOURCE|INSURANCE_SOURCE|GOVT_SOCIAL_MED_SOURCE|EXT_GOVT_SOURCE|INTERNAL_MEDIA_SOURCE|EXT_MEDIA_SOURCE|OTHER_SOURCE|END_SOURCE|COMMENTS|OLD_ID\n")


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
                if (row['Q1_5_TEXT'] in acapsSource.keys()):
                    source = acapsSource[row['Q1_5_TEXT']]

            print("NOSTARTDATE, %s"%(row['Q1_5_TEXT']))
            outputfile.write(row['Q1_5_TEXT']+"|"+countryName+"|"+row['ISO3']+"|"+iso2+"|NOSTARTDATE|NONE|NONE|NONE|0|NA|NA|0|NA|NA|0|NA|NA|0|NA|0|NA|0|NA|0|NA|NA|0|NA|0|NA|0|NA|"+source+"\n")
    
    elif(row['Q5'] == "I did a full contextual search"):
        source = row['Q5_3_TEXT']
        endDate = row['Q4'].split()[1].strip('()').rjust(2,'0') + "_" + row['Q22_1_TEXT'].rjust(2,'0') + "_20"
        outputfile.write(row['Q1_5_TEXT']+"|"+countryName+"|"+row['ISO3']+"|"+iso2+"|NOPOLICYIMPLEMENTED|NONE|NONE|"+endDate+"|0|NA|NA|0|NA|NA|0|NA|NA|0|NA|0|NA|0|NA|0|NA|NA|0|NA|0|NA|0|NA|"+source+"\n")
    
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
        endsource = ""
        for indexEndDates,rowEndDates in endDatesSurvey.iterrows():  
            if (rowEndDates['Q1_2_TEXT'] == row['Q1_5_TEXT']):
                if(rowEndDates['Q5']=='2020' or rowEndDates['Q5']==''):
                    endDate = month_to_num(rowEndDates['Q3']).rjust(2,'0') + '_' + rowEndDates['Q4_1_TEXT'].rjust(2,'0')+'_20'
                else:
                    endDate = month_to_num(rowEndDates['Q3']).rjust(2,'0') + '_' + rowEndDates['Q4_1_TEXT'].rjust(2,'0')+'_21'
                endsource = rowEndDates['Q2_2_TEXT']
        #INTERNAL_GOVT_SOURCE|AIRLINE_SOURCE|INSURANCE_SOURCE|GOVT_SOCIAL_MED_SOURCE|EXT_GOVT_SOURCE|INTERNAL_MEDIA_SOURCE|EXT_MEDIA_SOURCE|OTHER_SOURCE|NON_ENGLISH_SOURCE
        govt_source= row['Q27_3_TEXT'] if (row['Q27_3_TEXT'] != "") else row['Q20_3_TEXT']
        airline_source= row['Q27_1_TEXT'] if (row['Q27_1_TEXT'] != "") else row['Q20_1_TEXT']
        insurance_source= row['Q27_2_TEXT'] if (row['Q27_2_TEXT'] != "") else row['Q20_2_TEXT']
        social_media_source= row['Q27_4_TEXT'] if (row['Q27_4_TEXT'] != "") else row['Q20_4_TEXT']
        ext_govt_source=row['Q20_5_TEXT']
        int_media_source =row['Q20_6_TEXT']
        ext_media_source= row['Q20_14_TEXT']
        other_source =row['Q20_16_TEXT'] if (row['Q20_16_TEXT'] != "") else row['Q20_15_TEXT']
        if (other_source != ""):
            other_source = other_source +","+row['Q33_2_TEXT']
        else:
            other_source = row['Q33_2_TEXT']
        non_eng_source=row['Q28_1_TEXT']
        sourcetype = "1" if (govt_source != "") else ""
        sourcetype = sourcetype + ",2" if (airline_source != "" and sourcetype != "") else sourcetype + "2" if (airline_source != "") else sourcetype
        sourcetype = sourcetype + ",3" if (insurance_source != "" and sourcetype != "") else sourcetype + "3" if (insurance_source != "") else sourcetype
        sourcetype = sourcetype + ",4" if (social_media_source != "" and sourcetype != "") else sourcetype + "4" if (social_media_source != "") else sourcetype
        sourcetype = sourcetype + ",5" if (ext_govt_source != "" and sourcetype != "") else sourcetype + "5" if (ext_govt_source != "") else sourcetype
        sourcetype = sourcetype + ",6" if (int_media_source != "" and sourcetype != "") else sourcetype + "6" if (int_media_source != "") else sourcetype
        sourcetype = sourcetype + ",7" if (ext_media_source != "" and sourcetype != "") else sourcetype + "7" if (ext_media_source != "") else sourcetype
        sourcetype = sourcetype + ",8" if (other_source != "" and sourcetype != "") else sourcetype + "8" if (other_source != "") else sourcetype
        if (govt_source != ""):
            sourceQuality = "Very Sure"
        elif (airline_source!="" or insurance_source !=""):
            sourceQuality = "Sure"
        else:
            sourceQuality = "Less Sure"
        #grab source from acaps if no better source was found
        source = govt_source+"|"+airline_source+"|"+insurance_source+"|"+social_media_source+"|"+ext_govt_source+"|"+int_media_source+"|"+ext_media_source+"|"+ other_source+"|"+non_eng_source
        if (source == "||||||||"): #and row[13].split()[0] == "Unable"):
            sourcetype = "8"
            if (row['Q1_5_TEXT'] in acapsSource.keys()):
                other_source = acapsSource[row['Q1_5_TEXT']]
        source = govt_source+"|"+airline_source+"|"+insurance_source+"|"+social_media_source+"|"+ext_govt_source+"|"+int_media_source+"|"+ext_media_source+"|"+ other_source+"|"+non_eng_source

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

        unclear = 1 if "unclear" in row['Q7'] else 0
        unclearList = row['Q7_18_TEXT'] if (row['Q7_18_TEXT'] != "") else "NA"
        
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
        if (source == "||||||||"):
            print row['Q1_5_TEXT']
        if (decode_policy(0,visa,citizen,history,refugee,citException,workerException,countryException,air,land,sea,unclear) != 'NONE' or DEBUG):
            if (source != "||||||||"):
                if (row['ISO3'] in policyId.keys()):
                    policyId[row['ISO3']] = policyId[row['ISO3']] + 1
                    newId = policyId[row['ISO3']]

                else:
                    policyId[row['ISO3']] = 1;
                    newId = 1;
                policyList.append({'name' :countryName, 'id': row['Q1_5_TEXT'], 'ISO3': row['ISO3'], 'pc': 'PARTIAL', 'type': decode_policy(0,visa,citizen,history,refugee,citException,workerException,countryException,air,land,sea,0), 'policy_start' : startDate, 'policy_end': endDate, 'source':source})

                outputfile.write(iso2+"%02d" % (newId,)+"|"+countryName+"|"+row['ISO3']+"|"+iso2+"|PARTIAL|"+decode_policy(0,visa,citizen,history,refugee,citException,workerException,countryException,air,land,sea,unclear)+"|"+startDate+"|"+endDate+"|"+str(air)+"|"+str(airType)+"|"+targetsAir+"|"+str(land)+"|"+str(landType)+"|"+targetsLand+"|"+str(sea)+"|"+str(seaType)+"|"+targetsSea+"|"+str(citizen)+"|"+citizenshipList+"|"+str(history)+"|"+historyList+"|"+str(refugee)+"|"+refugeeList+"|"+str(visa)+"|"+visaType+"|"+visaList+"|"+str(citException)+"|"+citExceptionList+"|"+str(countryException)+"|"+countryExceptionList+"|"+str(workerException)+"|"+sourceQuality+"|"+sourcetype+"|"+govt_source+"|"+airline_source+"|"+insurance_source+"|"+social_media_source+"|"+ext_govt_source+"|"+int_media_source+"|"+ext_media_source+"|"+ other_source+"|"+endsource+"|"+row['Q33_1_TEXT']+"|"+row['Q1_5_TEXT']+"\n")

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

        endsource = ""
        for indexEndDates,rowEndDates in endDatesSurvey.iterrows():  
            if (rowEndDates['Q1_2_TEXT'] == row['Q1_5_TEXT']):
                if(rowEndDates['Q5']=='2020' or rowEndDates['Q5']==''):
                    endDate = month_to_num(rowEndDates['Q3']).rjust(2,'0') + '_' + rowEndDates['Q4_1_TEXT'].rjust(2,'0')+'_20'
                else:
                    endDate = month_to_num(rowEndDates['Q3']).rjust(2,'0') + '_' + rowEndDates['Q4_1_TEXT'].rjust(2,'0')+'_21'
                endsource = rowEndDates['Q2_2_TEXT']

        govt_source= row['Q27_3_TEXT'] if (row['Q27_3_TEXT'] != "") else row['Q20_3_TEXT']
        airline_source= row['Q27_1_TEXT'] if (row['Q27_1_TEXT'] != "") else row['Q20_1_TEXT']
        insurance_source= row['Q27_2_TEXT'] if (row['Q27_2_TEXT'] != "") else row['Q20_2_TEXT']
        social_media_source= row['Q27_4_TEXT'] if (row['Q27_4_TEXT'] != "") else row['Q20_4_TEXT']
        ext_govt_source=row['Q20_5_TEXT']
        int_media_source =row['Q20_6_TEXT']
        ext_media_source= row['Q20_14_TEXT']
        other_source =row['Q20_16_TEXT'] if (row['Q20_16_TEXT'] != "") else row['Q20_15_TEXT']
        if (other_source != ""):
            other_source = other_source +","+row['Q33_2_TEXT']
        else:
            other_source = row['Q33_2_TEXT']
        non_eng_source=row['Q28_1_TEXT']
        source = govt_source+"|"+airline_source+"|"+insurance_source+"|"+social_media_source+"|"+ext_govt_source+"|"+int_media_source+"|"+ext_media_source+"|"+ other_source+"|"+non_eng_source
        sourcetype = "1" if (govt_source != "") else ""
        sourcetype = sourcetype + ",2" if (airline_source != "" and sourcetype != "") else sourcetype + "2" if (airline_source != "") else sourcetype
        sourcetype = sourcetype + ",3" if (insurance_source != "" and sourcetype != "") else sourcetype + "3" if (insurance_source != "") else sourcetype
        sourcetype = sourcetype + ",4" if (social_media_source != "" and sourcetype != "") else sourcetype + "4" if (social_media_source != "") else sourcetype
        sourcetype = sourcetype + ",5" if (ext_govt_source != "" and sourcetype != "") else sourcetype + "5" if (ext_govt_source != "") else sourcetype
        sourcetype = sourcetype + ",6" if (int_media_source != "" and sourcetype != "") else sourcetype + "6" if (int_media_source != "") else sourcetype
        sourcetype = sourcetype + ",7" if (ext_media_source != "" and sourcetype != "") else sourcetype + "7" if (ext_media_source != "") else sourcetype
        sourcetype = sourcetype + ",8" if (other_source != "" and sourcetype != "") else sourcetype + "8" if (other_source != "") else sourcetype
        if (govt_source != ""):
            sourceQuality = "Very Sure"
        elif (airline_source!="" or insurance_source !=""):
            sourceQuality = "Sure"
        else:
            sourceQuality = "Less Sure"
        #grab source from acaps if no better source was found
        if (source == "||||||||"): #and row[13].split()[0] == "Unable"):
            sourcetype = "8"
            if (row['Q1_5_TEXT'] in acapsSource.keys()):
                other_source = acapsSource[row['Q1_5_TEXT']]

        source = govt_source+"|"+airline_source+"|"+insurance_source+"|"+social_media_source+"|"+ext_govt_source+"|"+int_media_source+"|"+ext_media_source+"|"+ other_source+"|"+non_eng_source

        citException = 1 if  "Yes" in row['Q6'] else 0 
        countryException = 1 if  "Yes" in row['Q9'] else 0
        workerException = 1 if "Yes" in row['Q8'] else 0

        unclear = 0 #1 if ("Unclear" in row['Q8'] or "Unclear" in row['Q9']) else 0

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
        if (source == "||||||||"):
            print row['Q1_5_TEXT']
        for indexCountryLists,rowCountryLists in targetsFixed.iterrows():  
            if (rowCountryLists[0] == row['Q1_5_TEXT']):
                if (rowCountryLists[3] != "Unclear" and rowCountryLists[3] != "" and rowCountryLists[3] != "No" and rowCountryLists[3] != "NA"):
                    countryExceptionList = rowCountryLists[3]
        if (decode_policy(1,visa,citizen,history,refugee,citException,workerException,countryException,air,land,sea,unclear) != 'NONE' or DEBUG):
            if (source != "||||||||"):
                if (row['ISO3'] in policyId.keys()):
                    policyId[row['ISO3']] = policyId[row['ISO3']] + 1
                    newId = policyId[row['ISO3']]
                else:
                    policyId[row['ISO3']] = 1;
                    newId = 1;
                policyList.append({'name' :countryName, 'id': row['Q1_5_TEXT'], 'ISO3': row['ISO3'], 'pc': 'COMPLETE', 'type': decode_policy(1,visa,citizen,history,refugee,citException,workerException,countryException,air,land,sea,0), 'policy_start' : startDate, 'policy_end': endDate, 'source':source})
                outputfile.write(iso2+"%02d" % (newId,)+"|"+countryName+"|"+row['ISO3']+"|"+iso2+"|COMPLETE|"+decode_policy(1,visa,citizen,history,refugee,citException,workerException,countryException,air,land,sea,unclear)+"|"+startDate+"|"+endDate+"|"+str(air)+"|"+airType+"|"+targetsAir+"|"+str(land)+"|"+landType+"|"+targetsLand+"|"+str(sea)+"|"+seaType+"|"+targetsSea+"|"+str(citizen)+"|"+citizenshipList+"|"+str(history)+"|"+historyList+"|"+str(refugee)+"|"+refugeeList+"|"+str(visa)+"|"+visaType+"|"+visaList+"|"+str(citException)+"|"+citExceptionList+"|"+str(countryException)+"|"+countryExceptionList+"|"+str(workerException)+"|"+sourceQuality+"|"+sourcetype+"|"+govt_source+"|"+airline_source+"|"+insurance_source+"|"+social_media_source+"|"+ext_govt_source+"|"+int_media_source+"|"+ext_media_source+"|"+ other_source+"|"+endsource+"|"+row['Q33_1_TEXT']+"|"+row['Q1_5_TEXT']+"\n")

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

outputfile.close()

def web_policy_language(policy):
    if(policy == "WORK_EXCEP"):
        return 'Workers Exception'
    if(policy == "SPECIFIC_COUNTRY"):
        return 'Specific Country(ies) Exception'
    if(policy == "CITIZEN_EXCEP"):
        return 'Citizen Exception'
    if(policy == "ESSENTIAL_ONLY"):
        return 'Essentials-only Exception'
    if(policy == "VISA_BAN"):
        return 'Visa ban'
    if(policy == "CITIZENSHIP_BAN"):
        return 'Citizenship ban'
    if(policy == "HISTORY_BAN"):
        return 'Travel history ban'
    if(policy == "REFUGEE_BAN"):
        return 'NONE'
    if(policy == "BORDER_CLOSURE"):
        return 'Border Closure'
    if(policy == "NONE"):
        return 'NONE'

def carto_policy_language(policy):
    if(policy == "WORK_EXCEP"):
        return 'Workers Exception'
    if(policy == "SPECIFIC_COUNTRY"):
        return 'Specific Country(ies) Exception'
    if(policy == "CITIZEN_EXCEP"):
        return 'Citizen Exception'
    if(policy == "ESSENTIAL_ONLY"):
        return 'Essentials-only Exception'
    if(policy == "VISA_BAN"):
        return 'Visa ban(s)'
    if(policy == "CITIZENSHIP_BAN"):
        return 'Citizenship ban(s)'
    if(policy == "HISTORY_BAN"):
        return 'Travel history ban(s)'
    if(policy == "REFUGEE_BAN"):
        return 'NONE'
    if(policy == "BORDER_CLOSURE"):
        return 'Border Closure(s)'
    if(policy == "NONE"):
        return 'NONE'

test_countries = ('ABW','AFG')

countries = ('ABW','AFG','AGO','AIA','ALA','ALB','AND','ARE','ARG','ARM','ASM','ATA','ATF','ATG','AUS','AUT','AZE','BDI','BEL','BEN','BES','BFA','BGD','BGR','BHR',
    'BHS','BIH','BLM','BLR','BLZ','BMU','BOL','BRA','BRB','BRN','BTN','BVT','BWA','CAF','CAN','CCK','CHE','CHL','CHN','CIV','CMR','COD','COG','COK','COL','COM','CPV',
    'CRI','CUB','CUW','CXR','CYM','CYP','CZE','DEU','DJI','DMA','DNK','DOM','DZA','ECU','EGY','ERI','SAH','ESP','EST','ETH','FIN','FJI','FLK','FRA','FRO','FSM','GAB',
    'GBR','GEO','GGY','GHA','GIB','GIN','GLP','GMB','GNB','GNQ','GRC','GRD','GRL','GTM','GUF','GUM','GUY','HKG','HMD','HND','HRV','HTI','HUN','IDN','IMN','IND','IOT',
    'IRL','IRN','IRQ','ISL','ISR','ITA','JAM','JEY','JOR','JPN','KAZ','KEN','KGZ','KHM','KIR','KNA','KOR','KWT','LAO','LBN','LBR','LBY','LCA','LIE','LKA','LSO','LTU',
    'LUX','LVA','MAC','MAF','MAR','MCO','MDA','MDG','MDV','MEX','MHL','MKD','MLI','MLT','MMR','MNE','MNG','MNP','MOZ','MRT','MSR','MTQ','MUS','MWI','MYS','MYT','NAM',
    'NCL','NER','NFK','NGA','NIC','NIU','NLD','NOR','NPL','NRU','NZL','OMN','PAK','PAN','PCN','PER','PHL','PLW','PNG','POL','PRI','PRK','PRT','PRY','KOS','PYF','QAT',
    'REU','ROU','RUS','RWA','SAU','SDN','SEN','SGP','SGS','SHN','SJM','SLB','SLE','SLV','SMR','SOL','SOM','SPM','SRB','SSD','STP','SUR','SVK','SVN','SWE','SWZ','SXM','SYC',
    'SYR','TCA','TCD','TGO','THA','TJK','TKL','TKM','TLS','TON','TTO','TUN','TUR','TUV','TWN','TZA','UGA','UKR','UMI','URY','USA','UZB','VAT','VCT','VEN','VGB','VIR',
    'VNM','VUT','WLF','WSM','YEM','ZAF','ZMB','ZWE','PSX','EUR')

weeks = ('1_26_20','2_2_20','2_9_20','2_16_20','2_23_20','3_1_20','3_8_20','3_15_20','3_22_20','3_29_20','4_5_20','4_12_20','4_19_20','4_26_20','5_3_20','5_10_20','5_17_20','5_24_20','5_31_20','6_7_20','6_14_20','6_21_20','6_28_20','7_5_20','7_12_20','7_19_20','7_26_20','8_2_20','8_9_20','8_16_20','8_23_20','8_30_20','9_6_20','9_13_20','9_20_20','9_27_20','10_4_20','10_11_20','10_18_20','10_25_20','11_1_20','11_8_20','11_15_20','11_22_20','11_29_20','12_6_20','12_13_20','12_20_20','12_27_20')

policies = ["Workers Exception","Specific Country(ies) Exception","Citizen Exception","Essentials-only Exception","Visa ban(s)","Citizenship ban(s)","Travel history ban(s)","Border Closure(s)","NONE"]


if(TIME_SERIES):
    outputfile = codecs.open("policy_timeseries.csv", 'w',"utf-8")

    outputfile.write("iso3|countryname|date|complete|partial|completenew|partialnew|work_excepnew|specific_countrynew|citizen_excepnew|essential_onlynew|visa_bannew|citizenship_bannew|history_bannew|border_closurenew\n")
    for country in countries:
        if(country=="EUR"):
            iso3 = "EUR"
            name = "European Union"
        elif(country=="SAH"):
            iso3 = "ESH"
            name = "Sahrawi Arab Democratic Republic"
        elif(country=="KOS"):
            iso3 = "XKX"
            name = "Kosovo"
        elif(country=="PSX"):
            iso3 = "PSE"
            name = "Palestine"
        elif(country=="SOL"):
            iso3 = "SOL"
            name = "Somaliland"
        else:
            iso3 = country
            name = pycountry.countries.get(alpha_3=country).name
        date_iter = 0
        for dates in weeks:
            complete = 0
            partial = 0
            completenew = 0
            partialnew = 0
            work_excepnew = 0
            specific_countrynew = 0
            citizen_excepnew = 0 
            essential_onlynew = 0
            visa_bannew = 0
            citizenship_bannew = 0
            history_bannew = 0
            border_closurenew = 0
            for policy in policyList:
                if("00" in policy['policy_start'] or "and" in policy['policy_start']):
                    continue
                if (policy['ISO3'] == country):
                    #start month less, end month greater
                    if ((int(policy['policy_start'].split('_')[0]) < int(weeks[date_iter].split('_')[0])) and (int(policy['policy_start'].split('_')[2]) == 20)) and \
                     ((policy['policy_end'] == "NONE") or (int(policy['policy_end'].split('_')[0]) > int(weeks[date_iter].split('_')[0]))):
                        if (policy['pc'] == 'PARTIAL'):
                            partial = partial + 1
                        elif (policy['pc'] == 'COMPLETE'):
                            complete = complete + 1
                    #start month same, end month greater
                    elif ((int(policy['policy_start'].split('_')[0]) == int(weeks[date_iter].split('_')[0])) and (int(policy['policy_start'].split('_')[2]) == 20)) and \
                     ((policy['policy_end'] == "NONE") or (int(policy['policy_end'].split('_')[0]) > int(weeks[date_iter].split('_')[0]))):
                        if ((int(policy['policy_start'].split('_')[1]) <= int(weeks[date_iter].split('_')[1]) + 6)):
                            if (policy['pc'] == 'PARTIAL'):
                                partial = partial + 1
                            elif (policy['pc'] == 'COMPLETE'):
                                complete = complete + 1
                    #start month less, end month same
                    elif ((int(policy['policy_start'].split('_')[0]) < int(weeks[date_iter].split('_')[0])) and (int(policy['policy_start'].split('_')[2]) == 20)) and \
                     ((int(policy['policy_end'].split('_')[0]) == int(weeks[date_iter].split('_')[0])) and (int(policy['policy_end'].split('_')[2]) == 20)):
                        if ((int(policy['policy_end'].split('_')[1]) >= int(weeks[date_iter].split('_')[1]))):
                            if (policy['pc'] == 'PARTIAL'):
                                partial = partial + 1
                            elif (policy['pc'] == 'COMPLETE'):
                                complete = complete + 1
                    #start month smae, end month same
                    elif ((int(policy['policy_start'].split('_')[0]) == int(weeks[date_iter].split('_')[0])) and (int(policy['policy_start'].split('_')[2]) == 20)) and \
                     ((int(policy['policy_end'].split('_')[0]) == int(weeks[date_iter].split('_')[0])) and (int(policy['policy_end'].split('_')[2]) == 20)):
                        if ((int(policy['policy_end'].split('_')[1]) >= int(weeks[date_iter].split('_')[1]))):
                            if ((int(policy['policy_start'].split('_')[1]) <= int(weeks[date_iter].split('_')[1]) + 6)):
                                if (policy['pc'] == 'PARTIAL'):
                                    partial = partial + 1
                                elif (policy['pc'] == 'COMPLETE'):
                                    complete = complete + 1
            date_iter = date_iter + 1
            date_iter_date = datetime.strptime(dates, "%m_%d_%y")
            for delta in range (0,7):
                for policy in policyList:
                    if (policy['ISO3'] == country):
                        #start month less, end month greater
                        if (int(policy['policy_start'].split('_')[1]) != 0):
                            if((date_iter_date + timedelta(days=delta)) == datetime.strptime(policy['policy_start'], "%m_%d_%y")):
                                if (policy['pc'] == 'PARTIAL'):
                                    partialnew = partialnew + 1
                                elif (policy['pc'] == 'COMPLETE'):
                                    completenew = completenew + 1
                                if(policy['type'] == "WORK_EXCEP"):
                                    work_excepnew = work_excepnew + 1;
                                if(policy['type'] == "SPECIFIC_COUNTRY"):
                                    specific_countrynew = specific_countrynew + 1;
                                if(policy['type'] == "CITIZEN_EXCEP"):
                                    citizen_excepnew = citizen_excepnew + 1; 
                                if(policy['type'] == "ESSENTIAL_ONLY"):
                                    essential_onlynew = essential_onlynew + 1;
                                if(policy['type'] == "VISA_BAN"):
                                    visa_bannew = visa_bannew + 1;
                                if(policy['type'] == "CITIZENSHIP_BAN"):
                                    citizenship_bannew = citizenship_bannew + 1;
                                if(policy['type'] == "HISTORY_BAN"):
                                    history_bannew = history_bannew + 1;
                                if(policy['type'] == "BORDER_CLOSURE"):
                                    border_closurenew = border_closurenew + 1;

            outputfile.write(iso3+'|'+name+'|'+dates+'|'+str(complete)+'|'+str(partial)+'|'+str(completenew)+'|'+str(partialnew)+'|'+str(work_excepnew)+'|'+str(specific_countrynew)+'|')
            outputfile.write(str(citizen_excepnew)+'|'+str(essential_onlynew)+'|'+str(visa_bannew)+'|'+str(citizenship_bannew)+'|'+str(history_bannew)+'|'+str(border_closurenew)+'\n')


#File for website sidebar
if(WEBSITE_FILES):
    outputfile = codecs.open("website_info.csv", 'w',"utf-8")

    outputfile.write("iso3|country|policy|start_m|start_d|end_m|end_d|\n")

    for policy in policyList:
        #Carto ISO3 codes
        if(policy['ISO3']=="EUR"):
            iso3="XXX"
        elif(policy['ISO3']=="ESH"):
            iso3 = "SAH"
        elif(policy['ISO3']=="XKX"):
            iso3 = "KOS"
        elif(policy['ISO3']=="PSE"):
            iso3 = "PSX"
        else:
            iso3 = policy['ISO3']
        if("00" not in policy['policy_start'] and "and" not in policy['policy_start']):
            start_day = int(policy['policy_start'].split('_')[1])
            start_month =  int(policy['policy_start'].split('_')[0]) if (int(policy['policy_start'].split('_')[2]) == 20) else  int(policy['policy_start'].split('_')[0]) + 12
        if(policy['policy_end']!="NONE" and "00" not in policy['policy_end']):
            end_day = int(policy['policy_end'].split('_')[1])
            end_month =  int(policy['policy_end'].split('_')[0]) if (int(policy['policy_end'].split('_')[2]) == 20) else  int(policy['policy_end'].split('_')[0]) + 12
        if ("00" not in policy['policy_start'] and policy['policy_end']=="NONE"):
            outputfile.write(iso3+'|'+policy['name']+'|'+web_policy_language(policy['type']) + '|'+str(start_month)+'|'+str(start_day)+'|'+'24|31'+'|' + policy['source'] +'\n')
        elif("00" not in policy['policy_start'] and "00" not in policy['policy_end']):
            outputfile.write(iso3+'|'+policy['name']+'|'+web_policy_language(policy['type']) + '|'+str(start_month)+'|'+str(start_day)+'|'+str(end_month)+'|'+str(end_day)+'|' + policy['source'] +'\n')

    outputfile.close()

    outputfile = codecs.open("carto_output.csv", 'w',"utf-8")

    countrypolicyList = {}
    for country in countries:
        #Carto differing country codes
        if(country == "PSX"):
            #outputfile.write('Palestine|')
            iso3 = "PSE"
        elif(country == "SOL"):
            #outputfile.write('Somaliland|')
            iso3 = "SOL"
        elif(country == "KOS"):
            #outputfile.write('Kosovo|')
            iso3 = "XKX"
        elif(country == "SAH"):
            #outputfile.write('Sahrawi Arab Democratic Republic|')
            iso3 = "ESH"
        else:
            #outputfile.write(pycountry.countries.get(alpha_3=country).name+'|')
            iso3 = country
        countrypolicyList[iso3] = {}
        for policy in policies:
            countrypolicyList[iso3][policy] = {'start_m' : '24', 'start_d': '31', 'end_m': '24', 'end_d': '30'}
        countrypolicyList[iso3]["NONE"]['start_d'] = '1'
        countrypolicyList[iso3]["NONE"]['start_m'] = '1'

        for policy in policyList:
            if("00" not in policy['policy_start'] and "and" not in policy['policy_start']):
                start_day = int(policy['policy_start'].split('_')[1])
                start_month =  int(policy['policy_start'].split('_')[0]) if (int(policy['policy_start'].split('_')[2]) == 20) else  int(policy['policy_start'].split('_')[0]) + 12
            if(policy['policy_end']!="NONE" and "00" not in policy['policy_end']):
                end_day = int(policy['policy_end'].split('_')[1])
                end_month =  int(policy['policy_end'].split('_')[0]) if (int(policy['policy_end'].split('_')[2]) == 20) else  int(policy['policy_end'].split('_')[0]) + 12
            if (iso3 == policy['ISO3']):
                if("00" not in policy['policy_start'] and "and" not in policy['policy_start']):
                    if(int(countrypolicyList[iso3][carto_policy_language(policy['type'])]['start_m']) >= start_month):
                        if((int(countrypolicyList[iso3][carto_policy_language(policy['type'])]['start_m']) > start_month) or (int(countrypolicyList[iso3][carto_policy_language(policy['type'])]['start_d']) >= start_day)):
                            countrypolicyList[iso3][carto_policy_language(policy['type'])]['start_m'] = start_month
                            countrypolicyList[iso3][carto_policy_language(policy['type'])]['start_d'] = start_day
                        if((int(countrypolicyList[iso3][carto_policy_language(policy['type'])]['start_m']) == start_month) and (int(countrypolicyList[iso3][carto_policy_language(policy['type'])]['start_d']) >= start_day)):
                            countrypolicyList[iso3][carto_policy_language(policy['type'])]['start_m'] = start_month
                            countrypolicyList[iso3][carto_policy_language(policy['type'])]['start_d'] = start_day
                        if(policy['policy_end']=="NONE"):
                            countrypolicyList[iso3][carto_policy_language(policy['type'])]['end_m'] = '24'
                            countrypolicyList[iso3][carto_policy_language(policy['type'])]['end_d'] = '31'
                        elif("00" not in policy['policy_end']):
                            if((countrypolicyList[iso3][carto_policy_language(policy['type'])]['end_m'] == '24') and (countrypolicyList[iso3][carto_policy_language(policy['type'])]['end_d'] == '30')):
                                countrypolicyList[iso3][carto_policy_language(policy['type'])]['end_m'] = end_month
                                countrypolicyList[iso3][carto_policy_language(policy['type'])]['end_d'] = end_day
                    if(policy['policy_end']=="NONE" and "00" not in policy['policy_end']):
                        countrypolicyList[iso3][carto_policy_language(policy['type'])]['end_m'] = '24'
                        countrypolicyList[iso3][carto_policy_language(policy['type'])]['end_d'] = '31'
                    elif("00" not in policy['policy_end']):
                        if(int(countrypolicyList[iso3][carto_policy_language(policy['type'])]['end_m']) <= end_month):
                            if((int(countrypolicyList[iso3][carto_policy_language(policy['type'])]['end_m']) < end_month) or (int(countrypolicyList[iso3][carto_policy_language(policy['type'])]['end_d']) <= end_day)):
                                countrypolicyList[iso3][carto_policy_language(policy['type'])]['end_m'] = end_month
                                countrypolicyList[iso3][carto_policy_language(policy['type'])]['end_d'] = end_day    

    outputfile.write("iso3|country|policy_0|start_0d|end_0d|policy_1|start_1d|end_1d|policy_2|start_2d|end_2d|policy_3|start_3d|end_3d|policy_4|start_4d|end_4d|policy_5|start_5d|end_5d|policy_6|start_6d|end_6d|policy_7|start_7d|end_7d|policy_8|start_8d\n")
    for country in countries:
        outputfile.write(country+'|')
        #Carto differing country codes
        if(country == "PSX"):
            outputfile.write('Palestine|')
            iso3 = "PSE"
        elif(country == "SOL"):
            outputfile.write('Somaliland|')
            iso3 = "SOL"
        elif(country == "KOS"):
            outputfile.write('Kosovo|')
            iso3 = "XKX"
        elif(country == "SAH"):
            outputfile.write('Sahrawi Arab Democratic Republic|')
            iso3 = "ESH"
        elif(country == "EUR"):
            continue
        else:
            outputfile.write(pycountry.countries.get(alpha_3=country).name+'|')
            iso3 = country
        i=0
        for policy in policies:
            if policy == "NONE":
                outputfile.write('No Policy|0|731|')
            elif (countrypolicyList[iso3][policy]['start_m'] == "24" and countrypolicyList[iso3][policy]['start_d'] == "31"):
                outputfile.write('|731|731|')
            else:
                if(int(countrypolicyList[iso3][policy]['start_m']) > 12):
                    #print countrypolicyList[iso3][policy]['start_m']
                    #print iso3
                    startday = date(2021, int(countrypolicyList[iso3][policy]['start_m'])-12, int(countrypolicyList[iso3][policy]['start_d'])).timetuple().tm_yday + 365
                else:
                    startday = date(2020, int(countrypolicyList[iso3][policy]['start_m']), int(countrypolicyList[iso3][policy]['start_d'])).timetuple().tm_yday - 1
                if(int(countrypolicyList[iso3][policy]['end_m']) > 12):
                    #print iso3
                    endday = date(2021, int(countrypolicyList[iso3][policy]['end_m'])-12, int(countrypolicyList[iso3][policy]['end_d'])).timetuple().tm_yday + 365
                else:
                    endday = date(2020, int(countrypolicyList[iso3][policy]['end_m']), int(countrypolicyList[iso3][policy]['end_d'])).timetuple().tm_yday - 1
                outputfile.write(policy +'|'+str(startday)+'|'+str(endday)+'|')
            i = i+1
        outputfile.write('\n')
