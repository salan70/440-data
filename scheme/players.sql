-- プレイヤーのテーブル
CREATE TABLE Players (
    -- プレイヤーID
    playerId TEXT PRIMARY KEY,

    -- プレイヤーのファーストネーム
    nameFirst TEXT,

    -- プレイヤーのラストネーム
    nameLast TEXT NOT NULL
);
