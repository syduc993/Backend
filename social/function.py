import zipfile
import pandas as pd
import os
from pathlib import Path
import shutil
import warnings
import random
from django.core.files.storage import FileSystemStorage
import uuid

def Tach_file_tang_truong(file,folder):
	warnings.filterwarnings("ignore")
	pd.set_option('display.float_format', '{:.2f}'.format)

	df_on = pd.read_excel("/Backend/social/files_exel/"+file)
	cols = ['Mã model','Tên model','Giá bán khuyến mãi (SP cơ sở)','GrowNumber','Thời gian lên PO','Thời gian lên PO đến ngày','Thời gian áp dụng chia hàng','Thời gian kết thúc chia hàng','Thời gian áp dụng bán hàng','Thời gian kết thúc bán hàng','Siêu Thị Áp dụng']
	df_on.columns = cols

	lst_typestore = [1,2,3,4,5,18]
	lst_store = df_on['Siêu Thị Áp dụng'].unique().tolist()
	j = 1

	for store in lst_store:

		lst_product =  df_on[df_on['Siêu Thị Áp dụng']==store]['Mã model'].unique().tolist()
		k = len(lst_product)
		flag = 1
		while k > 0:
			df_Form = pd.read_excel("/Backend/social/form/Form.xlsx")
			flag_product = lst_product[(flag-1)*80:flag*80]
			for product in flag_product:
				for i in lst_typestore:

					growNumber = round(float(df_on[(df_on['Siêu Thị Áp dụng']==store)&(df_on['Mã model']==product)]['GrowNumber']),2)
					df_Form.loc[len(df_Form)] = {'Mã phân loại siêu thị': i, 'Mã model': product,'Số lần tăng trưởng sức bán (số thập phân, phần thập phân 2 chữ số, > 0)':growNumber}
			df_Form['Giá bán khuyến mãi (sản phẩm cơ sở)'] = 2000
			df_Form['Số lần tăng trưởng tồn min (số thập phân, phần thập phân 2 chữ số, > 0)'] = 1

	        ### File này để lưu thông tin tăng trưởng
			file_name = str(store) + ' - GROWTH-20230529-207158-1.' + str(flag) + '.xlsx'
			my_file = Path(folder+file_name)

			df_Form.to_excel(my_file,index=False)

			k = k - 80
			flag = flag + 1
		j = j + 1

def Extract_growth_data_product(file,folder):
	warnings.filterwarnings("ignore")
	pd.set_option('display.float_format', '{:.2f}'.format)

	df_off = pd.read_excel("/Backend/social/files_exel/"+file)
	cols = ['Mã model','Tên model','Giá bán khuyến mãi (SP cơ sở)','GrowNumber','Thời gian lên PO','Thời gian lên PO đến ngày','Thời gian áp dụng chia hàng','Thời gian kết thúc chia hàng','Thời gian áp dụng bán hàng','Thời gian kết thúc bán hàng','Siêu Thị Áp dụng']
	df_off.columns = cols
	lst_typestore = [1,2,3,4,5,18]
	lst_product = df_off['Mã model'].unique().tolist()
	k = 1

	### Chạy vào từng sản phẩm
	for product in lst_product:
		lst_number = df_off[(df_off['Mã model']==product)]['GrowNumber'].unique().tolist()
		name_product =''.join(df_off[(df_off['Mã model']==product)]['Tên model'].unique().tolist())
		lst_number = sorted(lst_number)
	    ### Chạy vào từng hệ số tăng trưởng
			
		for growNumber in lst_number:
			df_Form = pd.read_excel("/Backend/social/form/Form.xlsx")
			lst_store = df_off[(df_off['Mã model']==product)&(df_off['GrowNumber']==growNumber)]['Siêu Thị Áp dụng'].tolist()
			for i in lst_typestore:
				df_Form.loc[len(df_Form)] = {'Mã phân loại siêu thị': i, 'Mã model': product,'Số lần tăng trưởng sức bán (số thập phân, phần thập phân 2 chữ số, > 0)':growNumber}
			df_Form['Giá bán khuyến mãi (sản phẩm cơ sở)'] = 2000
			df_Form['Số lần tăng trưởng tồn min (số thập phân, phần thập phân 2 chữ số, > 0)'] = 1

	        ### File này để lưu thông tin tăng trưởng
			file_name = str(k) + ' - GROWTH-20230525-207158-'+str(name_product) + '-' + str(growNumber) + '-1.1.xlsx'
			my_file = Path(folder + file_name)
			df_Form.to_excel(my_file,index=False)

	        ### File này để lưu thông tin MST
			file_name2 = str(k) +"-"+ str(name_product) + ' - MST.xlsx'
			my_file2 = Path(folder + file_name2)
			df_stores = pd.DataFrame({'Mã siêu thị': lst_store})
			df_stores.to_excel(my_file2,index=False)

	        ### J lưu thông tin version, k lưu thông tin số thứ tự trước đầu file
			#j = j + 1
			k = k + 1


def get_calendar(file,folder):

	warnings.filterwarnings("ignore")
	pd.set_option('display.float_format', '{:.2f}'.format)

	### Đọc dữ liệu NotifyCalendar
	df_NotifyCalendar = pd.read_excel("/Backend/social/files_exel/"+file)
	df_NotifyCalendar['Mã sản phẩm'] = df_NotifyCalendar['Sản phẩm'].str.extract('(^[0-9]{0,13})')
	df_NotifyCalendar.rename(columns={'Lịch theo thứ / tuần':'Lịch về hàng'},inplace=True)
	df_NotifyCalendar.rename(columns={'Khu vực áp dụng':'Mã KV mua hàng'},inplace=True)

	df_NotifyCalendar = df_NotifyCalendar[['Mã sản phẩm','Mã KV mua hàng','Lịch về hàng']]
	df_NotifyCalendar['Mã KV mua hàng'] = df_NotifyCalendar['Mã KV mua hàng'].str.split(",")
	df_NotifyCalendar = df_NotifyCalendar.explode('Mã KV mua hàng')

	df_NotifyCalendar['Mã KV mua hàng'] = df_NotifyCalendar['Mã KV mua hàng'].astype(str)
	df_NotifyCalendar['Mã sản phẩm'] = df_NotifyCalendar['Mã sản phẩm'].astype(str)

	file_name = 'Calendar.xlsx'
	my_file = Path(folder+file_name)

	df_NotifyCalendar.to_excel(my_file,index=False)

def sort_packing(file,folder):

	warnings.filterwarnings("ignore")
	pd.set_option('display.float_format', '{:.2f}'.format)

	df_KV  = pd.read_excel("/Backend/social/files_exel/"+file,sheet_name='Sheet1')
	df_ST = pd.read_excel("Backend/git /files_exel/"+file,sheet_name='Sheet2')
	df_ST = df_ST[['Mã SP','Mã ST','Mã KV','Tổng SL bán','Quy cách mua']]

	df_ST['Số lượng rải custom'] = 0.0
	df = pd.DataFrame()
	df_ST.sort_values(by=['Tổng SL bán'],ascending=False,inplace=True)
	lst_area = df_KV['Ma KV'].unique().tolist()
	for area in lst_area:
		lst_product =  df_KV[df_KV['Ma KV']==area]['Ma SP'].unique().tolist()
		for product in lst_product:
			var_SL = round(float(df_KV[(df_KV['Ma KV']==area)&(df_KV['Ma SP']==product)]['SL']),2)
			df1 = df_ST[(df_ST['Mã KV']==area)&(df_ST['Mã SP']==product)]
			index = 0
			while var_SL > 0:
				
				if var_SL < df1['Quy cách mua'].values[index]:
					df1['Số lượng rải custom'].values[index] = var_SL
					var_SL = round(var_SL - df1['Số lượng rải custom'].values[index])
				else:
					df1['Số lượng rải custom'].values[index] = df1['Số lượng rải custom'].values[index] + df1['Quy cách mua'].values[index]
					var_SL = round(var_SL - df1['Quy cách mua'].values[index],2)
				index = index + 1
				if index >= len(df1):
					index = 0
			df = pd.concat([df, df1], ignore_index=True, sort=False)

	file_name = 'Data.xlsx'
	my_file = Path(folder+file_name)
	df.to_excel(my_file,index=False)