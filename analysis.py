from game_entities import GameState
from interface import save_screenshot, get_color, color16, np
import matplotlib.pyplot as plt
import matplotlib.colors
import math

_pyplot_factor = 1/3.2 #to convert sizes in game units to pyplot point/line size; can be tweaked
_bullet_factor = 15 #makes bullets bigger than their hitbox in bullet plot (1 = real size)

def _pyplot_color(color_str):
    if color_str == 'Dark Yellow':
        return 'Olive'
    elif color_str == 'Bronze':
        return 'Sienna'
    else:
        return color_str.replace(" ", "")

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
        
#Ex3: "Plot the bullet positions of the last frame at game scale (+player)"  (only requires bullets)
class AnalysisPlotBullets:
    def __init__(self):
        self.lastframe = None
    
    def step(self, state: GameState):
        self.lastframe = state

    def done(self, hasScreenshots):
        # Separate the x and y coordinates
        x_coords = [bullet.position[0] for bullet in self.lastframe.bullets]
        y_coords = [bullet.position[1] for bullet in self.lastframe.bullets]
        colors = [_pyplot_color(get_color(bullet.bullet_type, bullet.color)) for bullet in self.lastframe.bullets]
        size = [bullet.scale * bullet.hitbox_radius * _bullet_factor * _pyplot_factor for bullet in self.lastframe.bullets]

        plt.figure(figsize=(4.6, 5.4))
        plt.scatter(x_coords, y_coords, color=colors, s=size)
        plt.scatter(self.lastframe.player_position[0], self.lastframe.player_position[1], color='red')
        plt.xlim(-184, 184)
        plt.ylim(0, 440)
        plt.gca().invert_yaxis()
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title('Scatter Plot of Extracted Bullet Positions')
        plt.show()    
        
#Ex4: "Plot the line lasers of the last frame at game scale (+player)"  (only requires lasers)
class AnalysisPlotLineLasers:
    def __init__(self):
        self.lastframe = None
    
    def step(self, state: GameState):
        self.lastframe = state

    def done(self, hasScreenshots):
        plt.figure(figsize=(4.6, 5.4))
        plt.scatter(self.lastframe.player_position[0], self.lastframe.player_position[1], color='red')
        
        for laser in self.lastframe.lasers:
            if laser.laser_type == 0:
                tail_x = laser.position[0]
                tail_y = laser.position[1]
                head_x = tail_x + laser.length * np.cos(laser.angle)
                head_y = tail_y + laser.length * np.sin(laser.angle)
                plt.plot([head_x, tail_x], [head_y, tail_y], linewidth=laser.width * _pyplot_factor, color=_pyplot_color(get_color(laser.sprite, laser.color)))
        
        plt.xlim(-184, 184)
        plt.ylim(0, 440)
        plt.gca().invert_yaxis()
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title('Plot of Extracted Line Lasers')        
        plt.show()    

#Ex5: "Plot the curve lasers of the last frame at game scale (+player)"  (only requires lasers)
class AnalysisPlotCurveLasers:
    def __init__(self):
        self.lastframe = None
        self.has_points = False
        self.has_line = True
        self.smooth = True #more computation; closer to game visuals for lasers n>15, but not to hitboxes
        self.smooth_steepness = 0.1 #seems accurate?
    
    def step(self, state: GameState):
        self.lastframe = state

    def __sigmoid_factor(self, x, left, right): #note: looks bad with small lasers (<15 nodes)
        shift = (self.smooth_steepness ** -1) 
        return (1 / (1 + np.exp(-self.smooth_steepness * (x - left - shift)))) * (1 / (1 + np.exp(self.smooth_steepness * (x - right + shift))))        
        
    def done(self, hasScreenshots):
        plt.figure(figsize=(4.6, 5.4))
        plt.scatter(self.lastframe.player_position[0], self.lastframe.player_position[1], color='red')
        
        for laser in self.lastframe.lasers:
            if laser.laser_type == 2:
            
                if self.smooth:       
                    sizes = [laser.width * _pyplot_factor * self.__sigmoid_factor(node_i, 0, len(laser.inner.nodes)) for node_i in range(len(laser.inner.nodes))]

                    if self.has_points:
                        x_coords = [nodes.position[0] for nodes in laser.inner.nodes]
                        y_coords = [nodes.position[1] for nodes in laser.inner.nodes]
                        plt.scatter(x_coords, y_coords, color=_pyplot_color(color16[laser.color]), s=sizes) 
                    
                    if self.has_line:
                        for i in range(len(laser.inner.nodes) - 1): #i hate this
                            plt.plot([laser.inner.nodes[i].position[0], laser.inner.nodes[i+1].position[0]], [laser.inner.nodes[i].position[1], laser.inner.nodes[i+1].position[1]], color=_pyplot_color(color16[laser.color]), linewidth=(sizes[i]+sizes[i+1])/2)
                else: 
                    x_coords = [nodes.position[0] for nodes in laser.inner.nodes]
                    y_coords = [nodes.position[1] for nodes in laser.inner.nodes]

                    if self.has_points:
                        plt.scatter(x_coords, y_coords, color=_pyplot_color(color16[laser.color]), s=laser.width * _pyplot_factor)
                        
                    if self.has_line:
                        plt.plot(x_coords, y_coords, color=_pyplot_color(color16[laser.color]), linewidth=laser.width * _pyplot_factor)
        
        plt.xlim(-184, 184)
        plt.ylim(0, 440)
        plt.gca().invert_yaxis()
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title('Plot of Extracted Curvy Lasers\nwith Points ' + ('on' if self.has_points else 'off') + ', Line ' + ('on' if self.has_line else 'off') + ' and Smoothing ' + (f'on ({self.smooth_steepness})' if self.smooth else 'off'))        
        plt.show()    