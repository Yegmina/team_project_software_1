-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: mysql.metropolia.fi
-- Час створення: Гру 11 2024 р., 10:35
-- Версія сервера: 10.5.27-MariaDB
-- Версія PHP: 8.3.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База даних: `yehort`
--

-- --------------------------------------------------------

--
-- Структура таблиці `saved_games`
--

CREATE TABLE `saved_games` (
  `id` int(16) NOT NULL,
  `input_name` varchar(64) DEFAULT NULL,
  `money` int(16) DEFAULT NULL,
  `infected_population` int(16) DEFAULT NULL,
  `public_dissatisfaction` int(16) DEFAULT NULL,
  `research_progress` int(16) DEFAULT NULL,
  `game_over` tinyint(1) DEFAULT 0,
  `game_turn` int(16) DEFAULT NULL,
  `infection_rate` smallint(5) DEFAULT NULL,
  `max_distance` int(16) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Дамп даних таблиці `saved_games`
--

INSERT INTO `saved_games` (`id`, `input_name`, `money`, `infected_population`, `public_dissatisfaction`, `research_progress`, `game_over`, `game_turn`, `infection_rate`, `max_distance`) VALUES
(177, 'Test1', 65861, 0, 44, 100, 0, 22, -14, 9511),
(178, 'Test2', 6731, 0, 100, 100, 0, 30, -17, 10101),
(179, 'Test 3', 10000, 3, 7, 1, 0, 1, 7, 8000),
(180, 'test 4', 10000, 3, 7, 1, 0, 1, 7, 8000),
(181, 'test 5', 32914, 10, 46, 0, 0, 4, 6, 8152),
(182, 'gfds', 10000, 3, 7, 1, 0, 1, 7, 8000),
(183, 'test 6', 10000, 3, 7, 1, 0, 1, 7, 8000),
(184, 'test 7', 10000, 3, 7, 1, 0, 1, 7, 8000),
(185, 'test 8', 10000, 3, 7, 1, 0, 1, 7, 8000),
(186, 'test 9', 10000, 3, 7, 1, 0, 1, 7, 8000),
(187, 'test 10', 10000, 3, 7, 1, 0, 1, 7, 8000),
(188, 'test 11', 10000, 3, 7, 1, 0, 1, 7, 8000),
(189, 'test 12', 10000, 3, 7, 1, 0, 1, 7, 8000),
(190, 'test 13', 28140, 3, 7, 1, 0, 2, 7, 7992),
(191, 'test 100', 10000, 3, 7, 1, 0, 1, 7, 8000),
(192, 'test 101', 10000, 3, 7, 1, 0, 1, 7, 8000),
(193, 'test 102', 4215, 0, 97, 20, 1, 10, 1, 8439),
(194, 'Noah Stewart', 9317, 49, 100, 50, 1, 12, -3, 8716),
(195, 'Noah Stewart 1', 14544, 0, 0, 14, 1, 3, 3, 8175),
(196, 'Noah Stewart 5', 9644, 87, 100, 70, 1, 20, -6, 8930),
(197, 'Noah Stewart 2', 46882, 4, 7, 1, 0, 3, 7, 8090),
(198, 'Noah Stewart 4', 175018, 2, 6, 30, 0, 17, 5, 8618),
(199, 'test', 9341, 90, 100, 55, 1, 21, -9, 8718),
(200, 'tteeeesssttt', 3080, 31, 7, 55, 0, 8, 4, 8305),
(201, 'testtest', 28322, 36, 100, 18, 1, 9, 2, 8507);

--
-- Індекси збережених таблиць
--

--
-- Індекси таблиці `saved_games`
--
ALTER TABLE `saved_games`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT для збережених таблиць
--

--
-- AUTO_INCREMENT для таблиці `saved_games`
--
ALTER TABLE `saved_games`
  MODIFY `id` int(16) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=202;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
