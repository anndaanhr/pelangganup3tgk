--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5
-- Dumped by pg_dump version 14.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: pln_user
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);



--
-- Name: customers_2024; Type: TABLE; Schema: public; Owner: pln_user
--

CREATE TABLE public.customers_2024 (
    idpel bigint NOT NULL,
    unitup integer,
    nama character varying,
    alamat character varying,
    tarif character varying,
    daya integer,
    kddk character varying,
    gardu character varying,
    merk_kwh character varying,
    nomor_meter bigint,
    jenis character varying,
    layanan character varying,
    kd_proses character varying,
    dec_2023 numeric(15,2),
    jan_2024 numeric(15,2),
    feb_2024 numeric(15,2),
    mar_2024 numeric(15,2),
    apr_2024 numeric(15,2),
    may_2024 numeric(15,2),
    jun_2024 numeric(15,2),
    jul_2024 numeric(15,2),
    aug_2024 numeric(15,2),
    sep_2024 numeric(15,2),
    oct_2024 numeric(15,2),
    nov_2024 numeric(15,2),
    dec_2024 numeric(15,2),
    penyulang character varying,
    cater character varying
);



--
-- Name: customers_2024_idpel_seq; Type: SEQUENCE; Schema: public; Owner: pln_user
--

CREATE SEQUENCE public.customers_2024_idpel_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: customers_2024_idpel_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pln_user
--

ALTER SEQUENCE public.customers_2024_idpel_seq OWNED BY public.customers_2024.idpel;


--
-- Name: customers_2025; Type: TABLE; Schema: public; Owner: pln_user
--

CREATE TABLE public.customers_2025 (
    idpel bigint NOT NULL,
    unitup integer,
    nama character varying,
    alamat character varying,
    tarif character varying,
    daya integer,
    kddk character varying,
    gardu character varying,
    nomor_meter bigint,
    jenis character varying,
    layanan character varying,
    kd_proses character varying,
    dec_2024 numeric(15,2),
    jan_2025 numeric(15,2),
    feb_2025 numeric(15,2),
    mar_2025 numeric(15,2),
    apr_2025 numeric(15,2),
    may_2025 numeric(15,2),
    jun_2025 numeric(15,2),
    jul_2025 numeric(15,2),
    aug_2025 numeric(15,2),
    sep_2025 numeric(15,2),
    oct_2025 numeric(15,2),
    nov_2025 numeric(15,2),
    dec_2025 numeric(15,2),
    penyulang character varying,
    cater character varying
);



--
-- Name: customers_2025_idpel_seq; Type: SEQUENCE; Schema: public; Owner: pln_user
--

CREATE SEQUENCE public.customers_2025_idpel_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: customers_2025_idpel_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pln_user
--

ALTER SEQUENCE public.customers_2025_idpel_seq OWNED BY public.customers_2025.idpel;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying,
    hashed_password character varying,
    role character varying
);



--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: customers_2024 idpel; Type: DEFAULT; Schema: public; Owner: pln_user
--

ALTER TABLE ONLY public.customers_2024 ALTER COLUMN idpel SET DEFAULT nextval('public.customers_2024_idpel_seq'::regclass);


--
-- Name: customers_2025 idpel; Type: DEFAULT; Schema: public; Owner: pln_user
--

ALTER TABLE ONLY public.customers_2025 ALTER COLUMN idpel SET DEFAULT nextval('public.customers_2025_idpel_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: pln_user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: customers_2024 customers_2024_pkey; Type: CONSTRAINT; Schema: public; Owner: pln_user
--

ALTER TABLE ONLY public.customers_2024
    ADD CONSTRAINT customers_2024_pkey PRIMARY KEY (idpel);


--
-- Name: customers_2025 customers_2025_pkey; Type: CONSTRAINT; Schema: public; Owner: pln_user
--

ALTER TABLE ONLY public.customers_2025
    ADD CONSTRAINT customers_2025_pkey PRIMARY KEY (idpel);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_customers_2024_gardu; Type: INDEX; Schema: public; Owner: pln_user
--

CREATE INDEX ix_customers_2024_gardu ON public.customers_2024 USING btree (gardu);


--
-- Name: ix_customers_2024_idpel; Type: INDEX; Schema: public; Owner: pln_user
--

CREATE UNIQUE INDEX ix_customers_2024_idpel ON public.customers_2024 USING btree (idpel);


--
-- Name: ix_customers_2024_jenis; Type: INDEX; Schema: public; Owner: pln_user
--

CREATE INDEX ix_customers_2024_jenis ON public.customers_2024 USING btree (jenis);


--
-- Name: ix_customers_2024_kd_proses; Type: INDEX; Schema: public; Owner: pln_user
--

CREATE INDEX ix_customers_2024_kd_proses ON public.customers_2024 USING btree (kd_proses);


--
-- Name: ix_customers_2024_layanan; Type: INDEX; Schema: public; Owner: pln_user
--

CREATE INDEX ix_customers_2024_layanan ON public.customers_2024 USING btree (layanan);


--
-- Name: ix_customers_2024_penyulang; Type: INDEX; Schema: public; Owner: pln_user
--

CREATE INDEX ix_customers_2024_penyulang ON public.customers_2024 USING btree (penyulang);


--
-- Name: ix_customers_2024_tarif; Type: INDEX; Schema: public; Owner: pln_user
--

CREATE INDEX ix_customers_2024_tarif ON public.customers_2024 USING btree (tarif);


--
-- Name: ix_customers_2024_unitup; Type: INDEX; Schema: public; Owner: pln_user
--

CREATE INDEX ix_customers_2024_unitup ON public.customers_2024 USING btree (unitup);


--
-- Name: ix_customers_2025_gardu; Type: INDEX; Schema: public; Owner: pln_user
--

CREATE INDEX ix_customers_2025_gardu ON public.customers_2025 USING btree (gardu);


--
-- Name: ix_customers_2025_idpel; Type: INDEX; Schema: public; Owner: pln_user
--

CREATE UNIQUE INDEX ix_customers_2025_idpel ON public.customers_2025 USING btree (idpel);


--
-- Name: ix_customers_2025_jenis; Type: INDEX; Schema: public; Owner: pln_user
--

CREATE INDEX ix_customers_2025_jenis ON public.customers_2025 USING btree (jenis);


--
-- Name: ix_customers_2025_kd_proses; Type: INDEX; Schema: public; Owner: pln_user
--

CREATE INDEX ix_customers_2025_kd_proses ON public.customers_2025 USING btree (kd_proses);


--
-- Name: ix_customers_2025_layanan; Type: INDEX; Schema: public; Owner: pln_user
--

CREATE INDEX ix_customers_2025_layanan ON public.customers_2025 USING btree (layanan);


--
-- Name: ix_customers_2025_penyulang; Type: INDEX; Schema: public; Owner: pln_user
--

CREATE INDEX ix_customers_2025_penyulang ON public.customers_2025 USING btree (penyulang);


--
-- Name: ix_customers_2025_tarif; Type: INDEX; Schema: public; Owner: pln_user
--

CREATE INDEX ix_customers_2025_tarif ON public.customers_2025 USING btree (tarif);


--
-- Name: ix_customers_2025_unitup; Type: INDEX; Schema: public; Owner: pln_user
--

CREATE INDEX ix_customers_2025_unitup ON public.customers_2025 USING btree (unitup);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: ix_users_username; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_username ON public.users USING btree (username);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: ACER
--



--
-- Name: TABLE users; Type: ACL; Schema: public; Owner: postgres
--



--
-- Name: SEQUENCE users_id_seq; Type: ACL; Schema: public; Owner: postgres
--



--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--



--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--



--
-- PostgreSQL database dump complete
--

