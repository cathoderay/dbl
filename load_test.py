import dbl

for i in range(1000001):
    dbl.set(str(i), "word" + str(i))

# duplicates to test compaction
for j in range(1000000):
    dbl.set("0","word" + str(i))
