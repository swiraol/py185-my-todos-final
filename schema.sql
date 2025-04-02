CREATE TABLE list (
  id SERIAL PRIMARY KEY,
  title text UNIQUE NOT NULL
);

CREATE TABLE todo (
  id SERIAL PRIMARY KEY,
  title text NOT NULL,
  list_id integer NOT NULL UNIQUE REFERENCES list(id) ON DELETE CASCADE,
  completed boolean NOT NULL DEFAULT false
);