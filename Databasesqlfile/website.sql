-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 31, 2024 at 09:14 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `website`
--

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `User_ID` int(255) NOT NULL,
  `Username` varchar(255) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `Password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`User_ID`, `Username`, `Email`, `Password`) VALUES
(1, 'Kinso', 'mowinskikrystian@gmail.com', 'lol123451'),
(3, 'krystian', 'krystian@gmail.com', '$2b$12$lycuG.bsG92EPfRYrE0ynuOmVbtb1jmn5O069lNDzo/t4acRQGh76'),
(5, 'xdxdxd', 'krymdaking@gmail.com', '$2b$12$Xw4PI0wT6aWLzDFf1Xw4b.0DzGamNmTWsvZDokW3lX9HBhKdzdeMG'),
(6, 'anna', 'anna@gmail.com', '$2b$12$2QfSHJZK5HsE4T0Vs2uL6epxRgMzadj/LdGlIm5QKV14W.ATnfvcG'),
(7, 'test', 'test@gmail.com', '$2b$12$EGDLD2IAl2.Ui7jKE8cG4OAdZDQueutpESsA6fEb8tARLnT2eGwle'),
(8, 'User_data_test', 'Userdata@gmail.com', '$2b$12$rOSGvfLxojJYbwNvKTSaoud3JvHbxP6dfZzdg3.VOUAc6/BFCO3L2');

-- --------------------------------------------------------

--
-- Table structure for table `user_data`
--

CREATE TABLE `user_data` (
  `User_ID` int(255) NOT NULL,
  `fn_username` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_data`
--

INSERT INTO `user_data` (`User_ID`, `fn_username`) VALUES
(3, NULL),
(5, NULL),
(6, NULL),
(7, NULL),
(8, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `user_information`
--

CREATE TABLE `user_information` (
  `User_ID` int(11) NOT NULL,
  `Bio` varchar(255) DEFAULT NULL,
  `Age` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_information`
--

INSERT INTO `user_information` (`User_ID`, `Bio`, `Age`) VALUES
(3, 'Hey I\'m a full stack Web Developer', '2003-07-09'),
(5, 'this broke 20 time i want to cry axios didnt want to send headers properly ', '0000-00-00'),
(6, 'i am the graphic designer of this website :)', '2002-08-07'),
(7, NULL, NULL),
(8, NULL, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`User_ID`),
  ADD UNIQUE KEY `User_ID` (`User_ID`);

--
-- Indexes for table `user_data`
--
ALTER TABLE `user_data`
  ADD PRIMARY KEY (`User_ID`);

--
-- Indexes for table `user_information`
--
ALTER TABLE `user_information`
  ADD UNIQUE KEY `User_ID_2` (`User_ID`),
  ADD KEY `User_ID` (`User_ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `User_ID` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `user_data`
--
ALTER TABLE `user_data`
  ADD CONSTRAINT `user_data_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `users` (`User_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `user_information`
--
ALTER TABLE `user_information`
  ADD CONSTRAINT `user_information_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `users` (`User_ID`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
