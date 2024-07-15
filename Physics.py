import phylib
import sqlite3
import os

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH
SIM_RATE = phylib.PHYLIB_SIM_RATE
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON
DRAG = phylib.PHYLIB_DRAG
MAX_TIME = phylib.PHYLIB_MAX_TIME
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS
FRAME_INTERVAL = 0.01



HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />"""


FOOTER = """</svg>\n"""




################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;


    # add an svg method here

    def svg(self):

        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number]) 
        


class RollingBall( phylib.phylib_object ):
    """
    Python RollingBall class.
    """

    def __init__( self, number, pos, vel, acc):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a RollingBall class
        self.__class__ = RollingBall;


    # add an svg method here

    def svg(self):

        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number])



class Hole( phylib.phylib_object ):
    """
    Python Hole class.
    """

    def __init__( self, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       0, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a Hole class
        self.__class__ = Hole;


    # add an svg method here

    def svg(self):

        return """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS)


class HCushion( phylib.phylib_object ):
    """
    Python HCushion class.
    """

    def __init__( self, y):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCUSHION, 
                                       0, 
                                       None, None, None, 
                                       0.0, y )
      
        # this converts the phylib_object into a VCushion class
        self.__class__ = HCushion


    # add an svg method here
        

    def svg(self):

        y = 0

        if(self.obj.hcushion.y == 0):
            y = -25

        else:
            y = 2700



        return """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (y)
        


class VCushion( phylib.phylib_object ):
    """
    Python VCushion class.
    """

    def __init__( self, x):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_VCUSHION, 
                                       0, 
                                       None, None, None, 
                                       x, 0.0 )
      
        # this converts the phylib_object into a HCushion class
        self.__class__ = HCushion


    # add an svg method here
        
    def svg(self):

        x = 0

        if(self.obj.vcushion.x == 0):
            x = -25

        else:
            x = 1350

        return """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (x)
        



################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here

    def svg(self):
        svg_string = HEADER

        # Iterate through every object and add its svg return string
        for object in self:
            if(object != None):
                svg_string += object.svg()

        svg_string += FOOTER
        
        return svg_string
    
    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                        Coordinate(0,0),
                                        Coordinate(0,0),
                                        Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );

                # add ball to table
                new += new_ball;
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                                    Coordinate( ball.obj.still_ball.pos.x,
                                    ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;
        # return table
        return new;


    def cueBall(self):
        cue_ball = None
        for obj in self:
            if isinstance(obj, StillBall) and obj.obj.still_ball.number == 0:
                cue_ball = obj
        return cue_ball



class Database:

    conn: sqlite3.Connection

    def __init__( self, reset=False ):
        if reset and os.path.exists( 'phylib.db' ):
            os.remove( 'phylib.db' )

        self.conn = sqlite3.connect( 'phylib.db' )


    def createDB( self ):

        cursor = self.conn.cursor()

        # Ball
        cursor.execute("""CREATE TABLE IF NOT EXISTS Ball(
                       BALLID   INTEGER    NOT NULL,
                       BALLNO   INTEGER    NOT NULL,
                       XPOS     FLOAT      NOT NULL,
                       YPOS     FLOAT      NOT NULL,
                       XVEL     FLOAT,
                       YVEL     FLOAT,
                       PRIMARY KEY (BALLID AUTOINCREMENT))""")

        # TTable
        cursor.execute("""CREATE TABLE IF NOT EXISTS TTable(
                        TABLEID    INTEGER    NOT NULL,
                        TIME       FLOAT      NOT NULL,
                        PRIMARY KEY    (TABLEID AUTOINCREMENT))""")
        
        # BallTable
        cursor.execute("""CREATE TABLE IF NOT EXISTS BallTable(
                       BALLID    INTEGER    NOT NULL,
                       TABLEID   INTEGER    NOT NULL,
                       FOREIGN KEY (BALLID) REFERENCES Ball,
                       FOREIGN KEY (TABLEID) REFERENCES TTable)""")
        
        # Shot
        cursor.execute("""CREATE TABLE IF NOT EXISTS Shot(
                       SHOTID    INTEGER    NOT NULL,
                       PLAYERID  INTEGER    NOT NULL,
                       GAMEID    INTEGER    NOT NULL,
                       PRIMARY KEY (SHOTID AUTOINCREMENT),
                       FOREIGN KEY (PLAYERID) REFERENCES Player,
                       FOREIGN KEY (GAMEID) REFERENCES Player)""")
        

        # TableShot
        cursor.execute("""CREATE TABLE IF NOT EXISTS TableShot(
                       TABLEID    INT    NOT NULL,
                       SHOTID     INT    NOT NULL,
                       FOREIGN KEY (TABLEID) REFERENCES TTable,
                       FOREIGN KEY (SHOTID) REFERENCES Shot)""")
        
        # Game
        cursor.execute("""CREATE TABLE IF NOT EXISTS Game(
                       GAMEID    INTEGER    NOT NULL,
                       GAMENAME  VARCHAR(64)    NOT NULL,
                       PRIMARY KEY (GAMEID AUTOINCREMENT))""")

        
        # Player
        cursor.execute("""CREATE TABLE IF NOT EXISTS Player(
                       PLAYERID    INTEGER     NOT NULL,
                       GAMEID      INTEGER     NOT NULL,
                       PLAYERNAME  VARCHAR(64) NOT NULL,
                       PRIMARY KEY (PLAYERID AUTOINCREMENT),
                       FOREIGN KEY (GAMEID) REFERENCES Game)""")

        cursor.close()
        self.conn.commit()

    def readTable( self, tableID ):

        cursor = self.conn.cursor()

        table = Table()  
        cursor.execute("SELECT COUNT(*) FROM BallTable WHERE TABLEID = ?", (tableID + 1,))
        result = cursor.fetchone()[0]


        # If TABLEID does not exist, return None
        if result == 0:
            cursor.close()
            return None  
        

        cursor.execute("SELECT TIME FROM TTable WHERE TABLEID = ?", (tableID + 1,))
        time = cursor.fetchone()[0]

        cursor.execute("""SELECT Ball.BALLID, Ball.BALLNO, Ball.XPOS, Ball.YPOS, Ball.XVEL, Ball.YVEL FROM Ball
                    JOIN BallTable ON Ball.BALLID = BallTable.BALLID
                    WHERE BallTable.TABLEID = ?""", (tableID + 1,))
        
        balls_data = cursor.fetchall()

        table.time = time 


        for ball_data in balls_data:
            pos = Coordinate(ball_data[2], ball_data[3])
            acc = Coordinate(0, 0)

            if ball_data[4] == None and  ball_data[5] == None:
                sb = StillBall(ball_data[1], pos)
                table += sb
            else:
                vel = Coordinate(ball_data[4], ball_data[5])
                aSpeed = phylib.phylib_length(vel)

                if aSpeed > VEL_EPSILON:
                    acc.x = -vel.x / aSpeed * DRAG
                    acc.y = -vel.y / aSpeed * DRAG
                rb = RollingBall(ball_data[1], pos, vel, acc)
                table += rb

        cursor.close()
        self.conn.commit()
        return table 
    
    def writeTable( self, table: Table ):

        cursor = self.conn.cursor()
        
        cursor.execute("""INSERT
                       INTO TTable (TIME)
                       VALUES (?)""",(table.time,))
        
        tableID = cursor.lastrowid
        
        
        for obj in table:

            if isinstance(obj, StillBall):
                
                cursor.execute("""INSERT
                               INTO Ball (BALLNO, XPOS, YPOS)
                               VALUES (?,?,?)""", (obj.obj.still_ball.number, obj.obj.still_ball.pos.x, obj.obj.still_ball.pos.y,))

            elif isinstance(obj, RollingBall):
                cursor.execute("""INSERT
                                INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL)
                                VALUES (?,?,?,?,?)""", (obj.obj.rolling_ball.number, obj.obj.rolling_ball.pos.x, obj.obj.rolling_ball.pos.y, obj.obj.rolling_ball.vel.x, obj.obj.rolling_ball.vel.y,))
            else:
                continue

            ballID = cursor.lastrowid


            cursor.execute("""INSERT
                       INTO BallTable (BALLID, TABLEID)
                       VALUES (?,?)""", (ballID, tableID,))



        cursor.close()
        self.conn.commit()

        return tableID - 1


    def close( self ):
        
        self.conn.commit() 
        self.conn.close()




    def getGame(self, gameID):
        cursor = self.conn.cursor()


        cursor.execute("""SELECT Game.GAMENAME, Player.PLAYERNAME FROM Game
                    JOIN Player ON Game.GAMEID = Player.GAMEID
                    WHERE Game.GAMEID = ?""", (gameID + 1,))
        
        game_data = cursor.fetchall()


        cursor.close()
        self.conn.commit()

        return game_data
    



    def setGame(self, gameName, player1Name, player2Name):

        cursor = self.conn.cursor()

        cursor.execute("""INSERT
                       INTO Game (GAMENAME)
                       VALUES (?)""", (gameName,))
        gameID = (cursor.lastrowid)



        cursor.execute("""INSERT
                       INTO Player (GAMEID, PLAYERNAME)
                       VALUES (?, ?)""", (gameID, player1Name,))
        
        cursor.execute("""INSERT
                       INTO Player (GAMEID, PLAYERNAME)
                       VALUES (?, ?)""", (gameID, player2Name,))
        


        cursor.close()
        self.conn.commit()

        return gameID - 1

    def newShot(self, gameName, playerName):

        cursor = self.conn.cursor()

        cursor.execute("""SELECT PLAYERID FROM Player WHERE PLAYERNAME = ?""", (playerName,))

        playerID = cursor.fetchone()[0]

        cursor.execute("""SELECT GAMEID FROM Game WHERE GAMENAME = ?""", (gameName,))

        gameID = cursor.fetchone()[0]


        cursor.execute("""INSERT
                       INTO Shot (GAMEID, PLAYERID)
                       VALUES (?,?)""", (gameID, playerID,))
        
        shotID = cursor.lastrowid


        cursor.close()
        self.conn.commit()

        return shotID
    
    def insertTableShot(self,tableID, shotID):

        cursor = self.conn.cursor()

        cursor.execute("""INSERT
                        INTO TableShot (TABLEID, SHOTID)
                        VALUES (?,?)""",(tableID, shotID,))
                    

                
        cursor.close()
        self.conn.commit()




class Game:



    def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):

        db = Database()
        db.createDB()

        if gameID is not None and gameName is None and player1Name is None and player2Name is None:


            game_data = Database().getGame(gameID)

            self.gameID = gameID
            self.gameName = game_data[0][0]
            self.player1Name = game_data[0][1]
            self.player2Name = game_data[1][1]



        
        elif gameID is None and gameName is not None and player1Name is not None and player2Name is not None:

            no_gameID_game_data = Database().setGame(gameName, player1Name, player2Name)

            self.gameID = no_gameID_game_data
            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name


        else:
            raise TypeError("Arguments have invalid values")



    def shoot( self, gameName, playerName, table, xvel, yvel ):

        db = Database()
        array = []


        shotID = db.newShot(gameName, playerName)
        cueBall = table.cueBall()

        if cueBall is not None:

            xpos = cueBall.obj.still_ball.pos.x
            ypos = cueBall.obj.still_ball.pos.y


            cueBall.type = phylib.PHYLIB_ROLLING_BALL

            cueBall.obj.rolling_ball.number = 0
            cueBall.obj.rolling_ball.pos.x = xpos
            cueBall.obj.rolling_ball.pos.y = ypos
            cueBall.obj.rolling_ball.vel.x = xvel
            cueBall.obj.rolling_ball.vel.y = yvel



            aSpeed = phylib.phylib_length(cueBall.obj.rolling_ball.vel)
            
            if aSpeed > VEL_EPSILON:
                cueBall.obj.rolling_ball.acc.x = -cueBall.obj.rolling_ball.vel.x / aSpeed * DRAG
                cueBall.obj.rolling_ball.acc.y = -cueBall.obj.rolling_ball.vel.y / aSpeed * DRAG


            while(table):
                
                startTime = table.time
                copy = table
                table = table.segment()
                if table is not None:
                    endTime = table.time

                finalTime = endTime - startTime
                finalTime = int(finalTime // FRAME_INTERVAL)

                for frame in range(finalTime):

                    updateTable = copy.roll(frame * FRAME_INTERVAL)
                    array.append(updateTable.svg())
                    updateTable.time = startTime + (frame * FRAME_INTERVAL)
                    tableID = db.writeTable(updateTable)
                    db.insertTableShot(tableID, shotID)

        db.close()
        return array
