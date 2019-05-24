drop table if exists
	coordinates;

create temp table coordinates
(
    lat1 float,
    lon1 float,
    lat2 float,
    lon2 float
);

insert into
	coordinates
values
	(40.4168, -3.7038, 41.3851, 2.1734);


-- Haversine formula:
SELECT 2 * 6371 * asin(sqrt((sin(radians((lat2 - lat1) / 2))) ^ 2 + cos(radians(lat1)) 
				* cos(radians(lat2)) * (sin(radians((lon2 - lon1) / 2))) ^ 2)) as distance
from coordinates; 

SELECT 2 * 6371 * asin(sqrt((sin(radians((41.3851 - 40.4168) / 2))) ^ 2 + cos(radians(40.4168)) 
				* cos(radians(41.3851)) * (sin(radians((2.1734 - -3.7038) / 2))) ^ 2)) as distance;
