"""this is a test"""
def print_lol(the_list,indent=false,level=0):
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,level+1)
		else:
			if indent:
				for each_temp in range(level):
					print("\t",end='')
			print(each_item)


