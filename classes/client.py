import requests
import os
import time
from classes.database import JSONReader

class Client:
    def __init__(self, API_key: str) -> None:
        self.key = API_key
        self.user = None

        self.region_name, self.region_short, self.region_long = '', '', ''

        self.request = []
        self.request_lim_1sec, self.request_lim_2min = 10, 80  #20 & 100
        self.match_ids = []
        self.N_match = 0

        self.json = JSONReader()
    
    def _check_request(self) -> bool:
        request_1sec, request_2min = 0, 0
        for t in self.request:
            dt = time.time() - t
            if dt < 120:
                request_2min += 1
                if dt < 1:
                    request_1sec += 1
            else:
                self.request.remove(t)
        return request_1sec < self.request_lim_1sec and request_2min < self.request_lim_2min

    def _wait_for_request(self) -> None:
        is_waiting = False
        while not self._check_request():
            if not is_waiting:
                print(' > Program must wait few second ... Please wait')
            time.sleep(0.2)
            is_waiting = True
        self.request.append(time.time())
    
    def connect(self, summoner: str, region='NA', quantity=20, display=True) -> bool:
        self.user, self.N_match = summoner.replace(' ', '%20'), quantity

        self.region_set(region=region)

        # Get ID
        try:
            url = f'https://{self.region_short}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{self.user}'
            self._wait_for_request()
            response = requests.get(url, headers={'X-Riot-Token': self.key})
            user_data = response.json()
            self.puuid, level = user_data['puuid'], user_data['summonerLevel']
        except:
            if display:
                print(f' /!\\ Summoner {summoner} not found in {self.region_name} region.')
            return False
        
        # Match history
        try:
            url = f'https://{self.region_long}.api.riotgames.com/lol/match/v5/matches/by-puuid/{self.puuid}/ids?start=0&count={quantity}'
            self._wait_for_request()
            response = requests.get(url, headers={'X-Riot-Token': self.key})
            self.match_ids = response.json()[:]
        except:
            print(f' /!\\ No match history found')
            return False

        if display:
            print(f'\n > Connected to {summoner} (level {level}) in {self.region_name} region.\n')
        
        return True

    def get_match(self, index) -> dict:
        try:
            url = f'https://{self.region_long}.api.riotgames.com/lol/match/v5/matches/{self.match_ids[index]}'
            self._wait_for_request()
            response = requests.get(url, headers={'X-Riot-Token': self.key})
            match_data = response.json()
            return match_data
        except:
            print(f' /!\\ Match not found. Please retry another index.')

    def save_match_history(self, quantity=None, path='/data') -> None:
        if path[-1] == '/':
            path = path[:-1]
        if not quantity is None:
            self.connect(summoner=self.user, quantity=quantity, region=self.region_name, display=False)
        
        for index, id in enumerate(self.match_ids):
            if not os.path.exists(f"{path}/match_{id}.json"):
                self.json.save(data=self.get_match(index=index), name=f"{path}/match_{id}")
        print(' > History saved\n')

    def region_set(self, region: str) -> None:
        getattr(self, f'region_set_{region}')()
        self.region_name = region
    
    def region_set_NA(self) -> None:
        self.region_short, self.region_long = 'na1', 'americas'
    
    def region_set_EUW(self) -> None:
        self.region_short, self.region_long = 'euw1', 'europe'
    
    def region_set_EUN(self) -> None:
        self.region_short, self.region_long = 'eun1', 'europe'
    
    def region_set_KR(self) -> None:
        self.region_short, self.region_long = 'kr', 'asia'
    
    def region_set_OC(self) -> None:
        self.region_short, self.region_long = 'oc1', 'sea'

