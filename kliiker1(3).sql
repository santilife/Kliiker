-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 12-03-2025 a las 06:22:40
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
-- Estructura de tabla para la tabla `estadokliiker`
--

CREATE TABLE `estadokliiker` (
  `id_estado` int(11) NOT NULL,
  `estado` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `estadokliiker`
--

INSERT INTO `estadokliiker` (`id_estado`, `estado`) VALUES
(0, 'Nuevo'),
(1, 'llamada_1'),
(2, 'llamada_2'),
(3, 'llamada_3'),
(4, 'llamada_4');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `flujotrabajo`
--

CREATE TABLE `flujotrabajo` (
  `id_flujoTrabajo` int(11) NOT NULL,
  `nivel` tinyint(1) NOT NULL,
  `id_estado` int(11) NOT NULL,
  `diasParaGestion` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  `id_tipificacion` int(11) DEFAULT NULL,
  `motivoNoInteres` varchar(250) DEFAULT NULL,
  `id_estado` int(11) NOT NULL,
  `celular` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `gestiones`
--

INSERT INTO `gestiones` (`id_gestion`, `id_llamada`, `fecha`, `canal`, `tipoGestion`, `comentario`, `fechaProximaGestion`, `nombre_AS`, `id_tipificacion`, `motivoNoInteres`, `id_estado`, `celular`) VALUES
(1, 1000, '2025-03-12', 'Telefono', 'Nose', 'Nose', NULL, 'Marissa', 1, 'asda', 3, '3001234567'),
(24, 1002, '2025-03-12', 'Whatsapp', 'Entrada', 'Segunda Prueba', NULL, NULL, 10, 'Consiguió trabajo', 1, '3017654321');

--
-- Disparadores `gestiones`
--
DELIMITER $$
CREATE TRIGGER `tr_after_insert_gestiones` AFTER INSERT ON `gestiones` FOR EACH ROW BEGIN    
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
        id_tipificacion,
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
        NEW.id_tipificacion,
        NEW.celular,
        CASE 
            WHEN (SELECT tipificacion FROM tipificacion WHERE id_tipificacion = NEW.id_tipificacion) = 'Sin interes' 
            THEN NEW.motivoNoInteres
            ELSE NULL
        END
    );
END
$$
DELIMITER ;
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
        id_tipificacion,
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
        NEW.id_tipificacion,
        NEW.celular,
        CASE 
         WHEN (SELECT tipificacion FROM tipificacion WHERE id_tipificacion = NEW.id_tipificacion) = 'Sin interes' 
            THEN NEW.motivoNoInteres
            ELSE NULL
        END
    );
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historial_gestiones`
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
  `id_tipificacion` int(11) DEFAULT NULL,
  `celular` varchar(250) DEFAULT NULL,
  `motivoNoInteres` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `historial_gestiones`
--

INSERT INTO `historial_gestiones` (`id_historial`, `id_gestion`, `id_estado`, `id_llamada`, `fecha`, `canal`, `tipoGestion`, `comentario`, `fechaProximaGestion`, `nombre_AS`, `id_tipificacion`, `celular`, `motivoNoInteres`) VALUES
(19, 1, 3, 1000, '2025-03-12', 'Telefono', 'Nose', 'Nose', NULL, 'Marissa', 1, '3001234567', NULL),
(20, 24, 1, 1002, '2025-03-12', 'Whatsapp', 'Entrada', 'Segunda Prueba', NULL, NULL, 10, '3017654321', 'Consiguió trabajo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `kliiker`
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
-- Volcado de datos para la tabla `kliiker`
--

INSERT INTO `kliiker` (`id_Kliiker`, `nombre`, `apellido`, `celular`, `nivel`, `correo`, `fecha`, `venta`, `fechaIngreso`, `diaSinGestion`, `gestionable`, `id_estado`, `fechaSinGestion`) VALUES
('K003', 'Josue', 'Narvaez', '192831246', 0, 'josue@gmail.com', '2025-03-11', 0, NULL, NULL, NULL, 3, NULL),
('K001', 'Juan', 'Pérez', '3001234567', 1, 'juan.perez@mail.com', '2024-03-01', 0, '2024-03-05', 2, 1, 1, NULL),
('K002', 'María', 'González', '3017654321', 0, 'maria.gonzalez@mail.com', '2024-02-20', 1, '2024-02-25', 5, 0, 2, NULL),
('K004', 'Maria', 'Lopez', '321287463', 0, 'maria@gmail.com', NULL, 0, NULL, NULL, NULL, 4, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipificacion`
--

CREATE TABLE `tipificacion` (
  `id_tipificacion` int(11) NOT NULL,
  `id_estado` int(11) DEFAULT NULL,
  `tipificacion` varchar(250) DEFAULT NULL,
  `rpc` tinyint(1) NOT NULL,
  `contactabilidad` tinyint(1) NOT NULL,
  `cierre_flujo` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tipificacion`
--

INSERT INTO `tipificacion` (`id_tipificacion`, `id_estado`, `tipificacion`, `rpc`, `contactabilidad`, `cierre_flujo`) VALUES
(1, NULL, 'Buzón de voz', 0, 0, 0),
(2, NULL, 'Equivocado', 0, 1, 0),
(3, NULL, 'Información general', 1, 1, 0),
(4, NULL, 'Interesado a Futuro', 1, 1, 0),
(5, NULL, 'Lead ya compró', 1, 1, 0),
(6, NULL, 'No Contesta', 0, 0, 0),
(7, NULL, 'Novedad en el registro', 1, 1, 0),
(8, NULL, 'Registro exitoso', 1, 1, 0),
(9, NULL, 'Seguimiento', 1, 1, 0),
(10, NULL, 'Sin interés', 1, 1, 0),
(11, NULL, 'Volver a llamar', 1, 1, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `uploaded_db`
--

CREATE TABLE `uploaded_db` (
  `id_db` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `date_upload` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `uploaded_db`
--

INSERT INTO `uploaded_db` (`id_db`, `nombre`, `date_upload`) VALUES
(2, 'basesKliiker.csv', '2025-03-10 11:41:45'),
(3, 'Histórico.csv', '2025-03-10 11:42:01');

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
('Andres Lopez', 123456678, '123456678', 'andresGay', 'Asesor', 2),
('brayan ocampo', 1011394242, '1011394242', 'brayanOcam', 'Administrador', NULL),
('Marissa', 1036252264, '1036252264', 'MarissaLK', 'Asesor', 1),
('marissasa', 1234567890, '1234567890', 'marissasa', 'Administrador', 1),
('operador1', 87654321, 'op12345', 'operador_01', 'Operador', 1),
('Pedro PereZ', 123454321, '123454321', 'Pedrop', 'Asesor', 1),
('Santi', 10, '10', 'Santifile', 'Administrador', 2),
('santi otalvaro', 1040033660, '1040033660', 'Santifiles', 'Asesor', 2),
('Valentina', 1036252267, '1234567890', 'Valen1', 'Administrador', 1),
('valentina Tobón', 23456789, '23456789', 'valent22_', 'Asesor', 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `estadokliiker`
--
ALTER TABLE `estadokliiker`
  ADD PRIMARY KEY (`id_estado`);

--
-- Indices de la tabla `gestiones`
--
ALTER TABLE `gestiones`
  ADD PRIMARY KEY (`id_gestion`),
  ADD UNIQUE KEY `id_llamada` (`id_llamada`),
  ADD KEY `nombre_AS` (`nombre_AS`),
  ADD KEY `celular` (`celular`),
  ADD KEY `id_tipificacion` (`id_tipificacion`);

--
-- Indices de la tabla `historial_gestiones`
--
ALTER TABLE `historial_gestiones`
  ADD PRIMARY KEY (`id_historial`),
  ADD KEY `id_gestion` (`id_gestion`);

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
  ADD KEY `id_estado` (`id_estado`),
  ADD KEY `id_tipificacion` (`id_tipificacion`);

--
-- Indices de la tabla `uploaded_db`
--
ALTER TABLE `uploaded_db`
  ADD PRIMARY KEY (`id_db`);

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
  MODIFY `id_gestion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT de la tabla `historial_gestiones`
--
ALTER TABLE `historial_gestiones`
  MODIFY `id_historial` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `uploaded_db`
--
ALTER TABLE `uploaded_db`
  MODIFY `id_db` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `gestiones`
--
ALTER TABLE `gestiones`
  ADD CONSTRAINT `gestiones_ibfk_1` FOREIGN KEY (`nombre_AS`) REFERENCES `usuarios` (`nombre_AS`),
  ADD CONSTRAINT `gestiones_ibfk_2` FOREIGN KEY (`celular`) REFERENCES `kliiker` (`celular`),
  ADD CONSTRAINT `gestiones_ibfk_3` FOREIGN KEY (`id_tipificacion`) REFERENCES `tipificacion` (`id_tipificacion`);

--
-- Filtros para la tabla `historial_gestiones`
--
ALTER TABLE `historial_gestiones`
  ADD CONSTRAINT `historial_gestiones_ibfk_1` FOREIGN KEY (`id_gestion`) REFERENCES `gestiones` (`id_gestion`);

--
-- Filtros para la tabla `kliiker`
--
ALTER TABLE `kliiker`
  ADD CONSTRAINT `kliiker_ibfk_1` FOREIGN KEY (`id_estado`) REFERENCES `estadokliiker` (`id_estado`);

--
-- Filtros para la tabla `tipificacion`
--
ALTER TABLE `tipificacion`
  ADD CONSTRAINT `tipificacion_ibfk_1` FOREIGN KEY (`id_estado`) REFERENCES `estadokliiker` (`id_estado`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
