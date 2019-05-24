------- DISTANCE FUNCTION ---------
CREATE FUNCTION DISTANCE (orig_lat float, orig_long float, dest_lat float, dest_long float)
  RETURNS float
STABLE  
AS $$
  import math
  r = 6371          
  phi_orig = math.radians(orig_lat)
  phi_dest = math.radians(dest_lat)
  delta_lat = math.radians(dest_lat - orig_lat)
  delta_long = math.radians(dest_long - orig_long)
  a = math.sin(delta_lat/2) * math.sin(delta_lat/2) + math.cos(phi_orig) \
      * math.cos(phi_dest) * math.sin(delta_long/2) * math.sin(delta_long/2)
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
  d = r * c
  return d
$$ LANGUAGE plpythonu;


dist =# SELECT DISTANCE(40.4168, -3.7038, 41.3851, 2.1734) AS dist;