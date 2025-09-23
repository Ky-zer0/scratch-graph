# Visualising the Scratch Network
This project collects data about user connections on the Scratch website, and analyses the structure of the resulting graph. To read more, see this [article](https://medium.com/p/143a12c57836).

If you would like to use the data, it is available on [Kaggle](https://www.kaggle.com/datasets/is0morphism/scratch-users-with-follow-connections).

## Scripts overview
Note that some temporary scripts are not included. 


- main_crawler.py - For crawling the user graph and getting the data
- histogram.py - Plots the output from LargeVis
- communities.py - Runs Leiden community detection algorithm on the graph (note that the graph must be converted to graphml)
- join_dates_crawler.py - Finds join dates for a sample of users
- join_dates_plot.py - Creates a scatter plot of the join dates
