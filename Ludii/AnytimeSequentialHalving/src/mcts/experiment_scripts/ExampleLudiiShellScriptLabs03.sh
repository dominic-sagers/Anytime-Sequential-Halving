trap '' HUP		# allow us to disconnect the terminal

cd MicroRTS-Py-MultiMaps/experiments
nohup java -jar <jar fiel name> --game "Clobber.lud" -- some other things > /data/dsoemers/Train_MicroRTS_MultipleMaps-NoWANDB.out 2> /data/dsoemers/Train_MicroRTS_MultipleMaps-NoWANDB.err &
nohup java -jar <jar fiel name> --game "Clobber.lud" -- some other things > /data/dsoemers/Train_MicroRTS_MultipleMaps-NoWANDB.out 2> /data/dsoemers/Train_MicroRTS_MultipleMaps-NoWANDB.err &
nohup java -jar <jar fiel name> --game "Clobber.lud" -- some other things > /data/dsoemers/Train_MicroRTS_MultipleMaps-NoWANDB.out 2> /data/dsoemers/Train_MicroRTS_MultipleMaps-NoWANDB.err &
nohup java -jar <jar fiel name> --game "Clobber.lud" -- some other things > /data/dsoemers/Train_MicroRTS_MultipleMaps-NoWANDB.out 2> /data/dsoemers/Train_MicroRTS_MultipleMaps-NoWANDB.err &




java -jar ... --game-name "Clobber.lud" --game-options "Rows/7" "Columns/7" --agents "UCT" "SHUCT"

//data//I6255473//

java -jar AgentEval.jar --game "Clobber.lud" --game-options "Rows/7" "Columns/7" --agents "UCT" "SHUCTAnyTime" --out-dir "//data//I6255473//" --thinking-time 1 --num-games 1 --anytime-mode true --anytime-budget 1000 --output-alpha-rank-data --output-raw-results

Clobber 7x7 anytime vs SH 100 games:
nohup java -jar AgentEval.jar --game "Clobber.lud" --game-options "Rows/7" "Columns/7" --agents "SHUCT" "SHUCTAnyTime" --out-dir "//data//I6255473//anytimeSH_baseSH//1000" --thinking-time 1 --num-games 100 --anytime-mode true --anytime-budget 1000 --output-alpha-rank-data --output-raw-results > //data//I6255473//anytimeSH_baseSH//1000.out 2> //data//I6255473//anytimeSH_baseSH//1000.err &
nohup java -jar AgentEval.jar --game "Clobber.lud" --game-options "Rows/7" "Columns/7" --agents "SHUCT" "SHUCTAnyTime" --out-dir "//data//I6255473//anytimeSH_baseSH//5000" --thinking-time 5 --num-games 100 --anytime-mode true --anytime-budget 5000 --output-alpha-rank-data --output-raw-results > //data//I6255473//anytimeSH_baseSH//5000.out 2> //data//I6255473//anytimeSH_baseSH//5000.err &
nohup java -jar AgentEval.jar --game "Clobber.lud" --game-options "Rows/7" "Columns/7" --agents "SHUCT" "SHUCTAnyTime" --out-dir "//data//I6255473//anytimeSH_baseSH//10000" --thinking-time 10 --num-games 100 --anytime-mode true --anytime-budget 10000 --output-alpha-rank-data --output-raw-results > //data//I6255473//anytimeSH_baseSH//10000.out 2> //data//I6255473//anytimeSH_baseSH//10000.err &
nohup java -jar AgentEval.jar --game "Clobber.lud" --game-options "Rows/7" "Columns/7" --agents "SHUCT" "SHUCTAnyTime" --out-dir "//data//I6255473//anytimeSH_baseSH//50000" --thinking-time 50 --num-games 100 --anytime-mode true --anytime-budget 50000 --output-alpha-rank-data --output-raw-results > //data//I6255473//anytimeSH_baseSH//50000.out 2> //data//I6255473//anytimeSH_baseSH//50000.err &
nohup java -jar AgentEval.jar --game "Clobber.lud" --game-options "Rows/7" "Columns/7" --agents "SHUCT" "SHUCTAnyTime" --out-dir "//data//I6255473//anytimeSH_baseSH//100000" --thinking-time 100 --num-games 100 --anytime-mode true --anytime-budget 100000 --output-alpha-rank-data --output-raw-results > //data//I6255473//anytimeSH_baseSH//100000.out 2> //data//I6255473//anytimeSH_baseSH//100000.err &
nohup java -jar AgentEval.jar --game "Clobber.lud" --game-options "Rows/7" "Columns/7" --agents "SHUCT" "SHUCTAnyTime" --out-dir "//data//I6255473//anytimeSH_baseSH//150000" --thinking-time 150 --num-games 100 --anytime-mode true --anytime-budget 150000 --output-alpha-rank-data --output-raw-results > //data//I6255473//anytimeSH_baseSH//150000.out 2> //data//I6255473//anytimeSH_baseSH//150000.err &





java -jar AgentEval.jar --game "Clobber.lud" --game-options "Rows/7" "Columns/7" --agents "UCT" "SHUCTAnyTime" --out-dir "C://Users//domin//Documents//UM//Thesis//Code//Sequential-Halving-With-Time-Constraints-In-Ludii//Ludii//LudiiExampleAI-master//src//mcts" --thinking-time 1 --num-games 1 --anytime-mode true --anytime-budget 1000 --output-alpha-rank-data --output-raw-results


java -jar AgentEval.jar --game "Clobber.lud" --game-options "Rows/7" "Columns/7" --agents "SHUCT" "UCT" --out-dir "//data//I6255473//base_SH_UCT//1000" --iterationLimit 1000 --num-games 100 --anytime-mode true --sh-budget 1000 --output-alpha-rank-data --output-raw-results > //data//I6255473//base_SH_UCT//1000.out 2> //data//I6255473//base_SH_UCT//1000.err &