 CREATE TABLE IF NOT EXISTS ADOPTION(
    recorded_name VARCHAR,
    date_id INT FOREIGN KEY,
    outcome_id INT FOREIGN KEY,
    Animal_id INT FOREIGN KEY,
    Sex VARCHAR,
    Breed_id INT FOREIGN KEY,
    Color VARCHAR,
    ID VARCHAR
    );

CREATE TABLE IF NOT EXISTS OUTCOME(
    outcome VARCHAR,
    outcome_id INT PRIMARY KEY
  );

  CREATE TABLE IF NOT EXISTS ANIMAL(
    Animal VARCHAR,
    Animal_id INT PRIMARY KEY
  );

  CREATE TABLE IF NOT EXISTS BREED(
    Breed VARCHAR,
    Breed_id INT PRIMARY KEY
  );

CREATE TABLE IF NOT EXISTS DATE(
    Dt timestamp,
    date_id INT PRIMARY KEY,
    Mnt INT,
    Yr INT

  );
