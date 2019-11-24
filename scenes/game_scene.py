import math
import pygame
from components.button import Button
from components.clickable import Clickable
from components.label import Label
from game.entity.player import Player
from game.world.world import World
from scenes.scene import Scene
from utility.assets import Assets
from utility.colors import Colors
from utility.constants import Constants
from utility.fonts import Fonts
from pygame.color import Color

# Scene to display the gameplay
class GameScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        self.initGame()
        self.initComponents()

        self.isPaused = False

    def initGame(self):
        self.world = World()
        self.world.generateWorld()
        self.player = Player(self.world)

        y = self.world.getHighestBlock(0)
        print("Highest block", y)
        self.player.position = [0, y]

        self.previewWidth = 10
        self.blockSize = self.app.width / (self.previewWidth * 2 + 1)
        self.previewHeight = math.ceil(self.app.height / self.blockSize)
        print(self.previewWidth, self.previewHeight, self.blockSize)

    def initComponents(self):
        textFont = pygame.font.Font(Fonts.Courier, 30)
        self.label = Label(self.app.window, 0, 0, text="(0, 0)", font=textFont)
        rect = self.label.label.get_rect()
        width, height = rect.width, rect.height
        self.label.x = self.app.width - width
        self.label.y = height/2
        self.addComponent(self.label)

        window = self.app.window
        width, height = self.app.width, self.app.height

        resume = Button(window, width/2, 1.5*height/3,
                            font=textFont, text="Resume Game",
                            fillColor=Color(255, 255, 255),
                            padding=10)
        resume.setOnClickListener(self.removePause)

        quit = Button(window, width/2, 2*height/3,
                            font=textFont, text="Quit Game",
                            fillColor=Color(255, 255, 255),
                            padding=10)
        quit.setOnClickListener(self.app.quit)

        resume.setEnabled(False)
        quit.setEnabled(False)
        self.pauseComponents = [resume, quit]
        self.addComponents(self.pauseComponents)

    def drawComponents(self):
        self.drawBackground()
        self.drawTerrain()
        self.drawPlayer()
        self.drawInventory()
        if self.isPaused:
            self.drawPause()

        super().drawComponents()

    def drawBackground(self):
        window = self.app.window
        player = self.player
        bg = Assets.assets["background"]
        bgSize = bg.get_size()
        windowSize = window.get_size()
        coord = [windowSize[i] - bgSize[i] - player.position[i] for i in range(2)]
        window.blit(bg, coord)

    def drawTerrain(self):
        world = self.world
        height, width = self.previewHeight, self.previewWidth
        player = self.player
        px, py = player.position
        offset = 5 # load outside canvas to hide buffering
        renderOffset = 7
        for y in range(-height-offset, height+offset):
            for x in range(-width-offset, width+offset):
                bx = px + x
                by = py - y
                block = world.getBlock((bx, by))

                size = self.blockSize
                renderX = (x+width - (abs(px)%1)) * size
                renderY = (y+height-renderOffset - (abs(py)%1)) * size
                self.drawBlock(block, (renderX, renderY))

    def drawBlock(self, block, position):
        window = self.app.window
        texture = Assets.assets["textures"][block.getType().value]
        
        x, y = position
        size = self.blockSize
        blockRect = pygame.Rect(0, 0, size, size)
        blockRect.center = (x + size/2, y + size/2)

        window.blit(texture, blockRect)

    def drawPlayer(self):
        window = self.app.window
        cx, cy = self.app.width / 2, self.app.height / 2
        player = self.player
        player.draw(window, cx, cy)

        self.label.setText(player.getPosition())

    def drawInventory(self):
        inventory = self.player.getInventory()
        width, height = inventory.getDimensions()
        panelWidth = self.app.width / 2

        # rect = pygame.Rect(0, 0, panelWidth, 50)
        # pygame.draw.rect(self.app.window, Color(0, 0, 0), rect, 1)

        cellSize = 40
        offset = 5
        for i in range(width):
            rect = pygame.Rect(i * cellSize + offset, offset, cellSize, cellSize)
            borderWidth = 1
            if i == self.player.equipIndex:
                borderWidth = 3
            pygame.draw.rect(self.app.window, Color(0, 0, 0), rect, borderWidth)

    def onKeyPress(self, keys, mods):
        super().onKeyPress(keys, mods)
        if self.isPaused: return
        player = self.player

        if keys[pygame.K_a]:
            player.move(-1, 0, walk=True)
        elif keys[pygame.K_d]:
            player.move(1, 0, walk=True)
        elif keys[pygame.K_ESCAPE]:
            self.isPaused = True
        else:
            for i in range(9):
                if keys[pygame.K_1 + i]:
                    player.equipIndex = i
                    break
            else:
                player.faceDirection(0, 0)

        if not player.isJumping and keys[pygame.K_SPACE]:
            player.jump()
        
        player.update()

    def onMouseClick(self, mousePos):
        for component in self.components:
            if (isinstance(component, Clickable) and
                component.isEnabled and
                component.isClicked(mousePos)):
                component.click()

    def onMouseScroll(self, scroll):
        player = self.player
        inventory = player.getInventory()
        player.equipIndex = (player.equipIndex + scroll) % (inventory.width)

    def drawPause(self):
        filter = pygame.Surface((self.app.width, self.app.height))
        filter.set_alpha(100)
        filter.fill((255, 255, 255))
        self.app.window.blit(filter, (0, 0))

        for component in self.pauseComponents:
            component.setEnabled(True)

    def removePause(self):
        self.isPaused = False
        for component in self.pauseComponents:
            component.setEnabled(False)

        
