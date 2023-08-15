-- MariaDB dump 10.17  Distrib 10.4.14-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: cdctexcalac
-- ------------------------------------------------------
-- Server version	10.4.14-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `administradores`
--

DROP TABLE IF EXISTS `administradores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `administradores` (
  `id_admin` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_admin` varchar(50) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `aPaterno_admin` varchar(50) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `aMaterno_admin` varchar(50) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `correoE_admin` varchar(50) NOT NULL,
  `contrasenia_admin` varchar(102) NOT NULL,
  `telefono_admin` text NOT NULL,
  `edad_admin` int(2) NOT NULL,
  PRIMARY KEY (`id_admin`),
  UNIQUE KEY `id_admin` (`id_admin`),
  UNIQUE KEY `correoE_admin` (`correoE_admin`),
  UNIQUE KEY `telefono_admin` (`telefono_admin`) USING HASH
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administradores`
--

LOCK TABLES `administradores` WRITE;
/*!40000 ALTER TABLE `administradores` DISABLE KEYS */;
INSERT INTO `administradores` VALUES (1,'Mauricio','Lopez','Gatel','mauri.lop@gmail.com','admin','2411234556',42),(2,'Juan','Marin','Valente','valma3@gmail.com','admin','2476161231',39);
/*!40000 ALTER TABLE `administradores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alumnos`
--

DROP TABLE IF EXISTS `alumnos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alumnos` (
  `id_alumno` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_alumno` varchar(50) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `aPaterno_alumno` varchar(50) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `aMaterno_alumno` varchar(50) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `correoE_alumno` varchar(50) NOT NULL,
  `contrasenia_alumno` varchar(102) NOT NULL,
  `telefono_alumno` text NOT NULL,
  `edad_alumno` int(2) NOT NULL,
  `fechaRegistro_alumno` date DEFAULT NULL,
  PRIMARY KEY (`id_alumno`),
  UNIQUE KEY `correoE_alumno` (`correoE_alumno`),
  UNIQUE KEY `telefono_alumno` (`telefono_alumno`) USING HASH
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `profesores`
--

DROP TABLE IF EXISTS `profesores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `profesores` (
  `id_profesor` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_profesor` varchar(50) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `aPaterno_profesor` varchar(50) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `aMaterno_profesor` varchar(50) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `correoE_profesor` varchar(50) NOT NULL,
  `contrasenia_profesor` varchar(102) NOT NULL,
  `telefono_profesor` text NOT NULL,
  `edad_profesor` int(2) NOT NULL,
  `fechaRegistro_profesor` date DEFAULT NULL,
  PRIMARY KEY (`id_profesor`),
  UNIQUE KEY `correoE_profesor` (`correoE_profesor`),
  UNIQUE KEY `telefono_profesor` (`telefono_profesor`) USING HASH
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `talleres`
--

DROP TABLE IF EXISTS `talleres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `talleres` (
  `id_taller` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_taller` varchar(50) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `descrip_taller` text CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `categoria_taller` varchar(50) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `id_profesor` int(11) DEFAULT NULL,
  `fechaRegistro_taller` date NOT NULL,
  `fechaAsignacion_taller` date DEFAULT NULL,
  PRIMARY KEY (`id_taller`),
  KEY `id_profesor` (`id_profesor`),
  CONSTRAINT `talleres_ibfk_2` FOREIGN KEY (`id_profesor`) REFERENCES `profesores` (`id_profesor`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `toma`
--

DROP TABLE IF EXISTS `toma`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `toma` (
  `id_alumno` int(11) NOT NULL,
  `id_taller` int(11) NOT NULL,
  `fechaInscripcion` date DEFAULT NULL,
  KEY `id_alumno` (`id_alumno`),
  KEY `id_taller` (`id_taller`),
  CONSTRAINT `toma_ibfk_1` FOREIGN KEY (`id_alumno`) REFERENCES `alumnos` (`id_alumno`),
  CONSTRAINT `toma_ibfk_2` FOREIGN KEY (`id_taller`) REFERENCES `talleres` (`id_taller`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-08-15  0:31:00
