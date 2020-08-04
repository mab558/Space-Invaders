"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

Ahmad Bhatti(mab558) and Anthony Ma(ajm439)
12/12/2019
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    #
    # Attribute _move: determines the direction of the aliens
    # Invariant: _move is an int >= 0
    #
    # Attribute _random: a random integer upto BOLT_RATE
    # Invariant: _random is an int between 1 and BOLT_RATE
    #
    # Attribute _step: the number of steps taken by aliens after every bolt shot
    # Invariant: _step is an int >= 0
    #
    # Attribute: _pause: Sets to True if game needs to be paused
    # Invariant: _pause is a bool
    #
    # Attribute: _end: Determines the result of the game
    # Invariant: _end is an int between 0 and 3 (inclusive)
    #
    # Attribute: _speed: Speed of the aliens
    # Invariant: _speed is a float
    #
    # Attribute _sound: a list of Sound objects
    # Invariant: _sound is a list with Sound objects


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getPause(self):
        """
        Returns the value of pause
        """
        return self._pause

    def getEnd(self):
        """
        Returns the value of end
        """
        return self._end

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__ (self):
        """
        Intizializes a wave

        A wave consists of a Ship, a 2D array of aliens, a Defense Line, and
        bolts fired by the Aliens or the Ship.

        At the beginning of the game, there are ALIEN_ROWS*ALIENS_IN_ROW
        number of aliens. There is one Ship with three lives. A defense line
        above the ship. There are no bolts in the beginning.
        """
        self._makeAliens(ALIEN_ROWS,ALIENS_IN_ROW,ALIEN_H_SEP,
        ALIEN_V_SEP,ALIEN_CEILING)
        self._ship = Ship()
        self._dline = GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],
        linewidth = 1, linecolor = (0,0,0))
        self._time = 0
        self._move = 0
        self._bolts=[]
        self._random = random.randint(1,BOLT_RATE)
        self._step = 0
        self._lives = 3
        self._pause = False
        self._end = 0
        self._speed= ALIEN_SPEED
        self._sound = [Sound('blast1.wav'),Sound('pew1.wav'),Sound('pop1.wav')]

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, LASER BOLTS, AND CHECK GAME
    def update(self,input,dt):
        """Updates the Aliens, Ship, Bolt, and Game.

        The Aliens move across the screen, moving down when reached the edge.
        They also are set to None if a player's bolt collides with them.

        The Ship moves across the screen according to the required key presses
        by the player. The Ship is set to None if an Alien Bolt collides with
        the Ship.

        The Bolt is created according to the player's key press for the player.
        The Aliens shoot bolts randomly.

        It checks if the player has no more lives left or the bottommost alien's
        bottom edge crosses the defense line. If so, the player loses. If there
        are no aliens left on the screen, the player wins.

        Parameter input: user input, used to control the ship or resume the game
        Precondition: input is an instance of GInput (inherited from GameApp)

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert isinstance(input,GInput)
        assert isinstance(dt,int) or isinstance(dt,float)
        self._updAliens(dt)
        self._updShip(input)
        self._updBolt(input)
        self._checkGame()

    def draw(self,view):
        """
        Draws each individul Alien in the 2D List of Aliens

        Parameter view: the game view, used in drawing
        Precondition: view is an instance of GView (inherited from GameApp)
        """
        assert isinstance(view,GView)

        for row in self._aliens:
            for alien in row:
                if alien != None:
                    alien.draw(view)

        if self._ship != None:
            self._ship.draw(view)

        self._dline.draw(view)

        for x in self._bolts:
            if x!=None:
                x.draw(view)
    #Helper Methods and Functions

    #Creating an alien 2D list
    def _makeAliens(self,row,inrow,horsep,versep,ceiling):
        """
        Creates a 2D list of Aliens

        This method uses the row and column position to create an alien in the 2D
        list.

        Parameter row: the number of rows of aliens
        Precondition: row is an int > 0

        Parameter inrow: tne number of aliens in one row
        Precondition: inrow is an int > 0

        Parameter horsep: the horizonal seperation between the aliens
        Precondition: horsep is a float or int

        Parameter versep: the vertical seperation between the aliens
        Precondition: versep is a float or int

        Parameter ceiling: the vertical seperation between the top and aliens
        Precondition: ceiling is a float or int
        """
        assert isinstance(row,int) and row > 0
        assert isinstance(inrow,int) and inrow > 0
        assert isinstance(horsep,int) or isinstance(horsep,float)
        assert isinstance(versep,int) or isinstance(versep,float)
        assert isinstance(ceiling,int) or isinstance(ceiling,float)

        image=0
        self._aliens=[]
        alist=[]
        horizontal=horsep
        starty=GAME_HEIGHT-ceiling-(ALIEN_HEIGHT*(row-1))-(versep*(row-1))
        for x in range(row):
            if  x > 0 and x % 2 == 0:
                image += 1
            if image == len(ALIEN_IMAGES):
                image = 0

            for alien in range(inrow):
                alist.append(Alien(horizontal,starty,image))
                horizontal+=horsep + ALIEN_WIDTH
            horizontal=horsep
            starty+= versep + ALIEN_HEIGHT
            self._aliens.append(alist)
            alist=[]

    #Updating Ship
    def _updShip(self,input):
        """
        Updates the position of the ship according to key presses

        The ship moves right if the player press or holds down the key 'right'.
        The ship moves left if the plater press or holds down the key 'left'
        This method updates the x position of the ship according the key press.

        Parameter input: user input, used to control the ship or resume the game
        Precondition: input is an instance of GInput (inherited from GameApp)
        """
        assert isinstance(input,GInput)

        if self._ship != None:
            self._pause = False

        da=0
        if input.is_key_down('right'):
            da += SHIP_MOVEMENT
        if input.is_key_down('left'):
            da -= SHIP_MOVEMENT
        if self._ship != None:
            self._ship.x += da
        if self._ship != None and self._ship.x+(SHIP_WIDTH/2) > GAME_WIDTH:
            self._ship.x = GAME_WIDTH - SHIP_WIDTH/2
        if self._ship != None and self._ship.x - (SHIP_WIDTH/2) < 0:
            self._ship.x = SHIP_WIDTH/2

        for x in self._bolts:
            if self._ship!=None and x!=None and self._ship.collides(x):
                self._sound[0].play()
                self._ship = None
                self._bolts.remove(x)

    #Updating Aliens
    def _updAliens(self,dt):
        """
        Moves the aliens back and forth on screen.

        The aliens move right or left until the rightmost alien's right edge or
        the leftmost alien's left edge cross is closer to the edge of screen
        than ALIEN_H_SEP. Then, the aliens move vertically down by ALIEN_V_SEP

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._time += dt
        max = self._maxAlien(self._aliens)
        min = self._minAlien(self._aliens)
        rboundary= GAME_WIDTH - ALIEN_H_SEP

        if self._time>=self._speed and max<rboundary and self._move%2==0:
            self._moveRight(self._aliens)
            self._time = 0
            self._step += 1
        elif self._time >= self._speed and self._move%2==0:
            self._moveDown(self._aliens)
            self._time=0
            self._step += 1
            self._move+=1
        elif self._time >= self._speed and min>ALIEN_H_SEP and self._move%2==1:
            self._moveLeft(self._aliens)
            self._time = 0
            self._step += 1
        elif self._time >= self._speed and self._move%2==1:
            self._moveDown(self._aliens)
            self._time = 0
            self._step += 1
            self._move+=1

        self._alienCollision(self._bolts,self._aliens)

    #Functions & Methods to help update aliens
    def _maxAlien(self,list):
        """
        Returns the x value of the right edge of the rightmost alien

        Parameter list: the 2d list of aliens in the wave
        Precondition: list is a rectangular 2d list containing Alien objects or None
        """
        max = 0
        for row in list:
            for alien in row:
                if alien !=None and alien.right > max:
                    max = alien.right
        return max

    def _minAlien(self,list):
        """
        Returns the x value of the left edge of the leftmost alien

        Parameter list: the 2d list of aliens in the wave
        Precondition: list is a rectangular 2d list containing Alien objects or None
        """
        min = GAME_WIDTH
        for row in list:
            for alien in row:
                if alien != None and alien.left < min:
                    min = alien.left
        return min

    def _moveRight(self,list):
        """
        Moves every alien in the list by ALIEN_H_WALK to the right

        Parameter list: the 2d list of aliens in the wave
        Precondition: list is a rectangular 2d list containing Alien objects or None
        """
        for row in list:
            for alien in row:
                if alien != None:
                    alien.right += ALIEN_H_WALK

    def _moveLeft(self,list):
        """
        Moves every alien in the list by ALIEN_H_WALK to the left

        Parameter list: the 2d list of aliens in the wave
        Precondition: list is a rectangular 2d list containing Alien objects or None
        """
        for row in list:
            for alien in row:
                if alien != None:
                    alien.left -= ALIEN_H_WALK

    def _moveDown(self,list):
        """
        Moves every alien in the list downwards by ALIEN_V_WALK

        Parameter list: the 2d list of aliens in the wave
        Precondition: list is a rectangular 2d list containing Alien objects or None
        """
        for row in list:
            for alien in row:
                if alien != None:
                    alien.top-=ALIEN_V_WALK

    def _alienCollision(self,bolts,list):
        """
        Checks if a player bolt collided with an alien

        If player bolt collided with alien, the bolt is removed and the alien is
        set to None

        Parameter bolts: the laser bolts currently on screen
        Precondition: bolts is a list of Bolt objects, possibly empty

        Parameter list: the 2d list of aliens in the wave
        Precondition: list is a rectangular 2d list containing Alien objects or None
        """
        for x in bolts:
            for row in range(ALIEN_ROWS):
                for alien in range(ALIENS_IN_ROW):
                    if list[row][alien]!=None and x!=None:
                        if list[row][alien].collides(x):
                            self._sound[2].play()
                            list[row][alien] = None
                            bolts.remove(x)
                            self._speed = self._speed * 0.97

    #Updating Bolt
    def _updBolt (self,input):
        """
        Updates the bolt for aliens and ship

        Bolts are shot randomly from the bottommost aliens. Bolts are removed as
        soon as they go below the screen.

        Bolts are shot by Ship if player presses the fire key. Only one player
        bolt can exist on the screen at one time. Bolts are removed as soon as
        they go above the screen.

        Parameter input: user input, used to control the ship or resume the game
        Precondition: input is an instance of GInput (inherited from GameApp)
        """
        #Shooting Aliens
        if self._step == self._random:
            col = self._notEmpty(self._aliens)
            row = 0
            i = None
            while row <= ALIEN_ROWS and i == None:
                i = self._aliens[row][col]
                row += 1
            shooter = self._aliens[row-1][col]
            self._bolts.append(Bolt(shooter.x,shooter.bottom-1,-BOLT_SPEED))
            self._sound[1].play()
            self._step = 0
            self._random= random.randint(1,BOLT_RATE)
        #Shooting Ship
        self._shipShoot(input)
        #Updating Bolts
        if len(self._bolts)!=0:
            for x in range(len(self._bolts)):
                if self._bolts[x]!=None and self._bolts[x].isPlayerBolt():
                    self._bolts[x].y += self._bolts[x].getVelocity()
                    if self._bolts[x].bottom > GAME_HEIGHT:
                        self._bolts[x] = None
                elif self._bolts[x]!=None:
                    self._bolts[x].y += self._bolts[x].getVelocity()
                    if self._bolts[x].top < 0:
                        self._bolts[x] = None
            if None in self._bolts:
                self._bolts.remove(None)

    #Helper methods & functions to update bolt
    def _notEmpty(self,list):
        """
        Returns a random nonempty column number

        The function chooses a random column from the 2D Alien list. If the
        column is nonempty, it returns the column position. Else, it chooses
        another random column

        Parameter list: the 2d list of aliens in the wave
        Precondition: list is a rectangular 2d list containing Alien objects or None
        """
        col = random.randint(0,ALIENS_IN_ROW-1)
        colList =[]
        for i in range(len(list)):
            colList += [list[i][col]]
        check = False
        for x in colList:
            if x != None:
                check = True
        if check:
            return col
        else:
            return self._notEmpty(list)

    def _shipShoot(self,input):
        """
        Bolts are shot by Ship if player presses the fire key.

        Only one player bolt can exist on the screen at one time.

        Parameter input: user input, used to control the ship or resume the game
        Precondition: input is an instance of GInput (inherited from GameApp)
        """
        if input.is_key_down('up') or input.is_key_down('spacebar'):
            if len(self._bolts) == 0:
                if self._ship!=None:
                    tool = self._ship.top+BOLT_HEIGHT/2 + 1
                    self._bolts.append(Bolt(self._ship.x,tool,BOLT_SPEED))
            else:
                alist=[]
                for x in range(len(self._bolts)):
                    if self._bolts[x] != None:
                        alist.append(self._bolts[x].isPlayerBolt())
                if not(True in alist):
                    tool = self._ship.top+BOLT_HEIGHT/2 + 1
                    self._bolts.append(Bolt(self._ship.x,tool,BOLT_SPEED))


    #Checking Game
    def _checkGame(self):
        """
        Checks if the game should be paused or ended with a specific end value.

        Decreases the number of lives of the ship if the ship is destroyed by an
        alien bolt and pauses the game. If no lives are left, it ends the game
        with the player losing.

        Checks if all of the aliens have been destroyed by the player. If so,
        the game is ended with the player winning.

        Ends the game if the bottom edge of the bottommost alien crosses the
        defense line with the player losing.
        """

        if self._ship == None and self._lives > 0:
            self._lives -= 1
            self._ship = Ship()
            self._pause = True
        if self._ship == None and self._lives == 0:
            self._end = 1
        clist=[]
        for row in self._aliens:
            for alien in row:
                clist.append(str(alien==None))
        if not('False' in clist):
            self._end = 3
        bot = GAME_HEIGHT
        for row in self._aliens:
            for alien in row:
                if alien !=None and alien.bottom < bot:
                    bot = alien.bottom
        if bot < DEFENSE_LINE:
            self._end = 2
