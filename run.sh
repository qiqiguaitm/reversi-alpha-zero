CUDA_VISIBLE_DEVICES='0' nohup ../anaconda3/bin/python src/reversi_zero/run.py self > out.self.`hostname`.0 2>&1 &
CUDA_VISIBLE_DEVICES='1' nohup ../anaconda3/bin/python src/reversi_zero/run.py self > out.self.`hostname`.1 2>&1 &
CUDA_VISIBLE_DEVICES='2' nohup ../anaconda3/bin/python src/reversi_zero/run.py self > out.self.`hostname`.2 2>&1 &
CUDA_VISIBLE_DEVICES='3' nohup ../anaconda3/bin/python src/reversi_zero/run.py self > out.self.`hostname`.3 2>&1 &
#CUDA_VISIBLE_DEVICES='2' nohup ../anaconda3/bin/python src/reversi_zero/run.py opt > out.`hostname`.opt 2>&1 &
#CUDA_VISIBLE_DEVICES='3' nohup ../anaconda3/bin/python src/reversi_zero/run.py eval > out.`hostname`.eval 2>&1 &
 
