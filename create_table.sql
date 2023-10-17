 CREATE TABLE IF NOT EXISTS ADOPTION(
    recorded_name VARCHAR,
    date_id INT,
    outcome_id INT,
    Animal_id INT,
    Sex VARCHAR,
    Breed_id INT,
    Color VARCHAR,
    ID VARCHAR
    );

CREATE TABLE IF NOT EXISTS OUTCOME(
    outcome VARCHAR,
    outcome_id INT
  );

  CREATE TABLE IF NOT EXISTS ANIMAL(
    Animal VARCHAR,
    Animal_id INT
  );

  CREATE TABLE IF NOT EXISTS BREED(
    Breed VARCHAR,
    Breed_id INT
  );

CREATE TABLE IF NOT EXISTS DATE(
    Dt timestamp,
    date_id INT,
    Mnt INT,
    Yr INT

  );