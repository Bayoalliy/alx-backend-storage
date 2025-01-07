-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.
DELIMITER //
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser; 
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
	IN u_id INT
)
BEGIN
	CREATE VIEW view_score_and_weight AS
	SELECT corrections.score, corrections.user_id,
	projects.weight FROM corrections
	INNER JOIN projects
	ON projects.id = corrections.project_id;

	SET @weighted_avg = (SELECT
	SUM(score * weight) / SUM(weight)
	FROM view_score_and_weight
	WHERE user_id = u_id);

	UPDATE users
	SET average_score = @weighted_avg
	WHERE id = u_id;
END//
