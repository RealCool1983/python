



sStr1 = '11111=12,34, 5'
sStr2 = sStr1[1:4]

nPosx = sStr1.index("=")
nPosy = sStr1.index(",")
print("sStr1 = ", sStr1)
print("sStr2 = ", sStr2)
print("nPosx = ", nPosx)
print("nPosy = ", nPosy)
sStr3 = sStr1[nPosx:nPosy]
print("sStr3 = ", sStr3)
