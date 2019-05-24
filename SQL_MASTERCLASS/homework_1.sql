SELECT firstname, lastname, LEFT(firstname,1) || LEFT(lastname,1)
FROM sql_masterclass.users LIMIT 10;