import csv

def write_operation(filename,data):
	with open('./data_files/'+ filename, "wb") as f:
		writer = csv.writer(f)
		writer.writerows(data)


def create_url(url,page_number):
	return url + str(page_number)