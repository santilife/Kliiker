-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 12, 2025 at 12:42 AM
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
-- Database: `kliiker1`
--

-- --------------------------------------------------------

--
-- Table structure for table `estadokliiker`
--

CREATE TABLE `estadokliiker` (
  `id_estado` int(11) NOT NULL,
  `estado` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `estadokliiker`
--

INSERT INTO `estadokliiker` (`id_estado`, `estado`) VALUES
(1, 'llamada_1'),
(2, 'llamada_2'),
(3, 'llamada_3'),
(4, 'llamada_4');

-- --------------------------------------------------------

--
-- Table structure for table `flujotrabajo`
--

CREATE TABLE `flujotrabajo` (
  `id_flujoTrabajo` int(11) NOT NULL,
  `nivel` tinyint(1) NOT NULL,
  `id_estado` int(11) NOT NULL,
  `diasParaGestion` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `gestiones`
--

CREATE TABLE `gestiones` (
  `id_gestion` int(11) NOT NULL,
  `id_llamada` int(11) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `canal` varchar(250) DEFAULT NULL,
  `tipoGestion` varchar(250) DEFAULT NULL,
  `comentario` varchar(250) DEFAULT NULL,
  `fechaProximaGestion` date DEFAULT NULL,
  `nombre_AS` varchar(250) DEFAULT NULL,
  `tipificacion` varchar(250) DEFAULT NULL,
  `motivoNoInteres` varchar(250) DEFAULT NULL,
  `id_estado` int(11) NOT NULL,
  `celular` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `gestiones`
--

INSERT INTO `gestiones` (`id_gestion`, `id_llamada`, `fecha`, `canal`, `tipoGestion`, `comentario`, `fechaProximaGestion`, `nombre_AS`, `tipificacion`, `motivoNoInteres`, `id_estado`, `celular`) VALUES
(1, 1004, '2024-03-05', 'Via telefonica', 'Seguimiento', '      Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus consequuntur debitis laboriosam vitae odio amet facere adipisci necessitatibus possimus ab nam vel placeat sequi similique, alias obcaecati eveniet voluptates quos sit aperi', NULL, 'operador1', 'Buzón de voz', NULL, 3, '3001234567'),
(2, 10032025, '2024-03-04', 'Whatsapp', 'Información', 'sisa paaa', NULL, 'operador1', 'Registro exitoso', NULL, 3, '3017654321');

--
-- Triggers `gestiones`
--
DELIMITER $$
CREATE TRIGGER `tr_after_update_gestiones` AFTER UPDATE ON `gestiones` FOR EACH ROW BEGIN
    INSERT INTO historial_gestiones (
        id_gestion,
        id_llamada,
        id_estado,
        fecha,
        canal,
        tipoGestion,
        comentario,
        fechaProximaGestion,
        nombre_AS,
        tipificacion,
        celular,
        motivoNoInteres
    ) VALUES (
        NEW.id_gestion,
        NEW.id_llamada,
        NEW.id_estado,
        NEW.fecha,
        NEW.canal,
        NEW.tipoGestion,
        NEW.comentario,
        NEW.fechaProximaGestion,
        NEW.nombre_AS,
        NEW.tipificacion,
        NEW.celular,
        CASE 
            WHEN NEW.tipificacion = 'Sin interes' THEN NEW.motivoNoInteres
            ELSE NULL
        END
    );
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `historial_gestiones`
--

CREATE TABLE `historial_gestiones` (
  `id_historial` int(11) NOT NULL,
  `id_gestion` int(11) NOT NULL,
  `id_estado` int(11) NOT NULL,
  `id_llamada` int(11) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `canal` varchar(250) DEFAULT NULL,
  `tipoGestion` varchar(250) DEFAULT NULL,
  `comentario` varchar(250) DEFAULT NULL,
  `fechaProximaGestion` date DEFAULT NULL,
  `nombre_AS` varchar(250) DEFAULT NULL,
  `tipificacion` varchar(250) DEFAULT NULL,
  `celular` varchar(250) DEFAULT NULL,
  `motivoNoInteres` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `historial_gestiones`
--

INSERT INTO `historial_gestiones` (`id_historial`, `id_gestion`, `id_estado`, `id_llamada`, `fecha`, `canal`, `tipoGestion`, `comentario`, `fechaProximaGestion`, `nombre_AS`, `tipificacion`, `celular`, `motivoNoInteres`) VALUES
(4, 1, 0, 1003, '2024-03-05', 'Via telefonica', 'Seguimiento', 'Cliente interesado en el producto', '2025-03-21', 'operador1', 'Buzón de voz', '3001234567', NULL),
(5, 1, 0, 1003, '2024-03-05', 'Whatsapp', 'Seguimiento', 'Aguacate', '2025-03-12', 'operador1', 'Buzón de voz', '3001234567', NULL),
(6, 2, 0, 1004, '2024-03-04', 'Via telefonica', 'Información', 'Pailas', '2025-03-18', 'operador1', 'Sin interes', '3017654321', 'Consiguio trabajo'),
(7, 1, 0, 1234, '2024-03-05', 'Via telefonica', 'Seguimiento', 'Me la pelan', '2025-03-13', 'operador1', 'Información general', '3001234567', NULL),
(8, 2, 0, 10032025, '2024-03-04', 'Whatsapp', 'Información', 'sisa paaa', NULL, 'operador1', 'Registro exitoso', '3017654321', NULL),
(9, 1, 0, 33333, '2024-03-05', 'Whatsapp', 'Seguimiento', 'SAPO', '2025-03-11', 'operador1', 'Buzón de voz', '3001234567', NULL),
(10, 1, 2, 1005, '2024-03-05', 'Via telefonica', 'Seguimiento', 'SAPO', '2025-03-13', 'operador1', 'Equivocado', '3001234567', NULL),
(11, 1, 2, 12341234, '2024-03-05', 'Whatsapp', 'Seguimiento', 'SAPO hpta', '2025-03-26', 'operador1', 'No contesta', '3001234567', NULL),
(12, 1, 3, 12312, '2024-03-05', 'Via telefonica', 'Seguimiento', 'gg bro, se pudo', '2025-03-28', 'operador1', 'Registro exitoso', '3001234567', NULL),
(13, 1, 2, 2147483647, '2024-03-05', 'Whatsapp', 'Seguimiento', 'no se pudo', '2025-03-19', 'operador1', 'Sin interes', '3001234567', 'Precio alto'),
(14, 1, 3, 1004, '2024-03-05', 'Via telefonica', 'Seguimiento', '      Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus consequuntur debitis laboriosam vitae odio amet facere adipisci necessitatibus possimus ab nam vel placeat sequi similique, alias obcaecati eveniet voluptates quos sit aperi', NULL, 'operador1', 'Buzón de voz', '3001234567', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `kliiker`
--

CREATE TABLE `kliiker` (
  `id_Kliiker` varchar(250) DEFAULT NULL,
  `nombre` varchar(250) DEFAULT NULL,
  `apellido` varchar(250) DEFAULT NULL,
  `celular` varchar(250) NOT NULL,
  `nivel` tinyint(1) NOT NULL,
  `correo` varchar(250) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `venta` tinyint(1) DEFAULT 0,
  `fechaIngreso` date DEFAULT NULL,
  `diaSinGestion` int(11) DEFAULT NULL,
  `gestionable` tinyint(1) DEFAULT NULL,
  `id_estado` int(11) DEFAULT NULL,
  `fechaSinGestion` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `kliiker`
--

INSERT INTO `kliiker` (`id_Kliiker`, `nombre`, `apellido`, `celular`, `nivel`, `correo`, `fecha`, `venta`, `fechaIngreso`, `diaSinGestion`, `gestionable`, `id_estado`, `fechaSinGestion`) VALUES
('K003', 'Josue', 'Narvaez', '192831246', 0, 'josue@gmail.com', '2025-03-11', 0, NULL, NULL, NULL, 3, NULL),
('K001', 'Juan', 'Pérez', '3001234567', 1, 'juan.perez@mail.com', '2024-03-01', 0, '2024-03-05', 2, 1, 1, NULL),
('K002', 'María', 'González', '3017654321', 0, 'maria.gonzalez@mail.com', '2024-02-20', 1, '2024-02-25', 5, 0, 2, NULL),
('K004', 'Maria', 'Lopez', '321287463', 0, 'maria@gmail.com', NULL, 0, NULL, NULL, NULL, 4, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `tipificacion`
--

CREATE TABLE `tipificacion` (
  `id_tipificacion` int(11) NOT NULL,
  `id_estado` int(11) DEFAULT NULL,
  `tipificacion` varchar(250) DEFAULT NULL,
  `rpc` tinyint(1) DEFAULT NULL,
  `Contactabilidad` tinyint(1) DEFAULT NULL,
  `Cierre_flujo` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tipificacion`
--

INSERT INTO `tipificacion` (`id_tipificacion`, `id_estado`, `tipificacion`, `rpc`, `Contactabilidad`, `Cierre_flujo`) VALUES
(1, 1, 'Llamada efectiva', 1, 1, 0),
(2, 2, 'No contesta', 0, 0, 0),
(3, 3, 'Volver a llamar', 1, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `uploaded_db`
--

CREATE TABLE `uploaded_db` (
  `id_db` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `date_upload` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `uploaded_db`
--

INSERT INTO `uploaded_db` (`id_db`, `nombre`, `date_upload`) VALUES
(2, 'basesKliiker.csv', '2025-03-10 11:41:45'),
(3, 'Histórico.csv', '2025-03-10 11:42:01');

-- --------------------------------------------------------

--
-- Table structure for table `usuarios`
--

CREATE TABLE `usuarios` (
  `nombre_AS` varchar(250) NOT NULL,
  `documento` int(11) DEFAULT NULL,
  `password` varchar(250) DEFAULT NULL,
  `usuario` varchar(250) DEFAULT NULL,
  `rol` varchar(250) DEFAULT NULL,
  `estadoUsuario` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `usuarios`
--

INSERT INTO `usuarios` (`nombre_AS`, `documento`, `password`, `usuario`, `rol`, `estadoUsuario`) VALUES
('admin', 12345678, 'admin123', 'admin_user', 'Administrador', 1),
('Andres Lopez', 123456678, '123456678', 'andresGay', 'Asesor', 2),
('brayan ocampo', 1011394242, '1011394242', 'brayanOcam', 'Administrador', NULL),
('Marissa', 1036252264, '1036252264', 'MarissaLK', 'Asesor', 1),
('marissasa', 1234567890, '1234567890', 'marissasa', 'Administrador', 1),
('operador1', 87654321, 'op12345', 'operador_01', 'Operador', 1),
('Pedro PereZ', 123454321, '123454321', 'Pedrop', 'Asesor', 1),
('Santi', 10, '10', 'Santifile', 'Administrador', 2),
('Valentina', 1036252267, '1234567890', 'Valen1', 'Administrador', 1),
('valentina Tobón', 23456789, '23456789', 'valent22_', 'Asesor', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `estadokliiker`
--
ALTER TABLE `estadokliiker`
  ADD PRIMARY KEY (`id_estado`);

--
-- Indexes for table `gestiones`
--
ALTER TABLE `gestiones`
  ADD PRIMARY KEY (`id_gestion`),
  ADD UNIQUE KEY `id_llamada` (`id_llamada`),
  ADD KEY `nombre_AS` (`nombre_AS`),
  ADD KEY `celular` (`celular`);

--
-- Indexes for table `historial_gestiones`
--
ALTER TABLE `historial_gestiones`
  ADD PRIMARY KEY (`id_historial`),
  ADD KEY `id_gestion` (`id_gestion`);

--
-- Indexes for table `kliiker`
--
ALTER TABLE `kliiker`
  ADD PRIMARY KEY (`celular`),
  ADD UNIQUE KEY `id_Kliker` (`id_Kliiker`),
  ADD UNIQUE KEY `correo` (`correo`),
  ADD KEY `id_estado` (`id_estado`);

--
-- Indexes for table `tipificacion`
--
ALTER TABLE `tipificacion`
  ADD PRIMARY KEY (`id_tipificacion`),
  ADD KEY `id_estado` (`id_estado`);

--
-- Indexes for table `uploaded_db`
--
ALTER TABLE `uploaded_db`
  ADD PRIMARY KEY (`id_db`);

--
-- Indexes for table `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`nombre_AS`),
  ADD UNIQUE KEY `documento` (`documento`),
  ADD UNIQUE KEY `usuario` (`usuario`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `gestiones`
--
ALTER TABLE `gestiones`
  MODIFY `id_gestion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `historial_gestiones`
--
ALTER TABLE `historial_gestiones`
  MODIFY `id_historial` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `uploaded_db`
--
ALTER TABLE `uploaded_db`
  MODIFY `id_db` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `gestiones`
--
ALTER TABLE `gestiones`
  ADD CONSTRAINT `gestiones_ibfk_1` FOREIGN KEY (`nombre_AS`) REFERENCES `usuarios` (`nombre_AS`),
  ADD CONSTRAINT `gestiones_ibfk_2` FOREIGN KEY (`celular`) REFERENCES `kliiker` (`celular`);

--
-- Constraints for table `historial_gestiones`
--
ALTER TABLE `historial_gestiones`
  ADD CONSTRAINT `historial_gestiones_ibfk_1` FOREIGN KEY (`id_gestion`) REFERENCES `gestiones` (`id_gestion`);

--
-- Constraints for table `kliiker`
--
ALTER TABLE `kliiker`
  ADD CONSTRAINT `kliiker_ibfk_1` FOREIGN KEY (`id_estado`) REFERENCES `estadokliiker` (`id_estado`);

--
-- Constraints for table `tipificacion`
--
ALTER TABLE `tipificacion`
  ADD CONSTRAINT `tipificacion_ibfk_1` FOREIGN KEY (`id_estado`) REFERENCES `estadokliiker` (`id_estado`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
