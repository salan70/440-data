-- 打撃成績のテーブル
CREATE TABLE BattingStats (
    -- プレイヤーID
    playerId TEXT,

    -- 表示順
    displayOrder INTEGER,
    
    -- 年
    year INTEGER NOT NULL,

    -- チーム
    teamId TEXT,

    -- 試合数
    G INTEGER NOT NULL,

    -- 打席数
    PA INTEGER NOT NULL,

    -- 打数
    AB INTEGER NOT NULL,

    -- 安打数
    H INTEGER NOT NULL,

    -- 長打数
    XBH INTEGER NOT NULL,

    -- 塁打数
    TB INTEGER NOT NULL,

    -- 二球打数
    "2B" INTEGER NOT NULL,

    -- 三球打数
    "3B" INTEGER NOT NULL,

    -- ホームラン数
    HR INTEGER NOT NULL,

    -- 得点数
    R INTEGER NOT NULL,

    -- 打点数
    RBI INTEGER NOT NULL,

    -- 四球数
    BB INTEGER NOT NULL,

    -- 敬遠数
    IBB INTEGER NOT NULL,

    -- 死球数
    HBP INTEGER NOT NULL,
    
    -- 三振数
    SO INTEGER NOT NULL,
    
    -- 盗塁数
    SB INTEGER NOT NULL,

    -- 盗塁死数
    CS INTEGER NOT NULL,

    -- 犠牲バント数
    SAC INTEGER NOT NULL,

    -- 犠牲フライ数
    SF INTEGER NOT NULL,

    -- ダブルプレイ数
    GIDP INTEGER NOT NULL,

    -- 打率
    AVG FLOAT,

    -- 出塁率
    OBP FLOAT,

    -- 長打率
    SLG FLOAT,

    -- OPS
    OPS FLOAT,

    -- BABIP
    BABIP FLOAT,

    -- ISO（ 長打率 - 打率 ）
    ISO FLOAT,

    -- 打数/ホームラン数（ホームラン1本にかかる打数）
    "AB/HR" FLOAT,

    -- 四球/三振
    "BB/K" FLOAT,

    -- BB%
    "BB%" FLOAT,

    -- SO%
    "SO%" FLOAT,

    -- 複合主キーの定義
    PRIMARY KEY (playerId, displayOrder),

    -- 外部キーの定義
    FOREIGN KEY (playerId) REFERENCES Players(playerId),
    FOREIGN KEY (teamId) REFERENCES Teams(teamId)
);
