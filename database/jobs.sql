--
-- PostgreSQL database dump
--

-- Dumped from database version 13.3
-- Dumped by pg_dump version 13.3

-- Database: post_jobs

-- DROP DATABASE post_jobs;

CREATE DATABASE post_jobs
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_American Samoa.1252'
    LC_CTYPE = 'English_American Samoa.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;


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
-- Name: job; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.job (
    id bigint NOT NULL,
    title character varying(120) NOT NULL,
    description text,
    created_date timestamp with time zone,
    updated_date timestamp with time zone,
    created_by integer,
    updated_by integer
);


ALTER TABLE public.job OWNER TO postgres;

--
-- Name: job_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.job ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.job_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    username character varying(64),
    password character varying(350),
    fullname character varying(64)
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- Name: user_Id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."user" ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."user_Id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: job; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.job (id, title, description, created_date, updated_date, created_by, updated_by) FROM stdin;
3	Technical Recruiter	Highly qualified	2021-07-11 00:00:00+05	2021-07-11 00:00:00+05	5	5
4	Software Developer	ASP.NET, Unity, Game Development	2021-07-11 00:00:00+05	2021-07-11 00:00:00+05	5	5
5	Team Lead	Experience of 10+ years	2021-07-11 00:00:00+05	2021-07-11 00:00:00+05	5	5
6	Intern	BSSE Fresh graduate	2021-07-11 00:00:00+05	2021-07-11 00:00:00+05	5	5
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (id, username, password, fullname) FROM stdin;
5	keven.john	sha256$GrVW0zS4kg6EZPJK$41078149673360af730bc41b261f2f31e4cff6c5b56bae1820910e91d09ddc47	Keven John
\.


--
-- Name: job_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.job_id_seq', 9, true);


--
-- Name: user_Id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."user_Id_seq"', 5, true);


--
-- Name: user PK_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT "PK_id" PRIMARY KEY (id);


--
-- Name: user UNIQUE_username; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT "UNIQUE_username" UNIQUE (username);


--
-- Name: job pk_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job
    ADD CONSTRAINT pk_id PRIMARY KEY (id);


--
-- Name: fki_c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fki_c ON public.job USING btree (created_by);


--
-- Name: fki_fk_job_user_updated_by; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fki_fk_job_user_updated_by ON public.job USING btree (updated_by);


--
-- Name: job fk_job_user_created_by; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job
    ADD CONSTRAINT fk_job_user_created_by FOREIGN KEY (created_by) REFERENCES public."user"(id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- Name: job fk_job_user_updated_by; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job
    ADD CONSTRAINT fk_job_user_updated_by FOREIGN KEY (updated_by) REFERENCES public."user"(id) ON UPDATE CASCADE ON DELETE SET NULL NOT VALID;


--
-- PostgreSQL database dump complete
--

