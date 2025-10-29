-- Insert initial Bootstrap Icons data into icon_tag table

INSERT INTO icon_tag (icon, icon_name, category_tag_use_flag, receipt_location_use_flag) VALUES
-- Category tag icons (most useful for merchandise)
('bi-robot', 'ロボット (フィギュア)', 1, 0),
('bi-person-standing', '人 (アクリルスタンド)', 1, 0),
('bi-circle', '円 (バッジ)', 1, 0),
('bi-image', '画像 (ポスター)', 1, 0),
('bi-columns', '列 (タペストリー)', 1, 0),
('bi-star', '星', 1, 0),
('bi-heart', 'ハート', 1, 0),
('bi-lightning', '稲妻', 1, 0),
('bi-gear', '歯車', 1, 0),
('bi-music-note', '音符', 1, 0),
('bi-camera', 'カメラ', 1, 0),
('bi-book', '本', 1, 0),
('bi-pencil', '鉛筆', 1, 0),
('bi-palette', 'パレット', 1, 0),
('bi-trophy', 'トロフィー', 1, 0),

-- Receipt location icons (most useful for storage)
('bi-archive', 'アーカイブ (タンス)', 0, 1),
('bi-bookshelf', '本棚 (書棚)', 0, 1),
('bi-box', '箱 (段ボール)', 0, 1),
('bi-folder', 'フォルダ', 0, 1),
('bi-file-earmark', 'ファイル (クリアファイル)', 0, 1),
('bi-tv', 'テレビ (ディスプレイ)', 0, 1),
('bi-house', '家', 0, 1),
('bi-safe', '金庫', 0, 1),
('bi-drawer', '引き出し', 0, 1),
('bi-briefcase', 'ブリーフケース', 0, 1),
('bi-basket', 'バスケット', 0, 1),
('bi-bag', 'バッグ', 0, 1),
('bi-truck', 'トラック', 0, 1),
('bi-building', 'ビル', 0, 1),
('bi-shop', 'ショップ', 0, 1),

-- Shared icons (can be used for both)
('bi-gift', 'ギフト', 1, 1),
('bi-tag', 'タグ', 1, 1),
('bi-box-seam', '箱', 1, 1),
('bi-collection', 'コレクション', 1, 1),
('bi-grid', 'グリッド', 1, 1)
ON CONFLICT (icon) DO NOTHING;
