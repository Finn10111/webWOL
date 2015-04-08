CREATE TABLE host
(
      id serial NOT NULL,
      name character varying(80) NOT NULL,
      mac macaddr NOT NULL,
      ip inet NOT NULL,
      CONSTRAINT id_pkey PRIMARY KEY (id)
)
