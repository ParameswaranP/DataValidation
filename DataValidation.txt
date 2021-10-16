@echo off

echo "-------------- Classes Graph -------------"

python classes_count_graph.py

echo "----------- classes seperate ------------"

pause

python LT_Full_Classes_Seperate.py

echo "------------- Time Split ------------"

pause

cd ./OCR

python Time_Based_Split_HeatMap.py

echo " "

echo "x-x-x-x-x-x-x-x-x-x-  validation Complated  -x-x-x-x-x-x-x-x-x-x" 

pause