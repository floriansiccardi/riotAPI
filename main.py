import matplotlib.pyplot as plt
import numpy as np
from classes.client import Client
from classes.database import LoLReader



# --- PARAMETERS ---
API_key = 'xxx-xxx-xxx'      # https://developer.riotgames.com/
summoner = 'mySummoner'
region = 'NA'          # NA, EUW, KR
rank_of = 'Damage'        # Kill, Death, Assist, KD, Damage, Tank, Golds
# ------------------



client = Client(API_key=API_key)
if not client.connect(summoner=summoner, region=region):
    exit()
client.save_match_history(quantity=100, path=f"data/{summoner.replace(' ', '_')}")

reader = LoLReader(summoner=summoner)
ranks = reader.rank(path=f"data/{summoner.replace(' ', '_')}/", categorie=rank_of, cumulative=False)
print(f" > Ranks in Team ({ranks['total']} games):\n{ranks['team']}\n\n   Ranks in Global ({ranks['total']} games):\n{ranks['global']}")

plt.bar(np.arange(1, 6, dtype=int), ranks['team'])
plt.title(f"{rank_of} rank in Team ({ranks['total']} games)")
plt.show()
plt.bar(np.arange(1, 11, dtype=int), ranks['global'])
plt.title(f"{rank_of} rank in Global ({ranks['total']} games)")
plt.show()

