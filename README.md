# 2022_CS4386_assignment1
 CityU CS4386 Assignment 1 (Board Game With AI AlphaBeta Pruning)
2022.3.20
----------------------------------
cmd run:
cd java
javac AIPlayer.java
mkdir -force com
mv -force AIPlayer.class com
mv -force ABNegamaxResult.class com
jar cvf AIPlayer.jar com
cd..

python3 game.py Human JAVA 1
----------------------------------
