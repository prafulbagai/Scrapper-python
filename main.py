import multiprocessing, logging
import workers, config


def main():

	print '#################################################################'
	print '#####                      Scrapper                         #####'
	print '#################################################################'
	print '\n'
	print 'This scrapper scraps the data from Maplin e-Commerce store.'
	print 'The category it scraps are : '
	print '\n'
	print '1. I.P. CCTV'
	print '2. DVRs (Digital Video Recorders)'
	print '3. Security Systems and Alarms'
	print '4. Covert & Mobile Surveillance'
	print '5. Safes & Locks'
	print '\n'
	print 'It also identifies leading brands and the number of SKUs offered.'	
	print '\n'
	print 'Note: The final outcome are the excel files for each category that\ncontains name of SKU, SKU Code and Current Price.'
	print '\n'
	raw_input('################### Press Enter to continue #####################')
	
	logging.basicConfig(filename='logging.log',level=logging.DEBUG)

	for url in config.SEED_LIST:
		d = multiprocessing.Process(target = workers.scrap_url, args = (url,)) #starting a new process for each category.
		d.start()

if __name__ == "__main__":
	main()