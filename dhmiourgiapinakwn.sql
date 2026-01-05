PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS `etairia` (
	`etairia_id` integer primary key AUTOINCREMENT,
	`onoma` TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS `aerodromio` (
	`aerodromio_id` integer primary key AUTOINCREMENT,
	`kwdikos` TEXT NOT NULL UNIQUE,
	`polh` TEXT NOT NULL,
	`xwra` TEXT NOT NULL,
	`zwnh_wras` TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS `katigoria_theshs` (
	`katigoria_id` integer primary key AUTOINCREMENT,
	`onoma` TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS `aeroplano` (
	`aeroplano_id` integer primary key AUTOINCREMENT,
	`montelo` TEXT NOT NULL,
	`sunolo_thesewn` INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS `thesh` (
	`thesh_id` integer primary key AUTOINCREMENT,
	`aeroplano_id` INTEGER NOT NULL,
	`katigoria_id` INTEGER NOT NULL,
	`arithmos_theshs` TEXT NOT NULL,
FOREIGN KEY(`aeroplano_id`) REFERENCES `aeroplano`(`aeroplano_id`),
FOREIGN KEY(`katigoria_id`) REFERENCES `katigoria_theshs`(`katigoria_id`)
);
CREATE TABLE IF NOT EXISTS `xrhsths` (
	`xrhsths_id` integer primary key AUTOINCREMENT,
	`onoma` TEXT NOT NULL,
    `epitheto` TEXT NOT NULL,
	`email` TEXT NOT NULL UNIQUE,
	`thlefwno` TEXT NOT NULL,
	`dieuthunsh` TEXT NOT NULL,
	`kwdikos` TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS `epivaths` (
	`epivaths_id` integer primary key AUTOINCREMENT,
	`onoma` TEXT NOT NULL,
    `epitheto` TEXT NOT NULL,
	`at_diabathrio` TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS `krathsh` (
	`ar_krathshs` integer primary key AUTOINCREMENT,
	`xrhsths_id` INTEGER NOT NULL,
	`hmeromhnia_krathshs` TEXT NOT NULL,
	`sunoliko_kostos` REAL NOT NULL,
	`ar_atomwn` INTEGER NOT NULL,
FOREIGN KEY(`xrhsths_id`) REFERENCES `xrhsths`(`xrhsths_id`)
);
CREATE TABLE IF NOT EXISTS `pthsh` (
	`pthsh_id` integer primary key AUTOINCREMENT,
	`arithmos_pthshs` TEXT NOT NULL,
	`etairia_id` INTEGER NOT NULL,
	`aeroplano_id` INTEGER NOT NULL,
	`aerodromio_anaxwrhshs_id` INTEGER NOT NULL,
	`aerodromio_afikshs_id` INTEGER NOT NULL,
	`wra_anaxwrhshs` TEXT NOT NULL,
	`wra_afikshs` TEXT NOT NULL,
	`pulh` TEXT NOT NULL,
    `vasikh_timh` REAL NOT NULL,
FOREIGN KEY(`etairia_id`) REFERENCES `etairia`(`etairia_id`),
FOREIGN KEY(`aeroplano_id`) REFERENCES `aeroplano`(`aeroplano_id`),
FOREIGN KEY(`aerodromio_anaxwrhshs_id`) REFERENCES `aerodromio`(`aerodromio_id`),
FOREIGN KEY(`aerodromio_afikshs_id`) REFERENCES `aerodromio`(`aerodromio_id`)
);
CREATE TABLE IF NOT EXISTS `eisithrio` (
	`eisithrio_id` integer primary key AUTOINCREMENT,
	`krathsh_id` INTEGER NOT NULL,
	`pthsh_id` INTEGER NOT NULL,
	`epivaths_id` INTEGER NOT NULL,
	`arithmos_theshs` TEXT NOT NULL,
	`timh` REAL NOT NULL,
	`hmeromhnia_wra` TEXT NOT NULL,
FOREIGN KEY(`krathsh_id`) REFERENCES `krathsh`(`ar_krathshs`),
FOREIGN KEY(`pthsh_id`) REFERENCES `pthsh`(`pthsh_id`),
FOREIGN KEY(`epivaths_id`) REFERENCES `epivaths`(`epivaths_id`)
);