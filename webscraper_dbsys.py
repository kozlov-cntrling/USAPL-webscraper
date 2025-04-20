from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, parse_qs
url = 'https://usapl.liftingdatabase.com/competitions-view?id=121634'
scrape_url = requests.get(url)
soup = BeautifulSoup(scrape_url.text, 'html.parser')


#initialize variables
category = None
comp_log_lifter_id = 0
category_id = 0
squat = None 
benchPress = None 
deadlift = None 
lift_id = 0
lift_numbers = [0] * 9

#dictonaries
teams_inserted = {}
lift_types = ['Squat', 'Bench Press', 'Deadlift']
category_mapping = {
    "Female - Raw Junior": {"id": 1, "experience": 2, "gender": "F"},
    "Female - Raw Master 1": {"id": 2, "experience": 5, "gender": "F"},
    "Female - Raw Master 2": {"id": 3, "experience": 5, "gender": "F"},
    "Female - Raw Open": {"id": 4, "experience": 0, "gender": "F"},
    "Female - Raw Teen 2": {"id": 5, "experience": 1, "gender": "F"},
    "Female - Raw Teen 3": {"id": 6, "experience": 1, "gender": "F"},
    "Female - Raw Teen 1": {"id": 7, "experience": 1, "gender": "F"},
    "Male - Raw Junior": {"id": 8, "experience": 2, "gender": "M"},
    "Male - Raw Master 1": {"id": 9, "experience": 5, "gender": "M"},
    "Male - Raw Master 2": {"id": 10, "experience": 5, "gender": "M"},
    "Male - Raw Master 3": {"id": 11, "experience": 5, "gender": "M"},
    "Male - Raw Open": {"id": 12, "experience": 0, "gender": "M"},
    "Male - Raw Teen 2": {"id": 13, "experience": 1, "gender": "M"},
    "Male - Raw Teen 3": {"id": 14, "experience": 1, "gender": "M"},
    "Male - Raw Teen 1": {"id": 15, "experience": 1, "gender": "M"},
    "Female - Equipped Junior": {"id": 16, "experience": 2, "gender": "F"},
    "Female - Equipped Master 1": {"id": 17, "experience": 5, "gender": "F"},
    "Female - Equipped Master 2": {"id": 18, "experience": 5, "gender": "F"},
    "Female - Equipped Open": {"id": 19, "experience": 0, "gender": "F"},
    "Female - Equipped Teen 2": {"id": 20, "experience": 1, "gender": "F"},
    "Female - Equipped Teen 3": {"id": 21, "experience": 1, "gender": "F"},
    "Female - Equipped Teen 1": {"id": 22, "experience": 1, "gender": "F"},
    "Male - Equipped Junior": {"id": 23, "experience": 2, "gender": "M"},
    "Male - Equipped Master 1": {"id": 24, "experience": 5, "gender": "M"},
    "Male - Equipped Master 2": {"id": 25, "experience": 5, "gender": "M"},
    "Male - Equipped Master 3": {"id": 26, "experience": 5, "gender": "M"},
    "Male - Equipped Open": {"id": 27, "experience": 0, "gender": "M"},
    "Male - Equipped Teen 2": {"id": 28, "experience": 1, "gender": "M"},
    "Male - Equipped Teen 3": {"id": 29, "experience": 1, "gender": "M"},
    "Male - Equipped Teen 1": {"id": 30, "experience": 1, "gender": "M"},
}

#Comp name
comp_name = soup.find("h3").get_text(strip=True)
print(f"Competition Name: {comp_name}")

# Parse competition id from URL
query = parse_qs(urlparse(url).query)
comp_id = query.get('id', [None])[0]
print(f"Competition ID: {comp_id}")

#Comp date
header_table = soup.find("table")
if header_table:
    tbody = header_table.find("tbody")
    if tbody:
        rows = tbody.find_all("tr")
        for row in rows:
            th = row.find("th")
            if th and th.get_text(strip=True) == "Date":
                td = row.find("td")
                if td:
                    comp_date = td.get_text(strip=True)

compResults_table = soup.find("table", id="competition_view_results")

if compResults_table:
    for row in compResults_table.find_all("tr"):

        td_lifterID = row.find("td", id=lambda x: x and x.startswith("lifter_"))
        
        #Lifter category
        if td_lifterID is None:
            if row.find("th", colspan="20"):
                    category = row.find("th", colspan="20").get_text(strip=True)
            continue

        #Lifter ID
        td_id = td_lifterID.get('id')
        lifter_id = td_id.split("_")[1]
        comp_log_lifter_id += 1
        #Lifter name
        a_tag = td_lifterID.find("a")
        if a_tag:
            full_name = a_tag.get_text(strip=True)
            split_name = full_name.split(" ")
            first_name = split_name[0] if split_name else ""
            last_name = " ".join(split_name[1:]) if len(split_name) > 1 else ""
        else:
            first_name, last_name = "", ""

        #Team name and ID
        td_team = row.find("td", class_="competition_view_club")
        if td_team:
            a_team = td_team.find("a")
            if a_team:
                team_name = a_team.get_text(strip=True)
                href = a_team.get("href", "")
                team_id = href.split("=")[-1]
            else:
                team_name, team_id = "NULL", "NULL"
        else:
            team_name, team_id = "NULL", "NULL"

        #Lifter state
        td_state = row.find("td", class_="competition_view_state")
        lifter_state = td_state.get_text(strip=True)
        #Lifter year of birth
        td_yob = row.find_all("td")[3]
        lifter_YOB = td_yob.get_text(strip=True)
    
        #Lifter BW
        td_weight = row.find("td", class_="competition_view_weight")
        lifter_weight = td_weight.get_text(strip=True) if td_weight else "NULL"

        #Drug test pass/null
        td_DT = row.find("td", style="text-align: center;")
        drug_test = td_DT.get_text(strip=True)
        if drug_test == "X":
            drug_test = "Pass"
        else:
            drug_test = "NULL"

        #All lift attempts
        lift_tds = row.find_all("td", id=lambda x: x and x.startswith("lift_"))
        for lift_td in lift_tds:
            td_lift_id = lift_td.get("id")
            if lifter_id in td_lift_id:
                parts = td_lift_id.split("_")
                if len(parts) >= 3:
                    try:
                        lift_number = int(parts[2])
                        weight_text = lift_td.get_text(strip=True)
                        lift_numbers[lift_number - 1] = weight_text
                    except Exception:
                        pass
        
        ## COMPETITION_LOG TABLE INSERTS ##

        #if category in category_mapping:
            #category_deets = category_mapping[category]
            #lifter_experience = category_deets["experience"]
            #comp_log_insert = (f"({comp_log_lifter_id}, {lifter_id}, {comp_id}, {category}, '{lifter_weight}', '{lifter_experience}');")
            #print(comp_log_insert)

        ## TEAM TABLE INSERTS ##

        #if team_id not in teams_inserted:
            #teams_inserted[team_id] = team_name
            #team_insert = (
                #f"INSERT INTO TEAM (TEAM_ID, TEAM_NAME) "
                #f"VALUES ({team_id}, '{team_name}');"
            #)
            #print(team_insert)

        ## CATEGORY TABLE INSERTS in disc (needs to be static) ##
        
        ## LIFTER CATEGORY TABLE INSERTS ##
        #if category in category_mapping:
            #category_deets = category_mapping[category]
            #lifter_gender = category_deets["gender"]
            #lifter_insert = (
                #f"({lifter_id}, {team_id}, {lifter_YOB}, '{lifter_state}', '{lifter_gender}', '{first_name}', '{last_name}', '{drug_test}');")
            #print(lifter_insert)

        ## LIFT TABLE INSERTS ##

        ## ATTEMPTED LIFT TABLE INSERTS ##
