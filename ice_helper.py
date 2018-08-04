import cv2
import numpy as np
from glob import glob
import os

def show(mat,tag='image'):
	try:
		cv2.imshow(tag,mat)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
	except Exception as e:
		print('Error occured : {}'.format(e))

# will split an image in two
def crop(input_img):
	#print('cropping the guy')
	input_img = cv2.resize(input_img, (512, 1024))

	#show(input_img)
	shape_in = np.shape(input_img)
	#print(shape_in)
	top = input_img[ 0:512, 0:512, :]
	bot = input_img[512:1024, 0:512, :]
	#show(top)
	#show(bot)

	return top, bot


def create_splits(dir_='I:/Rahnemoonfar group/ICEData/train_test_split/train/'):
	# first setup our files
	save = dir_ + 'GAN_tiles/'
	lab_files = glob(dir_ + 'label_/*.png')
	img_files = ['' + x.replace('label_', 'img_') for x in lab_files]

	#print(lab_files[0])
	#print(img_files[0])
	num_files = len(lab_files)
	for idx in range(num_files):
		# open the two
		print('\r{}/{}'.format(idx,num_files),end='')
		img_files[idx] = img_files[idx].replace('\\', '/')
		lab_files[idx] = lab_files[idx].replace('\\', '/')

		img_ = cv2.imread(img_files[idx])
		lab_ = cv2.imread(lab_files[idx])

		img_ = cv2.resize(img_, (512, 1024))
		lab_ = cv2.resize(lab_, (512, 1024))

		#img_top, img_bot = crop(img_)
		image_save = img_files[idx].split('/')[-1].replace('.png','')
		cv2.imwrite('datasets/ice/normal/' + 'trainA/' + image_save + '.png', img_)
		#cv2.imwrite(save + 'testA/' + image_save + '_0.png', img_top)
		#cv2.imwrite(save + 'testA/' + image_save + '_1.png', img_bot)

		#lab_top, lab_bot = crop(lab_)
		cv2.imwrite('datasets/ice/normal/' + 'trainB/' + image_save + '.png', lab_)
		#cv2.imwrite(save + 'testB/' + image_save + '_0.png', lab_top)
		#cv2.imwrite(save + 'testB/' + image_save + '_1.png', lab_bot)
		#input('->')

	print('\nDone!')
if __name__ == '__main__':
	create_splits()