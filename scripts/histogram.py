#load the result from largevis and generate a density plot
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

lvdf = pd.read_csv('embedding.csv', header=None, sep=' ',
                   skiprows=1, names=['id','x', 'y'])

data= pd.read_csv('users_with_communities_res_3.csv', header=0)

data=data.merge(lvdf ,on='id')
print(data.head())

plt.figure(figsize=(10, 10), dpi=300)
plt.hist2d(data['x'].values, data['y'].values, bins=1000, norm=LogNorm());
ax = plt.gca()
ax.set_facecolor('black')
plt.gca().set_aspect("equal")
plt.show()

