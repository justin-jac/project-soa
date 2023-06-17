-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 17, 2023 at 06:58 AM
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
-- Database: `orderdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `idOrder` int(11) NOT NULL,
  `idClient` int(11) NOT NULL,
  `namaOrder` varchar(255) NOT NULL,
  `deskripsiOrder` varchar(1000) DEFAULT NULL,
  `tanggalOrder` date NOT NULL,
  `totalHargaOrder` int(11) NOT NULL DEFAULT 0,
  `statusOrder` varchar(255) NOT NULL DEFAULT 'not_done'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`idOrder`, `idClient`, `namaOrder`, `deskripsiOrder`, `tanggalOrder`, `totalHargaOrder`, `statusOrder`) VALUES
(1, 1, 'Dies Natalis Ke-10 Genshin Impact', 'acara ulang tahun ke-10 dari game Genshin Impact', '2023-06-15', 3000000, 'not_done'),
(2, 2, 'Peringatan Hari Pahlawan', 'Acara memperingati hari pahlawan', '2023-06-16', 500000, 'not_done'),
(4, 1, 'dummyOrder1', 'dummydesk', '2023-06-15', 100, 'not_done'),
(5, 1, 'dummyOrder2', 'dummydesk2', '2023-06-15', 100, 'not_done');

-- --------------------------------------------------------

--
-- Table structure for table `order_events`
--

CREATE TABLE `order_events` (
  `idEvent` int(11) NOT NULL,
  `idOrder` int(11) NOT NULL,
  `subtotal` int(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `order_events`
--

INSERT INTO `order_events` (`idEvent`, `idOrder`, `subtotal`) VALUES
(1, 1, 1000000),
(2, 1, 1000000),
(3, 1, 1000000),
(4, 2, 250000),
(5, 2, 250000),
(7, 4, 200);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`idOrder`);

--
-- Indexes for table `order_events`
--
ALTER TABLE `order_events`
  ADD PRIMARY KEY (`idEvent`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `idOrder` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `order_events`
--
ALTER TABLE `order_events`
  MODIFY `idEvent` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
