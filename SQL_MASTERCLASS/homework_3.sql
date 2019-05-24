-- Get total number of unsold tickets per venue in Ohio state
select *
from sql_masterclass.listing limit 10;
select *
from sql_masterclass.sales limit 10;
select *
from sql_masterclass.event limit 10;
select *
from sql_masterclass.venue limit 10;



select v1, sold, unsold
from
(select venuename, sum(qtysold) as sold
from sql_masterclass.venue v, sql_masterclass.event e, sql_masterclass.sales s
where v.venueid = e.venueid and e.eventid = s.eventid and v.venuestate='OH'
group by venuename) as a(v1, sold)
join
(select venuename, sum(numtickets)-sum(qtysold) as unsold
from sql_masterclass.venue v, sql_masterclass.event e, sql_masterclass.sales s, sql_masterclass.listing l
where v.venueid = e.venueid and e.eventid = s.eventid and v.venuestate='OH'
and s.listid = l.listid
group by venuename) as b(v2, unsold)
on a.v1 = b.v2
order by 1;
