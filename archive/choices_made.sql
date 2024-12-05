CREATE TABLE IF NOT EXISTS choices_made (
    game_id INT(16) NOT NULL,
    choice_id BIGINT(20) UNSIGNED NOT NULL,
    PRIMARY KEY (game_id, choice_id),
    FOREIGN KEY (game_id) REFERENCES saved_games(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (choice_id) REFERENCES choices(id) ON DELETE CASCADE ON UPDATE CASCADE
);
