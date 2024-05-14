from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent
import pandas as pd
from functools import reduce

ua = UserAgent()
user_agent = ua.random
options = Options()

options.add_argument(f'user-agent={user_agent}')
#options.add_argument('--headless=new')  #İsteğe bağlı olarak kullanılabilir. Tarayıcı açılmadan işlemler arkaplanda yapılacaktır.
driver = webdriver.Chrome(options=options)
driver.maximize_window()
players_data = []

# Sayfayı yükle
driver.get("Link") #Hedeflenen takımın sofascore linki
driver.execute_script("document.body.style.zoom='33%'")

# WebDriverWait nesnesini başlat
wait = WebDriverWait(driver, 10)
wait2 = WebDriverWait(driver, 200)
# Sayfanın tam olarak yüklenmesini bekle


Player_Statics_Button = driver.find_element (By.XPATH,"//div[contains(@class, 'Box') and contains(@class, 'bkrWzf') and contains(@class, 'sc-imWYAI') and contains(@class, 'gzXbCV') and contains(@class, 'secondary') and contains(text(), 'Player statistics')]")
try:
    Player_Statics_Button.click()
except ElementClickInterceptedException:
    # Eğer normal click çalışmazsa, JavaScript ile tıklama yap
    driver.execute_script("arguments[0].click();", Player_Statics_Button)


wait

rows = driver.find_elements(By.XPATH, "//tbody[@class='TableBody juEMAj']/tr")

data = []

for row in rows:
    name = row.find_element(By.XPATH, ".//td[2]").text  
    goals = row.find_element(By.XPATH, ".//td[3]").text 
    assists = row.find_element(By.XPATH, ".//td[4]").text 
    tackles = row.find_element(By.XPATH, ".//td[5]").text 
    passes = row.find_element(By.XPATH, ".//td[6]").text  
    
    acc_pass, remaining_passes = passes.split('/')
    total_passes, percentage = remaining_passes.split(' ')
    acc_pass_percent = percentage.strip('()%')
    acc_pass = int(acc_pass) 
    total_passes = int(total_passes)
    acc_pass_percent = int(acc_pass_percent)

    total_duels_won = row.find_element(By.XPATH, ".//td[7]").text  
    total_duels_try, total_duels_won = total_duels_won.split('(')
    total_duels_try = total_duels_try.strip()  
    total_duels_won = total_duels_won.strip(')') 

    # Değişkenlere atama
    total_duels_try = int(total_duels_try)  
    total_duels_won = int(total_duels_won)

    ground_duels_won = row.find_element(By.XPATH, ".//td[8]").text 
    ground_duels_try, ground_duels_won = ground_duels_won.split('(')
    # Parantez ve boşlukları temizleme
    ground_duels_try = ground_duels_try.strip()  
    ground_duels_won = ground_duels_won.strip(')') 

    # Değişkenlere atama
    ground_duels_try = int(ground_duels_try)  
    ground_duels_won = int(ground_duels_won)

    aerial_duels_won = row.find_element(By.XPATH, ".//td[9]").text  
    aerial_duels_try, aerial_duels_won = aerial_duels_won.split('(')
    # Parantez ve boşlukları temizleme
    aerial_duels_try = aerial_duels_try.strip()  
    aerial_duels_won = aerial_duels_won.strip(')')  

    # Değişkenlere atama
    aerial_duels_try = int(aerial_duels_try)  
    aerial_duels_won = int(aerial_duels_won)

    minutes_played = row.find_element(By.XPATH, ".//td[10]").text
    minutes_played = minutes_played.replace("'", "")

    position = row.find_element(By.XPATH, ".//td[11]").text
    rating_x = row.find_element(By.XPATH, ".//td[12]/div[2]/div/div/span")
    rating = rating_x.get_attribute("aria-valuenow")
    # Çekilen verileri listeye ekle
    data.append([name, goals, assists, tackles, acc_pass,total_passes,acc_pass_percent,total_duels_try,total_duels_won,ground_duels_try,ground_duels_won,aerial_duels_try,aerial_duels_won,minutes_played,position,rating])

df = pd.DataFrame(data, columns=['Name', 'Goals', 'Assists', 'Tackles', 'Accurate Passes', 'Total Passes', 'Accurate Passes (/100)','Total Duels Try', 'Total Duels Won','Ground Duels Try', 'Ground Duels Won','Aerial Duels Try', 'Aerial Duels Won','Minutes Played','Position','Rating'])

Attack_Button = driver.find_element (By.XPATH,"//span[@class='Text eSPCzT' and contains(text(), 'Attack')]")
try:
    Attack_Button.click()
except ElementClickInterceptedException:
    # Eğer normal click çalışmazsa, JavaScript ile tıklama yap
    driver.execute_script("arguments[0].click();", Attack_Button)

wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='Text eSPCzT']")))
data_attack = []
rows2 = driver.find_elements(By.XPATH, "//tbody[@class='TableBody juEMAj']/tr")

# Her satır için gerekli bilgileri çek
for row in rows2:
    name = row.find_element(By.XPATH, ".//td[2]").text  # Oyuncu ismi
    shots_on_target = row.find_element(By.XPATH, ".//td[3]").text 
    expected_goals = row.find_element(By.XPATH, ".//td[4]").text 
    expected_goals = float(expected_goals) if expected_goals else 0
    shots_off_target = row.find_element(By.XPATH, ".//td[5]").text 
    shots_blocked = row.find_element(By.XPATH, ".//td[6]").text 
    succ_dribble = row.find_element(By.XPATH, ".//td[7]").text 
    total_dribble_attempt, succ_dribble = succ_dribble.split('(')
    # Parantez ve boşlukları temizleme
    total_dribble_attempt = total_dribble_attempt.strip()  # Sağ ve sol taraftaki boşlukları kaldırma
    succ_dribble = succ_dribble.strip(')')  # Sağdaki parantezi kaldırma
    attack_notes = row.find_element(By.XPATH, ".//td[8]").text 
    data_attack.append([name,shots_on_target, expected_goals, shots_off_target, shots_blocked, total_dribble_attempt,succ_dribble,attack_notes])
    

df2 = pd.DataFrame(data_attack, columns=['Name','Shots on Target','Expected Goals','Shots Off Target','Shots Blocked','Total Dribble Attempts','Succ Dribble','Attack Notes'])

Defence_Button = driver.find_element (By.XPATH,"//span[@class='Text eSPCzT' and contains(text(), 'Defence')]")
try:
    Defence_Button.click()
except ElementClickInterceptedException:
    # Eğer normal click çalışmazsa, JavaScript ile tıklama yap
    driver.execute_script("arguments[0].click();", Defence_Button)

wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='Text eSPCzT']")))
data_defence = []
rows3 = driver.find_elements(By.XPATH, "//tbody[@class='TableBody juEMAj']/tr")

# Her satır için gerekli bilgileri çek
for row in rows3:
    name = row.find_element(By.XPATH, ".//td[2]").text  
    defencive_actions = row.find_element(By.XPATH, ".//td[3]").text 
    clearances = row.find_element(By.XPATH, ".//td[4]").text 
    blocked_shots = row.find_element(By.XPATH, ".//td[5]").text 
    interceptions = row.find_element(By.XPATH, ".//td[6]").text 
    dribbled_past = row.find_element(By.XPATH, ".//td[8]").text 
    defence_notes = row.find_element(By.XPATH, ".//td[9]").text
    data_defence.append([name,defencive_actions,clearances,blocked_shots,interceptions,dribbled_past,defence_notes])
    

df3 = pd.DataFrame(data_defence, columns=['Name','Defencive Actions','Clearances','Blocked Shots','Interceptions','Dribbled Past','Defence Notes'])



Passing_Button = driver.find_element (By.XPATH,"//span[@class='Text eSPCzT' and contains(text(), 'Passing')]")
try:
    Passing_Button.click()
except ElementClickInterceptedException:
    # Eğer normal click çalışmazsa, JavaScript ile tıklama yap
    driver.execute_script("arguments[0].click();", Passing_Button)

wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='Text eSPCzT']")))
data_passing = []
rows4 = driver.find_elements(By.XPATH, "//tbody[@class='TableBody juEMAj']/tr")

# Her satır için gerekli bilgileri çek
for row in rows4:
    name = row.find_element(By.XPATH, ".//td[2]").text  
    touches = row.find_element(By.XPATH, ".//td[3]").text 
    key_passes = row.find_element(By.XPATH, ".//td[5]").text 
    suc_crosses = row.find_element(By.XPATH, ".//td[6]").text 
    total_crosses, suc_crosses = suc_crosses.split('(')
    # Parantez ve boşlukları temizleme
    total_crosses = total_crosses.strip()  # Sağ ve sol taraftaki boşlukları kaldırma
    suc_crosses = suc_crosses.strip(')')  # Sağdaki parantezi kaldırma
    succ_long_balls = row.find_element(By.XPATH, ".//td[7]").text 
    total_long_balls, succ_long_balls = succ_long_balls.split('(')
    # Parantez ve boşlukları temizleme
    total_long_balls = total_long_balls.strip()  # Sağ ve sol taraftaki boşlukları kaldırma
    succ_long_balls = succ_long_balls.strip(')')  # Sağdaki parantezi kaldırma
    passing_notes = row.find_element(By.XPATH, ".//td[8]").text
    
    data_passing.append([name,touches,key_passes,total_crosses,suc_crosses,total_long_balls,succ_long_balls,passing_notes])
    

df4 = pd.DataFrame(data_passing, columns=['Name','Touches','Key Passes','Total Crosses','Succ Crosses','Total Long Balls','Succ Long Balls','Passing Notes'])







Duels_Button = driver.find_element (By.XPATH,"//span[@class='Text eSPCzT' and contains(text(), 'Duels')]")
try:
    Duels_Button.click()
except ElementClickInterceptedException:
    # Eğer normal click çalışmazsa, JavaScript ile tıklama yap
    driver.execute_script("arguments[0].click();", Duels_Button)

wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='Text eSPCzT']")))
data_duels = []
rows5 = driver.find_elements(By.XPATH, "//tbody[@class='TableBody juEMAj']/tr")

# Her satır için gerekli bilgileri çek
for row in rows5:
    name = row.find_element(By.XPATH, ".//td[2]").text  # Oyuncu ismi
    possesion_lost = row.find_element(By.XPATH, ".//td[6]").text 
    fouls = row.find_element(By.XPATH, ".//td[7]").text 
    was_fouled = row.find_element(By.XPATH, ".//td[8]").text
    offsides = row.find_element(By.XPATH, ".//td[9]").text 
    
    data_duels.append([name,possesion_lost,fouls,was_fouled,offsides])
    

df5 = pd.DataFrame(data_duels, columns=['Name','Possesion Lost','Fouls','Was Fouled','Offsides'])





Goalkeeper_Button = driver.find_element (By.XPATH,"//span[@class='Text eSPCzT' and contains(text(), 'Goalkeeper')]")
try:
    Goalkeeper_Button.click()
except ElementClickInterceptedException:
    # Eğer normal click çalışmazsa, JavaScript ile tıklama yap
    driver.execute_script("arguments[0].click();", Goalkeeper_Button)

wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='Text eSPCzT']")))
data_goalkeepers = []
rows6 = driver.find_elements(By.XPATH, "//tbody[@class='TableBody juEMAj']/tr")

# Her satır için gerekli bilgileri çek
for row in rows6:
    name = row.find_element(By.XPATH, ".//td[2]").text  # Oyuncu ismi
    saves = row.find_element(By.XPATH, ".//td[3]").text 
    goals_prevented = row.find_element(By.XPATH, ".//td[4]").text 
    punches = row.find_element(By.XPATH, ".//td[5]").text
    runs_out_succ = row.find_element(By.XPATH, ".//td[6]").text 
    runs_out_total, runs_out_succ = runs_out_succ.split('(')
    # Parantez ve boşlukları temizleme
    runs_out_total = runs_out_total.strip()  # Sağ ve sol taraftaki boşlukları kaldırma
    runs_out_succ = runs_out_succ.strip(')')  # Sağdaki parantezi kaldırma
    high_claims = row.find_element(By.XPATH, ".//td[7]").text
    goalkeeper_notes = row.find_element(By.XPATH, ".//td[8]").text
    data_duels.append([name,saves,goals_prevented,punches,runs_out_total,runs_out_succ,high_claims,goalkeeper_notes])
    

df6 = pd.DataFrame(data_goalkeepers, columns=['Name','Saves','Goals Prevented','Punches','Runs Out Total','Runs Out Succ','High Claims','GoalKeeper Notes'])

dfs = [df, df2, df3, df4, df5, df6]

# Tüm DataFrame'leri 'Name' sütunu üzerinden birleştir
merged_df = reduce(lambda left, right: pd.merge(left, right, on='Name', how='outer'), dfs)

csv_file_path = 'İstenilen/dizin/dosya.csv' #Kaydetmek istenilen dizin, dosya adı ve uzantısı
merged_df.to_csv(csv_file_path, index=False, encoding='utf-8')
print("CSV dosyası başarıyla kaydedildi:", csv_file_path)
# CSV dosyasına kaydet

# Tarayıcıyı kapat
driver.quit()
