#!/Users/lts/Desktop/arc\ agi\ entry/game_engine_env/bin/python
"""
Simple Frogger - Standalone version
No external dependencies, just pygame
"""

import pygame
import random
from typing import Dict, List, Tuple, Optional, Any
from enum import Enum

# ARC color palette (hardcoded)
ARC_COLORS = {
    0: (0, 0, 0),        # Black
    1: (0, 116, 217),    # Blue  
    2: (255, 65, 54),    # Red
    3: (46, 204, 64),    # Green
    4: (255, 220, 0),    # Yellow
    5: (170, 170, 170),  # Gray
    6: (240, 18, 190),   # Magenta
    7: (255, 133, 27),   # Orange
    8: (127, 219, 255),  # Sky Blue
    9: (135, 12, 37)     # Maroon
}

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class LaneType(Enum):
    SAFE = 0
    ROAD = 1
    WATER = 2
    GOAL = 3

class GameObject:
    """Base class for all game objects."""
    def __init__(self, x: int, y: int, color: int, width: int = 1, height: int = 1):
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.active = True
    
    def update(self, dt: float):
        pass
    
    def collides_with(self, other: 'GameObject') -> bool:
        return (self.x < other.x + other.width and
                self.x + self.width > other.x and
                self.y < other.y + other.height and
                self.y + other.height > other.y)

class Player(GameObject):
    """Player-controlled frog."""
    def __init__(self, x: int, y: int):
        super().__init__(x, y, color=3)  # Green for player
        self.spawn_x = x
        self.spawn_y = y
        self.on_log = False
        self.current_log = None
        self.log_offset = 0
    
    def move(self, direction: Direction, grid_width: int, grid_height: int):
        dx, dy = direction.value
        new_x = max(0, min(grid_width - 1, self.x + dx))
        new_y = max(0, min(grid_height - 1, self.y + dy))
        
        self.x = new_x
        self.y = new_y
        
        # When player moves, they're no longer on a log
        self.on_log = False
        self.current_log = None
        self.log_offset = 0
    
    def reset_position(self):
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.on_log = False
        self.current_log = None
        self.log_offset = 0
    
    def update(self, dt: float):
        # Player position is handled by log movement in collision detection
        pass

class MovingObstacle(GameObject):
    """Moving obstacle (car, log, turtle)."""
    def __init__(self, x: int, y: int, color: int, speed: float, direction: Direction, width: int = 1):
        super().__init__(x, y, color, width, 1)
        self.speed = speed
        self.direction = direction
        self.move_timer = 0
        self.move_interval = 1000 / abs(speed) if speed != 0 else float('inf')
    
    def update(self, dt: float):
        if self.speed == 0:
            return
        
        self.move_timer += dt
        if self.move_timer >= self.move_interval:
            dx, dy = self.direction.value
            self.x += dx
            self.move_timer = 0
            
            # Wrap around screen
            if self.x < -self.width:
                self.x = 16
            elif self.x >= 16:
                self.x = -self.width

class Lane:
    """Represents a lane in the Frogger game."""
    def __init__(self, y: int, lane_type: LaneType, speed: float = 0, direction: Direction = Direction.RIGHT):
        self.y = y
        self.lane_type = lane_type
        self.speed = speed
        self.direction = direction
        self.obstacles: List[MovingObstacle] = []
    
    def add_obstacle(self, obstacle: MovingObstacle):
        self.obstacles.append(obstacle)
    
    def update(self, dt: float):
        for obstacle in self.obstacles:
            obstacle.update(dt)

class SimpleFrogger:
    """Simple Frogger game."""
    def __init__(self):
        pygame.init()
        
        # Game settings
        self.grid_width = 16
        self.grid_height = 16
        self.cell_size = 32
        
        # Screen setup
        self.screen_width = self.grid_width * self.cell_size + 200
        self.screen_height = self.grid_height * self.cell_size + 100
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Simple Frogger")
        
        # Game state
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 60
        
        # Game objects
        self.player = Player(self.grid_width // 2, self.grid_height - 1)
        self.lanes: List[Lane] = []
        self.game_objects: List[GameObject] = []
        
        # Game stats
        self.lives = 3
        self.score = 0
        self.level = 1
        self.game_over = False
        self.won = False
        
        self.setup_lanes()
    
    def setup_lanes(self):
        """Setup the lanes for the Frogger game."""
        self.lanes.clear()
        self.game_objects.clear()
        
        # Bottom safe zone (spawn)
        self.lanes.append(Lane(self.grid_height - 1, LaneType.SAFE))
        
        # Road section with cars
        road_start = self.grid_height - 6
        road_end = self.grid_height - 1
        
        for y in range(road_start, road_end):
            speed = random.choice([1, 2, 3])
            direction = Direction.RIGHT if y % 2 == 0 else Direction.LEFT
            lane = Lane(y, LaneType.ROAD, speed, direction)
            
            # Add cars to road lanes
            car_count = random.randint(1, 3)
            for i in range(car_count):
                x = random.randint(0, self.grid_width - 1)
                color = random.choice([1, 2, 5])  # Blue, red, gray for cars
                car = MovingObstacle(x, y, color, speed, direction, width=2)
                lane.add_obstacle(car)
                self.game_objects.append(car)
            
            self.lanes.append(lane)
        
        # Middle safe zone
        middle_y = self.grid_height // 2
        self.lanes.append(Lane(middle_y, LaneType.SAFE))
        
        # Water section with logs
        water_start = 2
        water_end = middle_y
        
        for y in range(water_start, water_end):
            speed = random.choice([1, 2])
            direction = Direction.RIGHT if y % 2 == 0 else Direction.LEFT
            lane = Lane(y, LaneType.WATER, speed, direction)
            
            # Add logs to water lanes
            log_count = random.randint(1, 2)
            for i in range(log_count):
                x = random.randint(0, self.grid_width - 3)
                color = 7  # Orange for logs
                log = MovingObstacle(x, y, color, speed, direction, width=3)
                lane.add_obstacle(log)
                self.game_objects.append(log)
            
            self.lanes.append(lane)
        
        # Top goal zone
        for y in range(0, 2):
            self.lanes.append(Lane(y, LaneType.GOAL))
    
    def update(self, dt: float):
        """Update game state."""
        if self.game_over or self.won:
            return
        
        # Update lanes
        for lane in self.lanes:
            lane.update(dt)
        
        # Update all game objects
        for obj in self.game_objects:
            obj.update(dt)
        
        # Update player
        self.player.update(dt)
        
        # If player is on a log, move with it (maintaining relative position)
        if self.player.on_log and self.player.current_log:
            new_x = self.player.current_log.x + self.player.log_offset
            # Keep player within log bounds and screen bounds
            new_x = max(0, min(self.grid_width - 1, new_x))
            # Only move if it would keep player on the log
            log_left = self.player.current_log.x
            log_right = self.player.current_log.x + self.player.current_log.width - 1
            if log_left <= new_x <= log_right:
                self.player.x = new_x
        
        # Check collisions
        self.check_collisions()
        
        # Check win condition
        if self.player.y <= 1:
            self.won = True
            self.score += 100
    
    def check_collisions(self):
        """Check for collisions between player and obstacles."""
        player_lane = self.get_lane_at(self.player.y)
        
        if player_lane.lane_type == LaneType.WATER:
            # In water - must be on a log to survive
            on_log = False
            for obstacle in player_lane.obstacles:
                if self.objects_collide(obstacle, self.player):
                    on_log = True
                    # If just stepped on log, calculate offset
                    if not self.player.on_log or self.player.current_log != obstacle:
                        self.player.log_offset = self.player.x - obstacle.x
                    self.player.on_log = True
                    self.player.current_log = obstacle
                    break
            
            if not on_log:
                self.player.on_log = False
                self.player.current_log = None
                self.player.log_offset = 0
                self.player_dies()
        
        elif player_lane.lane_type == LaneType.ROAD:
            # On road - collision with car kills player
            for obstacle in player_lane.obstacles:
                if self.objects_collide(obstacle, self.player):
                    self.player_dies()
                    break
        
        else:
            # Safe zone or goal
            self.player.on_log = False
            self.player.current_log = None
            self.player.log_offset = 0
    
    def objects_collide(self, obj1: GameObject, obj2: GameObject) -> bool:
        """Check if two objects collide."""
        return (obj1.x < obj2.x + obj2.width and
                obj1.x + obj1.width > obj2.x and
                obj1.y < obj2.y + obj2.height and
                obj1.y + obj1.height > obj2.y)
    
    def get_lane_at(self, y: int) -> Lane:
        """Get the lane at the given y coordinate."""
        for lane in self.lanes:
            if lane.y == y:
                return lane
        return Lane(y, LaneType.SAFE)
    
    def player_dies(self):
        """Handle player death."""
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True
        else:
            self.player.reset_position()
    
    def move_player(self, direction: Direction):
        """Move the player in the given direction."""
        if not self.game_over and not self.won:
            old_y = self.player.y
            self.player.move(direction, self.grid_width, self.grid_height)
            
            # Score for moving forward
            if direction == Direction.UP and self.player.y < old_y:
                self.score += 10
    
    def reset_game(self):
        """Reset the game to initial state."""
        self.lives = 3
        self.score = 0
        self.level = 1
        self.game_over = False
        self.won = False
        self.player.reset_position()
        self.setup_lanes()
    
    def draw_grid(self):
        """Draw the game grid."""
        # Draw background based on lane type
        for y in range(self.grid_height):
            lane = self.get_lane_at(y)
            
            # Lane background color
            if lane.lane_type == LaneType.ROAD:
                bg_color = (64, 64, 64)  # Dark gray for road
            elif lane.lane_type == LaneType.WATER:
                bg_color = ARC_COLORS[1]  # Blue for water
            elif lane.lane_type == LaneType.GOAL:
                bg_color = ARC_COLORS[3]  # Green for goal
            else:
                bg_color = (100, 200, 100)  # Light green for safe
            
            # Draw lane background
            lane_rect = pygame.Rect(0, y * self.cell_size, 
                                  self.grid_width * self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, bg_color, lane_rect)
        
        # Draw grid lines
        for x in range(self.grid_width + 1):
            pygame.draw.line(self.screen, (200, 200, 200), 
                           (x * self.cell_size, 0), 
                           (x * self.cell_size, self.grid_height * self.cell_size))
        
        for y in range(self.grid_height + 1):
            pygame.draw.line(self.screen, (200, 200, 200), 
                           (0, y * self.cell_size), 
                           (self.grid_width * self.cell_size, y * self.cell_size))
    
    def draw_objects(self):
        """Draw all game objects."""
        # Draw obstacles
        for obj in self.game_objects:
            color = ARC_COLORS.get(obj.color, (255, 255, 255))
            rect = pygame.Rect(obj.x * self.cell_size, obj.y * self.cell_size, 
                             obj.width * self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, color, rect)
        
        # Draw player
        player_color = ARC_COLORS.get(self.player.color, (0, 255, 0))
        player_rect = pygame.Rect(self.player.x * self.cell_size, self.player.y * self.cell_size, 
                                self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, player_color, player_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), player_rect, 2)  # Black border
    
    def draw_ui(self):
        """Draw the user interface."""
        ui_x = self.grid_width * self.cell_size + 10
        font = pygame.font.Font(None, 24)
        
        # Game stats
        stats = [
            f"Lives: {self.lives}",
            f"Score: {self.score}",
            "",
            "WASD - Move",
            "R - Restart", 
            "ESC - Quit"
        ]
        
        for i, text in enumerate(stats):
            if text:
                text_surface = font.render(text, True, (255, 255, 255))
                self.screen.blit(text_surface, (ui_x, 20 + i * 25))
        
        # Game over or win messages
        if self.game_over:
            game_over_text = pygame.font.Font(None, 48).render("GAME OVER", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(game_over_text, text_rect)
        
        elif self.won:
            win_text = pygame.font.Font(None, 48).render("YOU WIN!", True, (0, 255, 0))
            text_rect = win_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(win_text, text_rect)
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.move_player(Direction.UP)
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.move_player(Direction.DOWN)
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.move_player(Direction.LEFT)
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.move_player(Direction.RIGHT)
    
    def run(self):
        """Main game loop."""
        print("🐸 Simple Frogger started!")
        print("Controls:")
        print("  WASD or arrows - Move frog")
        print("  R - Restart")
        print("  ESC - Quit")
        print("Goal: Reach the green zone at the top!")
        
        while self.running:
            dt = self.clock.tick(self.fps)
            
            self.handle_events()
            self.update(dt)
            
            # Draw everything
            self.screen.fill((0, 0, 0))
            self.draw_grid()
            self.draw_objects()
            self.draw_ui()
            
            pygame.display.flip()
        
        pygame.quit()
        print("👋 Simple Frogger closed")

if __name__ == "__main__":
    game = SimpleFrogger()
    game.run()