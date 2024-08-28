CREATE TABLE Source (
    id INT PRIMARY KEY IDENTITY(1,1),
    name VARCHAR(255) NOT NULL,
    updated_on DATETIME NOT NULL
);


CREATE TABLE Targt (
    id INT PRIMARY KEY IDENTITY(1,1),
    name VARCHAR(255) NOT NULL,
    updated_on DATETIME NOT NULL,
	deleted BIT DEFAULT 0
);

ALTER TABLE Targt
ADD source_id INT;

ALTER TABLE Targt
ADD CONSTRAINT DF_Targt_updated DEFAULT 0 FOR updated;

update Source
set name='shrishm', updated_on=GETDATE()
where id=1;

delete from Source
where id=1;

insert into Source(name,updated_on) values ('raghul', GETDATE());