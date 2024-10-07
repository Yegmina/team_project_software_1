CREATE TABLE choices_made (
    game_id INT(16) NOT NULL,  -- Matches saved_games.id
    choice_id BIGINT(20) UNSIGNED NOT NULL,  -- Matches choices.id
    PRIMARY KEY (game_id, choice_id), --columns
    FOREIGN KEY (game_id) REFERENCES saved_games(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (choice_id) REFERENCES choices(id) ON DELETE CASCADE ON UPDATE CASCADE
);
