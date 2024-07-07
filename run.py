import base64
import random
import socket
import requests
import time
from datetime import datetime

def fetch_pet_info(headers):
    try:
        pet_response = requests.get("https://api-clicker.pixelverse.xyz/api/pets", headers=headers)
        if pet_response.status_code == 200:
            pet_data = pet_response.json()
            pets = pet_data.get('data', [])
            print("Pet Information:")
            for pet in pets:
                name = pet.get('name')
                user_pet = pet.get('userPet', {})
                level = user_pet.get('level')
                stats = user_pet.get('stats', [])

                # Initialize default values
                max_energy = power = recharge_speed = None

                # Extract specific stats
                for stat in stats:
                    stat_name = stat.get('petsStat', {}).get('name')
                    current_value = stat.get('currentValue')
                    if stat_name == 'Max energy':
                        max_energy = current_value
                    elif stat_name == 'Damage':
                        power = current_value
                    elif stat_name == 'Energy restoration':
                        recharge_speed = current_value

                print(f"Name: {name}, Level: {level}, Max energy: {max_energy}, Power: {power}, Recharge speed: {recharge_speed}")
            return pets  # Return the pet data for further processing
        else:
            print("Failed to fetch pet information. Status code:", pet_response.status_code)
    except Exception as e:
        print("Error fetching pet information:", e)
    return []

def upgrade_pet(headers, pet):
    try:
        user_pet = pet.get('userPet', {})
        pet_id = user_pet.get('id')

        upgrade_response = requests.post(f"https://api-clicker.pixelverse.xyz/api/pets/user-pets/{pet_id}/level-up", headers=headers)
        if upgrade_response.status_code == 201:
            print(f"Pet with ID {pet_id} upgraded successfully.")
            # Fetch and display the updated pet information
            fetch_pet_info(headers)
            return upgrade_response
        else:
            print(f"Failed to upgrade pet with ID {pet_id}. Status code:", upgrade_response.status_code)
            return None
    except Exception as e:
        print(f"Error upgrading pet with ID {pet_id}:", e)
    return None

def mainLoop(headers, auto_upgrade, level_monster):
    claim_count = 0
    try:
        # Login and get user information
        user_response = requests.get("https://api-clicker.pixelverse.xyz/api/users", headers=headers)
        if user_response.status_code == 200:
            user_data = user_response.json()
            telegram_user = user_data.get("telegramUserId")
            claim_count = user_data.get("clicksCount", 0)
            if telegram_user:
                print("Login successful!")
                print(f"User : {user_data['username']}")
                print("x"*20)
            else:
                print("Login successful! But Telegram User ID not found.")
        else:
            print("Login failed. Status code:", user_response.status_code)
            return

        # Fetch and display pet information after login
        pets = fetch_pet_info(headers)
        num_claims = 0
        time.sleep(10)
        claim_response = requests.post("https://api-clicker.pixelverse.xyz/api/mining/claim", headers=headers)
        if claim_response.status_code == 201:
            claim_data = claim_response.json()
            claimed_amount = claim_data.get("claimedAmount", 0)
            claim_count += claimed_amount
            num_claims += 1
            print("Claimed Amount: " + str(claimed_amount) + " ,Total Earned: " + str(claim_count))
                
            if auto_upgrade:
                print("Auto-upgrading pets...")
                for pet in pets:
                    user_pet = pet.get('userPet', {})
                    level = user_pet.get('level')
                    if level <= level_monster:
                        upgrade_pet(headers, pet)
                        time.sleep(1)
                    # Re-fetch pet information after upgrades
        else:
            print("Claim failed")

    except Exception as e:
        print("Error:", e)

def read_initdata_from_file(filename):
    initdata_list = []
    with open(filename, 'r') as file:
        for line in file:
            initdata_list.append(line.strip())
    return initdata_list

def checkin(headers):
    try:
        claim_response = requests.post("https://api-clicker.pixelverse.xyz/api/daily-rewards/claim", headers=headers)
        print(claim_response.text)
        if claim_response.status_code == 201:
            claim_data = claim_response.json()
            print("checkin success")
            return claim_data
        else:
            print("checkin failed")
    except Exception as e:
        print("Error:", e)

def maincheckin():
    initdata_file = "initdata.txt"
    initdata_list = read_initdata_from_file(initdata_file)
    for index, init_data in enumerate(initdata_list):
        headers = {
        'Accept': 'application/json, text/plain, */*',
        'Cache-Control': 'no-cache',
        'Initdata': init_data,
        'Origin': 'https://sexyzbot.pxlvrs.io',
        'Pragma': 'no-cache',
        'Referer': 'https://sexyzbot.pxlvrs.io/',
        'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
                }
        checkin(headers)
        # combo(headers)
        # buy_pet(headers, list_id_tg[index])
        time.sleep(5)

def mainclaim():
    getpcname = socket.gethostname()
    name = "PixelVerse"
    current_date = datetime.now() # Get the current date
    status = '0'
    level_monster = 0
    delay_time = 600
    auto_upgrade = input("Enable auto-upgrade for pets? (y/n): ").strip().lower()
    if auto_upgrade in ['y', 'n', '']:
            auto_upgrade = auto_upgrade or 'n'

    
    if auto_upgrade == 'y':
        level_monster = int(input("input max level pets? (min 5): ").strip().lower())
        if level_monster < 5:
            level_monster = level_monster or 5
     
    
    delay_time = int(input("input waiting time in second? (default 600): ").strip().lower())
    if delay_time < 600:
        delay_time = delay_time or 600


    while(True):
        initdata_file = "initdata.txt"
        initdata_list = read_initdata_from_file(initdata_file)
        for init_data in initdata_list:
            headers = {
            'Accept': 'application/json, text/plain, */*',
            'Cache-Control': 'no-cache',
            'Initdata': init_data,
            'Origin': 'https://sexyzbot.pxlvrs.io',
            'Pragma': 'no-cache',
            'Referer': 'https://sexyzbot.pxlvrs.io/',
            'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
                }
            mainLoop(headers, auto_upgrade, level_monster)
        # times = random.randint(10800, 13000)
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{now} | waiting {delay_time} seconds")
        time.sleep(delay_time)
        serial = get_serial(current_date, getpcname, name, status)
        decodeds = decode_pc(serial, getpcname, name, current_date)
        if decodeds == 0 :
            print_welcome_message(serial)
            break # Delay 60 detik sebelum membaca kembali file initData

def maincombo():
    initdata_file = "initdata.txt"
    initdata_list = read_initdata_from_file(initdata_file)
    user_input = input("imput list daily combo (example 1,4,3,2 | split use , every number): ")
    user_inputs = [int(x.strip()) for x in user_input.split(',')]
    for index, init_data in enumerate(initdata_list):
        headers = {
        'Accept': 'application/json, text/plain, */*',
        'Cache-Control': 'no-cache',
        'Initdata': init_data,
        'Origin': 'https://sexyzbot.pxlvrs.io',
        'Pragma': 'no-cache',
        'Referer': 'https://sexyzbot.pxlvrs.io/',
        'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
                }
        # checkin(headers)
        combo(headers, user_inputs)
        # buy_pet(headers, list_id_tg[index])
        time.sleep(5)

def combo(headers, input_user):
    

    try:

        response = requests.get(url="https://api-clicker.pixelverse.xyz/api/cypher-games/current", headers=headers)
        if response.status_code == 200:
            data = response.json()
            combo_id = data.get('id')
            options = data.get('availableOptions')
            json_data = {options[i-1]['id']: input_user.index(i) for i in input_user}
            response = requests.post(url=f"https://api-clicker.pixelverse.xyz/api/cypher-games/{combo_id}/answer", json=json_data, headers=headers)
            if response.status_code != 400:
                
                data = response.json()
          
                jumlah = data.get("rewardAmount")
                percent = data.get("rewardPercent")
                print(f"Daily Combo : Claimed {jumlah} | {percent}%", flush=True)

            else:
                response = response.json()
                print(f" Daily Combo : Failed to claim {response['message']}", flush=True)
                return None
        else:
            response = response.json()
            if "BadRequestException" in response['code']:
                print(f" Daily Combo  : You have already played cypher game today", flush=True)
            else:
                print(f" Daily Combo  : Failed to get data", flush=True)
            return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
#===================================== GENERATED =================================================
def print_welcome_message(serial=None):
    print(r"""
              
            Created By Snail S4NS Group
    find new airdrop & bot here: t.me/sansxgroup
              
          """)
    print()
    if serial is not None:
        print(f"Copy, tag bot @SnailHelperBot and paste this key in discussion group t.me/sansxgroup")
        print(f"Your key : {serial}")

def read_serial_from_file(filename):
    serial_list = []
    with open(filename, 'r') as file:
        for line in file:
            serial_list.append(line.strip())
    return serial_list

serial_file = "serial.txt"
serial_list = read_serial_from_file(serial_file)

def get_serial(current_date, getpcname, name, status):
    formatted_current_date = current_date.strftime("%d-%m-%Y")
    # Encode each value using base64
    getpcname += "knjt"
    name    += "knjt"
    encoded_getpcname = base64.b64encode(getpcname.encode()).decode().replace("=", "")
    encoded_current_date = base64.b64encode(formatted_current_date.encode()).decode().replace("=", "")
    encoded_name = base64.b64encode(name.encode()).decode().replace("=", "")
    encoded_status = base64.b64encode(str(status).encode()).decode().replace("=", "")

    # Calculate the length of each encoded value
    getpcname_len = len(encoded_getpcname)
    current_date_len = len(encoded_current_date)
    name_len = len(encoded_name)
    status_len = len(encoded_status)

    # Concatenate the encoded values with their lengths
    serial = "S4NS-"
    serial += str(getpcname_len).zfill(2) + encoded_getpcname
    serial += str(current_date_len).zfill(2) + encoded_current_date
    serial += str(name_len).zfill(2) + encoded_name
    serial += str(status_len).zfill(2) + encoded_status
    return serial

def decode_pc(serial, getpcname, name, current_date):
    try:
        getpcname_len = int(serial[5:7])
        encoded_getpcname = serial[7:7+getpcname_len]
        current_date_len = int(serial[7+getpcname_len:9+getpcname_len])
        encoded_current_date = serial[9+getpcname_len:9+getpcname_len+current_date_len]
        name_len = int(serial[9+getpcname_len+current_date_len:11+getpcname_len+current_date_len])
        encoded_name = serial[11+getpcname_len+current_date_len:11+getpcname_len+current_date_len+name_len]
        status_len = int(serial[11+getpcname_len+current_date_len+name_len:13+getpcname_len+current_date_len+name_len])
        encoded_status = serial[13+getpcname_len+current_date_len+name_len:13+getpcname_len+current_date_len+name_len+status_len]

        # Decode each value using base64
        decoded_getpcname = base64.b64decode(encoded_getpcname + "==").decode()
        decoded_current_date = base64.b64decode(encoded_current_date + "==").decode()
        decoded_name = base64.b64decode(encoded_name + "==").decode()
        decoded_status = base64.b64decode(encoded_status + "==").decode()
        
        dates = compare_dates(decoded_current_date)

        if decoded_status != '1':
            print("Key Not Generated")
            return None
            
        elif decoded_getpcname.replace("knjt", "") != getpcname:
            print("Different devices registered")
            return None
        
        elif decoded_name.replace("knjt", "") != name:
            print("Different bot registered")
            return None
        
        elif dates < 0:
            print("Key Expired")
            return None
        else:
            print(f"ur key alive until : {decoded_current_date}")
            return dates
    except Exception as e:
        print(f'Key Error : {e}')

def compare_dates(date_str):
    tanggal_compare_dt = datetime.strptime(date_str, '%d-%m-%Y')
    tanggal_now = datetime.now()
    perbedaan_hari = (tanggal_compare_dt - tanggal_now).days
    return perbedaan_hari

def started():
    getpcname = socket.gethostname()
    name = "PixelVerse"
    current_date = datetime.now() # Get the current date
    status = '0'

    if len(serial_list) == 0:
        serial = get_serial(current_date, getpcname, name, status)
        print_welcome_message(serial)
    else:
        serial = serial_list[0]
        if serial == 'S4NS-XXWEWANTBYPASSXX':
            main()
        else:
            decodeds = decode_pc(serial, getpcname, name, current_date)
            if decodeds is not None:
                    print_welcome_message()
                    time.sleep(10)
                    main()         
            else:
                serial = get_serial(current_date, getpcname, name, status)
                print_welcome_message(serial)
                print("Please submit the key to bot for get new key")
    

def main():
    print(r"""
=======================================
= Pilihan : 
= 1. checkin daily claim
= 2. claim daily
= 3. claim combo
=======================================
          """)
    while True:
        auto_upgrade = input("pilih fitur yang dipakai ? (1/2/3): ").strip().lower()
        if auto_upgrade in ['1', '2', '3', '']:
            auto_upgrade = auto_upgrade or '1'
            break
        else:
            print("Masukkan '1', '2' atau '3'.")

    if auto_upgrade == '1':
        maincheckin()
    elif auto_upgrade == '2':
        mainclaim()
    else:
        maincombo()

started()


