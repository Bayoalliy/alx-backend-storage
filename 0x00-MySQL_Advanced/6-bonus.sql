-- SQL script that creates a stored procedure AddBonus that adds a new correction for a student.
DELIMITER //
CREATE PROCEDURE AddBonus(
	IN user_id int,
	IN project_name varchar(255),
	IN score int
)
BEGIN
	IF NOT EXISTS (
		SELECT 1
		FROM projects
		WHERE name = project_name
	) THEN
		INSERT INTO projects (name)
		VALUES (project_name);
	END IF;

	SET @project_id = (SELECT id FROM projects
	WHERE name = project_name);

	INSERT INTO corrections
	VALUES(user_id, @project_id, score);
END//
