-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 02-03-2025 a las 02:49:17
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
-- Base de datos: `bd_klikeer`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gestiones`
--

CREATE TABLE `gestiones` (
  `id_gestiones` int(11) NOT NULL,
  `id_llamadas` int(11) NOT NULL,
  `fecha` datetime NOT NULL,
  `canal` varchar(250) NOT NULL,
  `tipoGestion` varchar(250) NOT NULL,
  `comentario` varchar(250) NOT NULL,
  `nombre_AS` varchar(250) NOT NULL,
  `tipificacion` varchar(250) NOT NULL,
  `subTipificacion` varchar(250) NOT NULL,
  `celular` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `kliiker`
--

CREATE TABLE `kliiker` (
  `celular` varchar(10) NOT NULL,
  `id_kliiker` varchar(250) DEFAULT NULL,
  `nombre` varchar(250) NOT NULL,
  `apellido` varchar(250) NOT NULL,
  `codigo s/n` tinyint(1) NOT NULL,
  `correo` varchar(250) NOT NULL,
  `fecha` datetime NOT NULL,
  `venta` tinyint(1) NOT NULL,
  `fechaIngreso` datetime NOT NULL,
  `diaSinGestion` tinyint(1) NOT NULL,
  `gestionable` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipificaciones`
--

CREATE TABLE `tipificaciones` (
  `id_tipificacion` int(11) NOT NULL,
  `tipificacion` varchar(250) NOT NULL,
  `subTipificacion` varchar(250) NOT NULL,
  `rcp` tinyint(1) NOT NULL,
  `contactabilidad` tinyint(1) NOT NULL,
  `cierreFlujo` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
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
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `gestiones`
--
ALTER TABLE `gestiones`
  ADD PRIMARY KEY (`id_gestiones`),
  ADD UNIQUE KEY `nombre_AS` (`nombre_AS`),
  ADD UNIQUE KEY `id_llamadas` (`id_llamadas`);

--
-- Indices de la tabla `kliiker`
--
ALTER TABLE `kliiker`
  ADD PRIMARY KEY (`celular`),
  ADD UNIQUE KEY `id_kliiker` (`id_kliiker`,`correo`);

--
-- Indices de la tabla `tipificaciones`
--
ALTER TABLE `tipificaciones`
  ADD PRIMARY KEY (`id_tipificacion`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`nombre_AS`),
  ADD UNIQUE KEY `documento` (`documento`),
  ADD UNIQUE KEY `usuario` (`usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `gestiones`
--
ALTER TABLE `gestiones`
  MODIFY `id_gestiones` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
