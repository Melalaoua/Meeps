CREATE SCHEMA moodyblues;

CREATE TABLE moodyblues.user (
    id SERIAL PRIMARY KEY,
    discord_id BIGINT NOT NULL,
    pseudo varchar(100)  NOT NULL,
    created_at timestamp with time zone NOT NULL,
    joined_at timestamp with time zone  NOT NULL
);


CREATE TABLE moodyblues.discord_message(
    id BIGSERIAL PRIMARY KEY,
    discord_id BIGINT NOT NULL,
    content TEXT NOT NULL,
    created_at timestamp with time zone NOT NULL
);


CREATE TABLE moodyblues.discord_channel (
    id SERIAL PRIMARY KEY,
    discord_id BIGINT NOT NULL,
    category_id BIGINT,
    channel_name varchar(200) NOT NULL,
    topic TEXT,
    position INT NOT NULL,
    nsfw bool,
    marked bool DEFAULT false
);


CREATE TABLE moodyblues.message_channel (
    id BIGSERIAL PRIMARY KEY,
    message_id BIGINT NOT NULL,
    channel_id INT NOT NULL,


    CONSTRAINT FK_message_channel 
        FOREIGN KEY (message_id)
        REFERENCES moodyblues.discord_message(id)
        ON DELETE CASCADE,
    CONSTRAINT FK_channel_message
        FOREIGN KEY (channel_id)
        REFERENCES moodyblues.discord_channel(id)
        ON DELETE CASCADE
);


CREATE TABLE moodyblues.user_message(
    id SERIAL PRIMARY KEY,
    message_id BIGINT NOT NULL,
    user_id INT NOT NULL,

    CONSTRAINT FK_message_user  
        FOREIGN KEY (message_id)
        REFERENCES moodyblues.discord_message(id) 
        ON DELETE CASCADE,
    CONSTRAINT FK_user_message
        FOREIGN KEY (user_id)
        REFERENCES moodyblues.user(id)
        ON DELETE CASCADE
);


CREATE TABLE moodyblues.fart(
    id BIGSERIAL PRIMARY KEY,
    date timestamp with time zone NOT NULL,
    fart_name varchar(150) NOT NULL
);


CREATE TABLE moodyblues.user_fart(
    id SERIAL PRIMARY KEY,
    fart_id BIGINT NOT NULL,
    user_id INT NOT NULL,
    is_emitter bool DEFAULT false,
    is_target bool DEFAULT false,

    CONSTRAINT FK_fart_user  
        FOREIGN KEY (fart_id)
        REFERENCES moodyblues.fart(id) 
        ON DELETE CASCADE,
    CONSTRAINT FK_user_fart
        FOREIGN KEY (user_id)
        REFERENCES moodyblues.user(id)
        ON DELETE CASCADE
);

CREATE TABLE moodyblues.message_fart(
    id SERIAL PRIMARY KEY,
    message_id BIGINT NOT NULL,
    fart_id BIGINT NOT NULL,

    CONSTRAINT FK_message_fart  
        FOREIGN KEY (message_id)
        REFERENCES moodyblues.discord_message(id) 
        ON DELETE CASCADE,
    CONSTRAINT FK_fart_message
        FOREIGN KEY (fart_id)
        REFERENCES moodyblues.fart(id)
        ON DELETE CASCADE
);




CREATE TABLE moodyblues.pdm(
    id BIGSERIAL PRIMARY KEY,
    date timestamp with time zone NOT NULL,
    fail bool DEFAULT false
);

CREATE TABLE moodyblues.user_pdm(
    id BIGSERIAL PRIMARY KEY,
    pdm_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    is_emitter bool DEFAULT false,
    is_target bool DEFAULT false,

    CONSTRAINT FK_pdm_user
        FOREIGN KEY (pdm_id)
        REFERENCES moodyblues.pdm(id)
        ON DELETE CASCADE,
    CONSTRAINT FK_user_pdm
        FOREIGN KEY (user_id)
        REFERENCES moodyblues.user(id)
        ON DELETE CASCADE
);


CREATE TABLE moodyblues.message_pdm(
    id SERIAL PRIMARY KEY,
    message_id BIGINT NOT NULL,
    pdm_id BIGINT NOT NULL,

    CONSTRAINT FK_message_pdm  
        FOREIGN KEY (message_id)
        REFERENCES moodyblues.discord_message(id) 
        ON DELETE CASCADE,
    CONSTRAINT FK_pdm_message
        FOREIGN KEY (pdm_id)
        REFERENCES moodyblues.pdm(id)
        ON DELETE CASCADE
);
