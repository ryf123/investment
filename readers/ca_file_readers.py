import csv
import numpy


class Reader:
	def get_column_names_index_mapping(self, row):
		"""
		:param row:
		:return: the mapping of column names and index
		"""
		map = {}
		for i, name in enumerate(row):
			map[name] = i
		return map


class CAHousingReader(Reader):
	# data is from: https://www.car.org/en/marketdata/data/ftbhai
	MonYrColName = 'Mon-Yr'

	def __init__(self):
		self.file_path = "../data/ca_housing_data.csv"
		self.prices_map = {}

		with open(self.file_path, 'r') as f:
			reader = csv.DictReader(f)

			# print reader.fieldnames

			# read prices from the file to prices map, for every month
			for row in reader:
				for key in reader.fieldnames:
					if key == self.MonYrColName:
						# skip if it's the column of year/month
						continue
					price = row[key]
					if price == 'NA' or price == '':
						continue

					price = self.parse_price(price)
					if key not in self.prices_map:
						self.prices_map[key] = []
					self.prices_map[key].append(price)

	def get_std_mean_for_each_city(self):
		# cal percentage change
		for key in self.prices_map:
			prices = self.prices_map[key]
			prices_length = len(prices)
			if prices_length < 12:
				continue

			pc = []
			i = 12  # since the prices is every month, we only use every 12 months
			price_prev = prices[0]
			while i < prices_length:
				price_current = prices[i]
				diff = (price_current - price_prev + 0.0) / price_prev
				pc.append(diff)
				price_prev = price_current
				i += 12

			numpy_array = numpy.array(pc)
			print '%s,%s,%s' % (key, str(numpy_array.std()), str(numpy_array.mean())), pc

	def parse_price(self, price):
		return int(price.replace('$', '').replace(',', ''))


reader = CAHousingReader()
reader.get_std_mean_for_each_city()


