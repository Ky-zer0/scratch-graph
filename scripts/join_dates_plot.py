#plot the join dates as a scatter plot
import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv("users_with_communities_res_3.csv")
df2=pd.read_csv("embedding.csv",sep=' ', names=['id','x','y'], skiprows=1)
df3=pd.read_csv("join_dates10k.csv")

data=df.merge(df2, on='id')
data=data.merge(df3, on='id', how="inner")
data['date']= pd.to_datetime(data["date"], errors="coerce") #convert to dates
print(data)

plt.figure(figsize=(10, 10))

scatter = plt.scatter(
    data["x"], 
    data["y"], 
    c=data["date"].map(pd.Timestamp.toordinal),  # convert dates to numbers
    cmap="viridis", 
    alpha=0.7,
    s=5
)

plt.gca().set_aspect("equal")
plt.axis("off")
plt.show()