CUDA_VISIBLE_DEVICES='0' nohup ~/alpha/anaconda3/bin/python src/reversi_zero/run.py self > out.self.0 2>&1 &
CUDA_VISIBLE_DEVICES='1' nohup ~/alpha/anaconda3/bin/python src/reversi_zero/run.py self > out.self.1 2>&1 &
CUDA_VISIBLE_DEVICES='2' nohup ~/alpha/anaconda3/bin/python src/reversi_zero/run.py opt > out.opt 2>&1 &
CUDA_VISIBLE_DEVICES='3' nohup ~/alpha/anaconda3/bin/python src/reversi_zero/run.py eval > out.eval 2>&1 &
 
