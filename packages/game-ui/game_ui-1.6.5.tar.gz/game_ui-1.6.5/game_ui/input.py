import pygame

pygame.init()

class Input:
    def __init__(self, surface,  **args):
        inputs.append(self)

        self.x = 0; self.y = 0   # начальное положение input
        self.width = 200; self.height = 50   # размеры input - (ширина, высота)

        self.noText = 'Text'   # текст который будет отоброжаться когда текст input будет пустой
        self.text = ''   # текст input

        self.textColor = (255, 255, 255)   # цвет текста
        self.color = (150, 150, 150)   # цвет input
        self.pressedColor = (100, 100, 100)   # цвет input когда она будет нажата

        self.cursorColor = (0, 150, 255)   # цвет курсора

        self.fontSize = 30   # размер шрифта
        self.fontPath = None   # путь до шрфита, если == None, будет использоваться стандартый

        """

        Настройки курсора:

        StartTime - интервал времени, через которое курсор будет появлятся - исчезать
        time - текущее время через которое курсор появится - исчезнет
        direct - указывает исчезнет ли курсор или появится при истекания времени

        """

        self.StartTime = 30
        self.time = 30
        self.direct = -1

        self.eding = True   # указывает на то, что можно ли на данный момент вводить текст в input

        self.maxChars = 16   # максимальное количество символов в input
        self.textEnd = 0

        self.font = pygame.font.Font(self.fontPath, self.fontSize)   # шрифт

        self.mode = 0   # режим отрисовки текста
        self.render = True   # переменная, отвечающая за отрисовку input на экране, если == True, то input будет рисоваться, иначе нет.
        self.borderRadius = -1   # уровень сглаживания углов у кнопки, если == -1, то сглаживание не будет
        self.fillSize = 0   # уровень заливки кнопки, если == 0, то будет заливаться полностью

        self.surface = surface   # окно на котором будет рисоваться кнопка

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        for arg in args:

            if arg == 'x':
                self.x = args[arg]
            elif arg == 'y':
                self.y = args[arg]
            
            elif arg == 'width':
                self.width = args[arg]
            elif arg == 'height':
                self.height = args[arg]
            
            elif arg == 'noText':
                self.noText = args[arg]
            
            elif arg == 'textColor':
                self.textColor = args[arg]
            elif arg == 'color':
                self.color = args[arg]
            elif arg == 'pressedColor':
                self.pressedColor = args[arg]
            
            elif arg == 'fontSize':
                self.fontSize = args[arg]
            
            elif arg == 'maxChars':
                self.maxChars = args[arg]
            
            elif arg == 'font':
                self.fontPath = args[arg]
            
            elif arg == 'borderRadius':
                self.borderRadius = args[arg]
            elif arg == 'fillSize':
                self.fillSize = args[arg]
            
            elif arg == 'cursorColor':
                self.cursorColor = args[arg]
            
            else:
                print(f'GameUI.Input.Error: "{arg}" is not defined')
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.font = pygame.font.Font(self.fontPath, self.fontSize)
    
    # функция устанавливающая отрисовку кнопки на экране - (True or False)
    def setRender(self, value):
        if value:
            self.render = True
        elif not value:
            self.render = False
    
    # функция которая добавляет символ в текст
    def Press(self, key):

        """

        Пояснение: переменная [mode] отвечает за режим отрисовки кнопки;

        Если [mode] == 0, то кнопка будет отрисоваться в обычном цвете;
        Если [mode] == 1, то кнопка будет отрисоваться в режиме нажатия на кнопку, и в input может добавляется текст;

        """

        if self.render and self.mode == 1 and self.eding:
            keys = pygame.key.get_pressed()

            # добавление символа в текст
            if not keys[pygame.K_BACKSPACE] and self.mode == 1 and len(self.text) < self.maxChars:
                self.text += key

                # проверка не выходит ли текст за границы input, если да, то текст будет сдвинут влево на один символ
                try:
                    while 1:
                        tx = self.font.render(self.text[self.textEnd:-1] + self.text[-1], 1, (255, 255, 255))
                        rect = pygame.Rect(tx.get_width(), 0, 0, 0)

                        if rect.right + 20 > self.rect.width:
                            self.textEnd += 1
                            continue
                        else:
                            break
                except:
                    pass
            
            # удаление последнего символа в тексте
            elif keys[pygame.K_BACKSPACE] and self.mode == 1 and self.text != '':
                self.text = self.text[:-1]
                if self.textEnd > 0: self.textEnd -= 1
    
    # функция обвноляющая весь input и взоимодействие с ней
    def update(self):
        if self.render:

            if self.mode == 1:

                """

                Если [direct] == -1, то курсор будет показан
                Иначе, курсор будет спрятан

                """

                if self.direct == -1:
                    self.time -= 1
                    if self.time <= 0: self.direct = 1
                else:
                    self.time += 1
                    if self.time >= self.StartTime: self.direct = -1

            mBT = pygame.mouse.get_pressed()
            mx, my = pygame.mouse.get_pos()

            # как только ЛКМ была нажата, и при этом позиция мыши касается input - [mode = 1]
            if mBT[0] and self.rect.collidepoint(mx, my):
                self.mode = 1
            
            # как только ЛКМ была нажата, и при этом позиция мыши не касается input - [mode = 0]
            elif mBT[0] and not self.rect.collidepoint(mx, my):
                self.mode = 0
            
            self.draw()


    def draw(self):

        # отрисовка кнопки от зависимости переменной [mode]
        if self.mode == 0:
            pygame.draw.rect(self.surface, self.color, self.rect, self.fillSize, self.borderRadius)
        elif self.mode == 1:
            pygame.draw.rect(self.surface, self.pressedColor, self.rect, self.fillSize, self.borderRadius)
        
        # если текст в input пустой
        if self.text == '':
            noText = self.font.render(self.noText, 1, self.textColor)
            textWin = noText.get_rect(center=((self.rect.x + noText.get_width() // 2) + 5, self.rect.centery))

            self.surface.blit(noText, textWin)
        
        # иначе
        else:
            Text = self.font.render(self.text[self.textEnd:-1] + self.text[-1], 1, self.textColor)
            textWin = Text.get_rect(center=((self.rect.x + Text.get_width() // 2) + 5, self.rect.centery))

            self.surface.blit(Text, textWin)

            rect = pygame.Rect(Text.get_width(), 0, 0, 0)

            # отрисовка курсора
            if self.mode == 1 and self.direct == -1 and self.eding and rect.x + 20 < self.rect.width:
                pygame.draw.rect(self.surface, self.cursorColor, (self.rect.x + Text.get_width() + 10, self.rect.centery - self.fontSize // 2, self.fontSize // 12, self.fontSize))

inputs = []