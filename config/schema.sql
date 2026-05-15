BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "categories" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "products" (
	"id"	INTEGER,
	"price"	REAL NOT NULL,
	"category_id"	INTEGER NOT NULL,
	PRIMARY KEY("id"),
	CONSTRAINT "fk_categories" FOREIGN KEY("category_id") REFERENCES ""
);
CREATE TABLE IF NOT EXISTS "regions" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "sales" (
	"id"	INTEGER,
	"quantity_sold"	INTEGER NOT NULL,
	"discount_percent" NUMERIC NOT NULL,
	"rating"	NUMERIC NOT NULL,
	"date"	TEXT NOT NULL,
	"product_id"	INTEGER NOT NULL,
	"region_id"	INTEGER NOT NULL,
	PRIMARY KEY("id"),
	CONSTRAINT "fk_products" FOREIGN KEY("product_id") REFERENCES "products",
	CONSTRAINT "fk_regions" FOREIGN KEY("region_id") REFERENCES ""
);
COMMIT;
