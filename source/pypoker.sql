-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3307
-- Generation Time: Jan 22, 2023 at 11:29 AM
-- Server version: 8.0.18
-- PHP Version: 7.3.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pypoker`
--

-- --------------------------------------------------------

--
-- Table structure for table `chat_global`
--

CREATE TABLE `chat_global` (
  `id` int(20) NOT NULL,
  `joueur` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `texte` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `date` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `invitations`
--

CREATE TABLE `invitations` (
  `joueur` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `invite` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `invitations`
--

INSERT INTO `invitations` (`joueur`, `invite`, `date`) VALUES
('joueur1', 'joueur2', '2023-01-20 14:39:58'),
('joueur2', 'joueur1', '2023-01-20 14:40:06');

-- --------------------------------------------------------

--
-- Table structure for table `joueur1§joueur2`
--

CREATE TABLE `joueur1§joueur2` (
  `firstname` varchar(30) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `joueurs`
--

CREATE TABLE `joueurs` (
  `pseudo` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `mdp` char(64) COLLATE utf8mb4_general_ci NOT NULL,
  `Gemmes` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `joueurs`
--

INSERT INTO `joueurs` (`pseudo`, `mdp`, `Gemmes`) VALUES
('joueur1', '12345', 0),
('joueur2', '12345', 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `chat_global`
--
ALTER TABLE `chat_global`
  ADD PRIMARY KEY (`id`),
  ADD KEY `joueur` (`joueur`);

--
-- Indexes for table `invitations`
--
ALTER TABLE `invitations`
  ADD PRIMARY KEY (`joueur`,`invite`),
  ADD KEY `invitations_ibfk_2` (`invite`);

--
-- Indexes for table `joueurs`
--
ALTER TABLE `joueurs`
  ADD PRIMARY KEY (`pseudo`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `chat_global`
--
ALTER TABLE `chat_global`
  MODIFY `id` int(20) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `chat_global`
--
ALTER TABLE `chat_global`
  ADD CONSTRAINT `chat_global_ibfk_1` FOREIGN KEY (`joueur`) REFERENCES `joueurs` (`pseudo`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `invitations`
--
ALTER TABLE `invitations`
  ADD CONSTRAINT `invitations_ibfk_1` FOREIGN KEY (`joueur`) REFERENCES `joueurs` (`pseudo`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `invitations_ibfk_2` FOREIGN KEY (`invite`) REFERENCES `joueurs` (`pseudo`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
