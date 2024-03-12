--
-- PostgreSQL database dump
--

-- Dumped from database version 14.9 (Homebrew)
-- Dumped by pg_dump version 14.9 (Homebrew)

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
-- Name: customer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customer (
    id integer NOT NULL,
    name character varying NOT NULL,
    email character varying(50) NOT NULL,
    phone character varying(25) NOT NULL
);


ALTER TABLE public.customer OWNER TO postgres;

--
-- Name: customer_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.customer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.customer_id_seq OWNER TO postgres;

--
-- Name: customer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.customer_id_seq OWNED BY public.customer.id;


--
-- Name: rental; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rental (
    id integer NOT NULL,
    customer_id integer NOT NULL,
    scooter_id integer NOT NULL,
    is_returned boolean NOT NULL
);


ALTER TABLE public.rental OWNER TO postgres;

--
-- Name: rental_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rental_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rental_id_seq OWNER TO postgres;

--
-- Name: rental_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rental_id_seq OWNED BY public.rental.id;


--
-- Name: scooter; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.scooter (
    id integer NOT NULL,
    model character varying NOT NULL,
    charge_percent double precision NOT NULL
);


ALTER TABLE public.scooter OWNER TO postgres;

--
-- Name: scooter_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.scooter_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.scooter_id_seq OWNER TO postgres;

--
-- Name: scooter_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.scooter_id_seq OWNED BY public.scooter.id;


--
-- Name: customer id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customer ALTER COLUMN id SET DEFAULT nextval('public.customer_id_seq'::regclass);


--
-- Name: rental id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rental ALTER COLUMN id SET DEFAULT nextval('public.rental_id_seq'::regclass);


--
-- Name: scooter id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.scooter ALTER COLUMN id SET DEFAULT nextval('public.scooter_id_seq'::regclass);


--
-- Data for Name: customer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.customer (id, name, email, phone) FROM stdin;
1	User One	One@email.com	(555) 555-1111
2	User Two	Two@email.com	(555) 555-2222
3	User Three	Three@email.com	(555) 555-3333
4	User Four	Four@email.com	(555) 555-4444
5	User Five	Five@email.com	(555) 555-5555
6	User Six	Six@email.com	(555) 555-6666
7	User Seven	Seven@email.com	(555) 555-7777
8	User Eight	Eight@email.com	(555) 555-8888
9	User Nine	Nine@email.com	(555) 555-9999
10	User Ten	Ten@email.com	(555) 555-0000
\.


--
-- Data for Name: rental; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rental (id, customer_id, scooter_id, is_returned) FROM stdin;
1	1	2	t
2	1	3	t
3	1	4	t
4	1	5	f
5	2	13	t
6	2	15	t
7	2	18	t
8	3	15	t
9	3	22	f
10	4	8	t
11	4	27	t
12	4	3	t
13	5	9	t
14	5	16	f
15	6	1	t
16	6	20	t
17	7	28	f
18	8	11	t
19	8	14	f
20	10	6	t
\.


--
-- Data for Name: scooter; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.scooter (id, model, charge_percent) FROM stdin;
1	Thunderbolt DX	25.6
2	Thunderbolt DX	15.3
3	Thunderbolt DX	89.2
4	Thunderbolt DX+	14
5	Thunderbolt DX+	58.4
6	Speedster IV	52
7	Speedster IV	27.3
8	Speedster V	76
9	Speedster VI	42.2
10	Speedster VII	61
11	Nimbus Sparkle	92.5
12	Nimbus Sparkle	88
13	Nimbus Sparkle+	74.2
14	Nimbus Rocket	70
15	Nimbus Rocket	53.7
16	Starlight V70	7.5
17	Starlight V70	82.5
18	Starlight V75	50.8
19	Starlight V75	28
20	Starlight V80	36.7
21	Shadow Scream	9.2
22	Shadow Scream	12.5
23	Shadow Scream	45
24	Shadow Scream	48.9
25	Shadow Scream	34.6
26	Trail Blazer A	33.3
27	Trail Blazer A	47.2
28	Trail Blazer XY	75.4
29	Trail Blazer Z	35.2
30	Trail Blazer Z+	84.6
\.


--
-- Name: customer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.customer_id_seq', 10, true);


--
-- Name: rental_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rental_id_seq', 20, true);


--
-- Name: scooter_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.scooter_id_seq', 30, true);


--
-- Name: customer customer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customer
    ADD CONSTRAINT customer_pkey PRIMARY KEY (id);


--
-- Name: rental rental_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rental
    ADD CONSTRAINT rental_pkey PRIMARY KEY (id);


--
-- Name: scooter scooter_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.scooter
    ADD CONSTRAINT scooter_pkey PRIMARY KEY (id);


--
-- Name: rental rental_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rental
    ADD CONSTRAINT rental_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customer(id);


--
-- Name: rental rental_scooter_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rental
    ADD CONSTRAINT rental_scooter_id_fkey FOREIGN KEY (scooter_id) REFERENCES public.scooter(id);


--
-- PostgreSQL database dump complete
--

