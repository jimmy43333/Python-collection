def Bug(a, r = None):	
	if r is None :
		r = [];
	r.append(a)
	print(r)

Bug('a')
Bug('b')
r = ["q"]
Bug('c',r)


def edit(words,func):
	return [func(word) for word in words]

words = ["jimmy","amy","jeff"]
change = edit(words,lambda word : word.capitalize())
print(change)
