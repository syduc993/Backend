import zipfile
import pandas as pd
import os
from pathlib import Path
import shutil
import warnings
import random
from django.core.files.storage import FileSystemStorage
import uuid

def Tach_file_tang_truong(aa,bb):
	warnings.filterwarnings("ignore")
	pd.set_option('display.float_format', '{:.2f}'.format)

	df_on = pd.read_excel("try_Django/social/files_exel/"+aa)
	cols = ['Mã model','Tên model','Giá bán khuyến mãi (SP cơ sở)','GrowNumber','Thời gian lên PO','Thời gian lên PO đến ngày','Thời gian áp dụng chia hàng','Thời gian kết thúc chia hàng','Thời gian áp dụng bán hàng','Thời gian kết thúc bán hàng','Siêu Thị Áp dụng']
	df_on.columns = cols
	df_on.head(2)

	lst_typestore = [1,2,3,4,5,18]
	lst_store = df_on['Siêu Thị Áp dụng'].unique().tolist()
	j = 1

	for store in lst_store:
	    #df_Form = pd.read_excel("D:/Thảo Ngân/Form.xlsx")
	    lst_product =  df_on[df_on['Siêu Thị Áp dụng']==store]['Mã model'].unique().tolist()
	    k = len(lst_product)
	    flag = 1
	    while k > 0:
	        df_Form = pd.read_excel("try_Django/social/files_exel/Form.xlsx")
	        flag_product = lst_product[(flag-1)*80:flag*80]
	        for product in flag_product:
	            for i in lst_typestore:
	            #print(store,product)
	                growNumber = round(float(df_on[(df_on['Siêu Thị Áp dụng']==store)&(df_on['Mã model']==product)]['GrowNumber']),2)
	                df_Form.loc[len(df_Form)] = {'Mã phân loại siêu thị': i, 'Mã model': product,'Số lần tăng trưởng sức bán (số thập phân, phần thập phân 2 chữ số, > 0)':growNumber}
	        df_Form['Giá bán khuyến mãi (sản phẩm cơ sở)'] = 2000
	        df_Form['Số lần tăng trưởng tồn min (số thập phân, phần thập phân 2 chữ số, > 0)'] = 1

	        ### File này để lưu thông tin tăng trưởng
	        file_name = str(store) + ' - GROWTH-20230529-207158-1.' + str(flag) + '.xlsx'
	        my_file = Path(bb+file_name)

	        df_Form.to_excel(my_file,index=False)

	        k = k - 80
	        flag = flag + 1

	    j = j + 1
	df_Form.head(2)