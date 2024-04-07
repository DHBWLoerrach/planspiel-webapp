-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema gamesimulationdb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema gamesimulationdb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `gamesimulationdb` DEFAULT CHARACTER SET utf8mb4 ;
USE `gamesimulationdb` ;

-- -----------------------------------------------------
-- Table `gamesimulationdb`.`games`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gamesimulationdb`.`games` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `status` VARCHAR(100) NOT NULL,
  `num_companies` INT(11) NOT NULL DEFAULT 0,
  `num_periods` INT(11) NOT NULL DEFAULT 0,
  `periods_offset` INT(11) NOT NULL DEFAULT 0,
  `market_0_activation` TINYINT(1) NULL DEFAULT NULL,
  `market_1_activation` TINYINT(1) NULL DEFAULT NULL,
  `market_2_activation` TINYINT(1) NULL DEFAULT NULL,
  `market_3_activation` TINYINT(1) NULL DEFAULT NULL,
  `scenario_id` INT(11) NULL DEFAULT NULL,
  `game_version` VARCHAR(255) NULL DEFAULT NULL,
  `ideal_rd` INT(11) NOT NULL DEFAULT 0,
  `offset` INT(11) NULL DEFAULT NULL,
  `num_markets` INT(11) NULL DEFAULT NULL,
  `num_cells` INT(11) NULL DEFAULT NULL,
  `cost_industry_report` INT(11) NULL DEFAULT NULL,
  `cost_market_report` INT(11) NULL DEFAULT NULL,
  `current_period` INT(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name` (`name` ASC))
ENGINE = InnoDB
AUTO_INCREMENT = 14
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `gamesimulationdb`.`teams`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gamesimulationdb`.`teams` (
  `name` VARCHAR(100) NOT NULL,
  `password` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`name`),
  UNIQUE INDEX `name` (`name` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `gamesimulationdb`.`gameteams`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gamesimulationdb`.`gameteams` (
  `game_id` INT(11) NOT NULL,
  `teams_name` VARCHAR(100) NOT NULL,
  `locked` TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`game_id`, `teams_name`),
  INDEX `fk_games_has_teams_teams1_idx` (`teams_name` ASC),
  INDEX `fk_games_has_teams_games1_idx` (`game_id` ASC),
  CONSTRAINT `fk_games_has_teams_games1`
    FOREIGN KEY (`game_id`)
    REFERENCES `gamesimulationdb`.`games` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_games_has_teams_teams1`
    FOREIGN KEY (`teams_name`)
    REFERENCES `gamesimulationdb`.`teams` (`name`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `gamesimulationdb`.`turns`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gamesimulationdb`.`turns` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `game_id` INT(11) NOT NULL,
  `turn_number` INT(11) NOT NULL,
  `submission_time` DATETIME NULL DEFAULT CURRENT_TIMESTAMP(),
  `inputSolidVerkaufspreisInland` DOUBLE NULL DEFAULT NULL,
  `inputIdealVerkaufspreisInland` DOUBLE NULL DEFAULT NULL,
  `inputSolidVerkaufspreisAusland` DOUBLE NULL DEFAULT NULL,
  `inputIdealVerkaufspreisAusland` DOUBLE NULL DEFAULT NULL,
  `inputSolidFETechnik` DOUBLE NULL DEFAULT NULL,
  `inputIdealFETechnik` DOUBLE NULL DEFAULT NULL,
  `inputSolidFEHaptik` DOUBLE NULL DEFAULT NULL,
  `inputIdealFEHaptik` DOUBLE NULL DEFAULT NULL,
  `inputSolidProduktwerbungInland` DOUBLE NULL DEFAULT NULL,
  `inputIdealProduktwerbungInland` DOUBLE NULL DEFAULT NULL,
  `inputSolidProduktwerbungAusland` DOUBLE NULL DEFAULT NULL,
  `inputIdealProduktwerbungAusland` DOUBLE NULL DEFAULT NULL,
  `inputSolidLiefermengeSondermarkt` DOUBLE NULL DEFAULT NULL,
  `inputIdealLiefermengeSondermarkt` DOUBLE NULL DEFAULT NULL,
  `inputSolidLiefermengeAusland` DOUBLE NULL DEFAULT NULL,
  `inputIdealLiefermengeAusland` DOUBLE NULL DEFAULT NULL,
  `inputSolidHilfsstoffe` DOUBLE NULL DEFAULT NULL,
  `inputIdealHilfsstoffe` DOUBLE NULL DEFAULT NULL,
  `inputSolidMaterialS` DOUBLE NULL DEFAULT NULL,
  `inputMaterialI` DOUBLE NULL DEFAULT NULL,
  `sumPR` DOUBLE NULL DEFAULT NULL,
  `sumVertriebspersonalInland` DOUBLE NULL DEFAULT NULL,
  `sumVertriebspersonalAusland` DOUBLE NULL DEFAULT NULL,
  `team_name` VARCHAR(100) NULL DEFAULT NULL,
  `selectIdealMarktbericht` VARCHAR(100) NULL DEFAULT NULL,
  `selectSolidMarktbericht` VARCHAR(100) NULL DEFAULT NULL,
  `selectBranchenbericht` VARCHAR(100) NULL DEFAULT NULL,
  `inputSolidFertigungsmengen` DOUBLE NULL DEFAULT NULL,
  `inputIdealFertigungsmengen` DOUBLE NULL DEFAULT NULL,
  `selectSolidAnlagenWerkstaette01` VARCHAR(100) NULL DEFAULT NULL,
  `selectSolidAnlagenWerkstaette08` VARCHAR(100) NULL DEFAULT NULL,
  `selectIdealAnlagenWerkstaette01` VARCHAR(100) NULL DEFAULT NULL,
  `selectIdealAnlagenWerkstaette08` VARCHAR(100) NULL DEFAULT NULL,
  `inputDarlehenS` DOUBLE NULL DEFAULT NULL,
  `inputDarlehenM` DOUBLE NULL DEFAULT NULL,
  `inputDarlehenL` DOUBLE NULL DEFAULT NULL,
  `inputFestgeldDarlehen` DOUBLE NULL DEFAULT NULL,
  `inputDividenden` DOUBLE NULL DEFAULT NULL,
  `gesamtFertigungspersonal` DOUBLE NULL DEFAULT NULL,
  `gesamtPersonalentwicklung` DOUBLE NULL DEFAULT NULL,
  `gesamtGehaltsaufschlag` DOUBLE NULL DEFAULT NULL,
  `gesamtInvestitionenBGA` DOUBLE NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `game_id` (`game_id` ASC),
  INDEX `team_name` (`team_name` ASC),
  CONSTRAINT `turns_ibfk_1`
    FOREIGN KEY (`game_id`)
    REFERENCES `gamesimulationdb`.`games` (`id`),
  CONSTRAINT `turns_ibfk_2`
    FOREIGN KEY (`team_name`)
    REFERENCES `gamesimulationdb`.`teams` (`name`))
ENGINE = InnoDB
AUTO_INCREMENT = 18
DEFAULT CHARACTER SET = utf8mb4;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
