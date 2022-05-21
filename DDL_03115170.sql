create database IF NOT EXISTS  ELIDEK_03115170;
use ELIDEK_03115170;

create user 

CREATE TABLE Organization (
  abrv varchar(10) not null,
  full_name varchar(50) default abrv not null,
  address varchar(200) not null,
  category enum ('university','research_institute','company') not null,
  PRIMARY KEY (abrv)
);

CREATE TABLE Researcher (
  r_id int auto_increment,
  name varchar(30) not null,
  surname varchar(50) not null,
  sex enum ('male', 'female', 'other') not null,
  date_of_birth date not null,
  abrv varchar(10) not null,
  date_since date not null,
  PRIMARY KEY (r_id),
  FOREIGN KEY (abrv) REFERENCES Organization(abrv) on delete restrict on update cascade,
  check (date_of_birth<date_since)
);

CREATE TABLE Evaluation (
  eval_id int auto_increment,
  r_id int not null,
  grade int not null,
  date_of_evaluation date not null,
  PRIMARY KEY (eval_id),
  FOREIGN KEY (r_id) REFERENCES Researcher(r_id),
  check (grade>=0 and grade<=10)
);

CREATE TABLE ELIDEK_Admin (
  admin_id int auto_increment,
  name varchar(30) not null,
  surname varchar(50) not null,
  sex enum ('male', 'female', 'other') not null,
  date_of_birth date not null,
  PRIMARY KEY (admin_id)
);

CREATE TABLE ELIDEK_Program (
  p_id int auto_increment,
  title varchar(50) not null,
  division varchar(100) not null,
  PRIMARY KEY (p_id)
);

CREATE TABLE Project (
  e_id int auto_increment,
  title varchar(100) not null,
  summary text,
  funds int default 0 not null,
  start_date date not null,
  end_date date not null,
  r_id int not null, 	#director
  abrv varchar(10),		#organization
  admin_id int,			#ELIDEK admin
  p_id int,				#ELIDEK program
  eval_id int unique,			#Evaluation
  PRIMARY KEY (e_id),
  FOREIGN KEY (r_id) REFERENCES Researcher(r_id),
  FOREIGN KEY (admin_id) REFERENCES ELIDEK_Admin(admin_id),
  FOREIGN KEY (abrv) REFERENCES Organization(abrv),
  FOREIGN KEY (p_id) REFERENCES ELIDEK_Program(p_id),
  FOREIGN KEY (eval_id)  REFERENCES Evaluation(eval_id),
  check (start_date<end_date),
  check (timestampdiff(year,start_date,end_date)>=0),
  check (timestampdiff(year,start_date,end_date)<=4),
  check (funds>=0)
);

CREATE TABLE Works_In (
  e_id int,
  r_id int,
  PRIMARY KEY (e_id, r_id), 
  FOREIGN KEY (e_id) REFERENCES Project(e_id),
  FOREIGN KEY (r_id) REFERENCES Researcher(r_id)
  );

CREATE TABLE Org_Phone_Number (
  abrv varchar(10) not null,
  phone_number varchar(14) not null, 		#κωδικός χώρας (4 ψηφία ή '+'και 2 ψηφία) και 10 ψηφία, 
  PRIMARY KEY (abrv,phone_number),			#ή απλά 10 ψηφία
  FOREIGN KEY (abrv) REFERENCES Organization(abrv),
  check (char_length(phone_number)>9)
);

CREATE TABLE Deliverable (
  e_id int not null,
  title varchar(50) not null,
  summary text,
  date_due date not null,
  PRIMARY KEY (e_id, title),
  FOREIGN KEY (e_id) REFERENCES Project(e_id)
);

CREATE TABLE Research_Field (
  Name varchar(50) not null,
  PRIMARY KEY (Name)
);

CREATE TABLE Part_Of (
  e_id int not null,
  Name varchar(50) not null,
  PRIMARY KEY (e_id, Name),
  FOREIGN KEY (e_id) REFERENCES Project(e_id),
  FOREIGN KEY (Name) REFERENCES Research_Field(Name)
);

delimiter //
create trigger if not exists org_check
before insert on works_in
for each row 
begin
declare abrv1 varchar(10);
declare abrv2 varchar(10);
select abrv into abrv1 from researcher r where new.r_id = r.r_id;
select abrv into abrv2 from project p where p.e_id=new.e_id;
if abrv1!=abrv2 then signal sqlstate '45000';
end if;
end//
delimiter ;

delimiter //
create trigger if not exists deliv_check
before insert on deliverable
for each row 
begin
declare cutoffDate date;
select start_date  into cutoffDate from project p where p.e_id=new.e_id;
if new.date_due<cutoffDate then signal sqlstate '45000';
end if;
end//
delimiter ;

delimiter //
create trigger if not exists eval_check
before insert on project
for each row 
begin
declare cutoffDate date;
select date_of_evaluation into cutoffDate from evaluation e  where new.eval_id=e.eval_id;
if new.start_date<cutoffDate then signal sqlstate '45000';
end if;
end//
delimiter ;

create view projects_per_researcher as
select  p.e_id ,r.r_id ,r.name,r.surname,p.title, p.summary,p.funds,p.start_date,p.end_date  from project p
join works_in wi 
on p.e_id =wi.e_id 
join researcher r 
on wi.r_id=r.r_id 
join researcher r2 
on r2.r_id =p.r_id;

create view project_evaluators as 
select p.e_id,e.eval_id,r.r_id ,p.title,e.grade,r.name,r.surname,e.date_of_evaluation,p.start_date,p.end_date from project p 
join evaluation e 
on p.eval_id =e.eval_id 
join researcher r 
on e.r_id =r.r_id ;