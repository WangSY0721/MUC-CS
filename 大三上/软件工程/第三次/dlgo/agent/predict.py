# tag::dl_agent_imports[]
import numpy as np

from dlgo.agent.base import Agent
from dlgo.agent.helpers import is_point_an_eye
from dlgo import encoders
from dlgo import goboard
from dlgo import kerasutil

# end::dl_agent_imports[]
__all__ = [
    'DeepLearningAgent',
    'load_prediction_agent',
]


# tag::dl_agent_init[]
class DeepLearningAgent(Agent):
    def __init__(self, model, encoder):
        Agent.__init__(self)
        self.model = model
        self.encoder = encoder

    # end::dl_agent_init[]

    # tag::dl_agent_predict[]
    def predict(self, game_state):
        encoded_state = self.encoder.encode(game_state)
        input_tensor = np.array([encoded_state])
        return self.model.predict(input_tensor)[0]

    def select_move(self, game_state):
        num_moves = self.encoder.board_width * self.encoder.board_height
        move_probs = self.predict(game_state)
        # end::dl_agent_predict[]

        # tag::dl_agent_probabilities[]
        move_probs = move_probs ** 3  # <1>
        eps = 1e-6
        move_probs = np.clip(move_probs, eps, 1 - eps)
        move_probs = move_probs / np.sum(move_probs)
        # tag::dl_agent_candidates[]
        candidates = np.arange(num_moves)
        ranked_moves = np.random.choice(
            candidates, num_moves, replace=False, p=move_probs)
        for point_idx in ranked_moves:
            point = self.encoder.decode_point_index(point_idx)
            if game_state.is_valid_move(goboard.Move.play(point)) and \
                    not is_point_an_eye(game_state.board, point, game_state.next_player):
                return goboard.Move.play(point)
        return goboard.Move.pass_turn()

    # tag::dl_agent_serialize[]
    def serialize(self, h5file):
        h5file.create_group('encoder')
        h5file['encoder'].attrs['name'] = self.encoder.name()
        h5file['encoder'].attrs['board_width'] = self.encoder.board_width
        h5file['encoder'].attrs['board_height'] = self.encoder.board_height
        h5file.create_group('model')
        kerasutil.save_model_to_hdf5_group(self.model, h5file['model'])

    def diagnostics(self):
         """
         Provide debugging or performance information for the agent.
         Since this implementation doesn't track diagnostics, we return an empty dictionary.
         """
         return {}


# end::dl_agent_serialize[]

def load_prediction_agent(h5file):
    from keras.models import load_model
    from dlgo.agent.predict import DeepLearningAgent

    # 直接加载 Keras 模型
    model = load_model(h5file)

    # 返回 DeepLearningAgent，需要在调用处手动提供编码器
    return model
