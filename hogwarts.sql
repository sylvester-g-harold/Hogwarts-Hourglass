# SQL commands used in setting up the database.
# TODO: manage this properly with a database migration framework.
# For now, for simplicity's sake, we're just running manual SQL statements.
CREATE TABLE hourglass_points ( 
	id serial PRIMARY KEY,
	house varchar(20) NOT NULL,
	points integer NOT NULL,
	professor_name varchar(50) NOT NULL,
	message text,
	created_at timestamp DEFAULT current_timestamp);

# Sample insert statement
insert into hourglass_points values ('gryffindor', 5, 'kang', '5 points to gryffindor! good job bu!');

	