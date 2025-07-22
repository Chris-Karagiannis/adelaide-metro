# Create tables
import sqlite3

conn = sqlite3.connect('adel-metro.db')

sql = \
'''
CREATE TABLE Routes ( 
    RouteID VARCHAR(10) PRIMARY KEY,
    Name TEXT NOT NULL,
    Description TEXT NOT NULL,
    Colour CHAR(6) NOT NULL
);

CREATE TABLE Shapes (
    ShapeID INT NOT NULL, 
    ShapeSeqNo INT NOT NULL, 
    Latitude FLOAT NOT NULL, 
    Longitude FLOAT NOT NULL, 
    DistanceTraveled FLOAT NOT NULL,
    CONSTRAINT shapesPk PRIMARY KEY (ShapeID, ShapeSeqNo)
);

CREATE TABLE Trips (
    TripID VARCHAR(20) NOT NULL, 
    RouteID VARCHAR(10) NOT NULL, 
    ShapeID INT NOT NULL, 
    CONSTRAINT tripPk PRIMARY KEY (TripID), 
    CONSTRAINT routeFk FOREIGN KEY (RouteID) REFERENCES Routes (RouteID), 
    CONSTRAINT shapeFk FOREIGN KEY (ShapeID) REFERENCES Shapes (ShapeID)
);

CREATE TABLE Stops (
    StopID INT NOT NULL, 
    StopName TEXT NOT NULL, 
    StopDescription TEXT NOT NULL, 
    Latitude FLOAT NOT NULL, 
    Longitude FLOAT NOT NULL, 
    Url TEXT NOT NULL, 
    CONSTRAINT stopPk PRIMARY KEY (StopID)
);

CREATE TABLE StopTimes ( 
    StopTimeID INTEGER PRIMARY KEY AUTOINCREMENT,
    StopID INT NOT NULL,
    TripID VARCHAR(20) NOT NULL,
    ArrivalTime TEXT NOT NULL,
    DepartureTime TEXT NOT NULL,
    CONSTRAINT stopTimeFk1 FOREIGN KEY (StopID) REFERENCES Stops (StopID),
    CONSTRAINT stopTimeFk2 FOREIGN KEY (TripID) REFERENCES Trips (TripID)
);
'''

conn.execute(sql)
conn.close()