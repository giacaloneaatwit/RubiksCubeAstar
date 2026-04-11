from probables import CountingBloomFilter as cbf

bf = cbf(est_elements=100, false_positive_rate=0.0001)

bf.add("hello")

r = bf.check("hello")

print(str(r))

bf.remove("hello")

print(bf.check("hello"))