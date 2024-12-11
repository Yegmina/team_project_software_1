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
-- Структура таблиці `choices_made`
--

CREATE TABLE `choices_made` (
  `game_id` int(16) NOT NULL,
  `choice_id` bigint(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Дамп даних таблиці `choices_made`
--

INSERT INTO `choices_made` (`game_id`, `choice_id`) VALUES
(177, 37),
(177, 45),
(177, 18),
(177, 36),
(177, 53),
(177, 13),
(177, 17),
(177, 7),
(177, 6),
(177, 20),
(177, 29),
(177, 5),
(177, 22),
(177, 51),
(177, 46),
(177, 10),
(178, 25),
(178, 14),
(178, 42),
(178, 31),
(178, 7),
(178, 55),
(178, 34),
(178, 11),
(178, 57),
(178, 45),
(178, 4),
(178, 29),
(178, 19),
(178, 43),
(178, 30),
(178, 26),
(178, 5),
(178, 2),
(178, 49),
(178, 16),
(178, 8),
(178, 20),
(178, 38),
(178, 53),
(178, 15),
(177, 16),
(177, 4),
(177, 56),
(177, 55),
(177, 34),
(177, 2),
(193, 3),
(193, 53),
(193, 10),
(193, 46),
(194, 56),
(194, 59),
(194, 4),
(194, 5),
(194, 18),
(194, 27),
(194, 40),
(194, 24),
(194, 11),
(195, 46),
(195, 15),
(195, 10),
(196, 34),
(196, 50),
(196, 42),
(196, 36),
(196, 43),
(196, 31),
(196, 27),
(196, 56),
(196, 32),
(196, 48),
(196, 38),
(196, 26),
(196, 10),
(198, 10),
(198, 31),
(198, 42),
(198, 8),
(199, 14),
(199, 54),
(199, 40),
(199, 53),
(199, 48),
(199, 8),
(199, 4),
(199, 35),
(199, 32),
(199, 28),
(199, 44),
(199, 15),
(199, 11),
(199, 10),
(199, 3),
(199, 20),
(200, 49),
(200, 54),
(200, 8),
(200, 19),
(200, 30),
(200, 18),
(181, 8),
(181, 13),
(181, 20),
(201, 50),
(201, 11),
(201, 38),
(201, 27),
(201, 2),
(201, 46),
(201, 55);

--
-- Індекси збережених таблиць
--

--
-- Індекси таблиці `choices_made`
--
ALTER TABLE `choices_made`
  ADD KEY `FK` (`game_id`),
  ADD KEY `FK 2` (`choice_id`) USING BTREE;

--
-- Обмеження зовнішнього ключа збережених таблиць
--

--
-- Обмеження зовнішнього ключа таблиці `choices_made`
--
ALTER TABLE `choices_made`
  ADD CONSTRAINT `choices_made_ibfk_1` FOREIGN KEY (`game_id`) REFERENCES `saved_games` (`id`),
  ADD CONSTRAINT `choices_made_ibfk_2` FOREIGN KEY (`choice_id`) REFERENCES `choices` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
