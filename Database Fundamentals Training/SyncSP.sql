CREATE OR ALTER PROCEDURE SyncTargetToSource(@debug_f1 int=0)
AS
BEGIN
	IF @debug_f1=1 select * from Source
	IF @debug_f1=1 select * from Targt

	/*Syncing new records*/
	insert into Targt(name,updated_on,deleted,source_id)
	select
		s.name,
		s.updated_on,
		0,
		s.id
	from Source s
	left join Targt t on s.id=t.source_id
	where t.source_id IS NULL;

	/*Syncing the Updated rows*/
	insert into Targt(name,updated_on,deleted,source_id)
	select
		s.name,
		s.updated_on,
		0,
		s.id
	from source s
	inner join Targt t on s.id=t.source_id
	where s.updated_on!=t.updated_on and t.updated=0;

	/*Marking updated rows as Updated in Targt*/
	update t
	set t.updated=1
	from source s
	inner join Targt t on s.id=t.source_id
	where s.updated_on!=t.updated_on and t.updated=0;

	/*Soft Delete records from Target*/
	update Targt
	set deleted=1
	where source_id NOT IN (select id from Source);
END;

EXEC SyncTargetToSource @debug_f1=1;