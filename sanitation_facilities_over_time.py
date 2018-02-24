# Name: Karthik Ramanathan
# Note: Reusing and improving upon code from a similar previous assignment

import requests
import pandas as pd
import json
import matplotlib.pyplot as plt
import pdb

def fetch_data(fetch=True, indicator = "SH.STA.ACSN"):
	"""
	Get data from the API and store it in a json file 
	"""
	# fetch new data only if the parameter for fetch is True
	if fetch:
		headers = {"user-agent": "drkarthi@umich.com"}
		sanitation_facilities = []
		page_num = 0
		# traverse in pages in order to handle larger data sets
		while True:
			page_num += 1
			print("Page Num = ", page_num)
			# get data from API using requests
			wb_data = requests.get("https://api.worldbank.org/countries/all/indicators/" + indicator + "?date=1960:2017&format=json&per_page=1000&page="+str(page_num), headers=headers)
			# convert requests object to json
			wb_json = wb_data.json()
			sanitation_facilities_page = wb_json[1]
			sanitation_facilities.extend(sanitation_facilities_page)
			# break when all the data has already been collected
			if len(sanitation_facilities_page) == 0:
				break
		# write data to json file
		with open('sanitation_facilities.json','w') as outfile:
			json.dump(sanitation_facilities, outfile)


def json_to_csv(fetch=True):
	"""
	Convert the data from json format to csv format for ease of analysis
	"""
	if fetch:
		# read data from json file
		with open('sanitation_facilities.json') as json_data:
			sanitation_facilities = json.load(json_data)
		# construct the data as a list of lists
		headings = ['CountryId', 'Country', 'Year', 'Sanitation', 'Decimal']
		sanitation_facilities_list = [headings]
		for item in sanitation_facilities:
			country_id = item['country']['id']
			country = item['country']['value']
			year = item['date']
			sanitation = item['value']
			decimal = item['decimal']
			row = [country_id, country, year, sanitation, decimal]
			sanitation_facilities_list.append(row)
		# write to csv format using pandas
		df_sanitation = pd.DataFrame(sanitation_facilities_list)
		df_sanitation.to_csv("sanitation_facilities.csv", header=False, index=False)


def plot_data():
	"""
	Plot the trends in life expectancy for countries in different income levels
	"""
	# initialization
	df_sanitation_raw = pd.read_csv('sanitation_facilities.csv', encoding='windows-1252')
	df_sanitation = df_sanitation_raw.dropna()
	income_levels = ['Low income', 'Lower middle income', 'Upper middle income', 'High income']
	colors = ['red', 'lightcoral', 'gray', 'silver']
	dfs = []

	df_world = df_sanitation[df_sanitation.Country == 'World']
	df_world = df_world.reindex(index=df_world.index[::-1])

	# get the data for different income levels and order them in ascending order by year
	for income_level in income_levels:
		df_income_level = df_sanitation[df_sanitation.Country == income_level]
		df_sorted = df_income_level.reindex(index=df_income_level.index[::-1])
		dfs.append(df_sorted)

	# plot the life expectancy for the different income levels
	fig, ax = plt.subplots(figsize=(15,10))
	df_world.plot(x='Year', y='Sanitation', color='black', subplots=True, figsize=(15,10), ax=ax, linestyle = '--', label='World')
	for i, df in enumerate(dfs):
		df.plot(x='Year', y='Sanitation', color=colors[i], subplots=True, figsize=(15,10), ax=ax, label=income_levels[i])
	
	# axis and title settings for the plot
	for spine in plt.gca().spines.values():
		spine.set_visible(False)
	ax.grid(b=True, axis = 'y', linestyle = "-", linewidth=0.5, color="#DCDCDC")
	ttl = ax.title
	ttl.set_position([.5, 1.08])

	# plot settings
	plt.ylim(-2, 100)
	plt.title('Improved sanitation facilities (% of population with access), 1990 to 2015')
	plt.xlabel("")
	plt.ylabel("% of population with access to improved sanitation facilities", labelpad = 20)
	plt.tick_params(top = False, right = False, bottom = False, left = False)
	plt.legend(loc = 'lower right', frameon = False)
	
	# pdb.set_trace()
	# handles, labels = ax.get_legend_handles_labels()
	# labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
	# ax.legend(handles, labels)

	plt.savefig('sanitation_facilities.png')
	plt.show()

def main():
	fetch = False
	fetch_data(fetch)
	json_to_csv(fetch)
	plot_data()

main()