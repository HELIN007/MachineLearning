a = [1, 2, 3, 4]
aa = []
b = a[:1]
print b
b.extend(a[2:])
print b
aa.append(b)
print aa