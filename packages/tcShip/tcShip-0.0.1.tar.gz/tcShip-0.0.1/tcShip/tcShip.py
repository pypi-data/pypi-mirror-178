import copy
import time
from abc import ABC, abstractmethod
import random



class config():
    board_l = 20
    board_h = 20
    ship_length = 5
    ship_length_max = 20000

    # 初始坐标
    shipPosition = [5, 5]
    if shipPosition[0] <ship_length:
        raise ValueError("shipPosition[0] must > ship_length")

    targetPosition = [[1, 7],[8, 8]]
    stonePosition = [[2,3], [7,8],[7,7]]

    WORKSPACE = "local"#"local"#"tianchi"#
    ele_size = 20

class config_simple():
    board_l = 10
    board_h = 10
    ship_length = 3
    ship_length_max = 20000

    # 初始坐标
    shipPosition = [5, 5]
    if shipPosition[0] <ship_length:
        raise ValueError("shipPosition[0] must > ship_length")

    targetPosition = [8, 8]

    WORKSPACE = "local"#"local"#"tianchi"#
    ele_size = 20

if config.WORKSPACE=="local":
    import pygame
    from pygame.locals import *

class tc_ship():
    def __init__(self):
        self.action_space = ["up", "down", "left", "right"]
        # shipBody = [[shipPosition[0] - i, shipPosition[1]] for i in range(ship_length)]
        self.shipBody = []
        for i in range(config.ship_length):
            self.shipBody.append([config.shipPosition[0] - i, config.shipPosition[1]])
        self._check_point(config, self.shipBody)

        self.observation_space = [config.board_h, config.board_l]
        self.shipPosition = config.shipPosition.copy()

        self.lastaction = "right"
        self.targetPosition = config.targetPosition.copy()
        self.stonePosition = config.stonePosition.copy()
        self.steps, self.rewards = 0, 0

        if config.WORKSPACE == "local":
            self.tc = tianchi()
            self._display_init()
        else:
            self.tc = tianchi()


    def reset(self):
        self.shipPosition = config.shipPosition.copy()
        self.shipBody = []
        for i in range(config.ship_length):
            self.shipBody.append([config.shipPosition[0] - i, config.shipPosition[1]])
        self._check_point(config, self.shipBody)
        self.lastaction = "right"
        self.targetPosition = config.targetPosition.copy()
        self.stonePosition = config.stonePosition.copy()
        self.steps = 0
        self.rewards = 0
        self.__render()

        target_obs = copy.deepcopy(self.targetPosition)
        body_obs = copy.deepcopy(self.shipBody)
        stone_obs = copy.deepcopy(self.stonePosition)
        obs = {"body": body_obs, "target": target_obs, "stone": stone_obs}
        return obs

    def step(self, action):
        if action not in ["right","left","down","up"]:
            print('ValueError("action  must be right,left,down,up"),give action right')
            action = "right"
        reward = 0
        if action == 'left' and not self.lastaction == 'right':
            self.lastaction = action
            direction = action
        if action == 'right' and not self.lastaction == 'left':
            self.lastaction = action
            direction = action
        if action == 'up' and not self.lastaction == 'down':
            self.lastaction = action
            direction = action
        if action == 'down' and not self.lastaction == 'up':
            self.lastaction = action
            direction = action

        # 3.7 根据方向移动蛇头的坐标
        if self.lastaction == 'right':
            self.shipPosition[0] += 1
        if self.lastaction == 'left':
            self.shipPosition[0] -= 1
        if self.lastaction == 'up':
            self.shipPosition[1] -= 1
        if self.lastaction == 'down':
            self.shipPosition[1] += 1

        self.shipBody.insert(0, list(self.shipPosition))

        for i, p in enumerate(self.targetPosition):
            if p == self.shipPosition:
                reward = 1
                self.targetPosition[i] = self.creat_position(1)
                # print("get reward!")
                if len(self.shipBody) >= config.ship_length_max:
                    self.shipBody.pop()
        if reward == 0:
            self.shipBody.pop()

        # if reward == 1:
        #     x = random.randrange(1, config.board_h)
        #     y = random.randrange(1, config.board_l)
        #     self.targetPosition = [int(x ), int(y )]
        #     # targetflag = 1

        done = False
        if self.shipPosition[0] > (config.board_l-1) or self.shipPosition[0] < 0:
            done = True
        elif self.shipPosition[1] > (config.board_h-1) or self.shipPosition[1] < 0:
            done = True
        # 碰到自己
        for body in self.shipBody[1:]:
            if self.shipPosition[0] == body[0] and self.shipPosition[1] == body[1]:
                done = True
        #碰到陨石
        if self.shipPosition in self.stonePosition:
            done = True

        self.steps += 1
        self.rewards += reward
        info = {"step": self.step, "rewards":self.rewards}
        target_obs = copy.deepcopy(self.targetPosition)
        body_obs = copy.deepcopy(self.shipBody)
        stone_obs = copy.deepcopy(self.stonePosition)
        obs = {"body":body_obs, "target":target_obs, "stone":stone_obs}
        if not done:
            self.__render()

        return obs, reward, done, info

    def __render_simple(self, mode="human"):
        #display
        if config.WORKSPACE == "local":
            redColour = pygame.Color(255, 0, 0)
            blackColour = pygame.Color(0, 0, 0)
            whiteColour = pygame.Color(255, 255, 255)
            self.playSurface.fill(blackColour)
            pygame.draw.rect(self.playSurface, redColour, pygame.Rect(self.targetPosition[0]*config.ele_size, self.targetPosition[1]*config.ele_size, config.ele_size, config.ele_size))  # 画目标方块
            for position in self.shipBody:
                pygame.draw.rect(self.playSurface, whiteColour, pygame.Rect(position[0]*config.ele_size, position[1]*config.ele_size, config.ele_size, config.ele_size))  # 画蛇
            pygame.display.flip()

            rew = [[0 for j in range(config.board_l)] for i in range(config.board_h)]
            rew[self.targetPosition[0]][self.targetPosition[0]] = 1  # 1为目标点位 2为蛇身 3为蛇头 4为陨石
            for i, position in enumerate(self.shipBody):
                if i == 0:
                    rew[position[0]][position[1]] = 3
                else:
                    rew[position[0]][position[1]] = 2

            self.tc.draw(rew, self.shipBody, self.targetPosition, None, self.lastaction, self.steps,
                         self.rewards)  # (画布矩阵,蛇头方向,步数,分数)

        else:
            rew = [[0 for j in range(config.board_l)] for i in range(config.board_h)]
            rew[self.targetPosition[0]][self.targetPosition[0]] = 1 #1为目标点位 2为蛇身 3为蛇头 4为陨石
            for i, position in enumerate(self.shipBody):
                if i == 0:
                    rew[position[0]][position[1]] = 3
                else:
                    rew[position[0]][position[1]] = 2

            self.tc.draw(rew, self.shipBody, self.targetPosition, None, self.lastaction, self.steps, self.rewards)#(画布矩阵,蛇头方向,步数,分数)

    def __render(self, mode="human"):
        #display
        if config.WORKSPACE == "local":
            redColour = pygame.Color(255, 0, 0)
            blackColour = pygame.Color(0, 0, 0)
            stoneColour = pygame.Color(0, 255, 0)
            whiteColour = pygame.Color(255, 255, 255)
            self.playSurface.fill(blackColour)
            for position in self.targetPosition:
                pygame.draw.rect(self.playSurface, redColour, pygame.Rect(position[0]*config.ele_size, position[1]*config.ele_size, config.ele_size, config.ele_size))  # 画目标方块
            for position in self.shipBody:
                pygame.draw.rect(self.playSurface, whiteColour, pygame.Rect(position[0]*config.ele_size, position[1]*config.ele_size, config.ele_size, config.ele_size))  # 画蛇
            for position in self.stonePosition:
                pygame.draw.rect(self.playSurface, stoneColour,
                                 pygame.Rect(position[0] * config.ele_size, position[1] * config.ele_size,
                                             config.ele_size, config.ele_size))  # 画陨石
            pygame.display.flip()

            rew = [[0 for j in range(config.board_l)] for i in range(config.board_h)]
            for target in self.targetPosition:
                rew[target[0]][target[1]] = 1  # 1为目标点位 2为蛇身 3为蛇头 4为陨石
            for stone in self.stonePosition:
                rew[stone[0]][stone[1]] = 4
            for i, position in enumerate(self.shipBody):
                if i == 0:
                    rew[position[0]][position[1]] = 3
                else:
                    rew[position[0]][position[1]] = 2

            self.tc.draw(rew, self.shipBody, self.targetPosition, self.stonePosition, self.lastaction, self.steps,
                         self.rewards)  # (画布矩阵,蛇头方向,步数,分数)

        else:
            rew = [[0 for j in range(config.board_l)] for i in range(config.board_h)]
            for target in self.targetPosition:
                rew[target[0]][target[1]] = 1 #1为目标点位 2为蛇身 3为蛇头 4为陨石
            for stone in self.stonePosition:
                rew[stone[0]][stone[1]] = 4
            for i, position in enumerate(self.shipBody):
                if i == 0:
                    rew[position[0]][position[1]] = 3
                else:
                    rew[position[0]][position[1]] = 2

            self.tc.draw(rew, self.shipBody, self.targetPosition, self.stonePosition, self.lastaction, self.steps, self.rewards)#(画布矩阵,蛇头方向,步数,分数)


    def sleep(self, t):
        if config.WORKSPACE == "local":
            time.sleep(t)
        else:
            self.tc.sleep(t)

    def close(self):
        if config.WORKSPACE == "local":
            pygame.quit()
            self.tc.draw_all()
            self.tc.close()
        else:
            # print("draw all")
            self.tc.draw_all()
            self.tc.close()

    def _display_init(self):
        if config.WORKSPACE == "local":
            self.tc.__init__()
            pygame.init()
            self.playSurface = pygame.display.set_mode(
                (config.board_l * config.ele_size, config.board_h * config.ele_size))  # 创建游戏界面的大小，每格20*20，大小（32*24）

        else:
            self.tc.__init__()

    def creat_position(self, n):
        positions = []
        for i in range(n):
            position = [random.randint(0, config.board_l-1), random.randint(0, config.board_h-1)]
            while position in (self.targetPosition + self.shipBody + self.stonePosition):
                position = [random.randint(0, config.board_l-1), random.randint(0, config.board_h-1)]
            positions.append(position)
        if n == 1:
            positions = positions[0]
        return positions

    def _display(self):
        pass

    def _check_point(self, data, shipBody):
        all_position = shipBody+data.targetPosition+data.stonePosition
        for position in all_position:
            if position[0] > data.board_l:
                raise ValueError("position x must <= board_l")
            if position[1] > data.board_h:
                raise ValueError("position y must <= board_h")
        for i, position in enumerate(all_position):
            if position in all_position[i+1:]:
                raise ValueError("all position can not repeat")


class tc_ship_simple():
    def __init__(self):
        self.action_space = ["up", "down", "left", "right"]
        # shipBody = [[shipPosition[0] - i, shipPosition[1]] for i in range(ship_length)]
        self.shipBody = []
        for i in range(config_simple.ship_length):
            self.shipBody.append([config_simple.shipPosition[0] - i, config_simple.shipPosition[1]])
        self._check_point(config_simple, self.shipBody)

        self.observation_space = [config_simple.board_h, config_simple.board_l]
        self.shipPosition = config_simple.shipPosition.copy()
        self.lastaction = "right"
        self.targetPosition = config_simple.targetPosition.copy()
        self.steps, self.rewards = 0, 0

        if config.WORKSPACE == "local":
            self._display_init()
            self.tc = tianchi()
        else:
            self.tc = tianchi()


    def reset(self):
        self.shipPosition = config_simple.shipPosition.copy()
        self.shipBody = []
        for i in range(config_simple.ship_length):
            self.shipBody.append([config_simple.shipPosition[0] - i, config_simple.shipPosition[1]])
        self._check_point(config_simple, self.shipBody)
        self.lastaction = "right"
        self.targetPosition = config_simple.targetPosition.copy()
        self.steps = 0
        self.rewards = 0
        self.__render_simple()
        target_obs = copy.deepcopy(self.targetPosition)
        body_obs = copy.deepcopy(self.shipBody)
        obs = {"body": body_obs, "target": target_obs, "stone": []}
        return obs

    def step(self, action):
        if action not in ["right", "left", "down", "up"]:
            print('ValueError("action  must be right,left,down,up"),give action right')
            action = "right"
        reward = 0
        if action == 'left' and not self.lastaction == 'right':
            self.lastaction = action
            direction = action
        if action == 'right' and not self.lastaction == 'left':
            self.lastaction = action
            direction = action
        if action == 'up' and not self.lastaction == 'down':
            self.lastaction = action
            direction = action
        if action == 'down' and not self.lastaction == 'up':
            self.lastaction = action
            direction = action

        # 3.7 根据方向移动蛇头的坐标
        if self.lastaction == 'right':
            self.shipPosition[0] += 1
        if self.lastaction == 'left':
            self.shipPosition[0] -= 1
        if self.lastaction == 'up':
            self.shipPosition[1] -= 1
        if self.lastaction == 'down':
            self.shipPosition[1] += 1

        self.shipBody.insert(0, list(self.shipPosition))


        if self.targetPosition == self.shipPosition:
            reward = 1
            self.targetPosition = self.creat_position(1)
            if len(self.shipBody) >= config_simple.ship_length_max:
                self.shipBody.pop()
        else:
            self.shipBody.pop()


        done = False
        if self.shipPosition[0] > (config_simple.board_l-1) or self.shipPosition[0] < 0:
            done = True
        elif self.shipPosition[1] > (config_simple.board_h-1) or self.shipPosition[1] < 0:
            done = True
        # 碰到自己
        for body in self.shipBody[1:]:
            if self.shipPosition[0] == body[0] and self.shipPosition[1] == body[1]:
                done = True
        #碰到陨石
        # if self.shipPosition in self.stonePosition:
        #     done = True

        self.steps += 1
        self.rewards += reward
        info = {"step": self.step, "rewards":self.rewards}
        target_obs = copy.deepcopy(self.targetPosition)
        body_obs = copy.deepcopy(self.shipBody)
        obs = {"body":body_obs, "target":target_obs, "stone":[]}
        if not done:
            self.__render_simple()

        return obs, reward, done, info

    def __render_simple(self, mode="human"):
        #display
        if config.WORKSPACE == "local":
            redColour = pygame.Color(255, 0, 0)
            blackColour = pygame.Color(0, 0, 0)
            whiteColour = pygame.Color(255, 255, 255)
            self.playSurface.fill(blackColour)

            pygame.draw.rect(self.playSurface, redColour, pygame.Rect(self.targetPosition[0]*config.ele_size, self.targetPosition[1]*config.ele_size, config.ele_size, config.ele_size))  # 画目标方块
            for position in self.shipBody:
                pygame.draw.rect(self.playSurface, whiteColour, pygame.Rect(position[0]*config.ele_size, position[1]*config.ele_size, config.ele_size, config.ele_size))  # 画蛇
            pygame.display.flip()

            rew = [[0 for j in range(config_simple.board_l)] for i in range(config_simple.board_h)]
            rew[self.targetPosition[0]][self.targetPosition[0]] = 1  # 1为目标点位 2为蛇身 3为蛇头 4为陨石
            for i, position in enumerate(self.shipBody):
                if i == 0:
                    rew[position[0]][position[1]] = 3
                else:
                    rew[position[0]][position[1]] = 2

            self.tc.draw(rew, self.shipBody, self.targetPosition, None, self.lastaction, self.steps,
                         self.rewards)  # (画布矩阵,蛇头方向,步数,分数)
        else:
            rew = [[0 for j in range(config_simple.board_l)] for i in range(config_simple.board_h)]
            rew[self.targetPosition[0]][self.targetPosition[0]] = 1 #1为目标点位 2为蛇身 3为蛇头 4为陨石
            for i, position in enumerate(self.shipBody):
                if i == 0:
                    rew[position[0]][position[1]] = 3
                else:
                    rew[position[0]][position[1]] = 2

            self.tc.draw(rew, self.shipBody, self.targetPosition, None, self.lastaction, self.steps, self.rewards)#(画布矩阵,蛇头方向,步数,分数)

    def __render(self, mode="human"):
        #display
        if config.WORKSPACE == "local":
            redColour = pygame.Color(255, 0, 0)
            blackColour = pygame.Color(0, 0, 0)
            stoneColour = pygame.Color(0, 255, 0)
            whiteColour = pygame.Color(255, 255, 255)
            self.playSurface.fill(blackColour)
            for position in self.targetPosition:
                pygame.draw.rect(self.playSurface, redColour, pygame.Rect(position[0]*config.ele_size, position[1]*config.ele_size, config.ele_size, config.ele_size))  # 画目标方块
            for position in self.shipBody:
                pygame.draw.rect(self.playSurface, whiteColour, pygame.Rect(position[0]*config.ele_size, position[1]*config.ele_size, config.ele_size, config.ele_size))  # 画蛇
            for position in self.stonePosition:
                pygame.draw.rect(self.playSurface, stoneColour,
                                 pygame.Rect(position[0] * config.ele_size, position[1] * config.ele_size,
                                             config.ele_size, config.ele_size))  # 画陨石
            pygame.display.flip()

            rew = [[0 for j in range(config_simple.board_l)] for i in range(config_simple.board_h)]
            for target in self.targetPosition:
                rew[target[0]][target[1]] = 1  # 1为目标点位 2为蛇身 3为蛇头 4为陨石
            for stone in self.stonePosition:
                rew[stone[0]][stone[1]] = 4
            for i, position in enumerate(self.shipBody):
                if i == 0:
                    rew[position[0]][position[1]] = 3
                else:
                    rew[position[0]][position[1]] = 2

            self.tc.draw(rew, self.shipBody, self.targetPosition, self.stonePosition, self.lastaction, self.steps,
                         self.rewards)  # (画布矩阵,蛇头方向,步数,分数)

        else:
            rew = [[0 for j in range(config_simple.board_l)] for i in range(config_simple.board_h)]
            for target in self.targetPosition:
                rew[target[0]][target[1]] = 1 #1为目标点位 2为蛇身 3为蛇头 4为陨石
            for stone in self.stonePosition:
                rew[stone[0]][stone[1]] = 4
            for i, position in enumerate(self.shipBody):
                if i == 0:
                    rew[position[0]][position[1]] = 3
                else:
                    rew[position[0]][position[1]] = 2

            self.tc.draw(rew, self.shipBody, self.targetPosition, self.stonePosition, self.lastaction, self.steps, self.rewards)#(画布矩阵,蛇头方向,步数,分数)


    def sleep(self, t):
        if config.WORKSPACE == "local":
            time.sleep(t)
            self.tc.sleep(t)
        else:
            self.tc.sleep(t)

    def close(self):
        if config.WORKSPACE == "local":
            pygame.quit()
            self.tc.draw_all()
            self.tc.close()
        else:
            # print("draw all")
            self.tc.draw_all()
            self.tc.close()

    def _display_init(self):
        if config.WORKSPACE == "local":
            pygame.init()
            self.playSurface = pygame.display.set_mode(
                (config_simple.board_l * config.ele_size, config_simple.board_h * config.ele_size))  # 创建游戏界面的大小，每格20*20，大小（32*24）
            self.tc.__init__()
        else:
            self.tc.__init__()

    def creat_position(self, n):
        positions = []
        for i in range(n):
            position = [random.randint(0, config_simple.board_l-1), random.randint(0, config_simple.board_h-1)]
            while position in (self.targetPosition + self.shipBody):# + self.stonePosition):
                position = [random.randint(0, config_simple.board_l-1), random.randint(0, config_simple.board_h-1)]
            positions.append(position)
        if n == 1:
            positions = positions[0]
        return positions

    def _display(self):
        pass

    def _check_point(self, data, shipBody):
        all_position = shipBody+[data.targetPosition]
        for position in all_position:
            if position[0] > data.board_l:
                raise ValueError("position x must <= board_l")
            if position[1] > data.board_h:
                raise ValueError("position y must <= board_h")
        for i, position in enumerate(all_position):
            if position in all_position[i+1:]:
                raise ValueError("all position can not repeat")

class tianchi():
    def __init__(self):
        self.raws = []
        self.info = {}
        self.info["board"] = [config.board_l, config.board_h]
        self.info["shipBody"] = []
        self.info["target"] = []
        self.info["stone"] = []
        self.info["d"] = []
        self.info["steps"] = []
        self.info["rewards"] = []

    def draw(self, raw, shipBody, targetPosition, stonePosition, d, steps, rewards):
        #print("step: "+str(steps)+" and rewards: "+str(rewards))
     
        self.raws.append(raw)
        if shipBody:
            self.info["shipBody"].append(shipBody)
        if targetPosition:
            self.info["target"].append(targetPosition)
        if stonePosition:
            self.info["stone"].append(stonePosition)
        self.info["d"].append(d)
        self.info["steps"].append(steps)
        self.info["rewards"].append(rewards)

    def sleep(self, t):
        pass

    def draw_all(self):
        #self.raws:全部N步之后的视频帧
        #self.info：全部N步的蛇头方向、步数、分数的字典，对应"d"、"steps"、"rewards"
        pass

    def close(self):
        pass

