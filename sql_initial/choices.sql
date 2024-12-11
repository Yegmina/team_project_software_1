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
-- Структура таблиці `choices`
--

CREATE TABLE `choices` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(255) NOT NULL,
  `money_needed` int(11) NOT NULL,
  `infected_changing` int(11) NOT NULL,
  `infection_rate` smallint(5) NOT NULL,
  `dissatisfaction_changing` int(11) NOT NULL,
  `research_progress_changing` int(11) NOT NULL,
  `text` text NOT NULL,
  `sql_query` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Дамп даних таблиці `choices`
--

INSERT INTO `choices` (`id`, `name`, `money_needed`, `infected_changing`, `infection_rate`, `dissatisfaction_changing`, `research_progress_changing`, `text`, `sql_query`) VALUES
(1, 'Vaccine Research Investment', 50000, -1, 1, 0, 15, 'You invested in vaccine research.', ''),
(2, 'Ignore the problem', 0, 0, 0, 0, 1, 'You ignored health protocols.', ''),
(3, 'Close all airports', 0, -1, -2, 50, -5, 'You closed all airports.', 'SET closed = 1'),
(4, 'Distribute Free Masks', 10000, -1, -2, -10, 0, 'You distributed free masks.', ''),
(5, 'Impose Lockdown', 0, -1, -2, 30, -2, 'You imposed a lockdown.', ''),
(6, 'Fast Track Vaccine Trials', 80000, 0, 1, -5, 40, 'You fast-tracked vaccine trials.', ''),
(7, 'Vaccine Research Investment', 50000, -1, 1, 0, 15, 'You invested in vaccine research.', ''),
(8, 'Ignore the problem', 0, 1, 2, 5, -1, 'You ignored health protocols.', ''),
(10, 'Distribute Free Masks', 10000, -1, -2, -10, 0, 'You distributed free masks.', ''),
(11, 'Impose Lockdown', 0, -1, -2, 30, -2, 'You imposed a lockdown.', ''),
(12, 'Fast Track Vaccine Trials', 80000, 0, 1, -5, 40, 'You fast-tracked vaccine trials.', ''),
(13, 'Increase Hospital Capacity', 20000, -1, -1, 0, 5, 'You increased hospital capacity.', ''),
(14, 'Implement Remote Work Policies', 5000, 0, -1, -2, 1, 'You implemented remote work policies.', ''),
(15, 'Launch Public Awareness Campaign', 15000, -1, -1, -5, 10, 'You launched a public awareness campaign.', ''),
(16, 'Enhance Contact Tracing', 30000, -1, -2, -5, 10, 'You enhanced contact tracing efforts.', ''),
(17, 'Deploy Mobile Testing Units', 25000, -1, -2, -8, 15, 'You deployed mobile testing units.', ''),
(18, 'Offer Incentives for Vaccination', 40000, -1, -1, -15, 20, 'You offered incentives for vaccination.', ''),
(19, 'Set Up Quarantine Facilities', 30000, -1, -2, 5, 15, 'You set up quarantine facilities.', ''),
(20, 'Ban Large Gatherings', 0, -1, -2, 25, -5, 'You banned large gatherings.', ''),
(21, 'Launch Vaccine Awareness Program', 20000, -1, -1, -5, 8, 'You launched a vaccine awareness program.', ''),
(22, 'Collaborate with Tech Companies', 30000, 0, -1, -3, 15, 'You collaborated with tech companies for tracking.', ''),
(23, 'Allocate More Funds to Healthcare', 60000, -1, -1, -10, 30, 'You allocated more funds to healthcare.', ''),
(24, 'Conduct Public Health Surveys', 5000, 0, -1, -1, 1, 'You conducted public health surveys.', ''),
(25, 'Create a Health Advisory Board', 10000, 0, -1, -2, 3, 'You created a health advisory board.', ''),
(26, 'Enforce Mask Mandates', 0, -1, -2, 10, -5, 'You enforced mask mandates.', ''),
(27, 'Promote Healthy Living Initiatives', 20000, -1, -1, -5, 8, 'You promoted healthy living initiatives.', ''),
(28, 'Improve Air Quality Regulations', 15000, 0, 0, -3, 5, 'You improved air quality regulations.', ''),
(29, 'Engage in International Collaboration', 50000, -1, -1, -5, 25, 'You engaged in international collaboration.', ''),
(30, 'Host Health Webinars', 5000, 0, 0, -1, 2, 'You hosted health webinars.', ''),
(31, 'Sponsor Research Grants', 30000, -1, -1, -5, 15, 'You sponsored research grants.', ''),
(32, 'Enhance Health Education in Schools', 20000, -1, -1, -10, 8, 'You enhanced health education in schools.', ''),
(33, 'Invest in Biotechnology', 80000, -1, 1, -5, 40, 'You invested in biotechnology.', ''),
(34, 'Implement Work-from-Home Policies', 10000, -1, -1, -5, 3, 'You implemented work-from-home policies.', ''),
(35, 'Provide Mental Health Support', 25000, -1, -1, -5, 10, 'You provided mental health support.', ''),
(36, 'Improve Sanitation in Public Areas', 15000, -1, -1, -5, 5, 'You improved sanitation in public areas.', ''),
(37, 'Launch a Health Hotline', 20000, 0, -1, -3, 8, 'You launched a health hotline.', ''),
(38, 'Conduct Vaccine Information Sessions', 10000, -1, -1, -5, 3, 'You conducted vaccine information sessions.', ''),
(39, 'Invest in Health Technology', 70000, -1, 1, -5, 35, 'You invested in health technology.', ''),
(40, 'Create Health Awareness Merchandise', 5000, 0, 0, -1, 2, 'You created health awareness merchandise.', ''),
(41, 'Support Local Businesses', 20000, -1, -1, 0, 8, 'You supported local businesses.', ''),
(42, 'Establish a Task Force', 30000, 0, -1, -5, 15, 'You established a task force to tackle the crisis.', ''),
(43, 'Conduct Regular Health Checks', 25000, -1, -1, -5, 10, 'You conducted regular health checks.', ''),
(44, 'Initiate a Blood Donation Drive', 15000, -1, -1, -5, 5, 'You initiated a blood donation drive.', ''),
(45, 'Launch a Youth Health Program', 20000, -1, -1, -5, 8, 'You launched a youth health program.', ''),
(46, 'Encourage Telemedicine Services', 10000, -1, -1, -5, 3, 'You encouraged telemedicine services.', ''),
(47, 'Support Healthcare Workers', 30000, -1, -1, -5, 15, 'You supported healthcare workers with resources.', ''),
(48, 'Raise Awareness on Mental Health', 10000, -1, -1, -5, 3, 'You raised awareness on mental health issues.', ''),
(49, 'Offer Free Health Screenings', 25000, -1, -1, -5, 10, 'You offered free health screenings.', ''),
(50, 'Engage in Social Media Campaigns', 5000, 0, 0, -3, 2, 'You engaged in social media campaigns.', ''),
(51, 'Develop a Community Health Program', 15000, -1, -1, -10, 5, 'You developed a community health program.', ''),
(52, 'Provide Subsidized Health Care', 50000, -1, -1, -5, 25, 'You provided subsidized health care.', ''),
(53, 'Implement Data Tracking Systems', 30000, -1, -1, -3, 15, 'You implemented data tracking systems for health.', ''),
(54, 'Host Community Health Fairs', 20000, -1, -1, -5, 8, 'You hosted community health fairs.', ''),
(55, 'Launch Health Workshops', 5000, 0, 0, -1, 2, 'You launched health workshops.', ''),
(56, 'Create a Health Blog', 2000, 0, 0, -1, 2, 'You created a health blog to share information.', ''),
(57, 'Promote Vaccination through Influencers', 30000, -1, -1, -10, 15, 'You promoted vaccination through social media influencers.', ''),
(58, 'Increase Funding for Mental Health', 60000, -1, -1, -5, 30, 'You increased funding for mental health programs.', ''),
(59, 'Invest in Preventive Care', 40000, -1, -1, -10, 20, 'You invested in preventive care initiatives.', '');

--
-- Індекси збережених таблиць
--

--
-- Індекси таблиці `choices`
--
ALTER TABLE `choices`
  ADD PRIMARY KEY (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
