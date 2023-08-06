import pygame

class Button:
    def __init__(self, surface, **args):
        
        Buttons.append(self)
        
        self.x, self.y = 0, 0    # начальоне положение кнопки
        self.width, self.height = 100, 100 # размер кнопки - (ширина, высота)
        self.pressedSize = (20, 20)
        self.surface = surface     # окно на котором будет рисоваться кнопка
        
        self.color = (150, 150, 150)   # цвет кнопки
        self.pressedColor = (80, 80, 80)   # цвет кнопки когда она нажата
        self.selectedColor = (120, 120, 120)   # цвет кнопки когда курсор наведен на нее
        self.thisColor = self.color
        self.speedChangeColor = 2

        self.func = None   # функция которая будет вызываться при нажатии кнопки

        self.defaultText = ''   # текст кнопки
        self.textColor = (255, 255, 255)   # цвет текста
        self.text = self.defaultText
        self.pressedText = self.text   # текст кнопки когда кнопка нажата

        self.fontSize = 50   # размер шрифта
        self.fast = False    # говорит о том будет ли вызываться функция после отжатия кнопки или до тех пор пока кнопка нажата
        self.fontPath = None    # путь до шрифта, если == None, то будет использован стандартный
        self.font = pygame.font.Font(self.fontPath, self.fontSize)

        self.mode = 0   # режим отрисовки кнопки
        self.lastMode = 0
        self.press = False
        self.render = True  # переменная, отвечающая за отрисовку кнопки на экране, если == True, то кнопка будет рисоваться, иначе нет.
        self.borderRadius = -1  # уровень сглаживания углов у кнопки, если == -1, то сглаживание не будет
        self.fillSize = 0   # уровень заливки кнопки, если == 0, то будет заливаться полностью

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.style = 1

        for arg in args:

            if arg == 'x':
                self.x = args[arg]
            elif arg == 'y':
                self.y = args[arg]
                
            elif arg == 'width':
                self.width = args[arg]
            elif arg == 'height':
                self.height = args[arg]
            
            elif arg == 'sizePress':
                self.pressedSize = args[arg]

            elif arg == 'color':
                self.color = args[arg]
            elif arg == 'pressedColor':
                self.pressedColor = args[arg]
            elif arg == 'speedChangeColor':
                self.speedChangeColor = args[arg]
            elif arg == 'func':
                self.func = args[arg]
            elif arg == 'text':
                self.defaultText = args[arg]
            elif arg == 'fast':
                self.fast = args[arg]
            elif arg == 'pressedText':
                self.pressedText = args[arg]
            elif arg == 'fontSize':
                self.fontSize = args[arg]
            elif arg == 'textColor':
                self.textColor = args[arg]
            
            elif arg == 'font':
                self.fontPath = args[arg]
            
            elif arg == 'borderRadius':
                self.borderRadius = args[arg]
            elif arg == 'fillSize':
                self.fillSize = args[arg]
            
            elif arg == 'style':
                self.style = args[arg]
            
            else:
                print(f'GameUI_Error: "{arg}" is not defined')
            
        self.text = self.defaultText
        self.pressedText = self.text
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.font = pygame.font.Font(self.fontPath, self.fontSize)
        self.thisColor = self.color
    
    def checkColor(self):
        get = list(self.thisColor)

        if self.mode == 0:
            if tuple(get) != self.color:
                if get[0] < self.color[0]: get[0] += self.speedChangeColor
                else: get[0] -= self.speedChangeColor

                if get[1] < self.color[1]: get[1] += self.speedChangeColor
                else: get[1] -= self.speedChangeColor

                if get[2] < self.color[2]: get[2] += self.speedChangeColor
                else: get[2] -= self.speedChangeColor

                if get[0] > 255: get[0] = 255
                if get[1] > 255: get[1] = 255
                if get[2] > 255: get[2] = 255

                if get[0] < 0: get[0] = 0
                if get[1] < 0: get[1] = 0
                if get[2] < 0: get[2] = 0

                return tuple(get)

        elif self.mode == 1:
            if get[0] < self.pressedColor[0]: get[0] += self.speedChangeColor
            else: get[0] -= self.speedChangeColor

            if get[1] < self.pressedColor[1]: get[1] += self.speedChangeColor
            else: get[1] -= self.speedChangeColor

            if get[2] < self.pressedColor[2]: get[2] += self.speedChangeColor
            else: get[2] -= self.speedChangeColor

            if get[0] > 255: get[0] = 255
            if get[1] > 255: get[1] = 255
            if get[2] > 255: get[2] = 255

            if get[0] < 0: get[0] = 0
            if get[1] < 0: get[1] = 0
            if get[2] < 0: get[2] = 0

            return tuple(get)

        return self.thisColor
    
    def setSize(self):
        if self.mode == 1:
            if self.pressedSize[0] > 0:
                self.font = pygame.font.Font(self.fontPath, self.fontSize + self.pressedSize[0] // 10)
            else: self.font = pygame.font.Font(self.fontPath, self.fontSize - abs(self.pressedSize[0] // 10))

            self.rect.width += self.pressedSize[0]
            self.rect.height += self.pressedSize[1]

            if self.pressedSize[0] > 0:
                self.rect.x -= self.pressedSize[0] // 2
            else: self.rect.x += abs(self.pressedSize[0] // 2)

            if self.pressedSize[0] > 0:
                self.rect.y -= self.pressedSize[1] // 2
            else: self.rect.y += abs(self.pressedSize[1] // 2)
        else:
            if self.pressedSize[0] > 0:
                self.font = pygame.font.Font(self.fontPath, self.fontSize - self.pressedSize[0] // 10)
            else: self.font = pygame.font.Font(self.fontPath, self.fontSize + abs(self.pressedSize[0] // 10))

            self.rect.width -= self.pressedSize[0]
            self.rect.height -= self.pressedSize[1]

            if self.pressedSize[0] > 0:
                self.rect.x += self.pressedSize[0] // 2
            else: self.rect.x -= abs(self.pressedSize[0] // 2)

            if self.pressedSize[0] > 0:
                self.rect.y += self.pressedSize[1] // 2
            else: self.rect.y -= abs(self.pressedSize[1] // 2)

    
    # функция обвноляющая всю кнопку и взоимодействие с ней
    def update(self):
        
        if self.render:

            mousePos = pygame.mouse.get_pos()
            mBT = pygame.mouse.get_pressed()
            
            # если переменная fast == False
            if not self.fast:
                """

                Пояснение: переменная [mode] отвечает за режим отрисовки кнопки;

                Если [mode] == 0, то кнопка будет отрисоваться в обычном цвете;
                Если [mode] == 1, то кнопка будет отрисоваться в режиме нажатия на кнопку;

                """

                # как только ЛКМ была нажата, и позиция мыши касалась кнопки - [mode = 1]
                if mBT[0] and self.rect.collidepoint(mousePos) and not self.press:
                    self.text = self.pressedText
                    self.mode = 1
                    self.press = True
                    if self.style == 2: self.setSize()

                # как только ЛКМ была отжата, и позиция мыши не касалась кнопки, и при этом до этого ЛКМ была нажата - [mode = 0]
                if not mBT[0] and self.press and self.rect.collidepoint(mousePos):
                    self.text = self.defaultText
                    if self.func != None:
                        self.func()
                    self.mode = 0
                    self.press = False
                    if self.style == 2: self.setSize()
                
                # как только позиция мыши не касается кнопки, и при этом ЛКМ была нажата - [mode = 0]
                if not self.rect.collidepoint(mousePos) and self.press and mBT[0]:
                    self.text = self.defaultText
                    self.mode = 0
                    self.press = False
                    if self.style == 2: self.setSize()
                
                # как только позиция мыши не касается кнопки, и ЛКМ не была нажата - [mode = 0]
                if not self.rect.collidepoint(mousePos) and not self.press and not mBT[0]:
                    self.mode = 0
            
            # иначе
            if self.fast:

                # как только ЛКМ была нажата, и позиция мыши касалась кнопки - [mode = 1]
                if mBT[0] and self.rect.collidepoint(mousePos):
                    self.text = self.pressedText
                    self.mode = 1
                    if self.func != None:
                        self.func()
                    self.press = True
                    if self.style == 2: self.setSize()
                
                # как только ЛКМ была отжата, и при этом позиция мыши касалась кнопки - [mode = 0]
                if not mBT[0] and self.press and self.rect.collidepoint(mousePos):
                    self.text = self.defaultText
                    self.mode = 0
                    self.press = False
                    if self.style == 2: self.setSize()
                
                # как только позиция мыши не касается кнопки, и при этом ЛКМ была нажата - [mode = 0]
                if not self.rect.collidepoint(mousePos) and self.press and mBT[0]:
                    self.text = self.defaultText
                    self.mode = 0
                    self.press = False
                    if self.style == 2: self.setSize()
                
                # как только позиция мыши не касается кнопки, и при этом ЛКМ не была нажата - [mode = 0]
                if not self.rect.collidepoint(mousePos) and not self.press and not mBT[0]:
                    self.mode = 0
            
            self.thisColor = self.checkColor()

            self.draw()
            
    def draw(self):

        # отрисовка кнопки от зависимости переменной [mode]
        if self.style == 1:
            if self.mode == 0:
                pygame.draw.rect(self.surface, self.color, self.rect, self.fillSize, self.borderRadius)
            elif self.mode == 1:
                pygame.draw.rect(self.surface, self.pressedColor, self.rect, self.fillSize, self.borderRadius)
        elif self.style == 2:
            pygame.draw.rect(self.surface, self.thisColor, self.rect, self.fillSize, self.borderRadius)
            
        # отрисовка текста кнопки
        if self.text != '':
            text = self.font.render(self.text, 1, self.textColor)
            textWin = text.get_rect(center=(self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2))
            self.surface.blit(text, textWin)

Buttons = []