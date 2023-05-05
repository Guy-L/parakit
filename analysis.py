from game_entities import GameState
from interface import save_screenshot

#EXAMPLE ANALYSIS: "Get the frame with most bullets (and save the screen it if screenshots are on)"

class Analysis:
    def __init__(self):
        self.frame_with_most_bullets = None
        self.max_bullets = 0
    
    #Called for each extracted frame
    def step(self, state: GameState):
        if state.bullets and len(state.bullets) > self.max_bullets:
            self.max_bullets = len(state.bullets)
            self.frame_with_most_bullets = state

    #Called after extraction finishes
    def done(self, hasScreenshots):
        print(f"Analysis results: frame with most bullet was #{self.frame_with_most_bullets.frame_id} at {self.max_bullets} bullets")
        
        if hasScreenshots:
            print("Saved screenshot of frame in most_bullets.png")
            save_screenshot("most_bullets.png", self.frame_with_most_bullets.screen)