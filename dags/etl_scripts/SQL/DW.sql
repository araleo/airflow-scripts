BEGIN;

-------------
-- SCHEMAS --
-------------

CREATE SCHEMA noticias
    AUTHORIZATION leonardo;

CREATE SCHEMA tjfacil
    AUTHORIZATION leonardo;

CREATE SCHEMA reddit
    AUTHORIZATION leonardo;

CREATE SCHEMA twitter
    AUTHORIZATION leonardo;


------------
-- TABLES --
------------

-- Noticias

CREATE TABLE noticias.paginas
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    nome varchar(100) NOT NULL UNIQUE,
    url text,
    PRIMARY KEY (id)
);

CREATE TABLE noticias.categorias
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    categoria varchar(100) NOT NULL UNIQUE,
    PRIMARY KEY (id)
);

CREATE TABLE noticias.noticias
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    id_pagina integer NOT NULL,
    id_categoria integer NOT NULL,
    titulo text NOT NULL,
    descricao text,
    datahora timestamp,
    comentarios boolean,
    url text NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_pagina)
        REFERENCES noticias.paginas (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    FOREIGN KEY (id_categoria)
        REFERENCES noticias.categorias (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);


-- TJFacil

CREATE TABLE tjfacil.tipo_sentenca
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    tipo varchar(50) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE tjfacil.competencias
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    competencia varchar(50) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE tjfacil.tribunais
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    sigla varchar(10) NOT NULL,
    justica varchar(100) NOT NULL,
    uf character(2) NOT NULL,
    codigo_cnj smallint NOT NULL,
    site_principal text NOT NULL,
    site_busca_1_f text,
    site_busca_1_e text,
    site_busca_2_f text,
    site_busca_2_e text,
    PRIMARY KEY (id)
);

CREATE TABLE tjfacil.sentencas
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    id_tribunal integer NOT NULL,
    id_competencia integer NOT NULL,
    id_tipo_sentenca integer NOT NULL,
    vara smallint,
    num_processo varchar(50),
    num_cnj character(20),
    texto_raw text,
    texto_decoded text,
    data_pub date,
    PRIMARY KEY (id),
    FOREIGN KEY (id_tribunal)
        REFERENCES tjfacil.tribunais (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    FOREIGN KEY (id_competencia)
        REFERENCES tjfacil.competencias (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    FOREIGN KEY (id_tipo_sentenca)
        REFERENCES tjfacil.tipo_sentenca (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);


-- Twitter

CREATE TABLE twitter.users
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    twitter_id text NOT NULL,
    name text,
    screen_name text NOT NULL,
    location text,
    url text,
    description text,
    created_at timestamp,
    geo_enabled boolean,
    profile_image_url text,
    profile_banner_url text,
    followers_count integer,
    friends_count integer,
    statuses_count integer,
    collection_time timestamp NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE twitter.tweets
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    user_twitter_id text NOT NULL,
    created_at timestamp,
    twitter_id text NOT NULL,
    text text,
    source text,
    in_reply_to_status_id text,
    in_reply_to_user_id text,
    in_reply_to_screen_name text,
    quoted_id text,
    retweeted_id text,
    geo text,
    coordinates text,
    place text,
    timestamp_ms timestamp,
    collection_time timestamp,
    PRIMARY KEY (id)
);

CREATE TABLE twitter.tweet_counts
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    tweet_id text NOT NULL,
    quote_count integer,
    reply_count integer,
    retweet_count integer,
    favorite_count integer,
    collection_time timestamp,
    PRIMARY KEY (id)
);

CREATE TABLE twitter.user_mentions
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    tweet_id text NOT NULL,
    screen_name text,
    name text,
    mentioned_id text,
    begin_index smallint,
    end_index smallint,
    collection_time timestamp,
    PRIMARY KEY (id)
);

CREATE TABLE twitter.urls
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    tweet_id text NOT NULL,
    url text,
    expanded_url text,
    begin_index smallint,
    end_index smallint,
    collection_time timestamp,
    PRIMARY KEY (id)
);

CREATE TABLE twitter.hashtags
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    tweet_id text NOT NULL,
    text text,
    begin_index smallint,
    end_index smallint,
    collection_time timestamp,
    PRIMARY KEY (id)
);

CREATE TABLE twitter.medias
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),df
    tweet_id text NOT NULL,
    twitter_id text,
    url text,
    type text,
    collection_time timestamp,
    PRIMARY KEY (id)
);

CREATE TABLE twitter.screen_names
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    screen_name text UNIQUE NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE twitter.scored_tweets
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    tweet_id text NOT NULL,
    text text NOT NULL,
    mentioned_user text NOT NULL,
    created_at timestamp NOT NULL,
    user_screen_name text NOT NULL,
    user_profile_image_url text NOT NULL,
    cap integer NOT NULL,
    astroturf integer NOT NULL,
    fake_follower integer NOT NULL,
    financial integer NOT NULL,
    other integer NOT NULL,
    overall integer NOT NULL,
    self_declared integer NOT NULL,
    spammer integer NOT NULL,
    scoring_time timestamp NOT NULL,
    PRIMARY KEY (id)
);


-- Reddit

CREATE TABLE reddit.subreddits
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    nome text NOT NULL UNIQUE,
    titulo text,
    PRIMARY KEY (id)
);

CREATE TABLE reddit.sub_counts
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    id_sub integer NOT NULL,
    active_user_count integer,
    accounts_active integer,
    subscribers integer,
    collection_time timestamp NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_sub)
        REFERENCES reddit.subreddits (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

CREATE TABLE reddit.users
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    reddit_id text NOT NULL UNIQUE,
    name text NOT NULL,
    description text,
    created timestamp,
    verified boolean,
    has_verified_email boolean,
    is_employee boolean,
    PRIMARY KEY (id)
);

CREATE TABLE reddit.user_stats
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    id_user integer NOT NULL,
    total_karma integer,
    link_karma integer,
    comment_karma integer,
    awarder_karma integer,
    awardee_karma integer,
    is_gold boolean,
    collection_time timestamp NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_user)
        REFERENCES reddit.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

CREATE TABLE reddit.posts
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    id_sub integer NOT NULL,
    id_user integer NOT NULL,
    reddit_post_id text NOT NULL,
    title text NOT NULL,
    flair text,
    score integer,
    upvote_ratio real,
    num_comments integer,
    gilded boolean,
    total_awards_received integer,
    num_crossposts integer,
    num_reports integer,
    over_18 boolean,
    stickied boolean,
    created timestamp,
    permalink varchar NOT NULL,
    collection_time timestamp NOT NULL,
    top_n smallint,
    PRIMARY KEY (id),
    FOREIGN KEY (id_sub)
        REFERENCES reddit.subreddits (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    FOREIGN KEY (id_user)
        REFERENCES reddit.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);


--------------
-- COMMANDS --
--------------

ALTER TABLE noticias.noticias
    OWNER to leonardo;

ALTER TABLE noticias.categorias
    OWNER to leonardo;

ALTER TABLE noticias.paginas
    OWNER to leonardo;

ALTER TABLE reddit.subreddits
    OWNER to leonardo;

ALTER TABLE reddit.sub_counts
    OWNER to leonardo;

ALTER TABLE reddit.users
    OWNER to leonardo;

ALTER TABLE reddit.user_stats
    OWNER to leonardo;

ALTER TABLE reddit.posts
    OWNER to leonardo;

ALTER TABLE tjfacil.tribunais
    OWNER to leonardo;

ALTER TABLE tjfacil.tipo_sentenca
    OWNER to leonardo;

ALTER TABLE tjfacil.competencias
    OWNER to leonardo;

ALTER TABLE tjfacil.sentencas
    OWNER to leonardo;

ALTER TABLE twitter.users
    OWNER to leonardo;

ALTER TABLE twitter.tweets
    OWNER to leonardo;

ALTER TABLE twitter.tweet_counts
    OWNER to leonardo;

ALTER TABLE twitter.user_mentions
    OWNER to leonardo;

ALTER TABLE twitter.hashtags
    OWNER to leonardo;

ALTER TABLE twitter.urls
    OWNER to leonardo;

ALTER TABLE twitter.medias
    OWNER to leonardo;



COMMIT;
