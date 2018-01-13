import enum
from logging import getLogger

from reversi_zero.agent.player import HistoryItem
from reversi_zero.agent.player import ReversiPlayer
from reversi_zero.config import Config
from reversi_zero.env.reversi_env import Player, ReversiEnv
from reversi_zero.lib.bitboard import find_correct_moves
from reversi_zero.lib.model_helpler import load_best_model_weight, reload_newest_next_generation_model_if_changed
from reversi_zero.play_game.EdaxPlayer import *

logger = getLogger(__name__)

GameEvent = enum.Enum("GameEvent", "update ai_move over pass")


class PlayWithHuman:
    def __init__(self, config: Config):
        self.config = config
        self.human_color = None
        self.observers = []
        self.env = ReversiEnv().reset()
        self.model = self._load_model()
        self.ai = None  # type: ReversiPlayer
        self.last_evaluation = None
        self.last_history = None  # type: HistoryItem

    def add_observer(self, observer_func):
        self.observers.append(observer_func)

    def notify_all(self, event):
        for ob_func in self.observers:
            ob_func(event)

    def start_game(self, human_is_black):
        self.human_color = Player.black if human_is_black else Player.white
        self.env = ReversiEnv().reset()
        self.ai = ReversiPlayer(self.config, self.model)
        self.edax_player = EdaxPlayer()
        self.act = None

    def play_next_turn(self):
        self.notify_all(GameEvent.update)

        if self.over:
            self.notify_all(GameEvent.over)
            return

        if self.next_player != self.human_color:
            self.notify_all(GameEvent.ai_move)

    @property
    def over(self):
        return self.env.done

    @property
    def next_player(self):
        return self.env.next_player

    def stone(self, px, py):
        """left top=(0, 0), right bottom=(7,7)"""
        pos = int(py * 8 + px)
        assert 0 <= pos < 64
        bit = 1 << pos
        if self.env.board.black & bit:
            return Player.black
        elif self.env.board.white & bit:
            return Player.white
        return None

    @property
    def number_of_black_and_white(self):
        return self.env.observation.number_of_black_and_white

    def available(self, px, py):
        pos = int(py * 8 + px)
        if pos < 0 or 64 <= pos:
            return False
        own, enemy = self.env.board.black, self.env.board.white
        if self.human_color == Player.white:
            own, enemy = enemy, own
        legal_moves = find_correct_moves(own, enemy)
        return legal_moves & (1 << pos)

    def move(self, px, py, use_edax=False):
        pos = int(py * 8 + px)
        assert 0 <= pos < 64
        if self.next_player != self.human_color:
            return False

        if use_edax:
            logger.debug(f"edax thinking,current act {self.act}...")
            '''
            if self.act == None:
                pos = self.edax_player.action_pos(pos=None, start=True)
            elif self.act == 'pass':
                pos = self.edax_player.action_pos(pos=None, start=False)
            else:
                pos = self.edax_player.action_pos(self.act)
            '''
            own, enemy = self.get_state_of_next_player()
            pos = action = self.edax_player.action(own, enemy)
            logger.debug("edax steped...")
            self.act = 'pass'
            self.env.step(pos)

    def _load_model(self):
        from reversi_zero.agent.model import ReversiModel
        model = ReversiModel(self.config)
        if self.config.play.use_newest_next_generation_model:
            loaded = reload_newest_next_generation_model_if_changed(model) or load_best_model_weight(model)
        else:
            loaded = \
                (model) or reload_newest_next_generation_model_if_changed(model)
        if not loaded:
            raise RuntimeError("No models found!")
        return model

    def move_by_ai(self):
        if self.next_player == self.human_color:
            return False

        own, enemy = self.get_state_of_next_player()
        action = self.ai.action(own, enemy)
        self.env.step(action)
        self.act = action
        self.last_history = self.ai.ask_thought_about(own, enemy)
        self.last_evaluation = self.last_history.values[self.last_history.action]
        logger.debug(f"evaluation by ai={self.last_evaluation}")

    def get_state_of_next_player(self):
        if self.next_player == Player.black:
            own, enemy = self.env.board.black, self.env.board.white
        else:
            own, enemy = self.env.board.white, self.env.board.black
        return own, enemy
