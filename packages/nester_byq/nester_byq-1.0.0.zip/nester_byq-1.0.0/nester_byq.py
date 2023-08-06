'''
这是nester.py模块，里面包含 print_lol 函数，
这个函数的作用是打印列表，其中有可能含有嵌套列表
'''
def print_lol(the_list):
	for each_tv in the_list:
		if isinstance(each_tv,list):
			print_lol(each_tv)
		else:
			print(each_tv)

tvshow = ["langyabang",2015,43,["huge",["liutao","wangkai","feiliu"]]]
print_lol(tvshow)