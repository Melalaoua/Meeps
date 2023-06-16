CREATE SCHEMA silverscrapes;

CREATE TABLE silverscrapes.scrape (
    id BIGSERIAL PRIMARY KEY,
    article_date timestamp with time zone NOT NULL,
    article_title TEXT NOT NULL,
    article_link TEXT NOT NULL,
    article_desc TEXT default ' ',
    website_link TEXT NOT NULL,
    category varchar(30) NOT NULL,
    to_recap bool default false,
    scrape_key BIGINT,
    score INT default 0
);

CREATE TABLE silverscrapes.scrape_message (
    id BIGSERIAL PRIMARY KEY,
    scrape_id BIGINT NOT NULL,
    message_id INT NOT NULL,


    CONSTRAINT FK_scrape_message 
        FOREIGN KEY (scrape_id)
        REFERENCES silverscrapes.scrape(id)
        ON DELETE CASCADE,
    CONSTRAINT FK_message_scrape 
        FOREIGN KEY (message_id)
        REFERENCES moodyblues.discord_message(id)
        ON DELETE CASCADE  
);

