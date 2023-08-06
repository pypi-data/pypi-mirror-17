"""this is the nester.py module and it provide one function called print_lol()
which prints lists that may or may not include nested listes,secord parameter is level insert tab"""
def print_lol(the_list, level=0):
	""" 这个函数取一个位置参数，名为“the_list”这可以是任何python列表（也可以包含嵌套列表）所指定列表中的每个数据项会递归的输入到屏幕上，个数据各占用一行"""
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,level+1)
		else:
			for  tab_stop in range(level):
				print("\t",end='')
			print(each_item)