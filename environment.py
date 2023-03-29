from interface import *
import gym
from gym import spaces
from collections import deque

class TouhouEnvironment(gym.Env):
    def __init__(self):
        super(TouhouEnvironment, self).__init__()

        # Define the action space
        self.action_space = gym.spaces.Discrete(2**len(keys)) #e.g. 2^7 for binary input set Shift + Arrow keys + Z + X

        # Define the observation space
        screen_width = 640 - 38  #base width adjusted for offset/crop
        screen_height = 480 - 18 #base height adjusted for offset/crop
        num_game_variables = 9  # lives, life pieces, bombs, bomb pieces, 2.0 cycle, power, points, and graze (+action)
        self.num_frames = 4  # number of concatenated frames

        # Frame buffer for concatenated frames
        self.frame_buffer = deque(maxlen=self.num_frames)
        
        # Concatenated greyscale frames + game variables
        #self.observation_space = gym.spaces.Dict({
        #    'frames': gym.spaces.Box(low=0, high=255, shape=(screen_height, screen_width, self.num_frames), dtype=np.uint8),
        #    'game_variables': gym.spaces.Box(low=0, high=np.array([9, 2, 9, 2, 1000, 400, 
        #                                                            np.iinfo(np.int32).max, 
        #                                                            np.iinfo(np.int32).max, 
        #                                                            2**len(keys)-1], 
        #                                                          dtype=np.int32), 
        #                                            shape=(num_game_variables,), 
        #                                            dtype=np.int32)
        #})
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(screen_height, screen_width, 1), dtype=np.uint8)

    def step(self, action):
        #print("Taking step: " + bin(action))
        # 1 - Apply the action
        apply_action(action)
        
        # 2 - Make an observation
        cur_score = read_game_int(score) 
        cur_lives = read_game_int(lives) #these are grabbed in this scope
        cur_bombs = read_game_int(bombs) #since they're used in part 3 (and 5)
        cur_power = read_game_int(power)
        state = self._get_state(cur_lives, cur_bombs, cur_power, action = action)
        #print('{:08b}'.format(action) + " -> " + str(state["game_variables"]))

        # 3 - Calculate the reward
        reward = cur_score + (cur_power * 10) + (cur_lives * 100000) + (cur_bombs * 10000) 
        # We mostly just care about score. The adjustements are meant to encourage it to grab power and discourage it from losing lives/bombs early,
        # but the hope it that will eventually figure out that smarter strategies make losing out on the life/bomb bonus negligeable.
        
        # 4 - Determine episode end
        done = (read_game_int(game_state) == 1)
        
        # 5 - Optional info
        info = {
            'score': cur_score,
            'lives': cur_lives,
            'bombs': cur_bombs,
            'power': cur_power,
            'reward': reward,
            'done': done,
            'action': action
        }
        
        return state, float(reward), bool(done), info

    def reset(self):
        print("Attempting reset...")
        
        restart_run()
        self.frame_buffer.clear() #remove memory from past lives...
                
        for _ in range(self.num_frames): #re-populate buffer
            self.frame_buffer.append(get_greyscale_screenshot())
                
        return self._get_state(read_game_int(lives), read_game_int(bombs), read_game_int(power))
        
    def _get_state(self, cur_lives, cur_bombs, cur_power, score = 0, action = 0):
        # Get the game screen 
        game_screen = get_greyscale_screenshot()

        # Add the game screen to the frame buffer
        self.frame_buffer.append(game_screen)

        # Concatenate the frames in the frame buffer into a single array
        concatenated_frames = np.stack(self.frame_buffer, axis=-1)
        
        # Get the game variables (life count, bomb count, power, points, and graze)
        print(f"Lives {np.int32(cur_lives)} LP {read_game_int(life_pieces)} Bombs {cur_bombs} BP {read_game_int(bomb_pieces)} Bonus {read_game_int(bonus_count)} Power {cur_power} PIV {read_game_int(piv)} Graze {read_game_int(graze)} Action {'{:08b}'.format(action)}")
        game_variables = np.array([
            np.int32(cur_lives), read_game_int(life_pieces),
            cur_bombs, read_game_int(bomb_pieces),
            read_game_int(bonus_count), 
            cur_power, 
            read_game_int(piv), 
            read_game_int(graze),
            #score,      # Optional: include the reward in the observation state (not needed)
            action       # Optional: include the previous action in the observation state (not needed)
            ], dtype=np.int32)

        # Combine the concatenated frames and game variables into the state dictionary
        #return {
        #    'frames': concatenated_frames,
        #    'game_variables': game_variables
        #}
        
        return game_screen