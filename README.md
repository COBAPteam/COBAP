# COVID Border Accountability Project (COBAP)

Last update: 06-27-2021 1,328 Policies, 246 Territories

This is the data repository for the [COBAP project](https://www.covidborderaccountability.org/). 

The COVID Border Accountability Project (COBAP) provides a dataset of  >1000 policies systematized to reflect a complete timeline of new country-level restrictions on movement across international borders during the 2020 year. Using a 20-question survey, trained research assistants (RAs) sourced and documented for each new border policy: start and end dates, whether the closure constitutes a "complete closure" or "partial closure", which exceptions are made, which countries are banned, and which borders are closed, among other variables. In addition, the source of each policy was included in the database. The data provided is updated on a weekly basis, by Monday 12PM EST (17:00 UTC).

# INFO
COBAP tracks national-level policies regarding immigration and travel introduced in response to the COVID-19 pandemic. The policies are recorded by a team of RAs using a curated Qualtrics survey per policy.
The initial list of policies is based on a travel-related policies in [ACAPS COVID-19 GOVERNMENT MEASURES DATASET](https://www.acaps.org/covid-19-government-measures-dataset), with the bulk of our database found by our team. 

The policies are recorded, noting start and end dates for the policy, sources, country exceptions/targets, and whether the policy falls into our framework of Complete or Partial Closure (or no policy implemented):

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
A small handful of nations have not implemented any restrictions falling into the categories above during the COVID-19 pandemic. A policy is recorded for these nations, with the end_date being the most recent date a thorough search was performed, as well as a government website on COVID-19 restrictions for the source.

## Notes
With the help of RAs, COBAP restricts the database to include policies which were implemented by the government or administrative structure of the country or territory recorded. We limit the scope of our data collection in this way in order to specify the country introducing the policy and the nations/persons who are targeted by it. This avoids the duplication of data and misrecording of policies at the national level. 

We do not include cases in which a country may effectively have experienced a border closure (or drastic human movement reduction) due to another country's policy decisions, or due to internal national-level or subnational level lockdowns. Furthermore, we do not capture the full extent of policies which are multidirectional, i.e. when one nation closes a border to both outgoing and ingoing traffic. 

We do not capture quarantine requirements for persons entering a country. We also do not capture rules regarding passenger transit. For instance, when Australia's government bars entry to all foreigners but allows specific nations' citizens to transit through Australia via commercial air travel, but we record this as an "complete closure (citizen exception) since they are not able to stay.

This policy interpretation process can, in practice, become complicated. Our goal was to approach federal-level governing territories systematically and produce correct data. Examples of the complicated cases we faced, and the decisions we made, include:

* France: French national-level policies apply to French overseas departments and regions (which are territorially not connected to mainland France). We do not include these national-level policies, for these overseas French entities .
* Guernsey's state-owned airline, Aurigny, suspended all flights, which effectively removed all commercial air access to Guernsey (except emergency service to Southampton). We did not record this as air border closure because Guernsey's government never explicitly banned arrivals.
* Vatican City was closed to all foreigners, but workers who live in Rome are allowed to travel into the Vatican City for work purposes. We record this as a "complete closure," with a "workers exception".
* Niuean, Cook Islander, and Tokelauan citizens travel on New Zealand passports as New Zealand citizens. This means when we record a "complete closure" for New Zealand, we might not capture a specific country exception for these nations. We only record the country names listed in the text.
* For additional complicated cases and the decisions we made, see our [RA FAQ list in the supplementary doc](https://github.com/COBAPteam/COBAP/blob/main/documentation/COBAP_Supplementary_Doc.pdf).

The following Codes are used in country lists:
* COVIDCASES: Policy indicates "Countries with active covid cases/transmission"

# FILELIST
File | Description
------------ | -------------
[data/output/policy_list.csv](https://github.com/COBAPteam/COBAP/blob/main/data/policy_list.csv)|The processed output to decode the survey responses into the policy types described below. View this file for the final, sanitized results.
[data/raw_survey_output/main_survey_raw.csv](https://github.com/COBAPteam/COBAP/blob/main/data/raw_survey_output/main_survey_raw.csv)|The output from the Qualtrics survey completed by RAs to record policy implementation, modified to remove duplicate/updated policies, and ISO country codes.
[data/raw_survey_output/end_dates_survey_raw.csv](https://github.com/COBAPteam/COBAP/blob/main/data/raw_survey_output/end_dates_survey_raw.csv)|The output from the Qualtrics survey to record the end dates of policies, with sources, as well as any policy which was implemented in conjunction with the end of another policy in the dataset.


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
source_quality | string | Very sure: internal government source, sure: airline or insurance source, less sure: any other source type
source_type|comma separated list| indication of source types included 1: internal_govt_source, 2: airline_source, 3: insurance_source, 4: govt_social_med_source, 5: ext_govt_source, 6: internal_media_source, 7: ext_media_source, 8: other source, 9: A combination of other partial closures leading to a complete closure, policies contributing listed in Comments and internal_govt_source
internal_govt_source| UTF-8 String | Web link to source of policy from a Government website of the host country
airline_source| UTF-8 String | Web link to source of policy from the airline industry or IATA
insurance_source| UTF-8 String | Web link to source of policy from the international insurance industry
govt_social_med_source| UTF-8 String | Web link to source of policy from a Government verified social media post 
ext_govt_source| UTF-8 String | Web link to source of policy from a Government website of an external country 
internal_media_source| UTF-8 String | Web link to source of policy from a major news outlet of host country
ext_media_source| UTF-8 String | Web link to source of policy from a major news outlet of external country 
other_source| UTF-8 String | Web link to source of policy that doesn't fit into other source categories above
end_source| UTF-8 String | Web link to source of policy indicating policy has ended if not present in original source
comment | UTF-8 String | Comments related to coding decisions
old_id | alphanumeric | ID for policy before ID change
# Contact
Please contact nikolas_lazar@brown.edu.

For any issues with the recorded policies, feel free to submit a github issue or give us a heads up [here](https://docs.google.com/forms/d/1OGd-56pqT0iRPGv6iJdTnIWWI5vkbF2faAnTz5sDNxI).
 
# Contributors 
Mary A. Shiraef, Mark A. Weiss, Cora Hirst, Bryn Walker, Thuy Nguyen, Camilla Kline, Aadya Bhaskaran, Elizabeth Beling, Layth Mattar, Matthew Amme, Maggie Shum, Johanna Sweere, Susanna Brantley, Luis Schenoni, Colin Lewis-Beck, Yashwini Selvaraj, Cayleigh Jackson, Nikolas Lazar, Rachel Musetti, Sarah Naseer, Noah Taylor, Amalia Gradie, William Yu, Jonathan Falcone, Erin Straight, Mary Mitsdarffer


# LICENSE 
GPL-3.0
