import pickle
import urllib.request
import requests # pip install requests --user For downloading, has a few extra thinkgs
import shutil
import tarfile
import zipfile
import os
from glob import glob
import numpy as np
import cv2

def download_with_progress(link, save_path):
	with open(save_path, 'wb') as f:
		print('Downloading {}'.format(save_path))
		response = requests.get(link, stream=True)
		total_length = response.headers.get('content-length')
		size_KB = int(total_length) / 1024.0 # in KB (Kilo Bytes)
		size_MB = size_KB / 1024.0 # size in MB (Mega Bytes)
		if(total_length is None):
			f.write(response.content)
		else:
			dl = 0
			total_length = int(total_length)

			for data in response.iter_content(chunk_size=4096):
				dl += len(data)
				f.write(data)
				done = (50 * dl // total_length)
				print('\r[{}{}] {:.2f}Mb/{:.2f}Mb'.format('=' * done, ' ' * (50 - done), (dl/1024.0)/1024.0,size_MB), end='')


# This function recursively makes directories.
def makedir(directory):
	directory = "".join(str(x) for x in directory)
	try:
		os.stat(directory)
	except:
		try:
			os.mkdir(directory)
		except:
			subDir = directory.split('/')
			while (subDir[-1] == ''):
				subdir = subdir[:-1]
			newDir = ""
			for x in range(len(subDir)-2):
				newDir += (subDir[x])
				newDir += ('/')
			#print ("Attempting to pass... " + str(newDir))
			directoryFixer(newDir)
			os.mkdir(directory)

# supports:
# ae_photos, apple2orange, summer2winter_yosemite, horse2zebra, monet2photo,
#  cezanne2photo, ukiyoe2photo, vangogh2photo, maps, cityscapes, facades,
#  iphone2dslr_flower, mini, mini_pix2pix.
def download_dataset(data_set='apple2orange', save='datasets/'):
	url = 'https://people.eecs.berkeley.edu/~taesung_park/CycleGAN/datasets/' + data_set + '.zip'
	file = save + data_set + '/' + data_set + '.zip'

	# first set up directories
	if(not os.path.exists(save)): makedir(save)
	if(not os.path.exists(save + data_set + '/')): makedir(save + data_set + '/')

	# download our zip file
	download_with_progress(url, file)
	# extract it 
	zip_ref = zipfile.ZipFile(file, 'r')
	zip_ref.extractall(save + '/')
	zip_ref.close()
	# remove it !
	os.remove(file)
	# DONE !

	# now make list files for our data
	data_path = save + data_set + '/'
	test_a = glob(data_path + 'testA/*.jpg')
	test_b = glob(data_path + 'testB/*.jpg')
	train_a = glob(data_path + 'trainA/*.jpg')
	train_b = glob(data_path + 'trainB/*.jpg')
	print('\nDone!\nMaking list files...')
	# test a
	with open(data_path + 'test_a.lst', 'w') as file:
		for path in test_a:
			path = path.replace('\\', '/')
			file.write(path + '\n')
		file.close()

	# test b
	with open(data_path + 'test_b.lst', 'w') as file:
		for path in test_b:
			path = path.replace('\\', '/')
			file.write(path + '\n')
		file.close()

	# train a
	with open(data_path + 'train_a.lst', 'w') as file:
		for path in train_a:
			path = path.replace('\\', '/')
			file.write(path + '\n')
		file.close()

	# train b
	with open(data_path + 'train_b.lst', 'w') as file:
		for path in train_b:
			path = path.replace('\\', '/')
			file.write(path + '\n')
		file.close()

	print('\nDone')
if __name__ == '__main__':
	
	download_dataset(data_set='horse2zebra')

