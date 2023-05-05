from game_entities import GameState
from interface import save_screenshot
import matplotlib.pyplot as plt
import math

class Analysis:
    #Called right before extraction starts
    def __init__(self):
        #Your initialization code here
        pass
    
    #Called for each extracted frame 
    def step(self, state: GameState):
        #Your analysis code here
        pass

    #Called after extraction finishes
    def done(self, hasScreenshots):
        print(f"Analysis results:")
        #Your printing code here
        

#Ex1: "Get the frame with the most bullets (and save the screen if screenshots are on)" (only requires bullets & optionally screenshots)
class AnalysisMostBulletsFrame:
    def __init__(self):
        self.frame_with_most_bullets = None
        self.max_bullets = 0
    
    def step(self, state: GameState):
        if state.bullets and len(state.bullets) > self.max_bullets:
            self.max_bullets = len(state.bullets)
            self.frame_with_most_bullets = state

    def done(self, hasScreenshots):
        print(f"Analysis results: frame with most bullet was #{self.frame_with_most_bullets.frame_id} at {self.max_bullets} bullets")
        
        if hasScreenshots:
            print("Saved screenshot of frame in most_bullets.png")
            save_screenshot("most_bullets.png", self.frame_with_most_bullets.screen)

#Ex2: "Track the number of bullets near the player across time and plot that as a graph"  (only requires bullets)
class AnalysisCloseBulletsOverTime:
    def __init__(self):
        self.bulletcounts = []
    
    def step(self, state: GameState):
        if state.bullets:
            nearby_bullets = 0
            for bullet in state.bullets:
                if math.dist(state.player_position, bullet.position) < 100:
                    nearby_bullets = nearby_bullets + 1
                    
            self.bulletcounts.append(nearby_bullets)

    def done(self, hasScreenshots):
        plt.plot(self.bulletcounts)
        plt.xlabel('Time (frames)')
        plt.ylabel('Bullets in a 100 unit radius around player')
        plt.title('Bullet Count Over Time')
        plt.show()
        
#Ex3: "Plot the bullet positions (+player) of the last frame at game scale"  (only requires bullets)
class AnalysisPlotBullets:
    def __init__(self):
        self.lastframe = None
    
    def step(self, state: GameState):
        self.lastframe = state

    def done(self, hasScreenshots):
        # Separate the x and y coordinates
        x_coords = [bullet.position[0] for bullet in self.lastframe.bullets]
        y_coords = [bullet.position[1] for bullet in self.lastframe.bullets]

        plt.figure(figsize=(4.6, 5.4))
        plt.scatter(x_coords, y_coords)
        plt.scatter(self.lastframe.player_position[0], self.lastframe.player_position[1], color='red')
        plt.xlim(-184, 184)
        plt.ylim(0, 440)
        plt.gca().invert_yaxis()
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title('Scatter Plot of Extracted Bullet Positions')
        plt.show()
        
