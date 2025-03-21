--
-- PostgreSQL database dump
--

-- Dumped from database version 16.8
-- Dumped by pg_dump version 16.5

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
-- Name: media_file; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.media_file (
    id integer NOT NULL,
    filename character varying(255) NOT NULL,
    original_filename character varying(255) NOT NULL,
    mime_type character varying(100) NOT NULL,
    file_size integer NOT NULL,
    media_type character varying(20) NOT NULL,
    thumbnail_filename character varying(255),
    upload_date timestamp without time zone,
    user_id integer
);


ALTER TABLE public.media_file OWNER TO neondb_owner;

--
-- Name: media_file_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.media_file_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.media_file_id_seq OWNER TO neondb_owner;

--
-- Name: media_file_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.media_file_id_seq OWNED BY public.media_file.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    username character varying(64) NOT NULL,
    email character varying(120) NOT NULL,
    password_hash character varying(256)
);


ALTER TABLE public."user" OWNER TO neondb_owner;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_id_seq OWNER TO neondb_owner;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: media_file id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.media_file ALTER COLUMN id SET DEFAULT nextval('public.media_file_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Data for Name: media_file; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.media_file (id, filename, original_filename, mime_type, file_size, media_type, thumbnail_filename, upload_date, user_id) FROM stdin;
1	727a4ac451884eefb43afde479a3bf38.jpg	582-536x354.jpg	image/jpeg	24676	image	thumb_727a4ac451884eefb43afde479a3bf38.jpg	2025-03-20 15:48:53.561142	\N
2	5062d7774380400db54afa285cf62432.gif	giphy.gif	image/gif	778158	image	thumb_5062d7774380400db54afa285cf62432.gif	2025-03-20 15:51:42.867666	\N
3	8751756370f94017a925f2e60243ee84.gif	giphy_1.gif	image/gif	1462435	image	thumb_8751756370f94017a925f2e60243ee84.gif	2025-03-20 15:51:54.696281	\N
4	eae0997377794d5f81f416b3a5cbeb46.mp4	SampleVideo_1280x720_1mb.mp4	video/mp4	1055736	video	\N	2025-03-20 15:52:09.908213	\N
5	016d37ebc67f458ea3b134cd6ed7c47b.mp4	SampleVideo_1280x720_5mb.mp4	video/mp4	5253880	video	\N	2025-03-20 15:52:24.032655	\N
6	3ab9a64d59ab47e4a999502a228e9eb3.jpg	870-536x354-blur_2-grayscale.jpg	image/jpeg	6430	image	thumb_3ab9a64d59ab47e4a999502a228e9eb3.jpg	2025-03-20 15:52:34.914732	\N
7	061ee02d59c940c7b447f990f7f9770a.jpg	866-536x354.jpg	image/jpeg	14799	image	thumb_061ee02d59c940c7b447f990f7f9770a.jpg	2025-03-20 16:05:22.494935	1
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public."user" (id, username, email, password_hash) FROM stdin;
1	jageshm	jagesh02mca@gmail.com	scrypt:32768:8:1$i8radDzSvRGCOyxY$c9d6b210741216e489ea2b34bd97970e01cd11b8780f35255d7f82288db24be35f5f58794a0a9314183c93be1b10e22e28dce3242c6f0612f8860e5bf66292de
\.


--
-- Name: media_file_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.media_file_id_seq', 7, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.user_id_seq', 1, true);


--
-- Name: media_file media_file_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.media_file
    ADD CONSTRAINT media_file_pkey PRIMARY KEY (id);


--
-- Name: user user_email_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: user user_username_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_username_key UNIQUE (username);


--
-- Name: media_file media_file_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.media_file
    ADD CONSTRAINT media_file_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: public; Owner: cloud_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE cloud_admin IN SCHEMA public GRANT ALL ON SEQUENCES TO neon_superuser WITH GRANT OPTION;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: cloud_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE cloud_admin IN SCHEMA public GRANT ALL ON TABLES TO neon_superuser WITH GRANT OPTION;


--
-- PostgreSQL database dump complete
--

