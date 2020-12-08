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

**Refugee ban(s)**: A partial closure which impacts those entering through a specified land, sea or air border; OR all land borders closed OR all air borders closed OR all sea borders closed (but not all three)

**Border Closure(s)**: A partial closure which impacts refugees or asylum seekers.

## No Policy Implemented
A small handful of nations have not implemented any restrictions falling into the categories above during the COVID-19 pandemic. These are included, recording the end date as the date the RA confirmed that no policies have been implemented, as well as a source of a government website on COVID-19 restrictions. 


## Notes
With the help of RAs, COBAP restricts the database to include policies which were implemented by the government or administrative structure of the country or territory. We limit the scope of our data collection in this way in order to specify the country introducing the policy and the nations/persons who are targeted by it. This avoids the duplication of data and misrecording of policies at the national level. 

We do not include cases in which a country may effectively have experienced a border closure (or drastic human movement reduction) due to another country's policy decisions, or due to internal national-level or subnational level lockdowns. Furthermore, we do not capture the full extent of policies which are multidirectional, i.e. when one nation closes a border to both outgoing and ingoing traffic. This policy interpretation process can, in practice, become complicated because some nations have limited transportation links through other nations. For instance, many of the island nations of the Pacific Island Forum rely on air transport links through Australia. These types of relationships are not explicitly captured as policies for the affected nations, but rather in the “Specific Country(ies) Exception” of the nations making the restriction (I.e. Australia’s Complete Closure lists New Zealand, the Pacific Island Forum countries, Timor-Leste, New Caledonia, and French Polynesia as exceptions to their travel ban in order not to sever these air transportation links). 




# FILELIST
File | Description
------------ | -------------
[data/raw_survey_output/main_survey_raw.csv](https://github.com/COBAPteam/COBAP/blob/main/data/raw_survey_output/main_survey_raw.csv)|The output from the Qualtrics survey completed by RAs to record policy implementation, modified to remove duplicate/updated policies, and ISO country codes.
[data/raw_survey_output/end_dates_survey_raw.csv](https://github.com/COBAPteam/COBAP/blob/main/data/raw_survey_output/end_dates_survey_raw.csv)|The output from the Qualtrics survey to record the end dates of policies, with sources, as well as any policy which was implemented in conjunction with the end of another policy in the dataset.
data/output/COBAP_policy_list.csv|The processed output to decode the survey responses into the policy types described below. 

# Data Fields in Policy List

Variable | Description
------------ | -------------
id | unique ID used for each policy
country_name| country name that implemented the restriction
iso3|unique three-letter country code as published by the International Organization for Standardization. Non-standard codes: XKX - Kosovo, SOL - Somaliland, EUR - European Union Schengen Zone
iso2|unique two-letter country code as published by the International Organization for Standardization. Non-standard codes: XK - Kosovo, XS - Somaliland, EU - European Union Schengen Zone
policy_type| one of COMPLETE, PARTIAL, or NOPOLICYIMPLEMENTED
policy_subtype|The policy sub-type, one of: ESSENTIAL_ONLY,CITIZEN_EXCEP,SPECIFIC_COUNTRY,WORK_EXCEP,VISA,CITIZENSHIP,HISTORY,REFUGEE_BAN,BORDER,NONE. Note: Only the most restrictive partial closure is included, so a policy with CITIZENSHIP exception may have travel history or specific border closure information in the related fields.
start_date| the date the policy was implemented (DD_MM_YY)
end_date| the date the policy was lifted (DD_MM_YY)
air| whether there was a air border closure or not (1 or 0)
air_type| whether the partial closure closed all or some air routes
targets_air| which air routes were targeted
land| whether there was a land border closure or not (1 or 0)
land_type| whether the partial closure closed all or some land routes
targets_land| which land routes were targeted
sea| whether there was a sea border closure or not (1 or 0)
sea_type| whether the partial closure closed all or some sea routes
targets_sea| which sea routes were targeted
citizen | whether the partial closure targets certain groups of travelers by citizenship (1 or 0)
citizen_list| which groups were targeted based on their citizenship status
history | whether the partial closure targets certain groups of travelers by travel history (1 or 0)
history_list| which groups were targeted based on their recent travel status
refugee| partial closure restriction which uses the language of “refugee” or “asylum seeker” (1 or 0)
refugee_list| which refugees are targeted
visa| whether visa seekers are targeted (1 or 0)
visa_type| which visa seekers are targeted, all or some
visa_list| which visa seekers are targeted
citizen_excep| whether the complete closure makes an exception for citizens (1 or 0)
citizen_excep_list| which persons are exempted from the complete closure
country_excep| which country(ies) are exempted from the complete closure (1 or 0)
country_excep_list| which country(ies) are exempted from the complete closure
work_excep| whether the complete closure exempts workers (1 or 0)
source(0-4)| Web link(s) to source of policy, separated per column

# Contact
Please contact cobap@covidborderaccountability.org

For any issues with the recorded policies, feel free to submit a github issue or give us a heads up [here](https://docs.google.com/forms/d/1OGd-56pqT0iRPGv6iJdTnIWWI5vkbF2faAnTz5sDNxI).

# LICENSE 
GPL-3.0
