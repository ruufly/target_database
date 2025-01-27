CREATE TABLE IF NOT EXISTS `disease` (
    `id` INT UNSIGNED AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `targets_P` TEXT,
    `targets_N` TEXT,
    PRIMARY KEY(`id`)
);
CREATE TABLE IF NOT EXISTS `target` (
    `id` INT UNSIGNED AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `type` VARCHAR(255) NOT NULL,
    `diseases` TEXT,
    `pathway` TEXT,
    `sequence` TEXT,
    `description` TEXT,
    PRIMARY KEY(`id`)
);
CREATE TABLE IF NOT EXISTS `drug` (
    `id` INT UNSIGNED AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `targets_P` TEXT,
    `targets_N` TEXT,
    `structure` TEXT,
    `description` TEXT,
    PRIMARY KEY(`id`)
)
