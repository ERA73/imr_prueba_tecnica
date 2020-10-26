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
  `id_bicicleta` int(11) NOT NULL AUTO_INCREMENT,
  `foto` longtext COLLATE utf8_unicode_ci DEFAULT NULL,
  `us_documento` int(11) NOT NULL,
  PRIMARY KEY (`id_bicicleta`),
  KEY `FK_bicicleta_usuario` (`us_documento`),
  CONSTRAINT `FK_bicicleta_usuario` FOREIGN KEY (`us_documento`) REFERENCES `usuario` (`documento`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bicicleta`
--

LOCK TABLES `bicicleta` WRITE;
/*!40000 ALTER TABLE `bicicleta` DISABLE KEYS */;
INSERT INTO `bicicleta` VALUES (1,'',1231231231),(2,'',1231231231),(3,'',1231231233),(4,'',1231231233);
/*!40000 ALTER TABLE `bicicleta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `carro`
--

DROP TABLE IF EXISTS `carro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `carro` (
  `id_carro` int(11) NOT NULL AUTO_INCREMENT,
  `placa` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `modelo` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `puertas` int(11) NOT NULL,
  `foto` longtext COLLATE utf8_unicode_ci DEFAULT NULL,
  `us_documento` int(11) NOT NULL,
  PRIMARY KEY (`id_carro`),
  KEY `FK_carro_usuario` (`us_documento`),
  CONSTRAINT `FK_carro_usuario` FOREIGN KEY (`us_documento`) REFERENCES `usuario` (`documento`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carro`
--

LOCK TABLES `carro` WRITE;
/*!40000 ALTER TABLE `carro` DISABLE KEYS */;
INSERT INTO `carro` VALUES (2,'asd123','2019',4,'',1231231231),(3,'qwe123','2010',2,'',1231231231),(4,'iop123','2016',4,'',1231231233),(5,'jkl123','1998',2,'',1231231233);
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
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `celda`
--

LOCK TABLES `celda` WRITE;
/*!40000 ALTER TABLE `celda` DISABLE KEYS */;
INSERT INTO `celda` VALUES (28,1,'carro','ocupado'),(29,2,'carro','ocupado'),(30,3,'carro','libre'),(31,4,'carro','libre'),(32,5,'carro','libre'),(33,6,'carro','libre'),(34,7,'carro','libre'),(35,8,'carro','libre'),(36,9,'carro','libre'),(37,10,'carro','libre'),(38,1,'moto','libre'),(39,2,'moto','libre'),(40,3,'moto','libre'),(41,4,'moto','libre'),(42,5,'moto','libre'),(43,6,'moto','libre'),(44,7,'moto','libre'),(45,8,'moto','libre'),(46,9,'moto','libre'),(47,10,'moto','libre'),(48,1,'bicicleta','libre'),(49,2,'bicicleta','libre'),(50,3,'bicicleta','libre'),(51,4,'bicicleta','libre'),(52,5,'bicicleta','libre'),(53,6,'bicicleta','libre'),(54,7,'bicicleta','libre'),(55,8,'bicicleta','libre'),(56,9,'bicicleta','libre'),(57,10,'bicicleta','libre');
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
  `fecha_entrada` datetime NOT NULL DEFAULT current_timestamp(),
  `fecha_salida` datetime DEFAULT NULL,
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
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrada`
--

LOCK TABLES `entrada` WRITE;
/*!40000 ALTER TABLE `entrada` DISABLE KEYS */;
INSERT INTO `entrada` VALUES (7,'2020-10-25 15:20:24','2020-10-25 15:55:18',2,NULL,NULL,28),(8,'2020-10-25 16:20:34','2020-10-25 16:20:53',NULL,NULL,1,48),(9,'2020-10-26 13:52:16','2020-10-26 13:52:38',3,NULL,NULL,28),(10,'2020-10-26 13:53:01',NULL,3,NULL,NULL,28),(11,'2020-10-26 15:35:07',NULL,4,NULL,NULL,29);
/*!40000 ALTER TABLE `entrada` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `moto`
--

DROP TABLE IF EXISTS `moto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `moto` (
  `id_moto` int(11) NOT NULL AUTO_INCREMENT,
  `placa` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `cilindraje` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `tiempos` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `foto` longtext COLLATE utf8_unicode_ci DEFAULT NULL,
  `us_documento` int(11) NOT NULL,
  PRIMARY KEY (`id_moto`),
  KEY `FK_moto_usuario` (`us_documento`),
  CONSTRAINT `FK_moto_usuario` FOREIGN KEY (`us_documento`) REFERENCES `usuario` (`documento`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `moto`
--

LOCK TABLES `moto` WRITE;
/*!40000 ALTER TABLE `moto` DISABLE KEYS */;
INSERT INTO `moto` VALUES (1,'zxc123','125','4','',1231231231),(2,'rty123','200','4','',1231231231),(3,'fgh123','150','4','',1231231233),(4,'bnm123','175','2','',1231231233);
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
INSERT INTO `usuario` VALUES (1231231231,'juan','peres'),(1231231233,'diana','gomez');
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

-- Dump completed on 2020-10-26 15:58:48
