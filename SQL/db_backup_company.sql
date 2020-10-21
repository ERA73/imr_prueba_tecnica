-- MySQL dump 10.16  Distrib 10.2.12-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: parqueadero
-- ------------------------------------------------------
-- Server version	10.2.12-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bicicleta`
--

DROP TABLE IF EXISTS `bicicleta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bicicleta` (
  `id_bicicleta` int(11) NOT NULL,
  `foto` longtext COLLATE utf8_unicode_ci DEFAULT NULL,
  `us_documento` int(11) NOT NULL,
  PRIMARY KEY (`id_bicicleta`),
  KEY `FK_bicicleta_usuario` (`us_documento`),
  CONSTRAINT `FK_bicicleta_usuario` FOREIGN KEY (`us_documento`) REFERENCES `usuario` (`documento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bicicleta`
--

LOCK TABLES `bicicleta` WRITE;
/*!40000 ALTER TABLE `bicicleta` DISABLE KEYS */;
/*!40000 ALTER TABLE `bicicleta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `carro`
--

DROP TABLE IF EXISTS `carro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `carro` (
  `id_carro` int(11) NOT NULL,
  `placa` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `modelo` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `puertas` int(11) NOT NULL,
  `foto` longtext COLLATE utf8_unicode_ci DEFAULT NULL,
  `us_documento` int(11) NOT NULL,
  PRIMARY KEY (`id_carro`),
  KEY `FK_carro_usuario` (`us_documento`),
  CONSTRAINT `FK_carro_usuario` FOREIGN KEY (`us_documento`) REFERENCES `usuario` (`documento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carro`
--

LOCK TABLES `carro` WRITE;
/*!40000 ALTER TABLE `carro` DISABLE KEYS */;
/*!40000 ALTER TABLE `carro` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `celda`
--

DROP TABLE IF EXISTS `celda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `celda` (
  `id_celda` int(11) NOT NULL AUTO_INCREMENT,
  `numero` int(11) NOT NULL,
  `tipo` set('carro','moto','bicicleta') COLLATE utf8_unicode_ci NOT NULL DEFAULT 'carro',
  `estado` set('libre','ocupado') COLLATE utf8_unicode_ci NOT NULL DEFAULT 'libre',
  PRIMARY KEY (`id_celda`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `celda`
--

LOCK TABLES `celda` WRITE;
/*!40000 ALTER TABLE `celda` DISABLE KEYS */;
/*!40000 ALTER TABLE `celda` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrada`
--

DROP TABLE IF EXISTS `entrada`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrada` (
  `consecutivo` int(11) NOT NULL AUTO_INCREMENT,
  `fecha` datetime NOT NULL DEFAULT current_timestamp(),
  `id_carro` int(11) DEFAULT NULL,
  `id_moto` int(11) DEFAULT NULL,
  `id_bicicleta` int(11) DEFAULT NULL,
  `id_celda` int(11) NOT NULL,
  PRIMARY KEY (`consecutivo`),
  KEY `FK_entrada_carro` (`id_carro`),
  KEY `FK_entrada_moto` (`id_moto`),
  KEY `FK_entrada_bicicleta` (`id_bicicleta`),
  KEY `FK_entrada_celda` (`id_celda`),
  CONSTRAINT `FK_entrada_bicicleta` FOREIGN KEY (`id_bicicleta`) REFERENCES `bicicleta` (`id_bicicleta`),
  CONSTRAINT `FK_entrada_carro` FOREIGN KEY (`id_carro`) REFERENCES `carro` (`id_carro`),
  CONSTRAINT `FK_entrada_celda` FOREIGN KEY (`id_celda`) REFERENCES `celda` (`id_celda`),
  CONSTRAINT `FK_entrada_moto` FOREIGN KEY (`id_moto`) REFERENCES `moto` (`id_moto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrada`
--

LOCK TABLES `entrada` WRITE;
/*!40000 ALTER TABLE `entrada` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrada` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `moto`
--

DROP TABLE IF EXISTS `moto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `moto` (
  `id_moto` int(11) NOT NULL,
  `placa` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `cilindraje` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `tiempos` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `foto` longtext COLLATE utf8_unicode_ci DEFAULT NULL,
  `us_documento` int(11) NOT NULL,
  PRIMARY KEY (`id_moto`),
  KEY `FK_moto_usuario` (`us_documento`),
  CONSTRAINT `FK_moto_usuario` FOREIGN KEY (`us_documento`) REFERENCES `usuario` (`documento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `moto`
--

LOCK TABLES `moto` WRITE;
/*!40000 ALTER TABLE `moto` DISABLE KEYS */;
/*!40000 ALTER TABLE `moto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuario` (
  `documento` int(11) NOT NULL,
  `nombres` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `apellidos` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`documento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'parqueadero'
--

--
-- Dumping routines for database 'parqueadero'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-10-20 20:00:20
