-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema health_monitoring
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `health_monitoring` ;

-- -----------------------------------------------------
-- Schema health_monitoring
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `health_monitoring` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `health_monitoring` ;

-- -----------------------------------------------------
-- Table `health_monitoring`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `health_monitoring`.`user` (
  `userId` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(255) NOT NULL,
  `firstName` VARCHAR(255) NOT NULL,
  `lastName` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `weight` DOUBLE NULL DEFAULT NULL,
  `height` DOUBLE NULL DEFAULT NULL,
  `bmi` DOUBLE NULL DEFAULT NULL,
  PRIMARY KEY (`userId`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

CREATE UNIQUE INDEX `username` ON `health_monitoring`.`user` (`username` ASC) VISIBLE;

CREATE UNIQUE INDEX `email` ON `health_monitoring`.`user` (`email` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `health_monitoring`.`meals`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `health_monitoring`.`meals` (
  `mealId` INT NOT NULL AUTO_INCREMENT,
  `mealName` VARCHAR(255) NOT NULL,
  `calories` FLOAT NOT NULL,
  `mealDate` DATE NOT NULL,
  `userId` INT NULL DEFAULT NULL,
  PRIMARY KEY (`mealId`),
  CONSTRAINT `fk_meals_user`
    FOREIGN KEY (`userId`)
    REFERENCES `health_monitoring`.`user` (`userId`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

CREATE INDEX `fk_meals_user` ON `health_monitoring`.`meals` (`userId` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `health_monitoring`.`sleep`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `health_monitoring`.`sleep` (
  `sleepId` INT NOT NULL AUTO_INCREMENT,
  `durationInHours` INT NOT NULL,
  `sleepQuality` VARCHAR(255) NULL DEFAULT NULL,
  `date` DATE NOT NULL,
  `userId` INT NULL DEFAULT NULL,
  PRIMARY KEY (`sleepId`),
  CONSTRAINT `fk_sleep_user`
    FOREIGN KEY (`userId`)
    REFERENCES `health_monitoring`.`user` (`userId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

CREATE INDEX `fk_sleep_user` ON `health_monitoring`.`sleep` (`userId` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `health_monitoring`.`workouts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `health_monitoring`.`workouts` (
  `workoutId` INT NOT NULL AUTO_INCREMENT,
  `workoutName` VARCHAR(255) NOT NULL,
  `durationInMinutes` INT NOT NULL,
  `caloriesBurned` FLOAT NOT NULL,
  `workoutDate` DATE NOT NULL,
  `userId` INT NULL DEFAULT NULL,
  PRIMARY KEY (`workoutId`),
  CONSTRAINT `fk_workouts_user`
    FOREIGN KEY (`userId`)
    REFERENCES `health_monitoring`.`user` (`userId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

CREATE INDEX `fk_workouts_user` ON `health_monitoring`.`workouts` (`userId` ASC) VISIBLE;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
