CREATE TABLE IF NOT EXISTS users (
    user_id               SERIAL             PRIMARY KEY,
    firstname             TEXT               NOT NULL,
    username              TEXT       UNIQUE  NOT NULL,
    password              TEXT               NOT NULL,
    email                 TEXT       UNIQUE  NOT NULL
);

CREATE TABLE IF NOT EXISTS uploaded_videos (
    video_id             SERIAL              PRIMARY KEY,
    video_name           TEXT                NOT NULL,
    username             TEXT                NOT NULL,
    timesdone            NUMERIC,
    exercise_type        TEXT,
    upload_time          TIMESTAMP           WITH TIME ZONE      DEFAULT CURRENT_TIMESTAMP
);


insert into users (username, firstname, email, password) values ('soxberry0', 'Shelagh', 'sroast0@chronoengine.com', '$2a$04$KQh8.ItSBXyLfSzPd/sJAuqxIQxCbF0tMazja0qMT9lRJxU8V6Q/m');
insert into users (username, firstname, email, password) values ('jtamburi1', 'Jammie', 'jmacgee1@ucsd.edu', '$2a$04$XYmkRK5KgZ3jLjWP63ueZOArYsL3Q7Ka49thE0WBEt9a26ceZXlq2');
insert into users (username, firstname, email, password) values ('ytourne2', 'Yorker', 'ynafzger2@who.int', '$2a$04$u8cbZiyVFXAsjiziZlz5Vubgrt.G0UBFXo/i8EM9KuhjHK7IhsQj.');
insert into users (username, firstname, email, password) values ('gnardi3', 'Gunter', 'gchristene3@microsoft.com', '$2a$04$0h/EE99Gy/GY1R9SwUO7yuyO94qrwra/0f/vms9FyOO3Afkc1XKcG');
insert into users (username, firstname, email, password) values ('nchamberlen4', 'Ninnetta', 'nlaycock4@mashable.com', '$2a$04$Cs3mxof06Siq8uMw7zaUOOJCPDW0X.6Ct9pU93VhYyXdoqTJDIEbu');
insert into users (username, firstname, email, password) values ('lyouhill5', 'Lori', 'lvassbender5@elegantthemes.com', '$2a$04$qJB0rR0xiaFDDvePR/KkKeizyfjO2ov/LHHxIQRLFmbg0Ofj63iXq');
insert into users (username, firstname, email, password) values ('tmccartney6', 'Teddy', 'tpantry6@cbc.ca', '$2a$04$b3LUkieTmycGBoUri1OvPOioIsEhPpXpGZQ5xe6VSoqyUcvvj.1Zy');
insert into users (username, firstname, email, password) values ('ppaxman7', 'Pia', 'pfayter7@engadget.com', '$2a$04$OUUlcaocVb4hqkC/77UjIOa4icsFgdQ.LoR6TJilPrsYHXWkzp/uC');
insert into users (username, firstname, email, password) values ('beisikovitsh8', 'Bernardine', 'bonyon8@independent.co.uk', '$2a$04$uvHXV3Lzan6IZH/1YPLnXuKS2unnSl7GDDw/Ps0zbYi8CqWTVXW9O');
insert into users (username, firstname, email, password) values ('rtebbett9', 'Read', 'rhayton9@mayoclinic.com', '$2a$04$0VRssVVpf2QIEAZlV3ycW.MCtzvxEZR7VtK3Q/tuwVeEA.1Wigq.2');