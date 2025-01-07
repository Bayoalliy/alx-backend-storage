-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.
DELIMITER //
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers; 
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
	CREATE TEMPORARY TABLE view_score_and_weight AS
	SELECT corrections.score, corrections.user_id,
	projects.weight FROM corrections
	INNER JOIN projects
	ON projects.id = corrections.project_id;

	CREATE TEMPORARY TABLE weighted_avg AS
	SELECT user_id, SUM(score * weight) / SUM(weight)
	AS average
	FROM view_score_and_weight GROUP BY(user_id);

	UPDATE users
	JOIN weighted_avg
	ON users.id = weighted_avg.user_id
	SET users.average_score = weighted_avg.average;
END//
