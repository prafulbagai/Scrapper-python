import itertools, logging , requests
from bs4 import BeautifulSoup as bs
import config, utils


def scrap_url(url):
	page_number = 1
	product_info = [['SKU','SKU Code', 'Current Price (in Pounds)']]
	brand_info = [['BrandName','Total SKUs']]

	while True:
		page_url = utils.create_url(url,page_number)
		r = requests.get(page_url)
		soup = bs(r.content)

		if page_number == 1: # Brand info is scraped only once.
			try:
				brand_data = soup.find_all("div",{"id" : "refinements"})
				brand_data = brand_data[0].contents[17]
				brands = iter(brand_data.find_all("a"))
				skus = iter(brand_data.find_all("span"))

				for brand,sku in itertools.izip(brands,skus):
					if brand.get("href") == "#":
						brand = next(brands)

					try: brand_name = brand.text
					except: pass

					try: sku_offered = sku.text
					except: pass

					brand_info.append([brand_name,sku_offered])

			except:
				continue

		#scraping product info.
		product_data = soup.find_all("div", {"class" : "tileinfo"})
		if not product_data: #testing whether or not products are there in the requested page. If not scraping is done. Else, its continued.
			break

		for item in product_data:
			try: sku_name = str(item.contents[1].find_all("a",{"data-segment":"CategoriesEditorial"})[0].text)
			except Exception,e: 
				logging.info(e)
				pass

			try: sku_code = str(item.contents[7].text)[6:]
			except Exception,e: 
				logging.info(e)
				pass
			
			try:
				new_price_tag = item.contents[9].find_all("p",{"class":"new-price"})
				if new_price_tag:
					price = (new_price_tag[0].text)[1:-1]
				else:
					price = (item.contents[11].find_all("p",{"class":"new-price"})[0].text)[1:-1]
			except Exception,e:
				logging.info(e)
				pass

			product_info.append([sku_name,sku_code,price])

		page_number +=1

	#finding the name of the category
	for category,category_url in (config.CATEGORY_URL_MAPPING).items():
		if category_url == url:
			category_name = category
			break

	product_filename = category_name + '_PRODUCT_FILE.csv'
	brand_filename = category_name + '_BRAND_FILE.csv'
	
	product_file = utils.write_operation(product_filename,product_info)
	brand_file = utils.write_operation(brand_filename,brand_info)