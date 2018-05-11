--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: censorcodecv; Type: TABLE; Schema: public; Owner: schwingbach-user; Tablespace: 
--

CREATE TABLE censorcodecv (
    term character varying(255) NOT NULL,
    definition character varying
);


ALTER TABLE public.censorcodecv OWNER TO "schwingbach-user";

--
-- Name: TABLE censorcodecv; Type: COMMENT; Schema: public; Owner: schwingbach-user
--

COMMENT ON TABLE censorcodecv IS '*** Controlled Vocabulary WOF interface required ***';


--
-- Name: COLUMN censorcodecv.definition; Type: COMMENT; Schema: public; Owner: schwingbach-user
--

COMMENT ON COLUMN censorcodecv.definition IS 'Definition of the CensorCode controlled vocabulary term. The definition is 
optional if the term is self explanatory.';


--
-- Name: censorcodecv_pkey; Type: CONSTRAINT; Schema: public; Owner: schwingbach-user; Tablespace: 
--

ALTER TABLE ONLY censorcodecv
    ADD CONSTRAINT censorcodecv_pkey PRIMARY KEY (term);


--
-- PostgreSQL database dump complete
--

