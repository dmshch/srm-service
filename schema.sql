CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE public.receiver_models ( guid uuid NOT NULL, model text NOT NULL, login text, password text );

INSERT INTO receiver_models (guid, model, login, password) VALUES (gen_random_uuid(), 'proview2962', 'ird', 'ird');

INSERT INTO receiver_models (guid, model, login, password) VALUES (gen_random_uuid(), 'proview7000', 'configure', 'configure');

INSERT INTO receiver_models (guid, model, login, password) VALUES (gen_random_uuid(), 'proview7100s', 'configure', 'configure');

INSERT INTO receiver_models (guid, model, login, password) VALUES (gen_random_uuid(), 'proview7100mold', 'configure', 'configure');

INSERT INTO receiver_models (guid, model, login, password) VALUES (gen_random_uuid(), 'proview7100mnew', 'configure', 'configure');

INSERT INTO receiver_models (guid, model, login, password) VALUES (gen_random_uuid(), 'proview8130', 'Admin', 'Admin');

INSERT INTO receiver_models (guid, model, login, password) VALUES (gen_random_uuid(), 'proview7100snew', 'configure', 'configure');

CREATE TABLE public.receivers ( guid uuid NOT NULL, ip text NOT NULL, port text NOT NULL, model uuid NOT NULL, satellite uuid, login text, password text, state boolean NOT NULL, "time" text, c_n text, eb_no text, l_m text, service text, cc_delta text, cc text );

CREATE TABLE public.satellites ( guid uuid NOT NULL, name text NOT NULL );

INSERT INTO satellites (guid, name) VALUES (gen_random_uuid(), '0.8-v-high');

INSERT INTO satellites (guid, name) VALUES (gen_random_uuid(), '4.8-h-high');

INSERT INTO satellites (guid, name) VALUES (gen_random_uuid(), '4.8-v-high');

INSERT INTO satellites (guid, name) VALUES (gen_random_uuid(), '4.8-v-low');

INSERT INTO satellites (guid, name) VALUES (gen_random_uuid(), '9-v-high');

INSERT INTO satellites (guid, name) VALUES (gen_random_uuid(), '9-h-high');

INSERT INTO satellites (guid, name) VALUES (gen_random_uuid(), '13-v-high');

INSERT INTO satellites (guid, name) VALUES (gen_random_uuid(), '13-h-high');

INSERT INTO satellites (guid, name) VALUES (gen_random_uuid(), '13-v-low');

INSERT INTO satellites (guid, name) VALUES (gen_random_uuid(), '13-h-low');

INSERT INTO satellites (guid, name) VALUES (gen_random_uuid(), '15-v-low');

INSERT INTO satellites (guid, name) VALUES (gen_random_uuid(), '15-h-low');

INSERT INTO satellites (guid, name) VALUES (gen_random_uuid(), '36-r');

INSERT INTO satellites (guid, name) VALUES (gen_random_uuid(), '36-l');

INSERT INTO satellites (guid, name) VALUES (gen_random_uuid(), '56-r');

INSERT INTO satellites (guid, name) VALUES (gen_random_uuid(), '75-v-low');

INSERT INTO satellites (guid, name) VALUES (gen_random_uuid(), '75-v-high');

INSERT INTO satellites (guid, name) VALUES (gen_random_uuid(), '75-h-low');

INSERT INTO satellites (guid, name) VALUES (gen_random_uuid(), '85-v-high');

INSERT INTO satellites (guid, name) VALUES (gen_random_uuid(), '85-h-high');

INSERT INTO satellites (guid, name) VALUES (gen_random_uuid(), '90-l');

INSERT INTO satellites (guid, name) VALUES (gen_random_uuid(), '90-v-high');

INSERT INTO satellites (guid, name) VALUES (gen_random_uuid(), '90-h-low');

INSERT INTO satellites (guid, name) VALUES (gen_random_uuid(), '80-v-low');

INSERT INTO satellites (guid, name) VALUES (gen_random_uuid(), '80-h-low');

CREATE TABLE public.statistics ( ip text NOT NULL, port text NOT NULL, c_n text NOT NULL, eb_no text NOT NULL, l_m text NOT NULL, date_time timestamp without time zone, guid uuid );