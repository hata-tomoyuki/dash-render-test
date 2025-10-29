-- Insert initial data for tag management

-- Insert color tags (7 colors)
INSERT INTO color_tag (color_tag_name, color_tag_color) VALUES
('黄', '#FFFF00'),
('赤', '#FF0000'),
('紫', '#800080'),
('青', '#0000FF'),
('緑', '#008000'),
('黒', '#000000'),
('白', '#FFFFFF')
ON CONFLICT DO NOTHING;

-- Insert category tags (5 items with icons)
INSERT INTO category_tag (category_tag_name, category_tag_color, category_tag_icon, category_tag_use_flag) VALUES
('フィギュア', '#FF6B6B', 'bi-robot', 1),
('アクリルスタンド', '#4ECDC4', 'bi-person-standing', 1),
('缶バッジ', '#45B7D1', 'bi-circle', 1),
('ポスター', '#96CEB4', 'bi-image', 1),
('タペストリー', '#FFEAA7', 'bi-columns', 1)
ON CONFLICT DO NOTHING;

-- Insert receipt location tags (6 items with icons)
INSERT INTO receipt_location (receipt_location_name, receipt_location_icon, receipt_location_use_flag) VALUES
('タンス', 'bi-archive', 1),
('書棚', 'bi-bookshelf', 1),
('段ボール', 'bi-box', 1),
('フォルダ', 'bi-folder', 1),
('クリアファイル', 'bi-file-earmark', 1),
('ディスプレイ', 'bi-tv', 1)
ON CONFLICT DO NOTHING;
