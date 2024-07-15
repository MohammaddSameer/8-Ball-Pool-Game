import sys; # used to get argv
import cgi; # used to parse Mutlipart FormData 
            # this should be replace with multipart in the future
import Physics
import os
import math


# Used parts from lab 2 below

# web server parts
from http.server import HTTPServer, BaseHTTPRequestHandler;

# used to parse the URL and extract form data for GET requests
from urllib.parse import urlparse, parse_qsl;

table_id = 0

# handler for our web-server - handles both GET and POST requests
class MyHandler( BaseHTTPRequestHandler ):
    def do_GET(self):
        global table_id
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path )

        # check if the web-pages matches the list
        if parsed.path in [ '/pool.html' ]:

            # retreive the HTML file
            fp = open( '.'+self.path )
            content = fp.read()

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" )
            self.send_header( "Content-length", len( content ) )
            self.end_headers()

            SVGTable = Physics.Table()

            ball1 = Physics.Coordinate(float(676), float(2025))
            ball2 = Physics.Coordinate(float(737), float(455))
            ball3 = Physics.Coordinate(float(800), float(455))
            ball4 = Physics.Coordinate(float(677), float(453))
            ball5 = Physics.Coordinate(float(615), float(455))
            ball6 = Physics.Coordinate(float(550), float(455))
            ball7 = Physics.Coordinate(float(585), float(509))
            ball8 = Physics.Coordinate(float(645), float(508))
            ball9 = Physics.Coordinate(float(675), float(565))
            ball10 = Physics.Coordinate(float(707), float(509))
            ball11 = Physics.Coordinate(float(767), float(511))
            ball12 = Physics.Coordinate(float(615), float(565))
            ball13 = Physics.Coordinate(float(733), float(566))
            ball14 = Physics.Coordinate(float(705), float(622))
            ball15 = Physics.Coordinate(float(645), float(622))
            ball16 = Physics.Coordinate(float(675), float(675))

            sb1 = Physics.StillBall(0, ball1)
            sb2 = Physics.StillBall(1, ball2)
            sb3 = Physics.StillBall(2, ball3)
            sb4 = Physics.StillBall(3, ball4)
            sb5 = Physics.StillBall(4, ball5)
            sb6 = Physics.StillBall(5, ball6)
            sb7 = Physics.StillBall(6, ball7)
            sb8 = Physics.StillBall(7, ball8)
            sb9 = Physics.StillBall(8, ball9)
            sb10 = Physics.StillBall(9, ball10)
            sb11 = Physics.StillBall(10, ball11)
            sb12 = Physics.StillBall(11, ball12)
            sb13 = Physics.StillBall(12, ball13)
            sb14 = Physics.StillBall(13, ball14)
            sb15 = Physics.StillBall(14, ball15)
            sb16 = Physics.StillBall(15, ball16)

            SVGTable +=sb1
            SVGTable +=sb2
            SVGTable +=sb3
            SVGTable +=sb4
            SVGTable +=sb5
            SVGTable +=sb6
            SVGTable +=sb7
            SVGTable +=sb8
            SVGTable +=sb9
            SVGTable +=sb10
            SVGTable +=sb11
            SVGTable +=sb12
            SVGTable +=sb13
            SVGTable +=sb14
            SVGTable +=sb15
            SVGTable +=sb16

            file = open("table00.svg", "w")
            svgString = SVGTable.svg()
            file.write(svgString)
            file.close()
            
            
            db = Physics.Database()
            db.createDB()
            table_id = db.writeTable(SVGTable)

            # send it to the broswer
            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close()

        # check if the web-pages matches the list
        elif parsed.path.startswith("/table") and parsed.path.endswith(".svg"):

            # this one is different because its an image file

            # retreive the JPG file (binary, not text file)
            fp = open( '.'+self.path, 'rb' );
            content = fp.read()

            self.send_response( 200 ); # OK
                # notice the change in Content-type
            self.send_header( "Content-type", "image/svg+xml" )
            self.send_header( "Content-length", len( content ) )
            self.end_headers()

            self.wfile.write( content );    # binary file
            fp.close()

        else:
            # generate 404 for GET requests that aren't the 3 files above
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )


    def do_POST(self):
        global table_id
        # hanle post request
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path )

        if parsed.path in [ '/display.html' ]:

            # get data send as Multipart FormData (MIME format)
            form = cgi.FieldStorage( fp=self.rfile,
                                     headers=self.headers,
                                     environ = { 'REQUEST_METHOD': 'POST',
                                                 'CONTENT_TYPE': 
                                                   self.headers['Content-Type'],
                                               } 
                                   )
            
            velX = form.getvalue('velocityX')
            velY = form.getvalue('velocityY')
            # cueBallX = form.getvalue('cueBallPosX')
            # cueBallY = form.getvalue('cueBallPosY')
            # Physics.Database(reset=True).close()

            postTable = Physics.Table()
            postDatabase = Physics.Database()

            postTable = postDatabase.readTable(table_id)

            if postTable is None:
                print("Test")
        
            game = Physics.Game(gameName= "Game 05", player1Name= "harden", player2Name="taylor")

            svgArray = game.shoot("Game 05", "harden", postTable, float(velX), float(velY))

            svgString = "|".join(svgArray)




            # i = 0

            # while postTable:

            #     with open("table%d.svg" % (i),"w") as file:
            #         file.write(postTable.svg())
            #     i +=1
            #     postTable = postTable.segment()

            # def write_svg( table_id, table ):
            #     with open( "table%02d.svg" % table_id, "w" ) as fp:
            #         fp.write( table.svg() );

            # # db = Physics.Database();

            # # table_id = 0;
            # table = postDatabase.readTable( table_id );

            # write_svg( table_id, table );

            # while table:
            #     table_id += 1;
            #     table = postDatabase.readTable( table_id );
            #     if not table:
            #         break;
            #     write_svg( table_id, table );

            # postDatabase.close();

            



            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" )
            self.send_header( "Content-length", len( svgString) )
            self.end_headers()

            # send it to the browser
            self.wfile.write( bytes( svgString, "utf-8" ) )
            # fp.close()

        else:
            # generate 404 for POST requests that aren't the file above
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )


if __name__ == "__main__":
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler )
    print( "Server listing in port:  ", int(sys.argv[1]) )
    httpd.serve_forever()


