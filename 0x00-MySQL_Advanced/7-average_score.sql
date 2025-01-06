-- SQL script that creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student.
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(
	IN user_id int
)
BEGIN
	SET @avg_score = (SELECT AVG(score) FROM corrections
		WHERE corrections.user_id = user_id
		GROUP BY corrections.user_id);
	UPDATE users
	SET average_score = @avg_score
	WHERE users.id = user_id;
END //
