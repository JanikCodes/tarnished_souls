-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema tarnished
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema tarnished
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `tarnished` DEFAULT CHARACTER SET utf8 ;
USE `tarnished` ;

-- -----------------------------------------------------
-- Table `tarnished`.`location`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tarnished`.`location` (
  `idLocation` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(75) NULL,
  `description` VARCHAR(160) NULL,
  PRIMARY KEY (`idLocation`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tarnished`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tarnished`.`user` (
  `idUser` VARCHAR(80) NOT NULL,
  `username` VARCHAR(100) CHARACTER SET 'utf8mb4' NOT NULL,
  `level` INT NOT NULL,
  `xp` INT NOT NULL,
  `souls` BIGINT NOT NULL,
  `vigor` INT NOT NULL,
  `mind` INT NOT NULL,
  `endurance` INT NOT NULL,
  `strength` INT NOT NULL,
  `dexterity` INT NOT NULL,
  `intelligence` INT NOT NULL,
  `faith` INT NOT NULL,
  `arcane` INT NOT NULL,
  `last_explore` BIGINT NOT NULL,
  `e_weapon` INT NULL DEFAULT NULL,
  `e_head` INT NULL DEFAULT NULL,
  `e_chest` INT NULL DEFAULT NULL,
  `e_legs` INT NULL DEFAULT NULL,
  `e_gauntlet` INT NULL DEFAULT NULL,
  `currentLocation` INT NOT NULL,
  `maxLocation` INT NOT NULL,
  `NG` INT NOT NULL,
  `last_quest` BIGINT NOT NULL,
  PRIMARY KEY (`idUser`),
  INDEX `fk_user_location1_idx` (`currentLocation` ASC),
  INDEX `fk_user_location2_idx` (`maxLocation` ASC),
  CONSTRAINT `fk_user_location1`
    FOREIGN KEY (`currentLocation`)
    REFERENCES `tarnished`.`location` (`idLocation`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_location2`
    FOREIGN KEY (`maxLocation`)
    REFERENCES `tarnished`.`location` (`idLocation`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tarnished`.`item`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tarnished`.`item` (
  `idItem` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `value` INT NOT NULL,
  `price` INT NOT NULL,
  `iconCategory` VARCHAR(100) NOT NULL,
  `type` VARCHAR(45) NOT NULL,
  `reqVigor` INT NOT NULL,
  `reqMind` INT NOT NULL,
  `reqEndurance` INT NOT NULL,
  `reqStrength` INT NOT NULL,
  `reqDexterity` INT NOT NULL,
  `reqIntelligence` INT NOT NULL,
  `reqFaith` INT NOT NULL,
  `reqArcane` INT NOT NULL,
  `obtainable` INT NOT NULL,
  `weight` DECIMAL NOT NULL,
  `iconUrl` VARCHAR(220) NULL DEFAULT NULL,
  `sclVigor` VARCHAR(2) NOT NULL,
  `sclMind` VARCHAR(2) NOT NULL,
  `sclEndurance` VARCHAR(2) NOT NULL,
  `sclStrength` VARCHAR(2) NOT NULL,
  `sclDexterity` VARCHAR(2) NOT NULL,
  `sclIntelligence` VARCHAR(2) NOT NULL,
  `sclFaith` VARCHAR(2) NOT NULL,
  `sclArcane` VARCHAR(2) NOT NULL,
  PRIMARY KEY (`idItem`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tarnished`.`user_has_item`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tarnished`.`user_has_item` (
  `idRel` INT NOT NULL AUTO_INCREMENT,
  `idUser` VARCHAR(80) NOT NULL,
  `idItem` INT NOT NULL,
  `level` INT NOT NULL,
  `count` INT NOT NULL,
  `value` INT NOT NULL,
  INDEX `fk_user_has_item_item1_idx` (`idItem` ASC),
  INDEX `fk_user_has_item_user_idx` (`idUser` ASC),
  PRIMARY KEY (`idRel`),
  CONSTRAINT `fk_user_has_item_user`
    FOREIGN KEY (`idUser`)
    REFERENCES `tarnished`.`user` (`idUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_has_item_item1`
    FOREIGN KEY (`idItem`)
    REFERENCES `tarnished`.`item` (`idItem`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tarnished`.`encounter`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tarnished`.`encounter` (
  `idEncounter` INT NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(200) NOT NULL,
  `dropRate` INT NOT NULL,
  `idLocation` INT NOT NULL,
  PRIMARY KEY (`idEncounter`),
  INDEX `fk_encounter_location1_idx` (`idLocation` ASC),
  CONSTRAINT `fk_encounter_location1`
    FOREIGN KEY (`idLocation`)
    REFERENCES `tarnished`.`location` (`idLocation`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tarnished`.`user_encounter`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tarnished`.`user_encounter` (
  `idRel` INT NOT NULL AUTO_INCREMENT,
  `idEncounter` INT NOT NULL,
  `idUser` VARCHAR(80) NOT NULL,
  `idItem` INT NULL DEFAULT NULL,
  `extra` INT NULL DEFAULT NULL,
  PRIMARY KEY (`idRel`),
  INDEX `fk_user_encounter_encounter1_idx` (`idEncounter` ASC),
  INDEX `fk_user_encounter_user1_idx` (`idUser` ASC),
  INDEX `fk_user_encounter_item1_idx` (`idItem` ASC),
  CONSTRAINT `fk_user_encounter_encounter1`
    FOREIGN KEY (`idEncounter`)
    REFERENCES `tarnished`.`encounter` (`idEncounter`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_encounter_user1`
    FOREIGN KEY (`idUser`)
    REFERENCES `tarnished`.`user` (`idUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_encounter_item1`
    FOREIGN KEY (`idItem`)
    REFERENCES `tarnished`.`item` (`idItem`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tarnished`.`enemy_logic`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tarnished`.`enemy_logic` (
  `idLogic` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idLogic`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tarnished`.`enemy`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tarnished`.`enemy` (
  `idEnemy` INT NOT NULL AUTO_INCREMENT,
  `idLogic` INT NOT NULL,
  `name` VARCHAR(75) NOT NULL,
  `description` VARCHAR(200) NULL,
  `health` INT NOT NULL,
  `runes` INT NOT NULL,
  `idLocation` INT NOT NULL,
  PRIMARY KEY (`idEnemy`, `idLocation`),
  INDEX `fk_enemy_enemy_logic1_idx` (`idLogic` ASC),
  INDEX `fk_enemy_location1_idx` (`idLocation` ASC),
  CONSTRAINT `fk_enemy_enemy_logic1`
    FOREIGN KEY (`idLogic`)
    REFERENCES `tarnished`.`enemy_logic` (`idLogic`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_enemy_location1`
    FOREIGN KEY (`idLocation`)
    REFERENCES `tarnished`.`location` (`idLocation`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tarnished`.`move_type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tarnished`.`move_type` (
  `idType` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idType`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tarnished`.`enemy_moves`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tarnished`.`enemy_moves` (
  `idMove` INT NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(200) NOT NULL,
  `phase` INT NOT NULL,
  `idType` INT NOT NULL,
  `idEnemy` INT NOT NULL,
  `damage` INT NULL DEFAULT NULL,
  `healing` INT NULL DEFAULT NULL,
  `duration` INT NULL DEFAULT NULL,
  `maxTargets` INT(1) NOT NULL,
  PRIMARY KEY (`idMove`, `idEnemy`),
  INDEX `fk_enemy_moves_move_type1_idx` (`idType` ASC),
  INDEX `fk_enemy_moves_enemy1_idx` (`idEnemy` ASC),
  CONSTRAINT `fk_enemy_moves_move_type1`
    FOREIGN KEY (`idType`)
    REFERENCES `tarnished`.`move_type` (`idType`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_enemy_moves_enemy1`
    FOREIGN KEY (`idEnemy`)
    REFERENCES `tarnished`.`enemy` (`idEnemy`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tarnished`.`enemy_has_item`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tarnished`.`enemy_has_item` (
  `idRel` INT NOT NULL AUTO_INCREMENT,
  `idItem` INT NOT NULL,
  `idEnemy` INT NOT NULL,
  `count` INT NOT NULL,
  `dropChance` INT NOT NULL,
  INDEX `fk_item_has_enemy_enemy1_idx` (`idEnemy` ASC),
  INDEX `fk_item_has_enemy_item1_idx` (`idItem` ASC),
  PRIMARY KEY (`idRel`),
  CONSTRAINT `fk_item_has_enemy_item1`
    FOREIGN KEY (`idItem`)
    REFERENCES `tarnished`.`item` (`idItem`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_item_has_enemy_enemy1`
    FOREIGN KEY (`idEnemy`)
    REFERENCES `tarnished`.`enemy` (`idEnemy`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tarnished`.`quest`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tarnished`.`quest` (
  `idQuest` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(80) NOT NULL,
  `description` VARCHAR(250) NOT NULL,
  `reqKills` INT NULL,
  `reqItemCount` INT NULL,
  `reqRunes` INT NULL,
  `idItem` INT NULL,
  `idEnemy` INT NULL,
  `runeReward` INT NULL,
  `locationIdReward` INT NULL,
  `reqExploreCount` INT NULL,
  `locationId` INT NULL,
  `cooldown` INT NULL,
  PRIMARY KEY (`idQuest`),
  INDEX `fk_quest_location1_idx` (`locationIdReward` ASC),
  INDEX `fk_quest_location2_idx` (`locationId` ASC),
  INDEX `fk_quest_item1_idx` (`idItem` ASC),
  INDEX `fk_quest_enemy1_idx` (`idEnemy` ASC),
  CONSTRAINT `fk_quest_location1`
    FOREIGN KEY (`locationIdReward`)
    REFERENCES `tarnished`.`location` (`idLocation`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_quest_location2`
    FOREIGN KEY (`locationId`)
    REFERENCES `tarnished`.`location` (`idLocation`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_quest_item1`
    FOREIGN KEY (`idItem`)
    REFERENCES `tarnished`.`item` (`idItem`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_quest_enemy1`
    FOREIGN KEY (`idEnemy`)
    REFERENCES `tarnished`.`enemy` (`idEnemy`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tarnished`.`quest_has_item`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tarnished`.`quest_has_item` (
  `idRel` INT NOT NULL AUTO_INCREMENT,
  `idQuest` INT NOT NULL,
  `idItem` INT NOT NULL,
  `count` INT NOT NULL,
  INDEX `fk_quest_has_item_item1_idx` (`idItem` ASC),
  INDEX `fk_quest_has_item_quest1_idx` (`idQuest` ASC),
  PRIMARY KEY (`idRel`),
  CONSTRAINT `fk_quest_has_item_quest1`
    FOREIGN KEY (`idQuest`)
    REFERENCES `tarnished`.`quest` (`idQuest`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_quest_has_item_item1`
    FOREIGN KEY (`idItem`)
    REFERENCES `tarnished`.`item` (`idItem`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tarnished`.`user_has_quest`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tarnished`.`user_has_quest` (
  `idRel` INT NOT NULL AUTO_INCREMENT,
  `idQuest` INT NOT NULL,
  `idUser` VARCHAR(80) NOT NULL,
  `remaining_kills` INT NULL,
  `remaining_items` INT NULL,
  `remaining_runes` INT NULL,
  `remaining_explores` INT NULL,
  PRIMARY KEY (`idRel`),
  INDEX `fk_quest_has_user1_user1_idx` (`idUser` ASC),
  INDEX `fk_quest_has_user1_quest1_idx` (`idQuest` ASC),
  CONSTRAINT `fk_quest_has_user1_quest1`
    FOREIGN KEY (`idQuest`)
    REFERENCES `tarnished`.`quest` (`idQuest`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_quest_has_user1_user1`
    FOREIGN KEY (`idUser`)
    REFERENCES `tarnished`.`user` (`idUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;