# COVID Border Accountability Project (COBAP)

Last update: 12-7-2020 1201 Policies, 242 Territories

This is the data repository for the [COBAP project](https://www.covidborderaccountability.org/). 

The COVID Border Accountability Project (COBAP) provides a dataset of  >1000 policies systematized to reflect a complete timeline of new country-level restrictions on movement across international borders during the 2020 year. Using a 20-question survey, trained research assistants (RAs) sourced and documented for each new border policy: start and end dates, whether the closure constitutes a "complete closure" or "partial closure", which exceptions are made, which countries are banned, and which borders are closed, among other variables. In addition, the source of each policy was included in the database. The data provided is updated on a weekly basis, by Monday 12PM EST (17:00 UTC).

# INFO
COBAP tracks national level policies regarding immigration and travel. The policies are recorded by a team of RAs using Qualtrics.
The initial list of policies is based on the travel-related policies in [ACAPS COVID-19 GOVERNMENT MEASURES DATASET](https://www.acaps.org/covid-19-government-measures-dataset), with additional policies found by our team.

The policies are recorded, noting start and end dates for the policy, sources, restriction notes, and whether the policy falls into our framework of Complete or Partial Closure (or no policy implemented):

## Complete Closure
A new policy in which all newcomers are banned from all ports of entry—AIR, LAND, and SEA—with limited exceptions, including citizens, nationals from a specified country or set of up to 10 countries, and/or essential reasons, e.g. health emergencies, extreme humanitarian/diplomatic reasons, dignitaries, cargo flights, commercial transport, essential deliveries, permanent residents, existing visa holders, and family members of citizens

Further questions about the policy implemented are use to categorize complete closures into one of the following categories:

**Workers Exception**: A complete closure with exceptions for specific work permit status holders

**Specific Country(ies) Exception**: A complete closure with exceptions for essentials and for nationals from a specific country or listed set of countries (up to 10)

**Citizen Exception**: A complete closure with exceptions for essentials and for citizens (including citizens, permanent residents, and/or the family members of citizens and permanent residents)

**Essentials-only Exception**: A complete closure with exceptions for essentials but not for citizens

## Partial Closure
A new policy which restricts access of specific groups of people, whether by certain nationalities, travel histories; those entering through a specified land, sea or air border; OR all land borders closed OR all air borders closed OR all sea borders closed (but not all three)

Further questions about the policy implemented are use to categorize partial closures into one or more of the following categories:

**Visa ban(s)**: A partial closure which bans the application for new visas, whether all visa seekers or impacting those from specified countries

**Citizenship ban(s)**: A partial closure which bans foreign nationals from one country or group of countries, e.g. "entry to the country is denied to foreign nationals from Austria, Belgium, and France"

**Travel history ban(s)**: A partial closure which bans travelers who, regardless of nationality, have recently travelled  through or from a specified country or group of countries, e.g. for "All travelers who have been to or travelled through China, Hong Kong, Iran, Italy, and Japan are advised to not enter the country, and may be denied entry"

**Refugee ban(s)**: A partial closure which uses language targeting "refugees" or "asylum seekers".

**Border Closure(s)**: A partial closure which impacts those entering through a specified land, sea or air border; OR all land borders closed OR all air borders closed OR all sea borders closed (but not all three)

## No Policy Implemented
A small handful of nations have not implemented any restrictions falling into the categories above during the COVID-19 pandemic. These are included, recording the end date as the date the RA confirmed that no policies have been implemented, as well as a source of a government website on COVID-19 restrictions. 


## Notes
With the help of RAs, COBAP restricts the database to include policies which were implemented by the government or administrative structure of the country or territory recorded. We limit the scope of our data collection in this way in order to specify the country introducing the policy and the nations/persons who are targeted by it. This avoids the duplication of data and misrecording of policies at the national level. 

We do not include cases in which a country may effectively have experienced a border closure (or drastic human movement reduction) due to another country's policy decisions, or due to internal national-level or subnational level lockdowns. Furthermore, we do not capture the full extent of policies which are multidirectional, i.e. when one nation closes a border to both outgoing and ingoing traffic. 

We do not capture quarantine requirements for persons entering a country, even if they are targeted at specific citizens or travel history. We also do not capture rules regarding passenger transit, which may be more lax than the restriction recorded in our database (i.e. Australia allowing specific nations' citizens to transit through Australia via commercial air travel, even though entering Australia is only allowed for citizens, permanent residents and family).

This policy interpretation process can, in practice, become complicated, and in general the goal is to not represent all such cases in this database. Some examples include:

* Overseas departments and regions of France do not record French national level policies, except in cases where those policies explicitly mention restrictions in those regions.
* Guernsey's state owned airline, Aurigny, suspending all flights, and therefore removing all commercial air access to Guernsey (except emergency service to Southampton) is not recorded as an air border closure, as Guernsey's government never explicitly banned arrivals. 
* Vatican City workers who live in Rome allowed to travel into Vatican City for work during the complete closure will not be recorded as a Workers Exception as it is unrelated to specific classes of work permits.
* Niuean, Cook Islander, and	Tokelauan citizens travel on New Zealand passports, and therefore policy text may not indicate that New Zealand has a Specific Country Exception for these nations.




# FILELIST
File | Description
------------ | -------------
[data/raw_survey_output/main_survey_raw.csv](https://github.com/COBAPteam/COBAP/blob/main/data/raw_survey_output/main_survey_raw.csv)|The output from the Qualtrics survey completed by RAs to record policy implementation, modified to remove duplicate/updated policies, and ISO country codes.
[data/raw_survey_output/end_dates_survey_raw.csv](https://github.com/COBAPteam/COBAP/blob/main/data/raw_survey_output/end_dates_survey_raw.csv)|The output from the Qualtrics survey to record the end dates of policies, with sources, as well as any policy which was implemented in conjunction with the end of another policy in the dataset.
data/output/COBAP_policy_list.csv|The processed output to decode the survey responses into the policy types described below. 

# Data Fields in Policy List

Variable | Type | Description
------------ | ------------- | ---------------
id | alphanumeric | unique ID used for each policy
country_name| UTF-8 String | country name that implemented the restriction
iso3| 3 character String | unique three-letter country code published by the International Organization for Standardization. Non-standard codes: XKX - Kosovo, SOL - Somaliland, EUR - European Union Schengen Zone
iso2| 2 character String | unique two-letter country code published by the International Organization for Standardization. Non-standard codes: XK - Kosovo, XS - Somaliland, EU - European Union Schengen Zone
policy_type| categorical | one of COMPLETE, PARTIAL, or NOPOLICYIMPLEMENTED
policy_subtype| categorical | The policy sub-type, one of: ESSENTIAL_ONLY,CITIZEN_EXCEP,SPECIFIC_COUNTRY_EXCEP,WORK_EXCEP,VISA_BAN,CITIZENSHIP_BAN,HISTORY_BAN,REFUGEE_BAN,BORDER_CLOSURE,NONE. Note: Only the most restrictive partial closure is included, so a policy with CITIZENSHIP exception may have travel history or specific border closure information in the related fields.
start_date| date string | the date the policy was implemented (DD_MM_YY)
end_date| date string| the date the policy was lifted (DD_MM_YY)
air| binary | whether there was an air border closure (1) or not (0)
air_type| categorical |  whether the partial closure closed all or some air routes. One of: All, Specific, NA
targets_air| comma separated list | which air routes were targeted
land| binary | whether there was a land border closure(1) or not (0)
land_type| categorical | whether the partial closure closed all or some land routes. One of: All, Specific, NA
targets_land| comma separated list | which land routes were targeted
sea| binary | whether there was a sea border closure(1) or not (0)
sea_type| categorical | whether the partial closure closed all or some sea routes. One of: All, Specific, NA
targets_sea| comma separated list | which sea routes were targeted
citizen | binary | whether the partial closure targets certain groups of travelers by citizenship (1) or not (0)
citizen_list| commma separated list | which groups were targeted based on their citizenship status
history | binary |  whether the partial closure targets certain groups of travelers by travel history (1) or not (0)
history_list | comma separated list | which groups were targeted based on their recent travel status
refugee | binary | whether the partial closure uses the language of “refugee” or “asylum seeker” (1) or not (0)
refugee_list | comma separated list| which refugees are targeted
visa|binary | whether visa seekers are targeted (1) or not (0)
visa_type| categorical | which visa seekers are targeted. One of: All, Specific, NA
visa_list| comma separated list| which visa seekers are targeted
citizen_excep| binary | whether the complete closure makes an exception for citizens (1) or not (0)
citizen_excep_list|comma separated list| which persons are exempted from the complete closure
country_excep|binary| whether specific country(ies) are exempted from the complete closure (1) or not (0)
country_excep_list|comma separated list| which country(ies) are exempted from the complete closure
work_excep| binary |whether the complete closure exempts workers (1) or not (0)
source(0-4)| UTF-8 String | Web link to source of policy, one per column

# Contact
Please contact cobap@covidborderaccountability.org

For any issues with the recorded policies, feel free to submit a github issue or give us a heads up [here](https://docs.google.com/forms/d/1OGd-56pqT0iRPGv6iJdTnIWWI5vkbF2faAnTz5sDNxI).
 
# LICENSE 
GPL-3.0
