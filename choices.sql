CREATE TABLE IF NOT EXISTS choices (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    money_needed INT NOT NULL,
    infected_changing INT NOT NULL,
    dissatisfaction_changing INT NOT NULL,
    research_progress_changing INT NOT NULL,
    text TEXT NOT NULL,
    sql_query TEXT
);

INSERT INTO choices (
    name, money_needed, infected_changing, dissatisfaction_changing,
    research_progress_changing, text, sql_query
)
VALUES
('Vaccine Research Investment', 50000, -1, 0, 15, 'You invested in vaccine research.', ''),
('Ignore the problem', 0, 1, 5, -1, 'You ignored health protocols.', ''),
('Close all airports', 0, -5, 50, -5, 'You closed all airports.', 'SET closed = 1 WHERE 1=1'),
('Distribute Free Masks', 10000, -2, -10, 0, 'You distributed free masks.', ''),
('Impose Lockdown', 0, -3, 30, -2, 'You imposed a lockdown.', ''),
('Fast Track Vaccine Trials', 80000, 0, -5, 25, 'You fast-tracked vaccine trials.', '');
