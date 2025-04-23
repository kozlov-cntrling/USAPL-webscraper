from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, parse_qs

#make function to iterate through url IDs to get a bunch of competitions, and format all the data accordingly to the insert into statements on mysql

url = 'https://usapl.liftingdatabase.com/competitions-view?id=121328'
scrape_url = requests.get(url)
soup = BeautifulSoup(scrape_url.text, 'html.parser')
with open("output.txt", "w") as file:
    file.write(
    "/* Database Systems, Group 12 /\n"
    "/ Type of SQL : MySQL /\n"
    "/ Be sure to name the schema USAPLCP */\n"
    "\nCREATE DATABASE IF NOT EXISTS USAPLCP;\n"
    "USE USAPLCP;\n"
    )
    # create table "category"
    file.write(
        "CREATE TABLE CATEGORY (\n"
        "\tCAT_ID INT PRIMARY KEY,\n"
        "\tCAT_NAME VARCHAR(100) NOT NULL,\n"
        "\tCAT_GENDER VARCHAR(1) NOT NULL,\n"
        "\tCAT_EXPERIENCE_MIN INT NOT NULL,\n"
        "\tCAT_EXPERIENCE_MAX INT NOT NULL\n"
        ");\n\n"
    )
    # create table "venue"
    file.write(
        "CREATE TABLE VENUE (\n"
        "\tVEN_ID INT PRIMARY KEY,\n"
        "\tVEN_NAME VARCHAR(100) NOT NULL,\n"
        "\tVEN_STREET_NUMBER INT NOT NULL,\n"
        "\tVEN_STREET_NAME VARCHAR(100) NOT NULL,\n"
        "\tVEN_CITY_NAME VARCHAR(100) NOT NULL,\n"
        "\tVEN_STATE_NAME VARCHAR(2) NOT NULL,\n"
        "\tVEN_ZIP_CODE INT NOT NULL\n"
        ");\n\n"
    )
    # create table "competition"
    file.write(
        "CREATE TABLE COMPETITION (\n"
        "\tCOMPETITION_ID INT PRIMARY KEY,\n"
        "\tVEN_ID INT,\n"
        "\tCOMPETITION_NAME VARCHAR(100) NOT NULL,\n"
        "\tCOMPETITION_DRUG_STATUS BOOLEAN NOT NULL,\n"
        "\tFOREIGN KEY(VEN_ID) REFERENCES VENUE(VEN_ID)\n"
        ");\n\n"
    )
    # create table "team"
    file.write(
        "CREATE TABLE TEAM (\n"
        "\tTEAM_ID INT PRIMARY KEY,\n"
        "\tTEAM_NAME VARCHAR(100) NOT NULL\n"
        ");\n\n"
    )
    # create table "lifter"
    file.write(
        "CREATE TABLE LIFTER (\n"
        "\tLIFTER_ID INT PRIMARY KEY,\n"
        "\tTEAM_ID INT DEFAULT NULL,\n"
        "\tLIFTER_YOB INT NOT NULL,\n"
        "\tLIFTER_STATE VARCHAR(2) NOT NULL,\n"
        "\tLIFTER_GENDER VARCHAR(1) NOT NULL,\n"
        "\tLIFTER_FNAME VARCHAR(100) NOT NULL,\n"
        "\tLIFTER_LNAME VARCHAR(100) NOT NULL,\n"
        "\tLIFTER_DRUG_TEST ENUM('pass', 'fail') DEFAULT NULL,\n"
        "\tFOREIGN KEY(TEAM_ID) REFERENCES TEAM(TEAM_ID)\n"
        ");\n\n"
    )
    file.write(
        "CREATE TABLE COMPETITION_LOG (\n"
        "\tCOMP_LOG_LIFTER_ID INT PRIMARY KEY,\n"
        "\tLIFTER_ID INT,\n"
        "\tCOMPETITION_ID INT,\n"
        "\tCAT_ID INT,\n"
        "\tCOMP_LOG_LIFTER_BODYWEIGHT DECIMAL(5,2) NOT NULL,\n"
        "\tCOMP_LOG_LIFTER_EXPERIENCE INT NOT NULL,\n"
        "\tFOREIGN KEY(LIFTER_ID) REFERENCES LIFTER(LIFTER_ID),\n"
        "\tFOREIGN KEY(COMPETITION_ID) REFERENCES COMPETITION(COMPETITION_ID),\n"
        "\tFOREIGN KEY(CAT_ID) REFERENCES CATEGORY(CAT_ID)\n"
        ");\n\n"
    )
    file.write(
        "CREATE TABLE LIFT ("
	    "LIFT_ID INT PRIMARY KEY,"

        ");"
    )
#initialize variables
category = None
category_id = 0
squat = None 
benchPress = None 
deadlift = None 
lift_numbers = [0] * 9
lift_id = None
lift_name = None
lift_insert = None
team_id = "Null"
#dictonaries
teams_inserted = {}
lift_dict = ['Squat', 'Bench Press', 'Deadlift']
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
# CATEGORY TABLE INSERTS in disc (needs to be static) ##
sql_category = """
/*Insert data CATEGORY */
START TRANSACTION;
INSERT INTO CATEGORY (CAT_ID, CAT_NAME, CAT_GENDER, CAT_EXPERIENCE_MIN, CAT_EXPERIENCE_MAX)
VALUES
(1, 'Female - Raw Junior', 'F', 2, 2),
(2, 'Female - Raw Master 1', 'F', 5, 5),
(3, 'Female - Raw Master 2', 'F', 5, 5),
(4, 'Female - Raw Open', 'F', 0, 0),
(5, 'Female - Raw Teen 2', 'F', 1, 1),
(6, 'Female - Raw Teen 3', 'F', 1, 1),
(7, 'Female - Raw Teen 1', 'F', 1, 1),
(8, 'Male - Raw Junior', 'M', 2, 2),
(9, 'Male - Raw Master 1', 'M', 5, 5),
(10, 'Male - Raw Master 2', 'M', 5, 5),
(11, 'Male - Raw Master 3', 'M', 5, 5),
(12, 'Male - Raw Open', 'M', 0, 0),
(13, 'Male - Raw Teen 2', 'M', 1, 1),
(14, 'Male - Raw Teen 3', 'M', 1, 1),
(15, 'Male - Raw Teen 1', 'M', 1, 1),
(16, 'Female - Equipped Junior', 'F', 2, 2),
(17, 'Female - Equipped Master 1', 'F', 5, 5),
(18, 'Female - Equipped Master 2', 'F', 5, 5),
(19, 'Female - Equipped Open', 'F', 0, 0),
(20, 'Female - Equipped Teen 2', 'F', 1, 1),
(21, 'Female - Equipped Teen 3', 'F', 1, 1),
(22, 'Female - Equipped Teen 1', 'F', 1, 1),
(23, 'Male - Equipped Junior', 'M', 2, 2),
(24, 'Male - Equipped Master 1', 'M', 5, 5),
(25, 'Male - Equipped Master 2', 'M', 5, 5),
(26, 'Male - Equipped Master 3', 'M', 5, 5),
(27, 'Male - Equipped Open', 'M', 0, 0),
(28, 'Male - Equipped Teen 2', 'M', 1, 1),
(29, 'Male - Equipped Teen 3', 'M', 1, 1),
(30, 'Male - Equipped Teen 1', 'M', 1, 1);
COMMIT;}
"""
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
        comp_log_lifter_id = lifter_id + '_' + comp_id
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
    
                        if lift_number in range(1,4):
                            lift_name = lift_dict[0]
                        elif lift_number in range(4,7):
                            lift_name = lift_dict[1]
                        elif lift_number in range(7,10):
                            lift_name = lift_dict[2]
                    except Exception:
                        pass
                ## LIFT TABLE INSERTS ##
                with open("output.txt", "w") as out_file:
                    lift_id = lifter_id + '_' + str(lift_number) + '_' + comp_id    
                    lift_insert = (
                    f"('{lift_id}', '{comp_log_lifter_id}', '{lift_name}', {weight_text}, {lift_number})"
                                )
                    if row != compResults_table.find_all("tr")[-1]:
                        lift_insert += ","
                    out_file.write(lift_insert + "\n")
                
        ## COMPETITION_LOG TABLE INSERTS ##
        with open("output.txt", "w") as out_file:
            if category in category_mapping:
                category_deets = category_mapping[category]
                lifter_experience = category_deets["experience"]
                comp_log_insert = f"('{comp_log_lifter_id}', {lifter_id}, {comp_id}, '{category}', {lifter_weight}, {lifter_experience})"
                if row != compResults_table.find_all("tr")[-1]:  # Check if it's not the last row
                    comp_log_insert += ","
                out_file.write(comp_log_insert + "\n")

        ## TEAM TABLE INSERTS ##
        with open("output.txt", "w") as out_file:
            if team_id not in teams_inserted:
                if team_id == "NULL":
                    team_id = "NULL"
                    team_name = "NULL"
                teams_inserted[team_id] = team_name
                team_insert = f"VALUES ({team_id}, '{team_name}')"
                if team_id != list(teams_inserted.keys())[-1]:
                    team_insert += ","
                out_file.write(team_insert + "\n")

        

        ## LIFTER CATEGORY TABLE INSERTS ##
        with open("output.txt", "w") as out_file:
            if category in category_mapping:
                category_deets = category_mapping[category]
                lifter_gender = category_deets["gender"]
                lifter_insert = (
                    f"({lifter_id}, {team_id}, {lifter_YOB}, '{lifter_state}', '{lifter_gender}', '{first_name}', '{last_name}', '{drug_test}')"
                )
                if row != compResults_table.find_all("tr")[-1]:
                    lifter_insert += ","
                out_file.write(lifter_insert + "\n")
    