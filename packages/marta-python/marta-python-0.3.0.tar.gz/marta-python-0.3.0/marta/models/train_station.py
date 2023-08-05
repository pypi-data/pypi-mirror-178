from enum import Enum
from typing import List, Union

from marta.enums.train_line import TrainLine


class _TransferDistances:
    def __init__(self,
                 time_from_five_points: int,
                 stops_from_five_points: int,
                 stops_from_red: int,
                 stops_from_gold: int,
                 stops_from_blue: int,
                 stops_from_green: int):
        self.time_to_five_points = time_from_five_points
        self.stops_from_five_points = stops_from_five_points
        self.stops_from_red = stops_from_red
        self.stops_from_gold = stops_from_gold
        self.stops_from_blue = stops_from_blue
        self.stops_from_green = stops_from_green


class _TrainStation:
    def __init__(self,
                 station_name: str,
                 station_code: str,
                 address: str,
                 link: str,
                 distances: _TransferDistances,
                 lines: List[TrainLine]):
        self.station_name = station_name
        self.station_code = station_code
        self.address = address
        self.link = link
        self.distances = distances
        self.lines = lines

    @staticmethod
    def stop_count_between(from_station: '_TrainStation', to_station: '_TrainStation') -> int:
        shared_lines = set(from_station.lines) & set(to_station.lines)
        if shared_lines:
            # The two stations are on the same line(s)
            # We can compare 5p times, since we don't need to worry about a transfer
            # (start -> 5p) - (5p -> end)
            return abs(from_station.distances.stops_from_five_points - to_station.distances.stops_from_five_points)
        else:
            # The two stations are on different lines
            # We need to account for transfers
            min_stop_count = None
            # This is the traveling salesman problem, but thankfully we only have 4 lines
            for from_line in from_station.lines:
                for to_line in to_station.lines:
                    stop_before_transfer = getattr(from_station.distances, line_to_from_attribute[to_line])
                    stop_after_transfer = getattr(to_station.distances, line_to_from_attribute[from_line])
                    stop_count = abs(stop_before_transfer) + abs(stop_after_transfer)
                    if min_stop_count is None or stop_count < min_stop_count:
                        min_stop_count = stop_count
            # Count will always be something, no need to check for None
            return min_stop_count

    @staticmethod
    def time_between(from_station: '_TrainStation', to_station: '_TrainStation') -> int:
        if from_station == to_station:
            # No time to travel to the same station
            return 0

        if len(from_station.lines) == 4:
            # The from_station is five points
            return to_station.distances.time_to_five_points

        if len(to_station.lines) == 4:
            # The to_station is five points
            return from_station.distances.time_to_five_points

        if any(line in from_station.lines for line in [TrainLine.RED, TrainLine.GOLD]) and any(
                line in to_station.lines for line in [TrainLine.RED, TrainLine.GOLD]):
            # The two stations are both on the red or gold line (north-south)
            # Account for transfer at lindbergh
            # (start -> 5p - lindbergh -> 5p) + (end -> 5p - lindbergh -> 5p)

            lindbergh_to_five_points = TrainStations.LINDBERGH_CENTER.details.distances.time_to_five_points
            start_to_lindbergh = from_station.distances.time_to_five_points - lindbergh_to_five_points
            end_to_lindbergh = to_station.distances.time_to_five_points - lindbergh_to_five_points
            return abs(start_to_lindbergh) + abs(end_to_lindbergh)

        elif any(line in from_station.lines for line in [TrainLine.BLUE, TrainLine.GREEN]) and any(
                line in to_station.lines for line in [TrainLine.BLUE, TrainLine.GREEN]):
            # The two stations are both on the blue or green line (east-west)
            # Could transfer at ashby or edgewood, we'll see which is faster
            # (start -> 5p - ashby/edgewood -> 5p) - (end -> 5p - ashby/edgewood -> 5p)

            ashby_to_five_points = TrainStations.ASHBY.details.distances.time_to_five_points
            start_to_ashby = from_station.distances.time_to_five_points - ashby_to_five_points
            end_to_ashby = to_station.distances.time_to_five_points - ashby_to_five_points
            ashby_time = abs(start_to_ashby) + abs(end_to_ashby)

            edgewood_to_five_points = TrainStations.EDGWOOD_CANDLER_PARK.details.distances.time_to_five_points
            start_to_edgewood = from_station.distances.time_to_five_points - edgewood_to_five_points
            end_to_edgewood = to_station.distances.time_to_five_points - edgewood_to_five_points
            edgewood_time = abs(start_to_edgewood) + abs(end_to_edgewood)

            return min(ashby_time, edgewood_time)

        else:
            # One station is north-south and the other is east-west
            # We need to account for a transfer at five points
            # (start -> 5p) + (5p -> end)
            return abs(from_station.distances.time_to_five_points) + abs(to_station.distances.time_to_five_points)

    def stop_count_to(self, to_station: '_TrainStation') -> int:
        return _TrainStation.stop_count_between(self, to_station)

    def time_to(self, to_station: '_TrainStation') -> int:
        return _TrainStation.time_between(self, to_station)


# noinspection PyTypeChecker
class TrainStations(Enum):
    NORTH_SPRINGS = _TrainStation(
        station_name="North Springs",
        station_code="NORTH SPRINGS STATION",
        lines=[TrainLine.RED],
        address="7010 Peachtree Dunwoody Rd Sandy Springs, GA 30328",
        link="https://itsmarta.com/North-Springs.aspx",
        distances=_TransferDistances(
            time_from_five_points=27,
            stops_from_five_points=11,
            stops_from_red=0,
            stops_from_gold=5,
            stops_from_blue=11,
            stops_from_green=11,
        ))
    SANDY_SPRINGS = _TrainStation(
        station_name="Sandy Springs",
        station_code="SANDY SPRINGS STATION",
        lines=[TrainLine.RED],
        address="1101 Mount Vernon Hwy Atlanta, GA 30338",
        link="https://itsmarta.com/Sandy-Springs.aspx",
        distances=_TransferDistances(
            time_from_five_points=25,
            stops_from_five_points=10,
            stops_from_red=0,
            stops_from_gold=4,
            stops_from_blue=10,
            stops_from_green=10
        ))
    DUNWOODY = _TrainStation(
        station_name="Dunwoody",
        station_code="DUNWOODY STATION",
        lines=[TrainLine.RED],
        address="1118 Hammond Dr Atlanta, GA 30328",
        link="https://itsmarta.com/Dunwoody.aspx",
        distances=_TransferDistances(
            time_from_five_points=22,
            stops_from_five_points=9,
            stops_from_red=0,
            stops_from_gold=3,
            stops_from_blue=9,
            stops_from_green=9
        ))
    MEDICAL_CENTER = _TrainStation(
        station_name="Medical Center",
        station_code="MEDICAL CENTER STATION",
        lines=[TrainLine.RED],
        address="5711 Peachtree-Dunwoody Rd, NE Atlanta, GA 30342",
        link="https://itsmarta.com/Medical-Center.aspx",
        distances=_TransferDistances(
            time_from_five_points=20,
            stops_from_five_points=8,
            stops_from_red=0,
            stops_from_gold=2,
            stops_from_blue=8,
            stops_from_green=8
        ))
    BUCKHEAD = _TrainStation(
        station_name="Buckhead",
        station_code="BUCKHEAD STATION",
        lines=[TrainLine.RED],
        address="3360 Peachtree Rd, NE Atlanta, GA 30326",
        link="https://itsmarta.com/Buckhead.aspx",
        distances=_TransferDistances(
            time_from_five_points=16,
            stops_from_five_points=7,
            stops_from_red=0,
            stops_from_gold=1,
            stops_from_blue=7,
            stops_from_green=7
        ))
    LINDBERGH_CENTER = _TrainStation(
        station_name="Lindbergh Center",
        station_code="LINDBERGH STATION",
        lines=[TrainLine.RED, TrainLine.GOLD],
        address="2424 Piedmont Rd, NE Atlanta, GA 30324",
        link="https://itsmarta.com/Lindbergh.aspx",
        distances=_TransferDistances(
            time_from_five_points=10,
            stops_from_five_points=6,
            stops_from_red=0,
            stops_from_gold=0,
            stops_from_blue=6,
            stops_from_green=6
        ))
    ARTS_CENTER = _TrainStation(
        station_name="Arts Center",
        station_code="ARTS CENTER STATION",
        lines=[TrainLine.RED, TrainLine.GOLD],
        address="1255 West Peachtree St Atlanta, GA 30309",
        link="https://itsmarta.com/Arts-Center.aspx",
        distances=_TransferDistances(
            time_from_five_points=6,
            stops_from_five_points=5,
            stops_from_red=0,
            stops_from_gold=0,
            stops_from_blue=5,
            stops_from_green=5
        ))
    MIDTOWN = _TrainStation(
        station_name="Midtown",
        station_code="MIDTOWN STATION",
        lines=[TrainLine.RED, TrainLine.GOLD],
        address="41 Tenth St, NE Atlanta, GA 30309",
        link="https://itsmarta.com/Midtown.aspx",
        distances=_TransferDistances(
            time_from_five_points=4,
            stops_from_five_points=4,
            stops_from_red=0,
            stops_from_gold=0,
            stops_from_blue=4,
            stops_from_green=4
        ))
    NORTH_AVENUE = _TrainStation(
        station_name="North Avenue",
        station_code="NORTH AVE STATION",
        lines=[TrainLine.RED, TrainLine.GOLD],
        address="713 West Peachtree St, NW Atlanta, GA 30308",
        link="https://itsmarta.com/North-Ave.aspx",
        distances=_TransferDistances(
            time_from_five_points=3,
            stops_from_five_points=3,
            stops_from_red=0,
            stops_from_gold=0,
            stops_from_blue=3,
            stops_from_green=3
        ))
    CIVIC_CENTER = _TrainStation(
        station_name="Civic Center",
        station_code="CIVIC CENTER STATION",
        lines=[TrainLine.RED, TrainLine.GOLD],
        address="435 West Peachtree St, NW Atlanta, GA 30308",
        link="https://itsmarta.com/Civic-Center.aspx",
        distances=_TransferDistances(
            time_from_five_points=2,
            stops_from_five_points=2,
            stops_from_red=0,
            stops_from_gold=0,
            stops_from_blue=2,
            stops_from_green=2
        ))
    PEACHTREE_CENTER = _TrainStation(
        station_name="Peachtree Center",
        station_code="PEACHTREE CENTER STATION",
        lines=[TrainLine.RED, TrainLine.GOLD],
        address="216 Peachtree St, NE Atlanta, GA 30303",
        link="https://itsmarta.com/Peachtree-Center.aspx",
        distances=_TransferDistances(
            time_from_five_points=1,
            stops_from_five_points=1,
            stops_from_red=0,
            stops_from_gold=0,
            stops_from_blue=1,
            stops_from_green=1
        ))
    FIVE_POINTS = _TrainStation(
        station_name="Five Points",
        station_code="FIVE POINTS STATION",
        lines=[TrainLine.RED, TrainLine.GOLD, TrainLine.BLUE, TrainLine.GREEN],
        address="30 Alabama St SW Atlanta, GA 30303",
        link="https://itsmarta.com/Five-Points.aspx",
        distances=_TransferDistances(
            time_from_five_points=0,
            stops_from_five_points=0,
            stops_from_red=0,
            stops_from_gold=0,
            stops_from_blue=0,
            stops_from_green=0
        ))
    GARNETT = _TrainStation(
        station_name="Garnett",
        station_code="GARNETT STATION",
        lines=[TrainLine.RED, TrainLine.GOLD],
        address="225 Peachtree St, SW Atlanta, GA 30303",
        link="https://itsmarta.com/Garnett.aspx",
        distances=_TransferDistances(
            time_from_five_points=-1,
            stops_from_five_points=-1,
            stops_from_red=0,
            stops_from_gold=0,
            stops_from_blue=-1,
            stops_from_green=-1
        ))
    WEST_END = _TrainStation(
        station_name="West End",
        station_code="WEST END STATION",
        lines=[TrainLine.RED, TrainLine.GOLD],
        address="680 Lee St, SW Atlanta, GA 30310",
        link="https://itsmarta.com/West-End.aspx",
        distances=_TransferDistances(
            time_from_five_points=-4,
            stops_from_five_points=-2,
            stops_from_red=0,
            stops_from_gold=0,
            stops_from_blue=-2,
            stops_from_green=-2
        ))
    OAKLAND_CITY = _TrainStation(
        station_name="Oakland City",
        station_code="OAKLAND CITY STATION",
        lines=[TrainLine.RED, TrainLine.GOLD],
        address="1400 Lee St, SW Atlanta, GA 30310",
        link="https://itsmarta.com/Oakland-City.aspx",
        distances=_TransferDistances(
            time_from_five_points=-6,
            stops_from_five_points=-3,
            stops_from_red=0,
            stops_from_gold=0,
            stops_from_blue=-3,
            stops_from_green=-3
        ))
    LAKEWOOD_FORT_MCPHERSON = _TrainStation(
        station_name="Lakewood/Fort McPherson",
        station_code="LAKEWOOD STATION",
        lines=[TrainLine.RED, TrainLine.GOLD],
        address="2020 Lee St, SW Atlanta, GA 30310",
        link="https://itsmarta.com/Lakewood.aspx",
        distances=_TransferDistances(
            time_from_five_points=-8,
            stops_from_five_points=-4,
            stops_from_red=0,
            stops_from_gold=0,
            stops_from_blue=-4,
            stops_from_green=-4
        ))
    EAST_POINT = _TrainStation(
        station_name="East Point",
        station_code="EAST POINT STATION",
        lines=[TrainLine.RED, TrainLine.GOLD],
        address="2848 East Main St East Point, GA 30344",
        link="https://itsmarta.com/East-Point.aspx",
        distances=_TransferDistances(
            time_from_five_points=-12,
            stops_from_five_points=-5,
            stops_from_red=0,
            stops_from_gold=0,
            stops_from_blue=-5,
            stops_from_green=-5
        ))
    COLLEGE_PARK = _TrainStation(
        station_name="College Park",
        station_code="COLLEGE PARK STATION",
        lines=[TrainLine.RED, TrainLine.GOLD],
        address="3800 Main St Atlanta, GA 30337",
        link="https://itsmarta.com/College-Park.aspx",
        distances=_TransferDistances(
            time_from_five_points=-15,
            stops_from_five_points=-6,
            stops_from_red=0,
            stops_from_gold=0,
            stops_from_blue=-6,
            stops_from_green=-6
        ))
    AIRPORT = _TrainStation(
        station_name="Airport",
        station_code="AIRPORT STATION",
        lines=[TrainLine.RED, TrainLine.GOLD],
        address="6000 S Terminal Pkwy Atlanta, GA 30337",
        link="https://itsmarta.com/Airport.aspx",
        distances=_TransferDistances(
            time_from_five_points=-15,
            stops_from_five_points=-7,
            stops_from_red=0,
            stops_from_gold=0,
            stops_from_blue=-7,
            stops_from_green=-7
        ))
    DORAVILLE = _TrainStation(
        station_name="Doraville",
        station_code="DORAVILLE STATION",
        lines=[TrainLine.GOLD],
        address="6000 New Peachtree Rd Doraville, GA 30340",
        link="https://itsmarta.com/Doraville.aspx",
        distances=_TransferDistances(
            time_from_five_points=24,
            stops_from_five_points=10,
            stops_from_red=4,
            stops_from_gold=0,
            stops_from_blue=10,
            stops_from_green=10
        ))
    CHAMBLEE = _TrainStation(
        station_name="Chamblee",
        station_code="CHAMBLEE STATION",
        lines=[TrainLine.GOLD],
        address="5200 New Peachtree Road Chamblee, GA 30341",
        link="https://itsmarta.com/Chamblee.aspx",
        distances=_TransferDistances(
            time_from_five_points=21,
            stops_from_five_points=9,
            stops_from_red=3,
            stops_from_gold=0,
            stops_from_blue=9,
            stops_from_green=9
        ))
    BROOKHAVEN_OGLETHORPE = _TrainStation(
        station_name="Brookhaven/Oglethorpe",
        station_code="BROOKHAVEN STATION",
        lines=[TrainLine.GOLD],
        address="4047 Peachtree Road, NE Atlanta, GA 30319",
        link="https://itsmarta.com/Brookhaven.aspx",
        distances=_TransferDistances(
            time_from_five_points=17,
            stops_from_five_points=8,
            stops_from_red=2,
            stops_from_gold=0,
            stops_from_blue=8,
            stops_from_green=8
        ))
    LENOX = _TrainStation(
        station_name="Lenox",
        station_code="LENOX STATION",
        lines=[TrainLine.GOLD],
        address="955 East Paces Ferry Rd, NE Atlanta, GA 30326",
        link="https://itsmarta.com/Lenox.aspx",
        distances=_TransferDistances(
            time_from_five_points=14,
            stops_from_five_points=7,
            stops_from_red=1,
            stops_from_gold=0,
            stops_from_blue=7,
            stops_from_green=7
        ))
    HAMILTON_E_HOLMES = _TrainStation(
        station_name="Hamilton E. Holmes",
        station_code="HAMILTON E HOLMES STATION",
        lines=[TrainLine.BLUE],
        address="70 Hamilton E Holmes Dr, NW Atlanta, GA 30311",
        link="https://itsmarta.com/Hamilton-E-Holmes.aspx",
        distances=_TransferDistances(
            time_from_five_points=-9,
            stops_from_five_points=-5,
            stops_from_red=-5,
            stops_from_gold=-5,
            stops_from_blue=0,
            stops_from_green=-2
        ))
    WEST_LAKE = _TrainStation(
        station_name="West Lake",
        station_code="WEST LAKE STATION",
        lines=[TrainLine.BLUE],
        address="80 Anderson Ave, SW Atlanta, GA 30314",
        link="https://itsmarta.com/West-Lake.aspx",
        distances=_TransferDistances(
            time_from_five_points=-6,
            stops_from_five_points=-4,
            stops_from_red=-4,
            stops_from_gold=-4,
            stops_from_blue=0,
            stops_from_green=-1
        ))
    ASHBY = _TrainStation(
        station_name="Ashby",
        station_code="ASHBY STATION",
        lines=[TrainLine.BLUE, TrainLine.GREEN],
        address="65 Joseph E Lowery Blvd Atlanta, GA 30314",
        link="https://itsmarta.com/Ashby.aspx",
        distances=_TransferDistances(
            time_from_five_points=-3,
            stops_from_five_points=-3,
            stops_from_red=-3,
            stops_from_gold=-3,
            stops_from_blue=0,
            stops_from_green=0
        ))
    VINE_CITY = _TrainStation(
        station_name="Vine City",
        station_code="VINE CITY STATION",
        lines=[TrainLine.BLUE, TrainLine.GREEN],
        address="502 Rhodes St, NW Atlanta, GA 30314",
        link="https://itsmarta.com/Vine-City.aspx",
        distances=_TransferDistances(
            time_from_five_points=-2,
            stops_from_five_points=-2,
            stops_from_red=-2,
            stops_from_gold=-2,
            stops_from_blue=0,
            stops_from_green=0
        ))
    GWCC_CNN_CENTER = _TrainStation(
        station_name="GWCC/CNN Center",
        station_code="OMNI DOME STATION",
        lines=[TrainLine.BLUE, TrainLine.GREEN],
        address="100 Centennial Olympic Park Atlanta, GA 30303",
        link="https://itsmarta.com/Omni.aspx",
        distances=_TransferDistances(
            time_from_five_points=-1,
            stops_from_five_points=-1,
            stops_from_red=-1,
            stops_from_gold=-1,
            stops_from_blue=0,
            stops_from_green=0
        ))
    GEORGIA_STATE = _TrainStation(
        station_name="Georgia State",
        station_code="GEORGIA STATE STATION",
        lines=[TrainLine.BLUE, TrainLine.GREEN],
        address="170 Piedmont Ave, SE Atlanta, GA 30303",
        link="https://itsmarta.com/Georgia-State.aspx",
        distances=_TransferDistances(
            time_from_five_points=1,
            stops_from_five_points=1,
            stops_from_red=1,
            stops_from_gold=1,
            stops_from_blue=0,
            stops_from_green=0
        ))
    KING_MEMORIAL = _TrainStation(
        station_name="King Memorial",
        station_code="KING MEMORIAL STATION",
        lines=[TrainLine.BLUE, TrainLine.GREEN],
        address="377 Decatur St, SE Atlanta, GA 30312",
        link="https://itsmarta.com/King-Memorial.aspx",
        distances=_TransferDistances(
            time_from_five_points=3,
            stops_from_five_points=2,
            stops_from_red=2,
            stops_from_gold=2,
            stops_from_blue=0,
            stops_from_green=0
        ))
    INMAN_PARK_REYNOLDSTOWN = _TrainStation(
        station_name="Inman Park/Reynoldstown",
        station_code="INMAN PARK STATION",
        lines=[TrainLine.BLUE, TrainLine.GREEN],
        address="1055 DeKalb Ave, NE Atlanta, GA 30307",
        link="https://itsmarta.com/Inman-Park.aspx",
        distances=_TransferDistances(
            time_from_five_points=6,
            stops_from_five_points=3,
            stops_from_red=3,
            stops_from_gold=3,
            stops_from_blue=0,
            stops_from_green=0
        ))
    EDGWOOD_CANDLER_PARK = _TrainStation(
        station_name="Edgewood/Candler Park",
        station_code="EDGEWOOD CANDLER PARK STATION",
        lines=[TrainLine.BLUE, TrainLine.GREEN],
        address="1475 DeKalb Ave, NE Atlanta, GA 30307",
        link="https://itsmarta.com/Edgewood-Candler-Park.aspx",
        distances=_TransferDistances(
            time_from_five_points=8,
            stops_from_five_points=4,
            stops_from_red=4,
            stops_from_gold=4,
            stops_from_blue=0,
            stops_from_green=0
        ))
    EAST_LAKE = _TrainStation(
        station_name="East Lake",
        station_code="EAST LAKE STATION",
        lines=[TrainLine.BLUE],
        address="2260 College Ave Atlanta, GA 30307",
        link="https://itsmarta.com/East-Lake.aspx",
        distances=_TransferDistances(
            time_from_five_points=11,
            stops_from_five_points=5,
            stops_from_red=5,
            stops_from_gold=5,
            stops_from_blue=0,
            stops_from_green=1
        ))
    DECATUR = _TrainStation(
        station_name="Decatur",
        station_code="DECATUR STATION",
        lines=[TrainLine.BLUE],
        address="400 Church St Decatur, GA 30030",
        link="https://itsmarta.com/Decatur.aspx",
        distances=_TransferDistances(
            time_from_five_points=13,
            stops_from_five_points=6,
            stops_from_red=6,
            stops_from_gold=6,
            stops_from_blue=0,
            stops_from_green=2
        ))
    AVONDALE = _TrainStation(
        station_name="Avondale",
        station_code="AVONDALE STATION",
        lines=[TrainLine.BLUE],
        address="915 E Ponce de Leon Ave Decatur, GA 30030",
        link="https://itsmarta.com/Avondale.aspx",
        distances=_TransferDistances(
            time_from_five_points=15,
            stops_from_five_points=7,
            stops_from_red=7,
            stops_from_gold=7,
            stops_from_blue=0,
            stops_from_green=3
        ))
    KENSINGTON = _TrainStation(
        station_name="Kensington",
        station_code="KENSINGTON STATION",
        lines=[TrainLine.BLUE],
        address="3350 Kensington Rd Decatur, GA 30032",
        link="https://itsmarta.com/Kensington.aspx",
        distances=_TransferDistances(
            time_from_five_points=18,
            stops_from_five_points=8,
            stops_from_red=8,
            stops_from_gold=8,
            stops_from_blue=0,
            stops_from_green=4
        ))
    INDIAN_CREEK = _TrainStation(
        station_name="Indian Creek",
        station_code="INDIAN CREEK STATION",
        lines=[TrainLine.BLUE],
        address="901 Durham Park Rd Stone Mountain, GA 30083",
        link="https://itsmarta.com/Indian-Creek.aspx",
        distances=_TransferDistances(
            time_from_five_points=20,
            stops_from_five_points=9,
            stops_from_red=9,
            stops_from_gold=9,
            stops_from_blue=0,
            stops_from_green=5
        ))
    BANKHEAD = _TrainStation(
        station_name="Bankhead",
        station_code="BANKHEAD STATION",
        lines=[TrainLine.GREEN],
        address="1335 Donald Hollowell Pkwy Atlanta, GA 30318",
        link="https://itsmarta.com/Bankhead.aspx",
        distances=_TransferDistances(
            time_from_five_points=-9,
            stops_from_five_points=-4,
            stops_from_red=-4,
            stops_from_gold=-4,
            stops_from_blue=-1,
            stops_from_green=0
        ))

    @property
    def details(self) -> _TrainStation:
        return self.value

    @staticmethod
    def from_keyword(keyword: str) -> Union['TrainStations', None]:
        return train_station_nicknames.get(keyword, None)


train_station_nicknames = {
    '5': TrainStations.FIVE_POINTS,
    '5points': TrainStations.FIVE_POINTS,
    '5pts': TrainStations.FIVE_POINTS,
    'airport': TrainStations.AIRPORT,
    'arena': TrainStations.GWCC_CNN_CENTER,
    'arts': TrainStations.ARTS_CENTER,
    'artscenter': TrainStations.ARTS_CENTER,
    'ashby': TrainStations.ASHBY,
    'avenue': TrainStations.NORTH_AVENUE,
    'avondale': TrainStations.AVONDALE,
    'bankhead': TrainStations.BANKHEAD,
    'basketball': TrainStations.GWCC_CNN_CENTER,
    'benz': TrainStations.GWCC_CNN_CENTER,
    'brookhaven': TrainStations.BROOKHAVEN_OGLETHORPE,
    'buckhead': TrainStations.BUCKHEAD,
    'candler': TrainStations.EDGWOOD_CANDLER_PARK,
    'candlerpark': TrainStations.EDGWOOD_CANDLER_PARK,
    'capitol': TrainStations.GWCC_CNN_CENTER,
    'chamblee': TrainStations.CHAMBLEE,
    'civic': TrainStations.CIVIC_CENTER,
    'civiccenter': TrainStations.CIVIC_CENTER,
    'cnn': TrainStations.GWCC_CNN_CENTER,
    'cnncenter': TrainStations.GWCC_CNN_CENTER,
    'college': TrainStations.COLLEGE_PARK,
    'collegepark': TrainStations.COLLEGE_PARK,
    'congress': TrainStations.GWCC_CNN_CENTER,
    'decatur': TrainStations.DECATUR,
    'dome': TrainStations.GWCC_CNN_CENTER,
    'doraville': TrainStations.DORAVILLE,
    'dunwoody': TrainStations.DUNWOODY,
    'eastlake': TrainStations.EAST_LAKE,
    'eastpoint': TrainStations.EAST_POINT,
    'edgewood': TrainStations.EDGWOOD_CANDLER_PARK,
    'edgewood/candler': TrainStations.EDGWOOD_CANDLER_PARK,
    'edgewood/candlerpark': TrainStations.EDGWOOD_CANDLER_PARK,
    'edgewoodcandlerpark': TrainStations.EDGWOOD_CANDLER_PARK,
    'end': TrainStations.WEST_END,
    'falcons': TrainStations.GWCC_CNN_CENTER,
    'farm': TrainStations.GWCC_CNN_CENTER,
    'five': TrainStations.FIVE_POINTS,
    'fivepoints': TrainStations.FIVE_POINTS,
    'fivepts': TrainStations.FIVE_POINTS,
    'football': TrainStations.GWCC_CNN_CENTER,
    'fort': TrainStations.LAKEWOOD_FORT_MCPHERSON,
    'garnett': TrainStations.GARNETT,
    'georgia': TrainStations.GEORGIA_STATE,
    'georgiastate': TrainStations.GEORGIA_STATE,
    'georgiastateuniversity': TrainStations.GEORGIA_STATE,
    'georgiatech': TrainStations.NORTH_AVENUE,
    'georgiaworldcongresscenter': TrainStations.GWCC_CNN_CENTER,
    'gsu': TrainStations.GEORGIA_STATE,
    'gt': TrainStations.NORTH_AVENUE,
    'gwcc': TrainStations.GWCC_CNN_CENTER,
    'h.e.holmes': TrainStations.HAMILTON_E_HOLMES,
    'hamilton': TrainStations.HAMILTON_E_HOLMES,
    'hamiltoneholmes': TrainStations.HAMILTON_E_HOLMES,
    'hamiltonholmes': TrainStations.HAMILTON_E_HOLMES,
    'hartsfield': TrainStations.AIRPORT,
    'hartsfieldjackson': TrainStations.AIRPORT,
    'hawks': TrainStations.GWCC_CNN_CENTER,
    'heholmes': TrainStations.HAMILTON_E_HOLMES,
    'hockey': TrainStations.GWCC_CNN_CENTER,
    'holmes': TrainStations.HAMILTON_E_HOLMES,
    'indian': TrainStations.INDIAN_CREEK,
    'indiancreek': TrainStations.INDIAN_CREEK,
    'inman': TrainStations.INMAN_PARK_REYNOLDSTOWN,
    'inmanpark': TrainStations.INMAN_PARK_REYNOLDSTOWN,
    'inmanpark/reynoldstown': TrainStations.INMAN_PARK_REYNOLDSTOWN,
    'inmanparkreynoldstown': TrainStations.INMAN_PARK_REYNOLDSTOWN,
    'jackson': TrainStations.AIRPORT,
    'kensington': TrainStations.KENSINGTON,
    'king': TrainStations.KING_MEMORIAL,
    'kingmemorial': TrainStations.KING_MEMORIAL,
    'lakewood': TrainStations.LAKEWOOD_FORT_MCPHERSON,
    'lakewood/fortmcpherson': TrainStations.LAKEWOOD_FORT_MCPHERSON,
    'lakewoodfortmcpherson': TrainStations.LAKEWOOD_FORT_MCPHERSON,
    'lenox': TrainStations.LENOX,
    'lindbergh': TrainStations.LINDBERGH_CENTER,
    'mcpherson': TrainStations.LAKEWOOD_FORT_MCPHERSON,
    'medcenter': TrainStations.MEDICAL_CENTER,
    'medical': TrainStations.MEDICAL_CENTER,
    'medicalcenter': TrainStations.MEDICAL_CENTER,
    'mercedes': TrainStations.GWCC_CNN_CENTER,
    'mercedes-benz': TrainStations.GWCC_CNN_CENTER,
    'mercedesbenz': TrainStations.GWCC_CNN_CENTER,
    'midtown': TrainStations.MIDTOWN,
    'mlk': TrainStations.KING_MEMORIAL,
    'northave': TrainStations.NORTH_AVENUE,
    'northavenue': TrainStations.NORTH_AVENUE,
    'northsprings': TrainStations.NORTH_SPRINGS,
    'oakland': TrainStations.OAKLAND_CITY,
    'oaklandcity': TrainStations.OAKLAND_CITY,
    'olgethorpe': TrainStations.BROOKHAVEN_OGLETHORPE,
    'omnidome': TrainStations.GWCC_CNN_CENTER,
    'peachtree': TrainStations.PEACHTREE_CENTER,
    'peachtreecenter': TrainStations.PEACHTREE_CENTER,
    'philips': TrainStations.GWCC_CNN_CENTER,
    'philipsarena': TrainStations.GWCC_CNN_CENTER,
    'point': TrainStations.EAST_POINT,
    'reynoldstown': TrainStations.INMAN_PARK_REYNOLDSTOWN,
    'sandy': TrainStations.SANDY_SPRINGS,
    'sandysprings': TrainStations.SANDY_SPRINGS,
    'school': TrainStations.GEORGIA_STATE,
    'springs': TrainStations.NORTH_SPRINGS,
    'state': TrainStations.GEORGIA_STATE,
    'statefarm': TrainStations.GWCC_CNN_CENTER,
    'statefarmarena': TrainStations.GWCC_CNN_CENTER,
    'tech': TrainStations.NORTH_AVENUE,
    'thrashers': TrainStations.GWCC_CNN_CENTER,
    'vine': TrainStations.VINE_CITY,
    'vinecity': TrainStations.VINE_CITY,
    'westend': TrainStations.WEST_END,
    'westlake': TrainStations.WEST_LAKE,
    'world': TrainStations.GWCC_CNN_CENTER,
    'worldcongress': TrainStations.GWCC_CNN_CENTER,
    'worldcongresscenter': TrainStations.GWCC_CNN_CENTER,
}

line_to_from_attribute = {
    TrainLine.BLUE: 'stops_from_blue',
    TrainLine.GREEN: 'stops_from_green',
    TrainLine.GOLD: 'stops_from_gold',
    TrainLine.RED: 'stops_from_red',
}
