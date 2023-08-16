import os
import numpy as np
import pandas as pd
import json

class LoLReader:

    def __init__(self, summoner=None) -> None:
        self.summoner = summoner
        self.json = JSONReader()

    def open(self, match) -> pd.DataFrame:
        if isinstance(match, str):
            match = self.json.open(path=match.replace('.json', '') + '.json')
        df = pd.DataFrame(columns=['Summoner', 'Champion', 'Team', 'Kill', 'Death', 'Assist', 'KD', 'Damage', 'Tank', 'Golds'])
        for p in match['info']['participants']:
            df = df.append({'Summoner': p['summonerName'], 'Champion': p['championName'], 'Team': str(p['teamId'])[0],
                            'Kill': p['kills'], 'Death': p['deaths'], 'Assist': p['assists'], 'KD': round(float(p['kills']) / max(float(p['deaths']), 1), 2),
                            'Damage': p['magicDamageDealtToChampions'] + p['physicalDamageDealtToChampions'],
                            'Tank': p['magicDamageTaken'] + p['physicalDamageTaken'], 'Golds': p['goldEarned']},
                            ignore_index=True)
        return df

    def stats(self, match, categorie, summoner=None) -> dict:
        if not summoner is None:
            self.summoner = summoner
        if self.summoner is None:
            print(f' /!\\ No summoner specified')
            return None
        
        df = self.open(match=match)

        df['Team Rank'] = df.groupby('Team')[categorie].rank(method='first', ascending=False).astype(int)
        df['Global Rank'] = df[categorie].rank(method='first', ascending=False).astype(int)

        player_team = df[df['Summoner'] == self.summoner]['Team'].iloc[0]

        
        if df['Kill'].sum() < 10:   # TO avoid unplayed games
            return {'statut': 'unplayed'}
        
        df = df[df[categorie] > 0]  # To avoid 0 damage player (division by zero on min)
        df_team = df[df['Team'] == player_team]
        value = float(df[df['Summoner'] == self.summoner][categorie])

        return {'rank':
                    {'team': int(df[df['Summoner'] == self.summoner]['Team Rank']),
                     'global': int(df[df['Summoner'] == self.summoner]['Global Rank'])},
                'gain':
                    {'team':
                        {'min': value / float(df_team[categorie].min()) - 1,
                         'mean': value / float(df_team[categorie].mean()) - 1,
                         'max': value / float(df_team[categorie].max()) - 1},
                    'global':
                        {'min': value / float(df[categorie].min()) - 1,
                         'mean': value / float(df[categorie].mean()) - 1,
                         'max': value / float(df[categorie].max()) - 1},
                    },
                'statut': 'played'
                }

    def rank(self, path, categorie, summoner=None, cumulative=True) -> dict:
        if not summoner is None:
            self.summoner = summoner
        if self.summoner is None:
            print(f' /!\\ No summoner specified')
            return None
        
        team_rank, global_rank, skipped = np.zeros((5, )), np.zeros((10, )), 0

        for file in os.listdir(path):
            data = self.stats(match=f"data/{self.summoner.replace(' ', '_')}/{file}", categorie=categorie)
            if data['statut'] == 'unplayed':
                skipped += 1
                continue
            ranks = [int(data['rank']['team']-1), int(data['rank']['global']-1)]
            if cumulative:
                team_rank[ranks[0]:] = team_rank[ranks[0]:] + np.ones((5-ranks[0]))
                global_rank[ranks[1]:] = global_rank[ranks[1]:] + np.ones((10-ranks[1]))
            else:
                team_rank[ranks[0]] += 1
                global_rank[ranks[1]] += 1
        
        return {'team': team_rank, 'global': global_rank, 'total': len(os.listdir(path)) - skipped}

    def show(self, match) -> None:
        print(self.open(match=match))

class JSONReader:

    def __init__(self) -> None:
        pass

    def open(self, path: str):
        with open(path.replace('.json', '') + '.json', 'r') as file:
            data = json.load(file)
        return data

    def save(self, data: dict, name: str) -> None:
        self.folder('/'.join(name.split('/')[:-1]))
        with open(f"{name.replace('.json', '')}.json", 'w') as file:
            json.dump(data, file)
        print(f' > File {name} saved')
    
    def show(self, data: dict) -> None:
        print(json.dumps(data, indent=4))

    def folder(self, path):
        if not os.path.exists(path):
            os.mkdir(path)
