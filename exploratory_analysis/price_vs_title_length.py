## let's plot the price of a listing against the number of chars in its title.

# 1] sql select *

# 2] for _ in listings, title_length = len(_.title)

# 3] plot title_length vs price


import pandas as pd


# /// Read CSV into DataFrame, labeling columns with headers, not specifying a column (index_col) to label each row
D = pd.read_csv("eggs.csv", index_col=False)  # popular LabVIEW clusters vs. ratings
print(D.head())

# new price - title only dataframe
new = D[['Vehicle Make','Vehicle Model','Model Year','Odometer miles','Purchase Price']].copy()
#'Seller Zip Code','Buyer Zip Code','Title Application Date','Issue Type'
print(new.head())

#Write to file
new.to_csv('mmyop_notation_gvmt_data.csv', encoding='utf-8', index=False, float_format='%.f')
print('mark')


# Sort my ascending miles, then descending year
df = pd.DataFrame(D)
df.sort_values(by=['Odometer miles'], inplace=True, ascending=True)
df.sort_values(by=['Model Year'], inplace=True, ascending=False)
print(df.head())
import matplotlib.pylab as plt
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


Z = D['Purchase Price']
Y = D['Odometer miles']
X = D['Model Year']
##ScatterPlot
ax.scatter(X, Y, Z, c='green', marker='o')
ax.set_zlabel('Purchase Price')
ax.set_ylabel('Odometer miles')
ax.set_xlabel('Model Year')
plt.show()

