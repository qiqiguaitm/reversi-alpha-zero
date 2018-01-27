CUDA_VISIBLE_DEVICES='0' nohup ../anaconda3/bin/python src/reversi_zero/run.py self > out.self.`hostname`.0 2>&1 &
sleep 2
CUDA_VISIBLE_DEVICES='1' nohup ../anaconda3/bin/python src/reversi_zero/run.py self > out.self.`hostname`.1 2>&1 &
sleep 2
CUDA_VISIBLE_DEVICES='2' nohup ../anaconda3/bin/python src/reversi_zero/run.py self > out.self.`hostname`.2 2>&1 &
sleep 2
CUDA_VISIBLE_DEVICES='3' nohup ../anaconda3/bin/python src/reversi_zero/run.py self > out.self.`hostname`.3 2>&1 &
sleep 2

CUDA_VISIBLE_DEVICES='0' nohup ../anaconda3/bin/python src/reversi_zero/run.py self > out.self.`hostname`.4 2>&1 &
sleep 2
CUDA_VISIBLE_DEVICES='1' nohup ../anaconda3/bin/python src/reversi_zero/run.py self > out.self.`hostname`.5 2>&1 &
sleep 2
CUDA_VISIBLE_DEVICES='2' nohup ../anaconda3/bin/python src/reversi_zero/run.py self > out.self.`hostname`.6 2>&1 &
sleep 2
CUDA_VISIBLE_DEVICES='3' nohup ../anaconda3/bin/python src/reversi_zero/run.py self > out.self.`hostname`.7 2>&1 &
sleep 2

CUDA_VISIBLE_DEVICES='0' nohup ../anaconda3/bin/python src/reversi_zero/run.py self > out.self.`hostname`.8 2>&1 &
sleep 2
CUDA_VISIBLE_DEVICES='1' nohup ../anaconda3/bin/python src/reversi_zero/run.py self > out.self.`hostname`.9 2>&1 &
sleep 2
CUDA_VISIBLE_DEVICES='2' nohup ../anaconda3/bin/python src/reversi_zero/run.py self > out.self.`hostname`.10 2>&1 &
sleep 2
CUDA_VISIBLE_DEVICES='3' nohup ../anaconda3/bin/python src/reversi_zero/run.py self > out.self.`hostname`.11 2>&1 &
sleep 2


#nohup ../anaconda3/bin/python -u  src/reversi_zero/run.py opt > out.opt.`hostname` 2>&1 &
#CUDA_VISIBLE_DEVICES='3' nohup ../anaconda3/bin/python -u src/reversi_zero/run.py eval > out.eval.`hostname` 2>&1 &