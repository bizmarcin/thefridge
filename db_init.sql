DROP TABLE IF EXISTS "products";
DROP TABLE IF EXISTS "types";
DROP TABLE IF EXISTS "alarms";
DROP TABLE IF EXISTS "alm_type";
DROP TABLE IF EXISTS "alm_active";
DROP TABLE IF EXISTS "users_alm";
DROP TABLE IF EXISTS "users";
DROP TABLE IF EXISTS "recipies";

CREATE TABLE "products"
(
    "id"     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    "name"  TEXT    NOT NULL,
    "quantity"   FLOAT,
    "type_id" INTEGER NOT NULL,
    FOREIGN KEY ("type_id") REFERENCES "types" ("id")
);


CREATE TABLE "types"
(
    "id"     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    "name"  TEXT    NOT NULL
);

INSERT INTO "types"
VALUES (?,'Drinks'),
       (?,'Meat'),
       (?,'Sweets'),
       (?,'Vegetables');


CREATE TABLE "alarms"
(
    "id"     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    "prod_id" INTEGER NOT NULL,
    "val"   FLOAT NOT NULL,
    "type_id" INTEGER NOT NULL,
    "message"  TEXT    NOT NULL,
    FOREIGN KEY ("prod_id") REFERENCES "products" ("id"),
    FOREIGN KEY ("type_id") REFERENCES "alm_type" ("id")
);

CREATE TABLE "alm_type"
(
    "id"     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    "name"  TEXT    NOT NULL
);

INSERT INTO "alm_type"
VALUES (?,'LT'),
       (?,'LE'),
       (?,'GE'),
       (?,'GT');

CREATE TABLE "alm_active"
(
    "id"     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    "alm_id" INTEGER NOT NULL,
    "datetime" CURRENT_DATE,
    FOREIGN KEY ("alm_id") REFERENCES "alarms" ("id")
);

CREATE TABLE "users_alm"
(
    "id"     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    "alm_id" INTEGER NOT NULL,
    "user_id" INTEGER NOT NULL,
    FOREIGN KEY ("alm_id") REFERENCES "alarms" ("id"),
    FOREIGN KEY ("user_id") REFERENCES "users" ("id")
);

CREATE TABLE "users"
(
    "id"     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    "name"  TEXT    NOT NULL,
    "mail" TEXT NOT NULL,
    "password" TEXT NOT NULL
);

CREATE TABLE "recipies"
(
    "Title" TEXT,
    "Directions"    TEXT,
    "Quantity" TEXT,
    "Unit01" TEXT,
    "Ingredient01" TEXT,
    "Quantity02" TEXT,
    "Unit02" TEXT,
    "Ingredient02" TEXT,
    "Quantity03" TEXT,
    "Unit03" TEXT,
    "Ingredient03" TEXT,
    "Quantity04" TEXT,
    "Unit04" TEXT,
    "Ingredient04" TEXT,
    "Quantity05" TEXT,
    "Unit05" TEXT,
    "Ingredient05" TEXT,
    "Quantity06" TEXT,
    "Unit06" TEXT,
    "Ingredient06" TEXT,
    "Quantity07" TEXT,
    "Unit07" TEXT,
    "Ingredient07" TEXT,
    "Quantity08" TEXT,
    "Unit08" TEXT,
    "Ingredient08" TEXT,
    "Quantity09" TEXT,
    "Unit09" TEXT,
    "Ingredient09" TEXT,
    "Quantity10" TEXT,
    "Unit10" TEXT,
    "Ingredient10" TEXT,
    "Quantity11" TEXT,
    "Unit11" TEXT,
    "Ingredient11" TEXT,
    "Quantity12" TEXT,
    "Unit12" TEXT,
    "Ingredient12" TEXT,
    "Quantity13" TEXT,
    "Unit13" TEXT,
    "Ingredient13" TEXT,
    "Quantity14" TEXT,
    "Unit14" TEXT,
    "Ingredient14" TEXT,
    "Quantity15" TEXT,
    "Unit15" TEXT,
    "Ingredient15" TEXT,
    "Quantity16" TEXT,
    "Unit16" TEXT,
    "Ingredient16" TEXT,
    "Quantity17" TEXT,
    "Unit17" TEXT,
    "Ingredient17" TEXT,
    "Quantity18" TEXT,
    "Unit18" TEXT,
    "Ingredient18" TEXT,
    "Quantity19" TEXT,
    "Unit19" TEXT,
    "Ingredient19" TEXT,
    "Category" TEXT
);