#!/usr/bin/env python3

v = "unsigned char colors[] = {"

for i in range(16):
    color = input()
    r = int(color[0:2],16)
    g = int(color[2:4],16)
    b = int(color[4:6],16)
    v += "{},{},{},".format(r,g,b)

v = v[:-1] + "};"

print(v)
