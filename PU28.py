import csv, datetime, json, math, os, pyautogui, pyperclip, random, re, requests, time, urllib.request, webbrowser
from datetime import timezone, timedelta, date
from os import rename
import pandas as pd
from tabulate import tabulate

# set UTC dates for links and new folder, so 'today' is around 30 minutes old when this is run
today = datetime.datetime.now(timezone.utc)
yesterday = today - timedelta(1)
print(today)

laugh_out = ["username", "lmthlss", "Troytech", "teamsherry", "Cityhunter34", "vapourminer", "Pushupper", "Push upper", "Mayorofogba", "kwarkam", "Zack5000", "Zackz500", "I_anime", "MayorofOgba", "Boron19", "Smilevictorobinna", "obulis", "kelward", "cityhunter34", "CossyBlack", "Uheuchukwu53", "Lose Control", "sum"]


json_page = "C:/PyProjects/PU/PU/current_page.json"
with open(json_page, "r") as json_file:
    latest_page = json.load(json_file)

# get the source pages till the end of the thread
current_page = latest_page.get("current_page")[0]
all_page_sources = []
while True:
    print(current_page)
    url = f"https://bitcointalk.org/index.php?topic=5484350.{current_page}"
    time.sleep(5)
    response = requests.get(url)
    filetext = response.text
    pattern = fr"smf_start = {current_page}"
    matches = re.findall(pattern, filetext)
    if matches:
        print(matches)
        all_page_sources.append(response.text)
        current_page += 20
    else:
        current_page -= 20
        latest_page["current_page"] = [current_page]
        with open(json_page, "w") as jsonfile:
            json.dump(latest_page, jsonfile)
        break

with open("C:/PyProjects/PU/PU/PUSource.txt", "w", encoding="UTF-8") as textfile:
    for source_code in all_page_sources:
        textfile.write(source_code)
with open("C:/PyProjects/PU/PU/PUSource.txt", "r", encoding="UTF-8") as textfile:
    filetext = textfile.read()

# Define the regex pattern for 100kchallenge with a date
pattern = r"(?:100\w{0,10}),(\w[\s\w]+\w),(\d+),(\d+),(\d{4}-\d{2}-\d{2})" 
matches = re.findall(pattern, filetext)
print(f"matches {matches}")

# load the latest_data dictionary from the JSON file (if it exists)
json_filename = "C:/PyProjects/PU/PU/latest_data.json"
try:
    with open(json_filename, "r") as jsonfile:
        latest_data = json.load(jsonfile)
except FileNotFoundError:
    # If the file doesn't exist, start with an empty dictionary
    latest_data = {}
  
# Process each match
for match in matches:
    user, days_in, total_pushups, report_date = match
    if user not in laugh_out:
        if user not in latest_data:
            user_csv = f"C:/PyProjects/PU/{user}.csv"
            with open(user_csv, "a", newline="") as csvfile:
                writer = csv.writer(csvfile)
                latest_data[user] = user, days_in, total_pushups, report_date 
                writer.writerow([f"{user}", f"{days_in}", f"{total_pushups}", f"{report_date}"])
                writer.writerow([f"{user}", f"{days_in}", f"{total_pushups}", f"{report_date}"])

for match in matches:
    user, days_in, pushups_completed, report_date = match
    if user not in laugh_out:
        if int(pushups_completed) >= 1:
            if user not in latest_data or int(days_in) > int(latest_data[user][1]):
                latest_data[user] = (user, days_in, pushups_completed, report_date)
                user_csv = f"C:/PyProjects/PU/{user}.csv"
                with open(user_csv, "a", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    print([f"{user}", f"{days_in}", f"{pushups_completed}", f"{report_date}"])
                    writer.writerow([f"{user}", f"{days_in}", f"{pushups_completed}", f"{report_date}"])
   
            
# Define the regex pattern for 100kchallenge with no date
pattern2 = r"(?:100\w{0,10}),(\w[\s\w]+\w),(\d+),(\d+)(?!,\d{4}-\d{2}-\d{2})"  
matches2 = re.findall(pattern2, filetext)
print(f"matches2 {matches2}")

new_matches = []
# append date to regex matches with no date
report_date = date.today().strftime("%Y-%m-%d")
for match in matches2:
    new_match = match + (report_date,)
    print(f"new matches {new_match}")
    new_matches.append(new_match)
  
# Process each match2
for match in new_matches:
    user, days_in, pushups_completed, report_date = match
    if user not in laugh_out:
        if int(pushups_completed) >= 1:
            if user not in latest_data or int(days_in) > int(latest_data[user][1]):
                latest_data[user] = (user, days_in, pushups_completed, report_date)
                user_csv = f"C:/PyProjects/PU/{user}.csv"
                with open(user_csv, "a", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([f"{user}", f"{days_in}", f"{pushups_completed}", f"{report_date}"])
  
# Write the data to a CSV file
csv_filename = "C:/PyProjects/PU/100kpushups_data.csv"
with open(csv_filename, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for entry in latest_data.values():
        writer.writerow(entry)

no_team_csv = "C:/PyProjects/PU/100k_no_team.csv"
def g(csv_filename):
  # Read the CSV file
  df = pd.read_csv(csv_filename)
  
  # Filter for the row where the first element is 'Team'
  df = df[df.iloc[:, 0] != 'Team']
  
  # Save the dataframe to a new CSV file (optional)
  df.to_csv(no_team_csv, index=False)

g(csv_filename)

json_filename = "C:/PyProjects/PU/PU/latest_data.json"
with open(json_filename, "w") as jsonfile:
    json.dump(latest_data, jsonfile)

print(f"Latest data saved to {json_filename}")

# read data from csv, and calculate average pushups per day
total_pushups = 0
days_total = 0
total_users = 0
rows = []
with open(no_team_csv, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        # calculate average pushups per day place it in the row
        user, days_in, pushups_completed = row[0], int(row[1]), int(row[2])
        total_pushups = total_pushups + pushups_completed
        days_total = days_total + days_in
        total_users = total_users + 1
        average_pushup = pushups_completed / days_in
        average_pushups = f"{average_pushup:.2f}"
        user_csv = f"C:/PyProjects/PU/{user}.csv"
        pushup_data = pd.read_csv(user_csv, header=None)
        df = pd.DataFrame(pushup_data)
        last_pushups = df[2].iloc[-2]
        this_pushups = df[2].iloc[-1]
        report_pushups = int(this_pushups) - int(last_pushups)
        row.append(average_pushups)
        row.append(report_pushups)
        rows.append(row)

for row in rows:
    pushups_completed = int(row[2])
    average_pushup = float(row[4])
    percent_of_pushups = (pushups_completed / total_pushups) * 100
    # if 1 <= pushups_completed <= 99:
    #     goal = 100
    # if 100 <= pushups_completed <= 999:
    #     goal = 1000
    # if 1000 <= pushups_completed <= 9999:
    #     goal = 10_000
    # if 10_000 <= pushups_completed <= 99_999:
    #     goal = 100_000
    # to_go = goal - pushups_completed
    
    # # average_pushup = float(average_pushups)
    # goal_days = math.ceil(to_go / average_pushup)
    row.append(f"{percent_of_pushups:.2f}%")
  
# percent_csv = "C:/PyProjects/PU/percent_csv.csv"
# with open(percent_csv, "w", newline="") as csvfile:
#     writer = csv.writer(csvfile)
#     for entry in rows:
#         writer.writerow(entry)

# Sort the rows by pushups completed (descending order)

sorted_rows = sorted(rows[0:], key=lambda row: row[3], reverse=True)



new_csv_filename = "C:/PyProjects/PU/100kpushups_rank.csv"
with open(new_csv_filename, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for entry in sorted_rows:
        writer.writerow(entry)


rows = []
with open(new_csv_filename, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        rows.append(row)

# Print the data as a table
headers = ["user", "Days\nIn", "Pushups\nDone", "Latest\nReport", "PU/day", "new\nPU", "% of\nTeam"]
print(tabulate(rows[0:], headers=headers, tablefmt="rounded_grid"))
post = (tabulate(rows[0:], headers=headers, tablefmt="rounded_grid"))
users = total_users
total_ave = total_pushups / users
ave_days = days_total / users
per_day = total_pushups / ave_days
overall = total_pushups / ave_days / users
goal = 400_000 - total_pushups
days_til = goal / per_day
# Print the data as a table
color = "orange"
togo_color = "black"
bar_progress = int(total_pushups / 4000) + 1
print(bar_progress)
bar_togo = 100 - bar_progress
print(bar_togo)
headers = ["Team\nPushups", "Pushers", "Pushups\n per Pusher", "Days\nper Pusher", "Pushups/Pusher\nper Day", "Pushups\nper Day", "Days till\n400_000"]
postpost = total_pushups, users, total_ave, ave_days, overall, per_day, days_til
post2 = (tabulate({postpost}, headers=headers, tablefmt="rounded_grid"))
print(tabulate({postpost}, headers=headers, tablefmt="rounded_grid"))
# top_line = f"[b][color={color}]{'█' * bar_progress}[color={togo_color}]{'█' * bar_togo}▌[/color][/b]"
mid_line = f"[b][color={color}]{'█' * bar_progress}[color={togo_color}]{'█' * bar_togo}▌[/color][/b]"
# low_line = f"[b][color={color}]{'█' * bar_progress}[color={togo_color}]{'█' * bar_togo}▌[/color][/b]"
lin_line = f"|         |         |         |         |         |         |         |         |         |         |"
num_line = f"0k       40k       80k       120k      160k      200k      240k      280k      320k      360k      400k"

Team_csv = "C:/PyProjects/PU/PU/Team.csv"
with open(Team_csv, "a", newline="") as csvfile:
    writer = csv.writer(csvfile)
    print(total_pushups)
    writer.writerow(["Team", f"{users}", f"{total_pushups}", f"{report_date}"])

with open(Team_csv, "r", newline="") as csvfile:
        pushup_data = pd.read_csv(Team_csv, header=None)
        df = pd.DataFrame(pushup_data)
        last_pushups = df[2].iloc[-2]
        report_pushups = int(total_pushups) - int(last_pushups)
       
pyperclip.copy(f"[pre]{post}\n{post2}\n{mid_line}\n{lin_line}\n{num_line}\n[/pre]\nReport Format: '100k,User Name,DaysPushing,TotalPushupsDone,Date(Optional)' See the OP for more details")
url = 'https://bitcointalk.org/index.php?action=post;topic=5484350.0'
webbrowser.open(url)
time.sleep(60)
pyautogui.hotkey('f11')
time.sleep(60)
pyautogui.hotkey('tab')
time.sleep(5)
pyautogui.write(f"{report_pushups} Pushups Reported for the {report_date} UTC Pushup Report", interval=0.25)
pyautogui.hotkey('tab')
time.sleep(5)
pyautogui.hotkey('ctrl', 'v')
time.sleep(5)
pyautogui.hotkey('tab')
time.sleep(5)
# we're doing it live if the next command is #ed out
# pyautogui.hotkey('tab')
time.sleep(5)
pyautogui.hotkey('enter')
time.sleep(60)
pyautogui.hotkey('f11')


print(f"{report_pushups} Pushups Reported for the {report_date} UTC Pushup Report")

# clean up for next run
json_filename = "C:/PyProjects/PU/PU/latest_data.json"
with open(json_filename, "r") as jsonfile:
    latest_data = json.load(jsonfile)
        
for user in latest_data:
    print(user)
    user_csv = f"C:/PyProjects/PU/{user}.csv"
    os.remove(user_csv)


os.remove("C:/PyProjects/PU/100kpushups_data.csv")
os.remove("C:/PyProjects/PU/100kpushups_rank.csv")
os.remove("C:/PyProjects/PU/percent_csv.csv")
os.remove("C:/PyProjects/PU/100k_no_team.csv")

for user in latest_data:
    print(user)
    user_csv = f"C:/PyProjects/PU/{user}.csv"
    with open(user_csv, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        user, days_in, total_pushups, report_date = latest_data[user]
        writer.writerow([f"{user}", f"{days_in}", f"{total_pushups}", f"{report_date}"])
        writer.writerow([f"{user}", f"{days_in}", f"{total_pushups}", f"{report_date}"])
          

###########                            ☰☰☰        ▟█
# The End #                       ☰☰☰☰☰☰  ⚞▇▇▇██▛(°)>
###########                            ☰☰☰        ▜█

