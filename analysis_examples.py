from analysis import * 

# ==========================================
# Please use your text editor's block collapse 
# functionality ([+] icon in Notepad++) to hide
# classes and browse this file quicker.
# ==========================================

# Ex1: "Get the frame with the most bullets (and save the screen if screenshots are on)" [only requires bullets & optionally screenshots]
class AnalysisMostBulletsFrame(Analysis):
    def __init__(self):
        self.frame_with_most_bullets = None
        self.max_bullets = 0
    
    def step(self, state: GameState):
        if state.bullets and len(state.bullets) > self.max_bullets:
            self.max_bullets = len(state.bullets)
            self.frame_with_most_bullets = state

    def done(self):
        if self.frame_with_most_bullets:
            print(f"Analysis results: frame with most bullet was stage frame #{self.frame_with_most_bullets.frame_stage} at {self.max_bullets} bullets.")
            
            if self.frame_with_most_bullets.screen is not None:
                print("Saved screenshot of frame in most_bullets.png")
                save_screenshot("most_bullets.png", self.frame_with_most_bullets.screen)
        else:
            print("No frame had any bullets.")

# Ex2: "Track the number of bullets across time and plot that as a graph" [only requires bullets]
class AnalysisBulletsOverTime(Analysis):
    def __init__(self):
        self.bulletcounts = []
    
    def step(self, state: GameState):
        if state.bullets:
            self.bulletcounts.append(len(state.bullets))

    def done(self):
        plt.plot(self.bulletcounts)
        plt.xlabel('Time (frames)')
        plt.ylabel('Bullets')
        plt.title('Bullet Count Over Time')
        plt.show()

# Ex3: "Track the number of bullets near the player across time and plot that as a graph" [only requires bullets]
class AnalysisCloseBulletsOverTime(Analysis):
    radius = 100
    
    def __init__(self):
        self.bulletcounts = []
    
    def step(self, state: GameState):
        if state.bullets:
            nearby_bullets = 0
            for bullet in state.bullets:
                if bullet.show_delay == 0 and math.dist(state.player_position, bullet.position) < self.radius:
                    nearby_bullets = nearby_bullets + 1
                    
            self.bulletcounts.append(nearby_bullets)

    def done(self):
        plt.plot(self.bulletcounts)
        plt.xlabel('Time (frames)')
        plt.ylabel(f'Bullets in a {self.radius} unit radius around player')
        plt.title('Bullet Count Over Time')
        plt.show()

# Plot0: Abstract base class to factorize common plotting code
class AnalysisPlot(Analysis, ABC):
    plot_title = 'DEFAULT PLOT TITLE' #to be customized
    
    def __init__(self, state: GameState = None):
        self.lastframe = state
    
    def step(self, state: GameState):
        self.lastframe = state #if sequence, use last frame
        
    @abstractmethod
    def plot(self):
        pass #custom plot behavior to be implemented
        
    def done(self):
        plt.figure(figsize=(4.6 * plot_scale, 5.6 * plot_scale)) #sets plot scale using game world's ratio
        
        plt.xlabel('X Coordinate')
        plt.xlim(-184, 184)
        plt.ylabel('Y Coordinate')
        plt.ylim(0, 448)
        plt.gca().invert_yaxis()
        
        player_scale = self.lastframe.player_hitbox_rad
        
        if game_id == 14 and self.lastframe.game_specific: 
            player_scale *= self.lastframe.game_specific['player_scale']
            
            if self.lastframe.game_specific['seija_flip'][0] == -1:
                plt.gca().invert_xaxis()
                
            if self.lastframe.game_specific['seija_flip'][1] == -1:
                plt.gca().invert_yaxis()
                
        plt.scatter(self.lastframe.player_position[0], self.lastframe.player_position[1], color='maroon', s=25*player_scale, marker='X') #plots player
            
        #custom plot title/behavior here then show
        plt.title(self.plot_title)
        self.plot()
        plt.show()   
       
# Plot1: "Plot the bullet positions of the last frame at game scale (+player)" [only requires bullets]
class AnalysisPlotBullets(AnalysisPlot):
    plot_title = 'Scatter Plot of Extracted Bullet Positions'
    
    def plot(self):
        if self.lastframe.bullets:
            x_coords = [bullet.position[0] for bullet in self.lastframe.bullets]
            y_coords = [bullet.position[1] for bullet in self.lastframe.bullets]
            colors = [pyplot_color(get_color(bullet.bullet_type, bullet.color)) for bullet in self.lastframe.bullets]
            sizes = [bullet.scale * bullet.hitbox_radius * bullet_factor * pyplot_factor for bullet in self.lastframe.bullets]
            alphas = [0.05 if bullet.show_delay else 1 for bullet in self.lastframe.bullets]

            plt.scatter(x_coords, y_coords, color=colors, s=sizes, alpha=alphas)

# Plot2: "Plot the enemy positions of the last frame at game scale (+player)" [only requires enemies]
class AnalysisPlotEnemies(AnalysisPlot):
    plot_title = 'Scatter Plot of Extracted Enemy Positions'

    def plot(self):
        if self.lastframe.enemies:
            x_coords = [enemy.position[0] for enemy in self.lastframe.enemies]
            y_coords = [enemy.position[1] for enemy in self.lastframe.enemies]
            sizes = [enemy.hitbox[0] * enemy_factor * pyplot_factor for enemy in self.lastframe.enemies] 
            #assumes square hitbox/point-like enemies, will only fix if someone yells at me

            plt.scatter(x_coords, y_coords, s=sizes, marker='s')
        
# Plot3: "Plot the item positions of the last frame at game scale (+player)" [only requires items]
class AnalysisPlotItems(AnalysisPlot):
    plot_title = 'Scatter Plot of Extracted Item Positions'
    
    def plot(self):
        if self.lastframe.items:
            x_coords = [item.position[0] for item in self.lastframe.items]
            y_coords = [item.position[1] for item in self.lastframe.items]
            colors = [item_color(item.item_type) for item in self.lastframe.items]
            colors = [item_color(item.item_type) for item in self.lastframe.items]
            
            plt.scatter(x_coords, y_coords, color=colors, marker='*')

# Plot4: "Plot the line lasers of the last frame at game scale (+player)" [only requires lasers]
class AnalysisPlotLineLasers(AnalysisPlot):
    plot_title = 'Plot of Extracted Line Lasers'

    def plot(self):
        for laser in self.lastframe.lasers:
            if laser.laser_type == 0:
            
                tail_x = laser.position[0]
                tail_y = laser.position[1]
                head_x = tail_x + laser.length * np.cos(laser.angle)
                head_y = tail_y + laser.length * np.sin(laser.angle)
                plt.plot([head_x, tail_x], [head_y, tail_y], linewidth=laser.width * pyplot_factor, color=pyplot_color(get_color(laser.sprite, laser.color)), zorder=0)
                
                if plot_laser_circles:
                    plt.scatter(head_x, head_y, color='white', edgecolors=pyplot_color(get_color(laser.sprite, laser.color)), s=75, zorder=1)
    
# Plot5: "Plot the infinite lasers of the last frame at game scale (+player)" [only requires lasers]
class AnalysisPlotInfiniteLasers(AnalysisPlot): 
    plot_title = 'Plot of Extracted Telegraphed Lasers'
    
    def plot(self):
        for laser in self.lastframe.lasers:
            if laser.laser_type == 1:
            
                origin_x = laser.position[0]
                origin_y = laser.position[1]
                end_x = origin_x + laser.length * np.cos(laser.angle)
                end_y = origin_y + laser.length * np.sin(laser.angle)
                plt.plot([origin_x, end_x], [origin_y, end_y], linewidth=laser.width * pyplot_factor, color=pyplot_color(get_color(laser.sprite, laser.color)), zorder=0, alpha=(1 if laser.state==2 else 0.25))
                
                if plot_laser_circles:
                    plt.scatter(origin_x, origin_y, color='white', edgecolors='blue', s=100, zorder=1, alpha=0.9)
        
# Plot6: "Plot the curve lasers of the last frame at game scale (+player)" [only requires lasers]
class AnalysisPlotCurveLasers(AnalysisPlot):
    has_points = False
    has_line = True
    smooth = True
    smooth_steepness = 0.1

    @property
    def plot_title(self):
        return f"Plot of Extracted Curvy Lasers\nwith Points {'on' if self.has_points else 'off'}, Line {'on' if self.has_line else 'off'} and Smoothing {'on (' + str(self.smooth_steepness) + ')' if self.smooth else 'off'}"

    def __sigmoid_factor(self, x, left, right): #note: looks bad with small lasers (<15 nodes)
        shift = (self.smooth_steepness ** -1) 
        return (1 / (1 + np.exp(-self.smooth_steepness * (x - left - shift)))) * (1 / (1 + np.exp(self.smooth_steepness * (x - right + shift))))        
        
    def plot(self):
        for laser in self.lastframe.lasers:
            if laser.laser_type == 2:
            
                if self.smooth:       
                    sizes = [laser.width * pyplot_factor * self.__sigmoid_factor(node_i, 0, len(laser.nodes)) for node_i in range(len(laser.nodes))]

                    if self.has_points:
                        x_coords = [nodes.position[0] for nodes in laser.nodes]
                        y_coords = [nodes.position[1] for nodes in laser.nodes]
                        plt.scatter(x_coords, y_coords, color=pyplot_color(color16[laser.color]), s=sizes) 
                    
                    if self.has_line:
                        for i in range(len(laser.nodes) - 1): #i hate this
                            plt.plot([laser.nodes[i].position[0], laser.nodes[i+1].position[0]], [laser.nodes[i].position[1], laser.nodes[i+1].position[1]], color=pyplot_color(color16[laser.color]), linewidth=(sizes[i]+sizes[i+1])/2)
                else: 
                    x_coords = [nodes.position[0] for nodes in laser.nodes]
                    y_coords = [nodes.position[1] for nodes in laser.nodes]

                    if self.has_points:
                        plt.scatter(x_coords, y_coords, color=pyplot_color(color16[laser.color]), s=laser.width * pyplot_factor)
                        
                    if self.has_line:
                        plt.plot(x_coords, y_coords, color=pyplot_color(color16[laser.color]), linewidth=laser.width * pyplot_factor)
        
# Plot7: "Plot all the above at game scale (+player)" [only doesn't require screenshots]
class AnalysisPlotAll(AnalysisPlot):
    plot_title = 'Scatter Plot of Extracted... Everything!'
    
    def plot(self):
        AnalysisPlotBullets(self.lastframe).plot()
        AnalysisPlotEnemies(self.lastframe).plot()
        AnalysisPlotItems(self.lastframe).plot()
        AnalysisPlotLineLasers(self.lastframe).plot()
        AnalysisPlotInfiniteLasers(self.lastframe).plot()
        AnalysisPlotCurveLasers(self.lastframe).plot()

# Plot8: "Plot a heatmap of positions hit by bullets over time" [only requires bullets]
class AnalysisPlotBulletHeatmap(AnalysisPlot):
    circles = True #otherwise square (faster)
    max_count = 100 #prevents bullet spawn overshadowing everything, should be bigger for longer analyses

    @property
    def plot_title(self):
        return f"Bullet Heatmap w/\ncircular collision {'on' if self.circles else 'off'},\nmax bullet count capped at {self.max_count}"
        
    def __init__(self, state: GameState = None):
        super().__init__(state)
        self.heatmap = np.zeros((449, 369))

    def step(self, state: GameState):
        super().step(state)
        for bullet in state.bullets:
            
            min_x = int(bullet.position[0] - bullet.hitbox_radius * bullet.scale) + 184
            max_x = int(bullet.position[0] + bullet.hitbox_radius * bullet.scale) + 184
            min_y = int(bullet.position[1] - bullet.hitbox_radius * bullet.scale)
            max_y = int(bullet.position[1] + bullet.hitbox_radius * bullet.scale)
            
            if min_x >= 0 and min_x <= 368 and max_x >= 0 and max_x <= 368 and min_y >= 0 and min_y <= 448 and max_y >= 0 and max_y <= 448:
                for x in range(min_x, max_x):
                    for y in range(min_y, max_y):
                        if not self.circles or (self.circles and (x - bullet.position[0] - 184) ** 2 + (y - bullet.position[1]) ** 2 <= (bullet.hitbox_radius * bullet.scale) ** 2) and self.heatmap[y, x] < self.max_count:
                            self.heatmap[y, x] += 1

    def plot(self):
        plt.imshow(self.heatmap, origin='lower', cmap='viridis', extent=(-184, 184, 0, 448))
        plt.colorbar(label='Bullet hits')
        
# Bonus: "Render the bullet positions as ASCII art in the terminal" [only requires bullets] [useless]
class AnalysisPrintBulletsASCII(Analysis):
    def __init__(self):
        self.lastframe = None
        self.size_x = 90 #at this size, can be pasted into discord nicely (.txt feature makes it not take space without cutting it off much)
        self.size_y = int((self.size_x*440)/368)
        self.radius = 3 #how far to look for bullets around each where each character maps (yes it should be the other way around whatever)
    
    def step(self, state: GameState):
        self.lastframe = state

    def done(self):
        if not self.lastframe.bullets:
            print("No bullets to print.")
            return
        
        print("```")
        for y in range(0, self.size_y):
            line = ""
            
            for x in range(0, self.size_x):
                ingame_x = (x / self.size_x) * 368 - 184
                ingame_y = (y / self.size_y) * 440
                
                found = False
                for bullet in self.lastframe.bullets:
                    if math.dist((ingame_x, ingame_y), bullet.position) < self.radius:
                        
                        if bullet.bullet_type == 20:
                            line += "☺"
                        elif bullet.bullet_type >= 38 and bullet.bullet_type <= 41:
                            line += "♪"
                        else:
                            line += "•"
                            
                        found = True
                        
                if not found:
                    line += " "
                
            print(line)
        print("```")
                    