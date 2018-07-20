a = [1,2]

a = 1


try:
	a[0]
	islist = 1
except: 
	islist = 0


if islist:
	print "Es lita"
else:
	print "no es lista"
