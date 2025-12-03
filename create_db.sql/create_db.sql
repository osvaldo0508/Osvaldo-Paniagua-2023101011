-- Script para crear la base de datos y la tabla de contactos
CREATE DATABASE IF NOT EXISTS ganados_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE ganados_db;

CREATE TABLE IF NOT EXISTS contactos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  apellido VARCHAR(100) NOT NULL,
  correo VARCHAR(150) NOT NULL,
  celular VARCHAR(50),
  horario VARCHAR(100),
  creado_en DATETIME,
  INDEX(correo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;