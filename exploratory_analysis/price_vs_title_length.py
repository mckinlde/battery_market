## let's plot the price of a listing against the number of chars in its title.

# 1] sql select *

# 2] for _ in listings, title_length = len(_.title)

# 3] plot title_length vs price


import pandas as pd


# /// Read CSV into DataFrame, labeling columns with headers, not specifying a column (index_col) to label each row
D = pd.read_csv("../eggs.csv", index_col=False)
print(D.head())

# new price - title only dataframe
new = D[['titles','prices']].copy()
#'Seller Zip Code','Buyer Zip Code','Title Application Date','Issue Type'
print(new.head())

# replace titles with len(title)
title_lengths = []
for _ in new['titles']:
    title_lengths.append(len(_))

print(title_lengths)

import numpy as np
df = pd.DataFrame(np.reshape(title_lengths,(len(title_lengths),1)),columns=['title_lengths'])

print(df.head())

# get it all into 1 dataframe
new = new.join(df, lsuffix='_new', rsuffix='_df')

print(new.head())


import matplotlib.pylab as plt
import seaborn as sns

new['prices'].replace('^\$+', '', regex=True, inplace=True) #trim leading $
Y = new['prices']
X = new['title_lengths']
##ScatterPlot
plt.scatter(X, Y, c='green', marker='o')
plt.title("Batteries from BatteryJunction.com")
plt.xlabel("Listing Title Length (char)")
plt.ylabel("Price ($USD)")
plt.show()

