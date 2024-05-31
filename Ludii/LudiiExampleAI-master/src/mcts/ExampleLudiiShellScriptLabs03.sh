trap '' HUP		# allow us to disconnect the terminal

cd MicroRTS-Py-MultiMaps/experiments
nohup java -jar <jar fiel name> --game "Clobber.lud" -- some other things > /data/dsoemers/Train_MicroRTS_MultipleMaps-NoWANDB.out 2> /data/dsoemers/Train_MicroRTS_MultipleMaps-NoWANDB.err &
nohup java -jar <jar fiel name> --game "Clobber.lud" -- some other things > /data/dsoemers/Train_MicroRTS_MultipleMaps-NoWANDB.out 2> /data/dsoemers/Train_MicroRTS_MultipleMaps-NoWANDB.err &
nohup java -jar <jar fiel name> --game "Clobber.lud" -- some other things > /data/dsoemers/Train_MicroRTS_MultipleMaps-NoWANDB.out 2> /data/dsoemers/Train_MicroRTS_MultipleMaps-NoWANDB.err &
nohup java -jar <jar fiel name> --game "Clobber.lud" -- some other things > /data/dsoemers/Train_MicroRTS_MultipleMaps-NoWANDB.out 2> /data/dsoemers/Train_MicroRTS_MultipleMaps-NoWANDB.err &




java -jar ... --game-name "Clobber.lud" --game-options "Rows/7" "Columns/7" --agents "UCT" "SHUCT"

java -jar AgentEval.jar --game "Clobber.lud" --game-options "Rows/7" "Columns/7" --agents "UCT" "SHUCTAnyTime" --out-dir "C:\Users\domin\Documents\UM\Thesis\Code\Sequential-Halving-With-Time-Constraints-In-Ludii\Ludii\LudiiExampleAI-master\src\mcts\out.txt" --thinking-time 1 --num-games 2 --anytime-mode true --anytime-budget 1000 