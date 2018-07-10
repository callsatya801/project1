-- Adminer 4.6.3-dev PostgreSQL dump

\connect "dc243657471did";

DROP TABLE IF EXISTS "location";
DROP SEQUENCE IF EXISTS location_location_id_seq;
CREATE SEQUENCE location_location_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."location" (
    "location_id" integer DEFAULT nextval('location_location_id_seq') NOT NULL,
    "zipcode" character varying NOT NULL,
    "city" character varying NOT NULL,
    "state" character varying NOT NULL,
    "latitude" numeric NOT NULL,
    "longitude" numeric NOT NULL,
    "population" integer NOT NULL,
    CONSTRAINT "location_pkey" PRIMARY KEY ("location_id")
) WITH (oids = false);


DROP TABLE IF EXISTS "location_checkin";
DROP SEQUENCE IF EXISTS location_checkin_checkin_id_seq;
CREATE SEQUENCE location_checkin_checkin_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."location_checkin" (
    "checkin_id" integer DEFAULT nextval('location_checkin_checkin_id_seq') NOT NULL,
    "user_id" integer,
    "location_id" integer,
    "comments" character varying,
    "checkin_time" timestamp NOT NULL,
    CONSTRAINT "location_checkin_pkey" PRIMARY KEY ("checkin_id"),
    CONSTRAINT "location_checkin_location_id_fkey" FOREIGN KEY (location_id) REFERENCES location(location_id) NOT DEFERRABLE,
    CONSTRAINT "location_checkin_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(user_id) NOT DEFERRABLE
) WITH (oids = false);


DROP TABLE IF EXISTS "users";
DROP SEQUENCE IF EXISTS users_user_id_seq;
CREATE SEQUENCE users_user_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."users" (
    "user_id" integer DEFAULT nextval('users_user_id_seq') NOT NULL,
    "username" character varying NOT NULL,
    "password" character varying NOT NULL,
    CONSTRAINT "users_pkey" PRIMARY KEY ("user_id")
) WITH (oids = false);


-- 2018-07-10 21:44:41.140822+00