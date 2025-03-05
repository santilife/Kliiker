-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 05-03-2025 a las 22:27:20
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `kliiker1`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estado`
--

CREATE TABLE `estado` (
  `id_estado` int(11) NOT NULL,
  `estado` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `estado`
--

INSERT INTO `estado` (`id_estado`, `estado`) VALUES
(1, 'Activo'),
(2, 'Inactivo'),
(3, 'Pendiente');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gestiones`
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
  `subTipificacion` varchar(250) DEFAULT NULL,
  `celular` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `gestiones`
--

INSERT INTO `gestiones` (`id_gestion`, `id_llamada`, `fecha`, `canal`, `tipoGestion`, `comentario`, `fechaProximaGestion`, `nombre_AS`, `tipificacion`, `subTipificacion`, `celular`) VALUES
(1, 1001, '2024-03-05', 'Telefónico', 'Seguimiento', 'Cliente interesado en el producto', '2024-03-10', 'operador1', 'Llamada efectiva', 'Cierre de venta', '3001234567'),
(2, 1002, '2024-03-04', 'WhatsApp', 'Información', 'Cliente pidió detalles', '2024-03-08', 'operador1', 'Volver a llamar', 'Interesado', '3017654321');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `kliiker`
--

CREATE TABLE `kliiker` (
  `id_Kliiker` varchar(250) DEFAULT NULL,
  `nombre` varchar(250) DEFAULT NULL,
  `apellido` varchar(250) DEFAULT NULL,
  `celular` varchar(250) NOT NULL,
  `nivel` tinyint(1) DEFAULT NULL,
  `correo` varchar(250) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `venta` tinyint(1) DEFAULT NULL,
  `fechaIngreso` date DEFAULT NULL,
  `diaSinGestion` int(11) DEFAULT NULL,
  `gestionable` tinyint(1) DEFAULT NULL,
  `id_estado` int(11) DEFAULT NULL,
  `motivo_no_int` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `kliiker`
--

INSERT INTO `kliiker` (`id_Kliiker`, `nombre`, `apellido`, `celular`, `nivel`, `correo`, `fecha`, `venta`, `fechaIngreso`, `diaSinGestion`, `gestionable`, `id_estado`, `motivo_no_int`) VALUES
('K001', 'Juan', 'Pérez', '3001234567', 1, 'juan.perez@mail.com', '2024-03-01', 0, '2024-03-05', 2, 1, 1, ''),
('K002', 'María', 'González', '3017654321', 0, 'maria.gonzalez@mail.com', '2024-02-20', 1, '2024-02-25', 5, 0, 2, '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipificacion`
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
-- Volcado de datos para la tabla `tipificacion`
--

INSERT INTO `tipificacion` (`id_tipificacion`, `id_estado`, `tipificacion`, `rpc`, `Contactabilidad`, `Cierre_flujo`) VALUES
(1, 1, 'Llamada efectiva', 1, 1, 0),
(2, 2, 'No contesta', 0, 0, 0),
(3, 3, 'Volver a llamar', 1, 1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
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
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`nombre_AS`, `documento`, `password`, `usuario`, `rol`, `estadoUsuario`) VALUES
('admin', 12345678, 'admin123', 'admin_user', 'Administrador', 1),
('operador1', 87654321, 'op12345', 'operador_01', 'Operador', 1),
('Valentina', 1036252267, '1234567890', 'Valen1', 'Administrador', 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `estado`
--
ALTER TABLE `estado`
  ADD PRIMARY KEY (`id_estado`);

--
-- Indices de la tabla `gestiones`
--
ALTER TABLE `gestiones`
  ADD PRIMARY KEY (`id_gestion`),
  ADD UNIQUE KEY `id_llamada` (`id_llamada`),
  ADD KEY `nombre_AS` (`nombre_AS`),
  ADD KEY `celular` (`celular`);

--
-- Indices de la tabla `kliiker`
--
ALTER TABLE `kliiker`
  ADD PRIMARY KEY (`celular`),
  ADD UNIQUE KEY `id_Kliker` (`id_Kliiker`),
  ADD UNIQUE KEY `correo` (`correo`),
  ADD KEY `id_estado` (`id_estado`);

--
-- Indices de la tabla `tipificacion`
--
ALTER TABLE `tipificacion`
  ADD PRIMARY KEY (`id_tipificacion`),
  ADD KEY `id_estado` (`id_estado`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`nombre_AS`),
  ADD UNIQUE KEY `documento` (`documento`),
  ADD UNIQUE KEY `usuario` (`usuario`);

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `gestiones`
--
ALTER TABLE `gestiones`
  ADD CONSTRAINT `gestiones_ibfk_1` FOREIGN KEY (`nombre_AS`) REFERENCES `usuarios` (`nombre_AS`),
  ADD CONSTRAINT `gestiones_ibfk_2` FOREIGN KEY (`celular`) REFERENCES `kliiker` (`celular`);

--
-- Filtros para la tabla `kliiker`
--
ALTER TABLE `kliiker`
  ADD CONSTRAINT `kliiker_ibfk_1` FOREIGN KEY (`id_estado`) REFERENCES `estado` (`id_estado`);

--
-- Filtros para la tabla `tipificacion`
--
ALTER TABLE `tipificacion`
  ADD CONSTRAINT `tipificacion_ibfk_1` FOREIGN KEY (`id_estado`) REFERENCES `estado` (`id_estado`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
