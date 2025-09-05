BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                question TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                image_name TEXT NOT NULL,
                predicted_disease TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
CREATE TABLE IF NOT EXISTS replies (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        query_id INTEGER NOT NULL,
                        expert_username TEXT,
                        reply TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (query_id) REFERENCES queries (id)
                    );
CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL
                );
INSERT INTO "queries" ("id","user_id","question","status","created_at") VALUES (1,2,'Hello,
Can blackheads be removed at home?
','answered','2025-08-29 17:19:36'),
 (2,4,'Hello,
Can acne leave scars?','answered','2025-08-31 17:38:45');
INSERT INTO "records" ("id","user_id","image_name","predicted_disease","created_at") VALUES (1,2,'C:\Users\ILAKSH~1\AppData\Local\Temp\tmp5wgyrfa9.png','Akne','2025-08-29 17:17:42'),
 (2,2,'C:\Users\ILAKSH~1\AppData\Local\Temp\tmppuwoeu_m.jpg','Akne','2025-08-30 17:40:12'),
 (3,2,'C:\Users\ILAKSH~1\AppData\Local\Temp\tmpfw6p4hu5.jpg','Enfeksiyonel','2025-08-30 17:41:15'),
 (4,2,'C:\Users\ILAKSH~1\AppData\Local\Temp\tmpxhg08d_x.jpeg','Malign','2025-08-30 17:43:58'),
 (5,4,'C:\Users\ILAKSH~1\AppData\Local\Temp\tmpml0wkt6e.jpg','Akne','2025-08-31 17:07:36'),
 (6,2,'C:\Users\ILAKSH~1\AppData\Local\Temp\tmpxamoi0lm.jpg','Enfeksiyonel','2025-09-01 09:52:03');
INSERT INTO "replies" ("id","query_id","expert_username","reply","created_at") VALUES (1,1,'expert1','Yes, using gentle exfoliation, salicylic acid products, or pore strips. Avoid harsh squeezing to prevent scarring or infection.','2025-08-29 17:20:26'),
 (2,2,'expert1','Hello,
Yes, untreated or severe acne can lead to scars and dark spots. Avoid squeezing or picking pimples to minimize scarring. Treatments like chemical peels, laser therapy, and microneedling may help reduce scars.','2025-08-31 18:07:31');
INSERT INTO "users" ("id","username","email","password") VALUES (1,'testuser','test@test.com','13d249f2cb4127b40cfa757866850278793f814ded3c587fe5889e889a7a9f6c'),
 (2,'Kasuni','kasuniik0217@gmail.com','11983d660ba37f0869b4ec9db6ac24c1877a38d8e91e559c104c427bec1df6b7'),
 (3,'testuser_unit','test_unit@example.com','fcf730b6d95236ecd3c9fc2d92d7b6b2bb061514961aec041d6c7a7192f592e4'),
 (4,'Kasun','Kasun@gmail.com','70502ac29f3e61a8a96f0173138c85bbe67f7a462a680f91f75798bc29025bf9');
COMMIT;
