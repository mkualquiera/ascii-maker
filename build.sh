#!/bin/bash

echo "<!> Building ascii maker..."

echo "<-> Cleaning up..."

set -e

rm -rf bin
rm -rf obj

find src -name "*.h" -type f -delete

echo "<-> Making headers..."
for file in $(find src -name "*.[ch]")
do
  makeheaders $file
  echo "<!> Headers for" $file "made"
done

echo "<-> Adding header guards..."
for file in $(find src -name "*.[h]")
do
  fbname=$(basename "$file" .h)
  upper=${fbname^^}
  echo -e "#ifndef" "$upper" "\n""#define" "$upper" "\n" "$(<$file)" "\n""#endif" > $file
  echo "<!> Headers guards for" $file "made"
done

cp include/* src/

mkdir bin
mkdir obj

echo "<-> Building source files"

for file in $(find src -name "*.[c]")
do
  echo "<!> Building $file ..."
  if [[ $1 == "release" ]]
  then
    gcc -c -Wall -fopenmp -march=native -O3 -g0 -lm $file
  else
    gcc -c -Wall -fopenmp -march=native -Og -g -lm $file
  fi
done

mv *.o obj/

echo "<-> Compiling executable"

if [[ $1 == "release" ]]
then
  gcc -march=native -fopenmp -O3 -g0 -lm -o bin/asciimaker obj/*.o
else
  gcc -march=native -fopenmp -Og -g -lm -o bin/asciimaker obj/*.o
fi

echo "<-> Done!"

chmod +x bin/asciimaker
./bin/asciimaker
