-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 17, 2023 at 06:59 AM
-- Server version: 10.4.20-MariaDB
-- PHP Version: 8.0.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `eventdb`
--

CREATE DATABASE IF NOT EXISTS `eventdb` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `eventdb`;

-- --------------------------------------------------------

--
-- Table structure for table `events`
--

CREATE TABLE `events` (
  `idEvent` int(11) NOT NULL,
  `idOrder` int(11) NOT NULL,
  `idStaffPIC` int(11) NOT NULL,
  `namaEvent` varchar(255) NOT NULL,
  `deskripsiEvent` varchar(1000) NOT NULL,
  `tanggalEvent` date NOT NULL,
  `jamMulaiEvent` time NOT NULL,
  `jamAkhirEvent` time NOT NULL,
  `subTotalEvent` int(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `events`
--

INSERT INTO `events` (`idEvent`, `idOrder`, `idStaffPIC`, `namaEvent`, `deskripsiEvent`, `tanggalEvent`, `jamMulaiEvent`, `jamAkhirEvent`, `subTotalEvent`) VALUES
(1, 1, 1, 'E-sport Genshin Impact', 'Lomba mengalahkan abyss dengan karakter Genshin Impact', '2023-07-01', '10:00:00', '15:00:00', 1000000),
(2, 1, 2, 'Lomba Kartu TCG', 'Lomba bermain kartu TCG', '2023-07-01', '15:00:00', '18:00:00', 1000000),
(3, 1, 1, 'Pameran Genshin Impact', 'Pameran game Genshin Impact bertema kota Fontain', '2023-07-02', '10:00:00', '20:00:00', 1000000),
(4, 2, 1, 'Upacara Peringatan Hari Pahlawan', 'Upacara memperingati hari Pahlawan', '2023-11-10', '07:00:00', '08:00:00', 250000),
(5, 2, 2, 'Lomba Tarik Tambang', 'Lomba tarik tambang untuk memperingati hari Pahlawan', '2023-11-10', '09:00:00', '12:00:00', 250000),
(7, 4, 1, 'dummyEvent1', 'deskDummy1', '2023-06-15', '01:00:00', '01:30:00', 200),
(8, 5, 2, 'dummyEvent2', 'deskDummy2', '2023-06-15', '01:00:00', '01:30:00', 100);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `events`
--
ALTER TABLE `events`
  ADD PRIMARY KEY (`idEvent`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `events`
--
ALTER TABLE `events`
  MODIFY `idEvent` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
