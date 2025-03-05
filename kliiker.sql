-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 05, 2025 at 10:18 PM
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
-- Database: `kliiker`
--

-- --------------------------------------------------------

--
-- Table structure for table `kliiker`
--

CREATE TABLE `kliiker` (
  `id_kliiker` varchar(250) DEFAULT NULL,
  `nombre` varchar(250) NOT NULL,
  `apellido` varchar(250) NOT NULL,
  `celular` varchar(250) NOT NULL,
  `codigo` tinyint(1) NOT NULL,
  `correo` varchar(250) NOT NULL,
  `fecha` date NOT NULL,
  `venta` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `kliiker`
--

INSERT INTO `kliiker` (`id_kliiker`, `nombre`, `apellido`, `celular`, `codigo`, `correo`, `fecha`, `venta`) VALUES
(NULL, 'Milton Javier', 'Muñoz Ortega', '3005609406', 0, 'miltonjavi_1991@hotmail.com', '2025-02-01', 0),
('Liden3169', 'Liden Antonio', 'Alfonso Montenegro', '3012189242', 1, 'lianalmo1230@gmail.com', '2025-02-01', 0),
(NULL, 'Denilce', 'Serrano florez', '3016299410', 0, 'denilcesf1004@outlook.com', '2025-02-01', 0),
(NULL, 'Diana', 'ruiz', '3016932955', 0, 'milenarui73@gmail.com', '2025-02-01', 0),
(NULL, 'Liliana', 'gonzalez', '3026482820', 0, 'sanliliana1989@gmail.com', '2025-02-01', 0),
(NULL, 'Martha', 'Pesca Cative', '3028012604', 0, 'isabella22.pes2023@gmail.com', '2025-02-01', 0),
(NULL, 'Sandra milena', 'Uribe Yepes', '3046533556', 0, 'sandrauribe534@gmail.com', '2025-02-01', 0),
(NULL, 'Ludyn Patricia', 'Manrique', '3104799831', 0, 'manripatricia84@gmail.com', '2025-02-01', 0),
(NULL, 'Deisy', 'Suarez', '3108530356', 0, 'deisysl13@gmail.com', '2025-02-01', 0),
(NULL, 'Brain hawin', 'Madroñero Erazo', '3113780559', 0, 'bmadroneroerazo@gmail.com', '2025-02-01', 0),
(NULL, 'Karina', 'Hinojosa', '3144754191', 0, 'kandi874@hotmail.com', '2025-02-01', 0),
(NULL, 'Angela maria ALEGRIA', 'ZUÑIGA', '3145159308', 0, 'angelam612@hotmail.com', '2025-02-01', 0),
('Angela3062', 'Angela maria', 'Lopez restrepo', '3148551475', 1, 'angelalopezr2222@gmail.com', '2025-02-01', 0),
('Luis6769', 'Luis Enrique', 'Sepúlveda', '3154153028', 1, 'lescj0915@gmail.com', '2025-02-01', 0),
('Delis6013', 'Delis María', 'Polo herazo', '3154661673', 1, 'arrietalisseth2004@gmail.com', '2025-02-01', 0),
('Breiner0437', 'Breiner', 'Gutierrez Arroyave', '3157469888', 1, '2mengutierrez@gmail.com', '2025-02-01', 0),
('Luz6110', 'Luz', 'Parra', '3161391842', 1, 'parraluz861@gmail.com', '2025-02-01', 0),
(NULL, 'Wilmer', 'Ascanio romero', '3163312017', 0, 'wilmerascanioromero@gamail.com', '2025-02-01', 0),
('Sara4503', 'Sara', 'Triviño', '3163897003', 1, 'trivinosara@gmail.com', '2025-02-01', 0),
('Melisa4813', 'Melisa', 'López', '3176239657', 1, 'melisajlo19@gmail.com', '2025-02-01', 0),
('Juan3363', 'Juan Pablo', 'Sarmiento', '3178250761', 1, 'jpsgutierrez1@hotmail.com', '2025-02-01', 0),
('Francisco4290', 'Francisco Javier', 'Fernández muñoz', '3204483113', 1, 'fjmana.ad@gmail.com', '2025-02-01', 0),
('Fernando5110', 'Fernando', 'Montealegre Gomez', '3205152160', 1, 'ferdimontes14@gmail.com', '2025-02-01', 0),
(NULL, 'Valentina', 'Giraldo Zapata', '3208417370', 0, 'valentinags2018@gmail.com', '2025-02-01', 0),
('Dilmer2248', 'Dilmer Hely', 'Garavito Piñeros', '3214139278', 1, 'dilmergaravito@hotmail.com', '2025-02-01', 0),
(NULL, 'Alonso jose', 'Esala sulvaran', '3219124216', 0, 'alonzoesala5@hotmail.com', '2025-02-01', 0),
('Norma6064', 'Norma jazmin', 'Jiménez robayo', '3224668424', 1, 'nojajiro@gmail.com', '2025-02-01', 0),
('Edinson1591', 'Edinson', 'Domínguez bravo', '3224681895', 1, 'edinson161176@gmail.com', '2025-02-01', 0),
('Jhon4650', 'Jhon Alexander', 'Carabali Mezu', '3229726028', 1, 'carabali18mezu@gmail.com', '2025-02-01', 0),
(NULL, 'Juancarlos', 'Patino', '3246806695', 0, 'obe762@hotmail.com', '2025-02-01', 0);

-- --------------------------------------------------------

--
-- Table structure for table `usuarios`
--

CREATE TABLE `usuarios` (
  `nombre_AS` varchar(250) NOT NULL,
  `documento` varchar(10) NOT NULL,
  `password` varchar(10) NOT NULL,
  `usuario` varchar(250) NOT NULL,
  `rol` varchar(250) NOT NULL,
  `estado` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `usuarios`
--

INSERT INTO `usuarios` (`nombre_AS`, `documento`, `password`, `usuario`, `rol`, `estado`) VALUES
('Santiago Otalvaro', '1040033667', '1040033667', 'santi23', 'Administrador', 'no se'),
('Valentina Tobón', '1234567890', '1234567890', 'valen1', 'Asesor', 'tampoco se');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `kliiker`
--
ALTER TABLE `kliiker`
  ADD PRIMARY KEY (`celular`),
  ADD UNIQUE KEY `correo` (`correo`),
  ADD UNIQUE KEY `id_kliiker` (`id_kliiker`);

--
-- Indexes for table `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`nombre_AS`),
  ADD UNIQUE KEY `documento` (`documento`),
  ADD UNIQUE KEY `usuario` (`usuario`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
