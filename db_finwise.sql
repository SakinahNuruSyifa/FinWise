CREATE DATABASE db_finwise;

USE db_finwise;

CREATE TABLE `user` (
	id INT PRIMARY KEY AUTO_INCREMENT,
	email VARCHAR(100) NOT NULL,
	`password` VARCHAR(100) NOT NULL
);

CREATE TABLE pengeluaran (
	id INT PRIMARY KEY AUTO_INCREMENT,
	tanggal DATE NOT NULL,
	jumlah INT NOT NULL,
	kategori VARCHAR(100) NOT NULL,
	user_id INT NOT NULL,
	FOREIGN KEY (user_id) REFERENCES `user` (id)
);

CREATE TABLE pemasukan (
	id INT PRIMARY KEY AUTO_INCREMENT,
	sumber VARCHAR(100) NOT NULL,
	tanggal DATE NOT NULL,
	jumlah INT NOT NULL,
	user_id INT NOT NULL,
	FOREIGN KEY (user_id) REFERENCES `user` (id)
); 

CREATE TABLE anggaran (
	id INT PRIMARY KEY AUTO_INCREMENT,
	tanggal_mulai DATE NOT NULL,
	tanggal_akhir DATE NOT NULL,
	total INT NOT NULL,
	user_id INT NOT NULL,
	FOREIGN KEY (user_id) REFERENCES `user` (id)
);

CREATE TABLE laporan (
	id INT PRIMARY KEY AUTO_INCREMENT,
	total_pengeluaran DECIMAL(10, 2) NOT NULL,
	total_pemasukan DECIMAL(10, 2) NOT NULL,
	user_id INT NOT NULL,
	FOREIGN KEY (user_id) REFERENCES `user` (id),
	FOREIGN KEY (id) REFERENCES pemasukan (id),
	FOREIGN KEY (id) REFERENCES pengeluaran (id)
);