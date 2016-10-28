CREATE TABLE person
(
    PersonId INT(11),
    LastName VARCHAR(250),
    FirstName VARCHAR(250)
);
CREATE TABLE `Character`
(
    experience INT(11) DEFAULT '0',
    character_name VARCHAR(30),
    health_points INT(11) DEFAULT '10',
    character_level INT(11) DEFAULT '1',
    player_id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    damage INT(11) DEFAULT '5',
    defense INT(11) DEFAULT '5',
    curr_location_id INT(11) DEFAULT '-1',
    inn_id INT(11)
);
CREATE TABLE Monster
(
    monster_id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    monster_name VARCHAR(50),
    challenge_level INT(11),
    hipoints INT(11),
    damage INT(11),
    defense INT(11),
    attack_type VARCHAR(250),
    max_loot INT(11)
);
CREATE TABLE Quest
(
    quest_id INT(11) PRIMARY KEY NOT NULL,
    active TINYINT(1) DEFAULT '0',
    start_time DATETIME,
    finished TINYINT(1) DEFAULT '0',
    reward INT(11),
    description VARCHAR(1000),
    CONSTRAINT Quest_Dungeon_id_fk FOREIGN KEY (quest_id) REFERENCES Dungeon (id)
);
CREATE TABLE Location
(
    Location_id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(250),
    num_buildings INT(11) DEFAULT '1' NOT NULL
);
CREATE TABLE Loot
(
    loot_id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    loot_name VARCHAR(75) NOT NULL,
    rarity DECIMAL(3,2) DEFAULT '0.99',
    health_modifier INT(11) DEFAULT '0',
    defense_modifier INT(11) DEFAULT '0',
    attack_modifier INT(11) DEFAULT '0',
    loot_type VARCHAR(20),
    item_value INT(11) DEFAULT '1' NOT NULL
);
CREATE TABLE Buildings
(
    Type VARCHAR(20) NOT NULL,
    building_id INT(11) PRIMARY KEY NOT NULL
);
CREATE TABLE Dungeon
(
    id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    difficulty_level INT(11),
    dungeon_name VARCHAR(250)
);
CREATE TABLE NPC
(
    npc_id INT(11) PRIMARY KEY NOT NULL,
    name VARCHAR(250),
    function VARCHAR(250),
    quest_id INT(11),
    CONSTRAINT NPC_Quest__fk FOREIGN KEY (quest_id) REFERENCES Quest (quest_id)
);
CREATE INDEX NPC_Quest__fk ON NPC (quest_id);
CREATE TABLE Building_npcs
(
    building_id INT(11),
    npc_id INT(11),
    CONSTRAINT Building_npcs_Buildings_building_id_fk FOREIGN KEY (building_id) REFERENCES Buildings (building_id),
    CONSTRAINT Building_npcs_NPC_npc_id_fk FOREIGN KEY (npc_id) REFERENCES NPC (npc_id)
);
CREATE INDEX Building_npcs_Buildings_building_id_fk ON Building_npcs (building_id);
CREATE INDEX Building_npcs_NPC_npc_id_fk ON Building_npcs (npc_id);
CREATE TABLE Character_loot
(
    player_id INT(11),
    loot_id INT(11),
    equipped TINYINT(1) DEFAULT '0',
    CONSTRAINT Character__fk FOREIGN KEY (player_id) REFERENCES `Character` (player_id),
    CONSTRAINT Loot___fk FOREIGN KEY (loot_id) REFERENCES Loot (loot_id)
);
CREATE INDEX Character__fk ON Character_loot (player_id);
CREATE INDEX Loot___fk ON Character_loot (loot_id);
CREATE TABLE Dungeon_monsters
(
    monster_id INT(11),
    dungeon_id INT(11),
    is_alive TINYINT(1) DEFAULT '1',
    CONSTRAINT Monster__fk FOREIGN KEY (monster_id) REFERENCES Monster (monster_id),
    CONSTRAINT Dungeon__fk FOREIGN KEY (dungeon_id) REFERENCES Dungeon (id)
);
CREATE INDEX Dungeon__fk ON Dungeon_monsters (dungeon_id);
CREATE INDEX Monster__fk ON Dungeon_monsters (monster_id);
CREATE TABLE Location_buildings
(
    location_id INT(11),
    building_id INT(11),
    CONSTRAINT Location__fk FOREIGN KEY (location_id) REFERENCES Location (Location_id),
    CONSTRAINT Buildings__fk FOREIGN KEY (building_id) REFERENCES Buildings (building_id)
);
CREATE INDEX Buildings__fk ON Location_buildings (building_id);
CREATE INDEX Location__fk ON Location_buildings (location_id);
CREATE TABLE Quest_log
(
    character_id INT(11),
    quest_id INT(11),
    CONSTRAINT Quest_log_ibfk_1 FOREIGN KEY (character_id) REFERENCES `Character` (player_id),
    CONSTRAINT Quest_log_ibfk_2 FOREIGN KEY (quest_id) REFERENCES Quest (quest_id)
);
CREATE INDEX character_id ON Quest_log (character_id);
CREATE INDEX quest_id ON Quest_log (quest_id);
CREATE PROCEDURE create_character(p_name VARCHAR);
CREATE PROCEDURE level_up(p_player_id INT);
CREATE PROCEDURE create_dungeon(p_difficulty_level INT, p_dangeon_name VARCHAR);
CREATE PROCEDURE populate_location(build_id INT, loc_id INT);