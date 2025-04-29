from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, parse_qs
import os
import platform
import subprocess

# MANUALLY FILL IN INSERTS FOR VENUE TABLE AND COMPETITION TABLE


print(os.getcwd())

os.makedirs("data", exist_ok=True)

sql_category = """
/*Insert data CATEGORY */
START TRANSACTION;
INSERT INTO CATEGORY (CAT_ID, CAT_NAME, CAT_GENDER, CAT_EXPERIENCE_MIN, CAT_EXPERIENCE_MAX)
VALUES
(1, 'Female - Collegiate', 'F', 3, 3),
(2, 'Female - High School', 'F', 1, 1),
(3, 'Female - High School JV', 'F', 1, 1),
(4, 'Female - High School Varsity', 'F', 3, 3),
(5, 'Female - Junior', 'F', 1, 1),
(6, 'Female - Master', 'F', 5, 5),
(7, 'Female - Master 1', 'F', 5, 5),
(8, 'Female - Master 2', 'F', 5, 5),
(9, 'Female - Master 3', 'F', 6, 6),
(10, 'Female - Master 4', 'F', 6, 6),
(11, 'Female - Master 5', 'F', 7, 7),
(12, 'Female - Master 6', 'F', 7, 7),
(13, 'Female - Military Open', 'F', 8, 8),
(14, 'Female - Open', 'F', 0, 0),
(15, 'Female - Police & Fire', 'F', 3, 3),
(16, 'Female - Raw Collegiate', 'F', 3, 3),
(17, 'Female - Raw High School', 'F', 1, 1),
(18, 'Female - Raw High School JV', 'F', 1, 1),
(19, 'Female - Raw High School Varsity', 'F', 2, 2),
(20, 'Female - Raw Junior', 'F', 1, 1),
(21, 'Female - Raw Master', 'F', 3, 3),
(22, 'Female - Raw Master 1', 'F', 5, 5),
(23, 'Female - Raw Master 2', 'F', 5, 5),
(24, 'Female - Raw Master 3', 'F', 5, 5),
(25, 'Female - Raw Master 4', 'F', 6, 6),
(26, 'Female - Raw Master 5', 'F', 7, 7),
(27, 'Female - Raw Master 6', 'F', 7, 7),
(28, 'Female - Raw Master 7', 'F', 7, 7),
(29, 'Female - Raw Military Open', 'F', 4, 4),
(30, 'Female - Raw Open', 'F', 0, 0),
(31, 'Female - Raw Open Pro', 'F', 10, 10),
(32, 'Female - Raw Special Olympian', 'F', 10, 10),
(33, 'Female - Raw Teen', 'F', 1, 1),
(34, 'Female - Raw Teen 1', 'F', 1, 1),
(35, 'Female - Raw Teen 2', 'F', 2, 2),
(36, 'Female - Raw Teen 3', 'F', 2, 2),
(37, 'Female - Raw Youth', 'F', 0, 0),
(38, 'Female - Raw Youth 1', 'F', 0, 0),
(39, 'Female - Raw Youth 2', 'F', 1, 1),
(40, 'Female - Raw Youth 3', 'F', 1, 1),
(41, 'Female - Raw with Wraps Collegiate', 'F', 3, 3),
(42, 'Female - Raw with Wraps High School', 'F', 2, 2),
(43, 'Female - Raw with Wraps Junior', 'F', 1, 1),
(44, 'Female - Raw with Wraps Master', 'F', 5, 5),
(45, 'Female - Raw with Wraps Master 1', 'F', 5, 5),
(46, 'Female - Raw with Wraps Master 2', 'F', 5, 5),
(47, 'Female - Raw with Wraps Master 3', 'F', 5, 5),
(48, 'Female - Raw with Wraps Master 4', 'F', 6, 6),
(49, 'Female - Raw with Wraps Master 5', 'F', 6, 6),
(50, 'Female - Raw with Wraps Military Open', 'F', 4, 4),
(51, 'Female - Raw with Wraps Open', 'F', 0, 0),
(52, 'Female - Raw with Wraps Teen', 'F', 0, 0),
(53, 'Female - Raw with Wraps Teen 1', 'F', 1, 1),
(54, 'Female - Raw with Wraps Teen 2', 'F', 1, 1),
(55, 'Female - Raw with Wraps Teen 3', 'F', 1, 1),
(56, 'Female - Raw with Wraps Youth 3', 'F', 1, 1),
(57, 'Female - Special Olympian', 'F', 10, 10),
(58, 'Female - Teen', 'F', 0, 0),
(59, 'Female - Teen 1', 'F', 1, 1),
(60, 'Female - Teen 2', 'F', 1, 1),
(61, 'Female - Teen 3', 'F', 1, 1),
(62, 'Male - Collegiate', 'M', 3, 3),
(63, 'Male - High School', 'M', 1, 1),
(64, 'Male - High School JV', 'M', 1, 1),
(65, 'Male - High School Varsity', 'M', 3, 3),
(66, 'Male - Junior', 'M', 1, 1),
(67, 'Male - Master', 'M', 5, 5),
(68, 'Male - Master 1', 'M', 5, 5),
(69, 'Male - Master 2', 'M', 5, 5),
(70, 'Male - Master 3', 'M', 6, 6),
(71, 'Male - Master 4', 'M', 6, 6),
(72, 'Male - Master 5', 'M', 7, 7),
(73, 'Male - Master 6', 'M', 7, 7),
(74, 'Male - Military Open', 'M', 8, 8),
(75, 'Male - Open', 'M', 0, 0),
(76, 'Male - Police & Fire', 'M', 3, 3),
(77, 'Male - Raw Collegiate', 'M', 3, 3),
(78, 'Male - Raw High School', 'M', 1, 1),
(79, 'Male - Raw High School JV', 'M', 1, 1),
(80, 'Male - Raw High School Varsity', 'M', 2, 2),
(81, 'Male - Raw Junior', 'M', 1, 1),
(82, 'Male - Raw Master', 'M', 3, 3),
(83, 'Male - Raw Master 1', 'M', 5, 5),
(84, 'Male - Raw Master 2', 'M', 5, 5),
(85, 'Male - Raw Master 3', 'M', 5, 5),
(86, 'Male - Raw Master 4', 'M', 6, 6),
(87, 'Male - Raw Master 5', 'M', 7, 7),
(88, 'Male - Raw Master 6', 'M', 7, 7),
(89, 'Male - Raw Master 7', 'M', 7, 7),
(90, 'Male - Raw Military Open', 'M', 4, 4),
(91, 'Male - Raw Open', 'M', 0, 0),
(92, 'Male - Raw Open Pro', 'M', 10, 10),
(93, 'Male - Raw Special Olympian', 'M', 10, 10),
(94, 'Male - Raw Teen', 'M', 1, 1),
(95, 'Male - Raw Teen 1', 'M', 1, 1),
(96, 'Male - Raw Teen 2', 'M', 2, 2),
(97, 'Male - Raw Teen 3', 'M', 2, 2),
(98, 'Male - Raw Youth', 'M', 0, 0),
(99, 'Male - Raw Youth 1', 'M', 0, 0),
(100, 'Male - Raw Youth 2', 'M', 1, 1),
(101, 'Male - Raw Youth 3', 'M', 1, 1),
(102, 'Male - Raw with Wraps Collegiate', 'M', 3, 3),
(103, 'Male - Raw with Wraps High School', 'M', 2, 2),
(104, 'Male - Raw with Wraps Junior', 'M', 1, 1),
(105, 'Male - Raw with Wraps Master', 'M', 5, 5),
(106, 'Male - Raw with Wraps Master 1', 'M', 5, 5),
(107, 'Male - Raw with Wraps Master 2', 'M', 5, 5),
(108, 'Male - Raw with Wraps Master 3', 'M', 5, 5),
(109, 'Male - Raw with Wraps Master 4', 'M', 6, 6),
(110, 'Male - Raw with Wraps Master 5', 'M', 6, 6),
(111, 'Male - Raw with Wraps Military Open', 'M', 4, 4),
(112, 'Male - Raw with Wraps Open', 'M', 0, 0),
(113, 'Male - Raw with Wraps Teen', 'M', 0, 0),
(114, 'Male - Raw with Wraps Teen 1', 'M', 1, 1),
(115, 'Male - Raw with Wraps Teen 2', 'M', 1, 1),
(116, 'Male - Raw with Wraps Teen 3', 'M', 1, 1),
(117, 'Male - Raw with Wraps Youth 3', 'M', 1, 1),
(118, 'Male - Special Olympian', 'M', 10, 10),
(119, 'Male - Teen', 'M', 0, 0),
(120, 'Male - Teen 1', 'M', 1, 1),
(121, 'Male - Teen 2', 'M', 1, 1),
(122, 'Male - Teen 3', 'M', 1, 1),
(123, 'Female - Raw Police & Fire', 'F', 3, 3),
(124, 'Male - Raw Police & Fire', 'M', 3, 3),
(125, 'Female - Raw Guest Lifter', 'F', 0, 0),
(126, 'Male - Raw Guest Lifter', 'M', 0, 0);
COMMIT;
"""
with open("data/output.txt", "w") as file:
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
        "\tCOMPETITION_DATE DATE NOT NULL,\n"
        "\tCOMPETITION_NAME VARCHAR(100) NOT NULL,\n"
        "\tCOMPETITION_DRUG_STATUS ENUM('tested', 'untested') NOT NULL,\n"
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
        "\tLIFTER_STATE VARCHAR(3) NOT NULL,\n"
        "\tLIFTER_GENDER VARCHAR(1) NOT NULL,\n"
        "\tLIFTER_FNAME VARCHAR(100) NOT NULL,\n"
        "\tLIFTER_LNAME VARCHAR(100) NOT NULL,\n"
        "\tLIFTER_DRUG_TEST ENUM('pass', 'fail') DEFAULT NULL,\n"
        "\tFOREIGN KEY(TEAM_ID) REFERENCES TEAM(TEAM_ID)\n"
        ");\n\n"
    )
    file.write(
        "CREATE TABLE COMPETITION_LOG (\n"
        "\tLIFTER_ID INT,\n"
        "\tCOMPETITION_ID INT,\n"
        "\tCAT_ID INT,\n"
        "\tCOMP_LOG_LIFTER_BODYWEIGHT DECIMAL(5,2) NOT NULL,\n"
        "\tCOMP_LOG_LIFTER_EXPERIENCE INT NOT NULL,\n"
        "\tPRIMARY KEY(LIFTER_ID, COMPETITION_ID), -- composite PK\n"
        "\tFOREIGN KEY(LIFTER_ID) REFERENCES LIFTER(LIFTER_ID),\n"
        "\tFOREIGN KEY(COMPETITION_ID) REFERENCES COMPETITION(COMPETITION_ID),\n"
        "\tFOREIGN KEY(CAT_ID) REFERENCES CATEGORY(CAT_ID)\n"
        ");\n\n"
    )
    file.write(
        "CREATE TABLE LIFT (\n"
	    "\tLIFT_ID VARCHAR(20) PRIMARY KEY,\n"
        "\tLIFT_NAME VARCHAR(13),\n"
        "\tLIFT_WEIGHT DECIMAL(4,1),\n"
        "\tLIFT_ATMPTNUM INT NOT NULL,\n"
        "\tLIFTER_ID INT,\n"
        "\tCOMPETITION_ID INT,\n"
        "\tFOREIGN KEY(LIFTER_ID, COMPETITION_ID) REFERENCES COMPETITION_LOG(LIFTER_ID, COMPETITION_ID)\n"
        ");\n\n"
        "/*  —------------------------------------------------------------------------------------------------------------------------- */"
    )
    file.write(
        sql_category
    )
#initialize variables
category = None
category_id = 30
squat = None 
benchPress = None 
deadlift = None 
lift_numbers = [0] * 9
lift_id = None
lift_name = None
lift_insert = None
team_id = "Null"

stored_lifter_ids = set()
lift_value = []
lifter_value = []
comp_log_value = []
team_value = []
comp_insert = set()

#dictonaries
teams_inserted = {}
lift_dict = ['Squat', 'Bench Press', 'Deadlift']
category_mapping = {
'Female - Collegiate': {'id': 1, 'experience': 3, 'gender': 'F'},
'Female - High School': {'id': 2, 'experience': 1, 'gender': 'F'},
'Female - High School JV': {'id': 3, 'experience': 1, 'gender': 'F'},
'Female - High School Varsity': {'id': 4, 'experience': 3, 'gender': 'F'},
'Female - Junior': {'id': 5, 'experience': 1, 'gender': 'F'},
'Female - Master': {'id': 6, 'experience': 5, 'gender': 'F'},
'Female - Master 1': {'id': 7, 'experience': 5, 'gender': 'F'},
'Female - Master 2': {'id': 8, 'experience': 5, 'gender': 'F'},
'Female - Master 3': {'id': 9, 'experience': 6, 'gender': 'F'},
'Female - Master 4': {'id': 10, 'experience': 6, 'gender': 'F'},
'Female - Master 5': {'id': 11, 'experience': 7, 'gender': 'F'},
'Female - Master 6': {'id': 12, 'experience': 7, 'gender': 'F'},
'Female - Military Open': {'id': 13, 'experience': 8, 'gender': 'F'},
'Female - Open': {'id': 14, 'experience': 0, 'gender': 'F'},
'Female - Police & Fire': {'id': 15, 'experience': 3, 'gender': 'F'},
'Female - Raw Collegiate': {'id': 16, 'experience': 3, 'gender': 'F'},
'Female - Raw High School': {'id': 17, 'experience': 1, 'gender': 'F'},
'Female - Raw High School JV': {'id': 18, 'experience': 1, 'gender': 'F'},
'Female - Raw High School Varsity': {'id': 19, 'experience': 2, 'gender': 'F'},
'Female - Raw Junior': {'id': 20, 'experience': 1, 'gender': 'F'},
'Female - Raw Master': {'id': 21, 'experience': 3, 'gender': 'F'},
'Female - Raw Master 1': {'id': 22, 'experience': 5, 'gender': 'F'},
'Female - Raw Master 2': {'id': 23, 'experience': 5, 'gender': 'F'},
'Female - Raw Master 3': {'id': 24, 'experience': 5, 'gender': 'F'},
'Female - Raw Master 4': {'id': 25, 'experience': 6, 'gender': 'F'},
'Female - Raw Master 5': {'id': 26, 'experience': 7, 'gender': 'F'},
'Female - Raw Master 6': {'id': 27, 'experience': 7, 'gender': 'F'},
'Female - Raw Master 7': {'id': 28, 'experience': 7, 'gender': 'F'},
'Female - Raw Military Open': {'id': 29, 'experience': 4, 'gender': 'F'},
'Female - Raw Open': {'id': 30, 'experience': 0, 'gender': 'F'},
'Female - Raw Open Pro': {'id': 31, 'experience': 10, 'gender': 'F'},
'Female - Raw Special Olympian': {'id': 32, 'experience': 10, 'gender': 'F'},
'Female - Raw Teen': {'id': 33, 'experience': 1, 'gender': 'F'},
'Female - Raw Teen 1': {'id': 34, 'experience': 1, 'gender': 'F'},
'Female - Raw Teen 2': {'id': 35, 'experience': 2, 'gender': 'F'},
'Female - Raw Teen 3': {'id': 36, 'experience': 2, 'gender': 'F'},
'Female - Raw Youth': {'id': 37, 'experience': 0, 'gender': 'F'},
'Female - Raw Youth 1': {'id': 38, 'experience': 0, 'gender': 'F'},
'Female - Raw Youth 2': {'id': 39, 'experience': 1, 'gender': 'F'},
'Female - Raw Youth 3': {'id': 40, 'experience': 1, 'gender': 'F'},
'Female - Raw with Wraps Collegiate': {'id': 41, 'experience': 3, 'gender': 'F'},
'Female - Raw with Wraps High School': {'id': 42, 'experience': 2, 'gender': 'F'},
'Female - Raw with Wraps Junior': {'id': 43, 'experience': 1, 'gender': 'F'},
'Female - Raw with Wraps Master': {'id': 44, 'experience': 5, 'gender': 'F'},
'Female - Raw with Wraps Master 1': {'id': 45, 'experience': 5, 'gender': 'F'},
'Female - Raw with Wraps Master 2': {'id': 46, 'experience': 5, 'gender': 'F'},
'Female - Raw with Wraps Master 3': {'id': 47, 'experience': 5, 'gender': 'F'},
'Female - Raw with Wraps Master 4': {'id': 48, 'experience': 6, 'gender': 'F'},
'Female - Raw with Wraps Master 5': {'id': 49, 'experience': 6, 'gender': 'F'},
'Female - Raw with Wraps Military Open': {'id': 50, 'experience': 4, 'gender': 'F'},
'Female - Raw with Wraps Open': {'id': 51, 'experience': 0, 'gender': 'F'},
'Female - Raw with Wraps Teen': {'id': 52, 'experience': 0, 'gender': 'F'},
'Female - Raw with Wraps Teen 1': {'id': 53, 'experience': 1, 'gender': 'F'},
'Female - Raw with Wraps Teen 2': {'id': 54, 'experience': 1, 'gender': 'F'},
'Female - Raw with Wraps Teen 3': {'id': 55, 'experience': 1, 'gender': 'F'},
'Female - Raw with Wraps Youth 3': {'id': 56, 'experience': 1, 'gender': 'F'},
'Female - Special Olympian': {'id': 57, 'experience': 10, 'gender': 'F'},
'Female - Teen': {'id': 58, 'experience': 0, 'gender': 'F'},
'Female - Teen 1': {'id': 59, 'experience': 1, 'gender': 'F'},
'Female - Teen 2': {'id': 60, 'experience': 1, 'gender': 'F'},
'Female - Teen 3': {'id': 61, 'experience': 1, 'gender': 'F'},
'Male - Collegiate': {'id': 62, 'experience': 3, 'gender': 'M'},
'Male - High School': {'id': 63, 'experience': 1, 'gender': 'M'},
'Male - High School JV': {'id': 64, 'experience': 1, 'gender': 'M'},
'Male - High School Varsity': {'id': 65, 'experience': 3, 'gender': 'M'},
'Male - Junior': {'id': 66, 'experience': 1, 'gender': 'M'},
'Male - Master': {'id': 67, 'experience': 5, 'gender': 'M'},
'Male - Master 1': {'id': 68, 'experience': 5, 'gender': 'M'},
'Male - Master 2': {'id': 69, 'experience': 5, 'gender': 'M'},
'Male - Master 3': {'id': 70, 'experience': 6, 'gender': 'M'},
'Male - Master 4': {'id': 71, 'experience': 6, 'gender': 'M'},
'Male - Master 5': {'id': 72, 'experience': 7, 'gender': 'M'},
'Male - Master 6': {'id': 73, 'experience': 7, 'gender': 'M'},
'Male - Military Open': {'id': 74, 'experience': 8, 'gender': 'M'},
'Male - Open': {'id': 75, 'experience': 0, 'gender': 'M'},
'Male - Police & Fire': {'id': 76, 'experience': 3, 'gender': 'M'},
'Male - Raw Collegiate': {'id': 77, 'experience': 3, 'gender': 'M'},
'Male - Raw High School': {'id': 78, 'experience': 1, 'gender': 'M'},
'Male - Raw High School JV': {'id': 79, 'experience': 1, 'gender': 'M'},
'Male - Raw High School Varsity': {'id': 80, 'experience': 2, 'gender': 'M'},
'Male - Raw Junior': {'id': 81, 'experience': 1, 'gender': 'M'},
'Male - Raw Master': {'id': 82, 'experience': 3, 'gender': 'M'},
'Male - Raw Master 1': {'id': 83, 'experience': 5, 'gender': 'M'},
'Male - Raw Master 2': {'id': 84, 'experience': 5, 'gender': 'M'},
'Male - Raw Master 3': {'id': 85, 'experience': 5, 'gender': 'M'},
'Male - Raw Master 4': {'id': 86, 'experience': 6, 'gender': 'M'},
'Male - Raw Master 5': {'id': 87, 'experience': 7, 'gender': 'M'},
'Male - Raw Master 6': {'id': 88, 'experience': 7, 'gender': 'M'},
'Male - Raw Master 7': {'id': 89, 'experience': 7, 'gender': 'M'},
'Male - Raw Military Open': {'id': 90, 'experience': 4, 'gender': 'M'},
'Male - Raw Open': {'id': 91, 'experience': 0, 'gender': 'M'},
'Male - Raw Open Pro': {'id': 92, 'experience': 10, 'gender': 'M'},
'Male - Raw Special Olympian': {'id': 93, 'experience': 10, 'gender': 'M'},
'Male - Raw Teen': {'id': 94, 'experience': 1, 'gender': 'M'},
'Male - Raw Teen 1': {'id': 95, 'experience': 1, 'gender': 'M'},
'Male - Raw Teen 2': {'id': 96, 'experience': 2, 'gender': 'M'},
'Male - Raw Teen 3': {'id': 97, 'experience': 2, 'gender': 'M'},
'Male - Raw Youth': {'id': 98, 'experience': 0, 'gender': 'M'},
'Male - Raw Youth 1': {'id': 99, 'experience': 0, 'gender': 'M'},
'Male - Raw Youth 2': {'id': 100, 'experience': 1, 'gender': 'M'},
'Male - Raw Youth 3': {'id': 101, 'experience': 1, 'gender': 'M'},
'Male - Raw with Wraps Collegiate': {'id': 102, 'experience': 3, 'gender': 'M'},
'Male - Raw with Wraps High School': {'id': 103, 'experience': 2, 'gender': 'M'},
'Male - Raw with Wraps Junior': {'id': 104, 'experience': 1, 'gender': 'M'},
'Male - Raw with Wraps Master': {'id': 105, 'experience': 5, 'gender': 'M'},
'Male - Raw with Wraps Master 1': {'id': 106, 'experience': 5, 'gender': 'M'},
'Male - Raw with Wraps Master 2': {'id': 107, 'experience': 5, 'gender': 'M'},
'Male - Raw with Wraps Master 3': {'id': 108, 'experience': 5, 'gender': 'M'},
'Male - Raw with Wraps Master 4': {'id': 109, 'experience': 6, 'gender': 'M'},
'Male - Raw with Wraps Master 5': {'id': 110, 'experience': 6, 'gender': 'M'},
'Male - Raw with Wraps Military Open': {'id': 111, 'experience': 4, 'gender': 'M'},
'Male - Raw with Wraps Open': {'id': 112, 'experience': 0, 'gender': 'M'},
'Male - Raw with Wraps Teen': {'id': 113, 'experience': 0, 'gender': 'M'},
'Male - Raw with Wraps Teen 1': {'id': 114, 'experience': 1, 'gender': 'M'},
'Male - Raw with Wraps Teen 2': {'id': 115, 'experience': 1, 'gender': 'M'},
'Male - Raw with Wraps Teen 3': {'id': 116, 'experience': 1, 'gender': 'M'},
'Male - Raw with Wraps Youth 3': {'id': 117, 'experience': 1, 'gender': 'M'},
'Male - Special Olympian': {'id': 118, 'experience': 10, 'gender': 'M'},
'Male - Teen': {'id': 119, 'experience': 0, 'gender': 'M'},
'Male - Teen 1': {'id': 120, 'experience': 1, 'gender': 'M'},
'Male - Teen 2': {'id': 121, 'experience': 1, 'gender': 'M'},
'Male - Teen 3': {'id': 122, 'experience': 1, 'gender': 'M'},
'Female - Raw Police & Fire': {'id': 123, 'experience': 3, 'gender': 'F'},
'Male - Raw Police & Fire': {'id': 124, 'experience': 3, 'gender': 'M'},
'Female - Raw Guest Lifter': {'id': 125, 'experience': 0, 'gender': 'F'},
'Male - Raw Guest Lifter': {'id': 126, 'experience': 0, 'gender': 'M'},
}
# CATEGORY TABLE INSERTS in disc (needs to be static) ##
sql_comp_log = f"""/*Insert data
COMPETITION_LOG */
START TRANSACTION;
INSERT INTO COMPETITION_LOG (LIFTER_ID, COMPETITION_ID, CAT_ID, COMP_LOG_LIFTER_BODYWEIGHT, COMP_LOG_LIFTER_EXPERIENCE)
VALUES
"""
sql_lift = f"""/*Insert data
LIFT */
START TRANSACTION;
INSERT INTO LIFT (LIFT_ID, LIFTER_ID, COMPETITION_ID, LIFT_NAME, LIFT_WEIGHT, LIFT_ATMPTNUM)
VALUES
"""
sql_lifter = f"""/*Insert data
LIFTER */
START TRANSACTION;
INSERT INTO LIFTER (LIFTER_ID, TEAM_ID, LIFTER_YOB, LIFTER_STATE, LIFTER_GENDER, LIFTER_FNAME, LIFTER_LNAME, LIFTER_DRUG_TEST)
VALUES
"""
venue_insert = """
/*Insert data
VENUE */
INSERT INTO VENUE (VEN_ID, VEN_NAME, VEN_STREET_NUMBER, VEN_STREET_NAME, VEN_CITY_NAME, VEN_STATE_NAME, VEN_ZIP_CODE)
VALUES 
( , , , , , , );
COMMIT;
"""

sql_comp = f"""
/*Insert data
COMPETITION */
INSERT INTO COMPETITION (COMPETITION_ID, VEN_ID, COMPETITION_NAME, COMPETITION_DATE, COMPETITION_DRUG_STATUS)
VALUES
"""
sql_team = (
"/*Insert data \nTEAM */"
"\nSTART TRANSACTION;\n"
"INSERT INTO TEAM (TEAM_ID, TEAM_NAME)\n"
"VALUES\n"
)


def scrape_stuff(url):
    scrape_url = requests.get(url)
    soup = BeautifulSoup(scrape_url.text, 'html.parser')
    
    #Comp name
    comp_name = soup.find("h3").get_text(strip=True)
    print(f"Competition Name: {comp_name}")
    
    # Parse competition id from URL
    query = parse_qs(urlparse(url).query)
    comp_id = query.get('id', [None])[0]
    print(f"Competition ID: {comp_id}")
    
    #Comp date
    comp_date = None
    header_table = soup.find("table")
    if header_table:
        tbody = header_table.find("tbody")
        if tbody:
            rows = tbody.find_all("tr")
            for row in rows:
                th = row.find("th")
                if th and th.get_text(strip=True) == "Date:":
                    td = row.find("td")
                    if td:
                        comp_date = td.get_text(strip=True)
                        year = comp_date.split("/")[2].strip()
                        month = comp_date.split("/")[0].strip()
                        day = comp_date.split("/")[1].strip()
                        comp_date = f"{year}-{month}-{day}"
    compResults_table = soup.find("table", id="competition_view_results")
    
    comp_insert = f"({comp_id}, /*ven_ID*/, '{comp_name}', '{comp_date}', 'tested')"
    
    if compResults_table:
        for row in compResults_table.find_all("tr"):
    
            td_lifterID = row.find("td", id=lambda x: x and x.startswith("lifter_"))
            
            #Lifter category
            if td_lifterID is None:
                if row.find("th", colspan="20"):
                        category = row.find("th", colspan="20").get_text(strip=True)
                        if category == "Bench press":
                            continue
                        if category == "Powerlifting":
                            continue
                        if category not in category_mapping:
                            category = category[:-1]
                            if category not in category_mapping:
                                print(f"Category '{category}' not found in mapping.")
                        continue
            #Lifter ID
            td_id = td_lifterID.get('id')
            lifter_id = td_id.split("_")[1]
    
            if lifter_id in stored_lifter_ids:
                continue
            stored_lifter_ids.add(lifter_id) 
    
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
                    if team_id == "1":
                        team_id = "NULL"
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
                drug_test = "pass"
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
                            if weight_text == "":
                                weight_text = 0
    
                            if lift_number in range(0,4):
                                lift_name = lift_dict[0]
                            elif lift_number in range(4,7):
                                lift_name = lift_dict[1]
                            elif lift_number in range(7,10):
                                lift_name = lift_dict[2]
                        except Exception:
                            pass
                    ## LIFT TABLE INSERTS ##
                    lift_id = lifter_id + '_' + str(lift_number) + '_' + comp_id    
                    lift_insert = (f"('{lift_id}', {lifter_id}, {comp_id}, '{lift_name}', {weight_text}, {lift_number})")
                    lift_value.append(lift_insert)
                    
            ## LIFTER CATEGORY TABLE INSERTS ##
    
            if category in category_mapping:
                category_deets = category_mapping[category]
                lifter_gender = category_deets["gender"]
            else:
                normalized_category = category.strip().lower()
                if "male" in normalized_category:
                    lifter_gender = "M"
                elif "female" in normalized_category:
                    lifter_gender = "F"
    
            if drug_test == "NULL":
                lifter_insert = (
                f"({lifter_id}, {team_id}, {lifter_YOB}, '{lifter_state}', '{lifter_gender}', '{first_name}', '{last_name}', {drug_test})"
                ) 
            else:
                lifter_insert = (
                f"({lifter_id}, {team_id}, {lifter_YOB}, '{lifter_state}', '{lifter_gender}', '{first_name}', '{last_name}', '{drug_test}')"
                ) 
            lifter_value.append(lifter_insert)
    
            ## COMPETITION_LOG TABLE INSERTS ##
    
            if category in category_mapping:
                category_deets = category_mapping[category]
                category_id = category_deets["id"]
                lifter_experience = category_deets["experience"]
                comp_log_insert = f"({lifter_id}, {comp_id}, {category_id}, {lifter_weight}, {lifter_experience})"
                comp_log_value.append(comp_log_insert)
            ## TEAM TABLE INSERTS ##
    
            if team_id not in teams_inserted:
                teams_inserted[team_id] = team_name
                team_insert = (f"({team_id}, '{team_name}')")
                if team_id != "NULL":
                    team_value.append(team_insert)


urls = [
    'https://usapl.liftingdatabase.com/competitions-view?id=121328',
    'https://usapl.liftingdatabase.com/competitions-view?id=121596',
    'https://usapl.liftingdatabase.com/competitions-view?id=120765',
    'https://usapl.liftingdatabase.com/competitions-view?id=121765',
    'https://usapl.liftingdatabase.com/competitions-view?id=121762',
    'https://usapl.liftingdatabase.com/competitions-view?id=121754'
]

for url in urls:
    scrape_stuff(url)

final_sql_blocks = []

final_sql_blocks.append(venue_insert)

if team_value:
    full_team_sql = f"{sql_team}" + ",\n".join(team_value) + ";\nCOMMIT;"
    final_sql_blocks.append(full_team_sql)

if comp_insert:
    full_comp_sql = f"{sql_comp}" + comp_insert + ";\nCOMMIT;"
    final_sql_blocks.append(full_comp_sql)

if lifter_value:
    full_lifter_sql = f"{sql_lifter}" + ",\n".join(lifter_value) + ";\nCOMMIT;"
    final_sql_blocks.append(full_lifter_sql)

if comp_log_value:
    full_comp_log_sql = f"{sql_comp_log}" + ",\n".join(comp_log_value) + ";\nCOMMIT;"
    final_sql_blocks.append(full_comp_log_sql)

if lift_value:
    full_lift_sql = f"{sql_lift}" + ",\n".join(lift_value) + ";\nCOMMIT;"
    final_sql_blocks.append(full_lift_sql)

final_sql_script = "\n\n".join(final_sql_blocks)

with open("data/output.txt", "a") as out_file:
    out_file.write(final_sql_script)


current_os = platform.system()

file_path = os.path.abspath("data/output.txt")
print(f"File saved at: {file_path}")

if current_os == "Windows":
    os.startfile(file_path)
elif current_os == "Darwin":
    subprocess.run(["open", file_path])
elif current_os == "Linux":
    subprocess.run(["xdg-open", file_path])
