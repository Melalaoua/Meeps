CREATE SCHEMA milestones;

CREATE TABLE milestones.milestone (
    id BIGSERIAL PRIMARY KEY,
    title varchar(100),
    info TEXT,
    reward_desc TEXT,
    reward_lauriers int NOT NULL  
);


CREATE TABLE milestones.pallier (
    id SERIAL PRIMARY KEY,
    parent BIGINT NOT NULL,
    child BIGINT NOT NULL,


    CONSTRAINT FK_milestone_parent
        FOREIGN KEY (parent)
        REFERENCES milestones.milestone(id),
    
    CONSTRAINT FK_milestone_child
        FOREIGN KEY (child)
        REFERENCES milestones.milestone(id)
);


CREATE TABLE milestones.user_milestone (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    milestone_id BIGINT NOT NULL,
    completed bool DEFAULT false,
    date timestamp with time zone NOT NULL,

    CONSTRAINT FK_user
        FOREIGN KEY (user_id)
        REFERENCES moodyblues.user(id),
    
    CONSTRAINT FK_milestone
        FOREIGN KEY (milestone_id)
        REFERENCES milestones.milestone(id)
);


CREATE TABLE milestones.milestone_categories(
    id SERIAL PRIMARY KEY,
    name varchar(100) NOT NULL
);


CREATE TABLE milestones.milestone_category(
    id BIGSERIAL PRIMARY KEY,
    milestone_id BIGINT NOT NULL,
    category_id BIGINT NOT NULL,

    CONSTRAINT FK_milestone
        FOREIGN KEY (milestone_id)
        REFERENCES milestones.milestone(id),

    CONSTRAINT FK_milestone_category
        FOREIGN KEY (category_id)
        REFERENCES milestones.milestone_categories(id)
);


CREATE TABLE milestones.title (
    id BIGSERIAL PRIMARY KEY,
    title varchar(100) NOT NULL,
    discord_id BIGINT
);


CREATE TABLE milestones.milestone_title (
    id SERIAL PRIMARY KEY,
    milestone_id BIGINT NOT NULL,
    title_id BIGINT NOT NULL,

    CONSTRAINT FK_milestone_title
        FOREIGN KEY (milestone_id)
        REFERENCES milestones.milestone(id)
        ON DELETE CASCADE,
    
    CONSTRAINT FK_title_milestone
        FOREIGN KEY (title_id)
        REFERENCES milestones.title(id)
        ON DELETE CASCADE
);


CREATE TABLE milestones.user_title(
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    title_id BIGINT NOT NULL,
    active bool DEFAULT false,

    CONSTRAINT FK_user_title
        FOREIGN KEY (user_id)
        REFERENCES moodyblues.user(id)
        ON DELETE CASCADE,
    
    CONSTRAINT FK_title_user
        FOREIGN KEY (title_id)
        REFERENCES milestones.title(id)
        ON DELETE CASCADE

);