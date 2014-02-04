CREATE TABLE IF NOT EXISTS sholl_analysis (
	filename TEXT PRIMARY KEY NOT NULL,
	data TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS feature (
	method TEXT NOT NULL,
	filename TEXT NOT NULL,
	sprout_count REAL NOT NULL,
	critical_value REAL NOT NULL,
	sprout_maximum REAL NOT NULL,
	ramification_index REAL NOT NULL,
	branching_count REAL NOT NULL,
	troc_average REAL NOT NULL,
	PRIMARY KEY (method, filename)
);

CREATE TABLE IF NOT EXISTS training (
	filename TEXT NOT NULL PRIMARY KEY,
	sprout_max_count INT NOT NULL,
	sprout_total_count INT NOT NULL,
	sprout_focus_count INT NOT NULL,
	branching_count INT NOT NULL
);

CREATE VIEW overview AS
	SELECT pred.method, 
		AVG((pred.sprout_count - act.sprout_focus_count) 
			* (pred.sprout_count - act.sprout_focus_count)) AS sprout_count_mse,
		AVG((pred.branching_count - act.branching_count) 
			* (pred.branching_count - act.branching_count)) AS branching_count_mse,
		AVG((pred.sprout_maximum - act.sprout_total_count) 
			* (pred.sprout_maximum - act.sprout_total_count)) AS sprout_total_mse
		FROM feature AS pred
		INNER JOIN training AS act
			ON pred.filename = act.filename
		GROUP BY pred.method;

CREATE VIEW best AS
	SELECT method, MIN(sprout_count_mse), MIN(branching_count_mse)
		FROM overview;
