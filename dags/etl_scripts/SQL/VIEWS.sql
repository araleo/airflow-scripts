-------------
-- TWITTER --
-------------

CREATE VIEW twitter.vw_last_scored AS
SELECT
  LEFT(text, 100)
  ,mentioned_user
  ,created_at
  ,user_screen_name
  ,cap
  ,scoring_time
FROM twitter.scored_tweets
ORDER BY scoring_time DESC
LIMIT 10;


CREATE VIEW twitter.vw_higher_scores AS
WITH scored AS (
  SELECT
    ROW_NUMBER() OVER(PARTITION BY mentioned_user ORDER BY scoring_time DESC) AS rank_
    ,text
    ,mentioned_user
    ,created_at
    ,user_screen_name
    ,user_profile_image_url
    ,cap
    ,astroturf
    ,fake_follower
    ,financial
    ,other
    ,overall
    ,self_declared
    ,spammer
    ,scoring_time
  FROM twitter.scored_tweets
  WHERE cap > 80
)
SELECT
  text
  ,mentioned_user
  ,created_at
  ,user_screen_name
  ,user_profile_image_url
  ,cap
  ,astroturf
  ,fake_follower
  ,financial
  ,other
  ,overall
  ,self_declared
  ,spammer
  ,scoring_time
FROM scored
WHERE rank_ = 1;


--------------
-- NOTICIAS --
--------------

CREATE VIEW noticias.vw_ultimas_noticias AS
SELECT
  p.nome AS pagina
  ,c.categoria AS categoria
  ,n.titulo
  ,n.descricao
  ,n.datahora
  ,n.comentarios
  ,n.url
FROM
  noticias.noticias AS n
  LEFT JOIN noticias.paginas AS p
    ON n.id_pagina = p.id
  LEFT JOIN noticias.categorias AS c
    ON n.id_categoria = c.id
ORDER BY n.datahora DESC
LIMIT 10;