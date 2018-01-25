import subprocess
import _thread
import time
import os
import shlex
import json
import copy
import sys

PROJ_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
class EdaxPlayer(object):
    def __init__(self, engine_path=os.path.join(PROJ_DIR,'edax/4.3/bin/lEdax'), time_per_move=1,
                 search_depth=5,debug=False):
        # default values for settings
        self.settings = {
            "enginepath": engine_path,
            "time_per_move": time_per_move,
            "search_depth": search_depth,
        }
        self.std_start_fen = "8/8/8/3pP3/3Pp3/8/8/8 b - - 0 1"
        self.debug = debug
        self.engine_init()  # may fail if first run and path not set

    def dprint(self, *args):
        if not self.debug:
            return
        for i in args:
            print(i, end=' ')
        print()

    def command(self, cmd):
        try:
            self.p.stdin.write(bytes(cmd, "UTF-8"))
            self.p.stdin.flush()
        except AttributeError:
            self.dprint("AttributeError")
        except IOError:
            self.dprint("ioerror")

    def bitboard_to_fen(self, black, white):
        line = ''
        for i in range(8):
            bit_cnt = 0
            for j in range(8):
                if black & 1:
                    if bit_cnt > 0:
                        line = line + str(bit_cnt)
                        bit_cnt = 0
                    line = line + 'p'
                elif white & 1:
                    if bit_cnt > 0:
                        line = line + str(bit_cnt)
                        bit_cnt = 0
                    line = line + 'P'
                else:
                    bit_cnt += 1
                black >>= 1
                white >>= 1
            if bit_cnt > 0:
                line = line + str(bit_cnt)
            line = line + '/'
        line = line[:-1]
        line = line + ' b - - 0 1'
        return line

    def action(self, black, white):
        std_start_fen = self.bitboard_to_fen(black=black, white=white)
        self.command("setboard " + std_start_fen + "\n")
        self.command("st " + str(self.settings["time_per_move"]) + "\n")  # time per move in seconds
        self.command("sd " + str(self.settings["search_depth"]) + "\n")
        self.command("go\n")
        self.mv = ""
        mv = self.get_move()
        pos = (7-mv[1]) * 8 + mv[0]
        return pos

    def action_pos(self, pos=None, start=False):
        if pos != None:
            y, x = 7 - pos // 8, pos % 8
        else:
            x, y = None, None
        mv = self.action_xy(x, y, start)
        pos = (7 - mv[1]) * 8 + mv[0]
        return pos

    def action_xy(self, x=None, y=None, start=False):
        if x == None and y == None and start == True:
            mv = self.start()
        elif x == None and y == None and start == False:
            mv = self.oppo_pass_on_move()
        else:
            assert x != None and y != None
            assert x in range(8) and y in range(8)
            mv = self.oppo_move(x, y)
        return mv

    def start(self):
        self.command("go\n")
        # Computers move
        self.mv = ""
        return self.get_move()

    def oppo_move(self, x, y):
        # start engine if needed
        if not self.engine_active:
            self.engine_init()
            if not self.engine_active:
                self.dprint("Error starting engine")
                return

        # convert move from board co-ordinates to othello format (e.g. 3, 5 goes to 'd6')
        move = self.coord_to_conv(x, y)

        # engine OK - send move

        str1 = "usermove " + move + "\n"
        # send human move to engine
        self.command(str1)
        # Computers move
        self.mv = ""
        return self.get_move()

    def oppo_pass_on_move(self):
        str1 = "usermove @@@@\n"
        self.command(str1)
        self.mv = ""
        return self.get_move()

    def get_move(self):
        # Check for move from engine
        for l in self.op:
            l = l.strip()
            if l.startswith('move'):
                self.mv = l[7:]
                break
        self.op = []
        # if no move from engine wait 1 second and try again
        for i in range(30):
            if self.mv == "":
                time.sleep(1)
                self.dprint("elapsed ", i, " secs")
                for l in self.op:
                    l = l.strip()
                    if l.startswith('move'):
                        self.mv = l[7:]
                        break
                self.op = []
            else:
                break
        if self.mv == "":
            raise Exception('EngineException', 'NoOutput')

        self.dprint("move:", self.mv)
        mv = self.mv

        # pass
        if mv == "@@":
            return -1

        # convert move to board coordinates (e.g. "d6" goes to 3, 5)
        x, y = self.conv_to_coord(mv)
        return x, y

    def conv_to_pos(self, mv):
        x, y = self.conv_to_coord(mv)
        return y * 8 + x

    def pos_to_conv(self, pos):
        x, y = pos // 8, pos % 8
        return self.coord_to_conv(x, y)

    def conv_to_coord(self, mv):
        letter = mv[0]
        num = mv[1]
        x = "abcdefgh".index(letter)
        y = int(num) - 1
        return x, y

    def coord_to_conv(self, x, y):
        l = "abcdefgh"[x]
        n = y + 1
        mv = l + str(n)
        return mv

    def engine_init(self):
        self.dprint("Initialising Engine")
        self.engine_active = False
        path = self.settings["enginepath"]
        if not os.path.exists(path):
            self.dprint("Error enginepath does not exist")
            return
        self.dprint("engine path", path)

        arglist = [path, "-xboard", "-n", "1"]
        optionsfile = os.path.join(self.settings["enginepath"], "edax.ini")
        if os.path.exists(optionsfile):
            arglist.extend(["option-file", optionsfile])
        self.dprint("subprocess args:", arglist)

        # engine working directory containing the executable
        engine_wdir = os.path.dirname(path)
        self.dprint("engine working directory", engine_wdir)

        try:
            p = subprocess.Popen(arglist, stdin=subprocess.PIPE, stdout=subprocess.PIPE, cwd=engine_wdir)
            self.p = p
        except OSError:
            self.dprint("Error starting engine - check path/permissions")
            # tkMessageBox.showinfo("OthelloTk Error", "Error starting engine",
            #                       detail="Check path/permissions")
            return

        # check process is running
        i = 0
        while (p.poll() is not None):
            i += 1
            if i > 40:
                self.dprint("unable to start engine process")
                return False
            time.sleep(0.25)

            # start thread to read stdout
        self.op = []
        self.soutt = _thread.start_new_thread(self.read_stdout, ())
        # self.command('xboard\n')
        self.command('protover 2\n')

        # Engine should respond to "protover 2" with "feature" command
        response_ok = False
        i = 0
        while True:
            for l in self.op:
                if l.startswith("feature "):
                    response_ok = True
                    f = shlex.split(l)
                    features = f[1:]
                    for f in features:
                        self.dprint(f)
            self.op = []
            if response_ok:
                break
            i += 1
            if i > 60:
                self.dprint("Error - no response from engine")
                return
            time.sleep(0.25)

        self.command('variant reversi\n')
        self.command("setboard " + self.std_start_fen + "\n")
        self.command("st " + str(self.settings["time_per_move"]) + "\n")  # time per move in seconds
        self.command("sd " + str(self.settings["search_depth"]) + "\n")
        self.engine_active = True

    def command(self, cmd):
        try:
            self.dprint(cmd.strip())
            self.p.stdin.write(bytes(cmd, "UTF-8"))
            self.p.stdin.flush()
        except AttributeError:
            self.dprint("AttributeError")
        except IOError:
            self.dprint("ioerror")

    def read_stdout(self):
        while True:
            try:
                self.p.stdout.flush()
                line = self.p.stdout.readline()
                line = line.decode("UTF-8")
                line = line.strip()
                if line == '':
                    self.dprint("eof reached in read_stdout")
                    break
                self.op.append(line)
            except Exception as e:
                self.dprint("subprocess error in read_stdout:", e)

    def close(self):
        self.p.kill()
        self.engine_active = False


def main():
    edaxPlayer = EdaxPlayer()
    while True:
        mv = input()
        if mv == 'white':
            act = edaxPlayer.action_xy(x=None, y=None, start=True)
        elif mv == 'pass':
            act = edaxPlayer.action_xy(x=None, y=None, start=False)
        else:
            x, y = edaxPlayer.conv_to_coord(mv)
            act = edaxPlayer.action_xy(x, y, start=False)
        print(act)
        print(edaxPlayer.coord_to_conv(*act))
        time.sleep(3)


if __name__ == "__main__":
    main()
