#find the join dates of a sample of users
import requests
import pandas as pd
from tqdm import tqdm

df=pd.read_csv("users_with_communities_res_3.csv")
df2=pd.read_csv("embedding.csv",sep=' ', names=['id','x','y'], skiprows=1)

data=df.merge(df2, on='id')
print(data.head())

def get_date(user): #get join date of a user
    response=requests.get("https://api.scratch.mit.edu/users/"+user)
    try:
        return response.json()["history"]["joined"].split("T")[0]
    except:
        return 0
    
sample=data.sample(n=10000)

results=[]
for index, row in tqdm(sample.iterrows()):
    date=get_date(row['username'])
    results.append({'id':row['id'], 'date':date})

results_df=pd.DataFrame(results)

results_df.to_csv("join_dates10k.csv", index=False)