-- animals of each type with outcomes
with src as (select distinct("ID"),"Animal" from "ADOPTION" join "ANIMAL" using ("Animal_id"))
select "Animal", count(*) as total_count from src group by "Animal" order by "Animal"


-- count of animals with more than one outcome
with src as (select "ID",  count(*)  from "ADOPTION"  group by "ID" having count(*) > 1)
select count(*) from src


-- Top 5 month for outcomes
select "Mnt" as month, count(*) as outcome_count from "DATE" join "ADOPTION" using (date_id) group by "Mnt" order by outcome_count desc limit 5


-- Total Adopted cats and the count of cat types that were adopted
with src as (select datediff(year, DATE(Dt), dob) as age, "outcome_id", case(when age < 1 then "kitten" when age between 1 and 10 then "Adult" else "Senior" end) as cat_type from "ADOPTION" join "DATE" on "ADOPTION".date_id = "DATE".date_id join "ANIMAL" on "ADOPTION".Animal_id = "ANIMAL".Animal_id where "Animal" = 'Cat'),
src1 as (select "outcome", "cat_type" from src join OUTCOME using(outcome_id))

-- Total kittens, adults and Seniors who were adopted
select count(*) from src1 where outcome = "Adopted"

-- Different cat types and their adopted count
select cat_type, count(*) as adopted_count from src1 where outcome = "Adopted" group by cat_type



-- Cumulative Outcomes till a given date
with src as (select DATE("Dt") as date from "ADOPTION" join "DATE" using (date_id))
select distinct("date"), sum(1) over (order by "date") as outcomes_till_date from src



