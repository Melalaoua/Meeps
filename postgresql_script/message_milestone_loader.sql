-- Table milestone
INSERT INTO milestones.milestone (title, info, reward_lauriers) VALUES('T''écrit bcp Machallah I', 'Envoyer 100 messages sur le serveur discord', 5);

INSERT INTO milestones.milestone (title, info, reward_lauriers) VALUES('T''écrit bcp Machallah II', 'Envoyer 500 messages sur le serveur discord', 10);

INSERT INTO milestones.milestone (title, info, reward_lauriers) VALUES('T''écrit bcp Machallah III', 'Envoyer 1000 messages sur le serveur discord', 10);

INSERT INTO milestones.milestone (title, info, reward_desc, reward_lauriers) VALUES('T''écrit bcp Machallah IV', 'Envoyer 5000 messages sur le serveur discord','Rôle et titre OG', 15);

INSERT INTO milestones.milestone (title, info, reward_lauriers) VALUES('T''écrit bcp Machallah V', 'Envoyer 10 000 messages sur le serveur discord', 20);

INSERT INTO milestones.milestone (title, info, reward_lauriers) VALUES('T''écrit bcp Machallah VI', 'Envoyer 25 000 messages sur le serveur discord', 20);

INSERT INTO milestones.milestone (title, info, reward_lauriers) VALUES('T''écrit bcp Machallah VII', 'Envoyer 50 000 messages sur le serveur discord', 50);

INSERT INTO milestones.milestone (title, info, reward_desc, reward_lauriers) VALUES('T''écrit bcp Machallah VIII', 'Envoyer 100 000 messages sur le serveur discord','Rôle et titre L''omniprésent', 50);

INSERT INTO milestones.milestone (title, info, reward_lauriers) VALUES('T''écrit bcp Machallah IX', 'Envoyer 500 000 messages sur le serveur discord', 50);

INSERT INTO milestones.milestone (title, info, reward_lauriers) VALUES('T''écrit bcp Machallah X', 'Envoyer 1 000 000 messages sur le serveur discord', 100);



-- Table pallier
INSERT INTO milestones.pallier(parent, child) VALUES((SELECT id from milestones.milestone WHERE title = 'T''écrit bcp Machallah I'),(SELECT id from milestones.milestone WHERE title = 'T''écrit bcp Machallah II'));

INSERT INTO milestones.pallier(parent, child) VALUES((SELECT id from milestones.milestone WHERE title = 'T''écrit bcp Machallah II'),(SELECT id from milestones.milestone WHERE title = 'T''écrit bcp Machallah III'));

INSERT INTO milestones.pallier(parent, child) VALUES((SELECT id from milestones.milestone WHERE title = 'T''écrit bcp Machallah III'),(SELECT id from milestones.milestone WHERE title = 'T''écrit bcp Machallah IV'));

INSERT INTO milestones.pallier(parent, child) VALUES((SELECT id from milestones.milestone WHERE title = 'T''écrit bcp Machallah IV'),(SELECT id from milestones.milestone WHERE title = 'T''écrit bcp Machallah V'));

INSERT INTO milestones.pallier(parent, child) VALUES((SELECT id from milestones.milestone WHERE title = 'T''écrit bcp Machallah V'),(SELECT id from milestones.milestone WHERE title = 'T''écrit bcp Machallah VI'));

INSERT INTO milestones.pallier(parent, child) VALUES((SELECT id from milestones.milestone WHERE title = 'T''écrit bcp Machallah VI'),(SELECT id from milestones.milestone WHERE title = 'T''écrit bcp Machallah VII'));

INSERT INTO milestones.pallier(parent, child) VALUES((SELECT id from milestones.milestone WHERE title = 'T''écrit bcp Machallah VII'),(SELECT id from milestones.milestone WHERE title = 'T''écrit bcp Machallah VIII'));

INSERT INTO milestones.pallier(parent, child) VALUES((SELECT id from milestones.milestone WHERE title = 'T''écrit bcp Machallah VIII'),(SELECT id from milestones.milestone WHERE title = 'T''écrit bcp Machallah IX'));

INSERT INTO milestones.pallier(parent, child) VALUES((SELECT id from milestones.milestone WHERE title = 'T''écrit bcp Machallah IX'),(SELECT id from milestones.milestone WHERE title = 'T''écrit bcp Machallah X'));


-- Categories
INSERT INTO milestones.milestone_categories(name) values('Messages');


-- Milestone categories association
INSERT INTO milestones.milestone_category(milestone_id, category_id) VALUES((SELECT id from milestones.milestone WHERE title = 'T''écrit bcp Machallah I'),(SELECT id from milestones.milestone_categories WHERE name = 'Messages'));

INSERT INTO milestones.milestone_category(milestone_id, category_id) VALUES((SELECT id from milestones.milestone WHERE title = 'T''écrit bcp Machallah II'),(SELECT id from milestones.milestone_categories WHERE name = 'Messages'));

INSERT INTO milestones.milestone_category(milestone_id, category_id) VALUES((SELECT id from milestones.milestone WHERE title = 'T''écrit bcp Machallah III'),(SELECT id from milestones.milestone_categories WHERE name = 'Messages'));

INSERT INTO milestones.milestone_category(milestone_id, category_id) VALUES((SELECT id from milestones.milestone WHERE title = 'T''écrit bcp Machallah IV'),(SELECT id from milestones.milestone_categories WHERE name = 'Messages'));

INSERT INTO milestones.milestone_category(milestone_id, category_id) VALUES((SELECT id from milestones.milestone WHERE title = 'T''écrit bcp Machallah V'),(SELECT id from milestones.milestone_categories WHERE name = 'Messages'));

INSERT INTO milestones.milestone_category(milestone_id, category_id) VALUES((SELECT id from milestones.milestone WHERE title = 'T''écrit bcp Machallah VI'),(SELECT id from milestones.milestone_categories WHERE name = 'Messages'));

INSERT INTO milestones.milestone_category(milestone_id, category_id) VALUES((SELECT id from milestones.milestone WHERE title = 'T''écrit bcp Machallah VII'),(SELECT id from milestones.milestone_categories WHERE name = 'Messages'));

INSERT INTO milestones.milestone_category(milestone_id, category_id) VALUES((SELECT id from milestones.milestone WHERE title = 'T''écrit bcp Machallah VIII'),(SELECT id from milestones.milestone_categories WHERE name = 'Messages'));

INSERT INTO milestones.milestone_category(milestone_id, category_id) VALUES((SELECT id from milestones.milestone WHERE title = 'T''écrit bcp Machallah IX'),(SELECT id from milestones.milestone_categories WHERE name = 'Messages'));

INSERT INTO milestones.milestone_category(milestone_id, category_id) VALUES((SELECT id from milestones.milestone WHERE title = 'T''écrit bcp Machallah X'),(SELECT id from milestones.milestone_categories WHERE name = 'Messages'));


--title
INSERT INTO milestones.title(title, discord_id) VALUES ('Korybantes', 1080906687646531725);
INSERT INTO milestones.title(title, discord_id) VALUES ('L''omniprésent', 1092085306334912614);

--association title // milestone
INSERT INTO milestones.milestone_title(milestone_id, title_id) VALUES ((SELECT id from milestones.milestone WHERE title = 'T''écrit bcp Machallah IV'), (SELECT id from milestones.title WHERE title='Korybantes'));

INSERT INTO milestones.milestone_title(milestone_id, title_id) VALUES ((SELECT id from milestones.milestone WHERE title = 'T''écrit bcp Machallah VIII'), (SELECT id from milestones.title WHERE title='L''omniprésent'));
