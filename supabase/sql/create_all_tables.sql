-- ============================================
-- 推し活グッズ管理アプリ - 完全なデータベーススキーマ作成
-- ============================================
-- このスクリプトは、registration_product_informationテーブルと
-- その依存テーブルをすべて作成します。
-- SupabaseのSQL Editorで実行してください。
-- ============================================

-- 更新トリガー関数の作成（既に存在する場合はスキップ）
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

-- ============================================
-- 1. 基本テーブル（依存関係なし）
-- ============================================

-- 作品シリーズテーブル
CREATE TABLE IF NOT EXISTS works_series (
  works_series_id SERIAL PRIMARY KEY,
  works_series_name TEXT NOT NULL UNIQUE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 色テーブル
CREATE TABLE IF NOT EXISTS color (
  color_group_id SERIAL PRIMARY KEY,
  color_group_name TEXT NOT NULL UNIQUE,
  color_preference TEXT, -- RGB value
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 版権元テーブル
CREATE TABLE IF NOT EXISTS copyright_source (
  copyright_company_id SERIAL PRIMARY KEY,
  copyright_company_name TEXT NOT NULL UNIQUE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 製品種別テーブル
CREATE TABLE IF NOT EXISTS product_type (
  product_group_id SERIAL PRIMARY KEY,
  product_group_name TEXT NOT NULL UNIQUE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 収納場所テーブル
CREATE TABLE IF NOT EXISTS receipt_location (
  receipt_location_id SERIAL PRIMARY KEY,
  receipt_location_name TEXT NOT NULL,
  receipt_location_size_horizontal INTEGER,
  receipt_location_size_depth INTEGER,
  receipt_location_size_vertical INTEGER,
  receipt_count_per_1 INTEGER DEFAULT 1,
  receipt_size_horizontal_per_1 INTEGER,
  receipt_size_depth_per_1 INTEGER,
  receipt_size_vertical_per_1 INTEGER,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 会員種別テーブル
CREATE TABLE IF NOT EXISTS member_type (
  members_type_name TEXT PRIMARY KEY,
  thumbnail_image_quality INTEGER DEFAULT 80,
  registerable_number INTEGER DEFAULT 100,
  number_registerable_high_resolution INTEGER DEFAULT 10,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 貨幣単位テーブル
CREATE TABLE IF NOT EXISTS currency_unit (
  currency_unit_id SERIAL PRIMARY KEY,
  currency_name TEXT NOT NULL UNIQUE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- 2. 依存テーブル（基本テーブルに依存）
-- ============================================

-- 作品情報テーブル
CREATE TABLE IF NOT EXISTS works_information (
  works_id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  works_series_id INTEGER REFERENCES works_series(works_series_id) ON DELETE SET NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 製品規格サイズテーブル
CREATE TABLE IF NOT EXISTS product_regulations_size (
  product_size_id SERIAL PRIMARY KEY,
  product_group_id INTEGER REFERENCES product_type(product_group_id) ON DELETE SET NULL,
  product_type TEXT,
  product_size_horizontal INTEGER,
  product_size_depth INTEGER,
  product_size_vertical INTEGER,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 会員情報テーブル
CREATE TABLE IF NOT EXISTS member_information (
  members_id SERIAL PRIMARY KEY,
  members_type_name TEXT REFERENCES member_type(members_type_name) ON DELETE SET NULL,
  user_name TEXT,
  email_address TEXT UNIQUE,
  x_id TEXT,
  instagram_id TEXT,
  line_id TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 写真テーブル
CREATE TABLE IF NOT EXISTS photo (
  photo_id SERIAL PRIMARY KEY,
  photo_theme_color INTEGER REFERENCES color(color_group_id) ON DELETE SET NULL,
  front_flag INTEGER DEFAULT 0,
  photo_thumbnail BYTEA,
  photo_thumbnail_image_quality INTEGER DEFAULT 80,
  photo_high_resolution_flag INTEGER DEFAULT 0,
  photo_edited_flag INTEGER DEFAULT 0,
  photo_registration_date TIMESTAMPTZ DEFAULT NOW(),
  photo_edit_date TIMESTAMPTZ,
  photo_thumbnail_url TEXT,
  photo_high_resolution_url TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- キャラクター情報テーブル
CREATE TABLE IF NOT EXISTS character (
  character_id SERIAL PRIMARY KEY,
  works_id INTEGER REFERENCES works_information(works_id) ON DELETE CASCADE,
  works_series_id INTEGER REFERENCES works_series(works_series_id) ON DELETE CASCADE,
  theme_color INTEGER REFERENCES color(color_group_id) ON DELETE SET NULL,
  hair_color INTEGER REFERENCES color(color_group_id) ON DELETE SET NULL,
  eye_color INTEGER REFERENCES color(color_group_id) ON DELETE SET NULL,
  character_name TEXT,
  nickname TEXT,
  sex TEXT,
  person_flag INTEGER DEFAULT 0,
  animal_flag INTEGER DEFAULT 0,
  existing_flag INTEGER DEFAULT 0,
  foot_number INTEGER,
  height INTEGER,
  weight INTEGER,
  birthday DATE,
  debut_date DATE,
  age INTEGER,
  student_flag INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- カラータグテーブル
CREATE TABLE IF NOT EXISTS color_tag (
  color_tag_id SERIAL PRIMARY KEY,
  members_id INTEGER REFERENCES member_information(members_id) ON DELETE CASCADE,
  color_tag_color TEXT, -- RGB value
  color_tag_name TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- カテゴリータグテーブル
CREATE TABLE IF NOT EXISTS category_tag (
  category_tag_id SERIAL PRIMARY KEY,
  members_id INTEGER REFERENCES member_information(members_id) ON DELETE CASCADE,
  category_tag_color TEXT, -- RGB value
  category_tag_name TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- 3. メインテーブル: registration_product_information
-- ============================================

-- 製品情報テーブル（既存の場合は削除して再作成）
DROP TABLE IF EXISTS registration_product_information CASCADE;

CREATE TABLE registration_product_information (
  registration_product_id SERIAL PRIMARY KEY,
  photo_id INTEGER REFERENCES photo(photo_id) ON DELETE SET NULL,
  works_series_id INTEGER REFERENCES works_series(works_series_id) ON DELETE SET NULL,
  works_id INTEGER REFERENCES works_information(works_id) ON DELETE SET NULL,
  character_id INTEGER REFERENCES character(character_id) ON DELETE SET NULL,
  copyright_company_id INTEGER REFERENCES copyright_source(copyright_company_id) ON DELETE SET NULL,
  product_group_id INTEGER REFERENCES product_type(product_group_id) ON DELETE SET NULL,
  product_size_id INTEGER REFERENCES product_regulations_size(product_size_id) ON DELETE SET NULL,
  receipt_location_id INTEGER REFERENCES receipt_location(receipt_location_id) ON DELETE SET NULL,
  receipt_location_tag_id INTEGER, -- Will reference another table if needed
  color_tag_id INTEGER REFERENCES color_tag(color_tag_id) ON DELETE SET NULL,
  category_tag_id INTEGER REFERENCES category_tag(category_tag_id) ON DELETE SET NULL,
  campaign_id INTEGER, -- Will reference campaign table if created
  currency_unit_id INTEGER REFERENCES currency_unit(currency_unit_id) ON DELETE SET NULL,
  works_series_name TEXT,
  title TEXT,
  character_name TEXT,
  copyright_company_name TEXT,
  product_type TEXT,
  product_size_horizontal INTEGER,
  product_size_depth INTEGER,
  product_size_vertical INTEGER,
  barcode_number TEXT,
  barcode_type TEXT,
  product_name TEXT,
  list_price INTEGER,
  purchase_price INTEGER,
  registration_quantity INTEGER DEFAULT 1,
  sales_desired_quantity INTEGER,
  product_series_quantity INTEGER,
  purchase_location TEXT,
  freebie_name TEXT,
  purchase_date DATE,
  creation_date TIMESTAMPTZ DEFAULT NOW(),
  updated_date TIMESTAMPTZ DEFAULT NOW(),
  other_tag TEXT,
  memo TEXT,
  product_series_flag INTEGER DEFAULT 0,
  commercial_product_flag INTEGER DEFAULT 1,
  personal_product_flag INTEGER DEFAULT 0,
  digital_product_flag INTEGER DEFAULT 0,
  sales_desired_flag INTEGER DEFAULT 0,
  want_object_flag INTEGER DEFAULT 0,
  flag_with_freebie INTEGER DEFAULT 0,
  product_series_complete_flag INTEGER DEFAULT 0,
  product_group_name TEXT
);

-- ============================================
-- 4. インデックスの作成
-- ============================================

-- registration_product_information のインデックス
CREATE INDEX IF NOT EXISTS idx_registration_product_photo ON registration_product_information(photo_id);
CREATE INDEX IF NOT EXISTS idx_registration_product_works_series ON registration_product_information(works_series_id);
CREATE INDEX IF NOT EXISTS idx_registration_product_works ON registration_product_information(works_id);
CREATE INDEX IF NOT EXISTS idx_registration_product_character ON registration_product_information(character_id);
CREATE INDEX IF NOT EXISTS idx_registration_product_copyright ON registration_product_information(copyright_company_id);
CREATE INDEX IF NOT EXISTS idx_registration_product_group ON registration_product_information(product_group_id);
CREATE INDEX IF NOT EXISTS idx_registration_product_size ON registration_product_information(product_size_id);
CREATE INDEX IF NOT EXISTS idx_registration_product_location ON registration_product_information(receipt_location_id);
CREATE INDEX IF NOT EXISTS idx_registration_product_color_tag ON registration_product_information(color_tag_id);
CREATE INDEX IF NOT EXISTS idx_registration_product_category_tag ON registration_product_information(category_tag_id);
CREATE INDEX IF NOT EXISTS idx_registration_product_barcode ON registration_product_information(barcode_number);
CREATE INDEX IF NOT EXISTS idx_registration_product_creation_date ON registration_product_information(creation_date DESC);
CREATE INDEX IF NOT EXISTS idx_registration_product_updated_date ON registration_product_information(updated_date DESC);
CREATE INDEX IF NOT EXISTS idx_registration_product_series_complete_flag ON registration_product_information(product_series_complete_flag);

-- その他のテーブルのインデックス
CREATE INDEX IF NOT EXISTS idx_character_works ON character(works_id);
CREATE INDEX IF NOT EXISTS idx_character_works_series ON character(works_series_id);
CREATE INDEX IF NOT EXISTS idx_member_info_type ON member_information(members_type_name);
CREATE INDEX IF NOT EXISTS idx_photo_theme_color ON photo(photo_theme_color);
CREATE INDEX IF NOT EXISTS idx_color_tag_member ON color_tag(members_id);
CREATE INDEX IF NOT EXISTS idx_category_tag_member ON category_tag(members_id);

-- ============================================
-- 5. Row Level Security (RLS) の設定
-- ============================================

-- RLSを有効化
ALTER TABLE works_series ENABLE ROW LEVEL SECURITY;
ALTER TABLE color ENABLE ROW LEVEL SECURITY;
ALTER TABLE copyright_source ENABLE ROW LEVEL SECURITY;
ALTER TABLE product_type ENABLE ROW LEVEL SECURITY;
ALTER TABLE receipt_location ENABLE ROW LEVEL SECURITY;
ALTER TABLE member_type ENABLE ROW LEVEL SECURITY;
ALTER TABLE currency_unit ENABLE ROW LEVEL SECURITY;
ALTER TABLE works_information ENABLE ROW LEVEL SECURITY;
ALTER TABLE product_regulations_size ENABLE ROW LEVEL SECURITY;
ALTER TABLE member_information ENABLE ROW LEVEL SECURITY;
ALTER TABLE photo ENABLE ROW LEVEL SECURITY;
ALTER TABLE character ENABLE ROW LEVEL SECURITY;
ALTER TABLE color_tag ENABLE ROW LEVEL SECURITY;
ALTER TABLE category_tag ENABLE ROW LEVEL SECURITY;
ALTER TABLE registration_product_information ENABLE ROW LEVEL SECURITY;

-- RLSポリシーの作成（全操作を許可）
-- 既存のポリシーを削除してから再作成
DROP POLICY IF EXISTS "Allow all operations on works_series" ON works_series;
CREATE POLICY "Allow all operations on works_series" ON works_series FOR ALL TO public USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all operations on color" ON color;
CREATE POLICY "Allow all operations on color" ON color FOR ALL TO public USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all operations on copyright_source" ON copyright_source;
CREATE POLICY "Allow all operations on copyright_source" ON copyright_source FOR ALL TO public USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all operations on product_type" ON product_type;
CREATE POLICY "Allow all operations on product_type" ON product_type FOR ALL TO public USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all operations on receipt_location" ON receipt_location;
CREATE POLICY "Allow all operations on receipt_location" ON receipt_location FOR ALL TO public USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all operations on member_type" ON member_type;
CREATE POLICY "Allow all operations on member_type" ON member_type FOR ALL TO public USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all operations on currency_unit" ON currency_unit;
CREATE POLICY "Allow all operations on currency_unit" ON currency_unit FOR ALL TO public USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all operations on works_information" ON works_information;
CREATE POLICY "Allow all operations on works_information" ON works_information FOR ALL TO public USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all operations on product_regulations_size" ON product_regulations_size;
CREATE POLICY "Allow all operations on product_regulations_size" ON product_regulations_size FOR ALL TO public USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all operations on member_information" ON member_information;
CREATE POLICY "Allow all operations on member_information" ON member_information FOR ALL TO public USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all operations on photo" ON photo;
CREATE POLICY "Allow all operations on photo" ON photo FOR ALL TO public USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all operations on character" ON character;
CREATE POLICY "Allow all operations on character" ON character FOR ALL TO public USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all operations on color_tag" ON color_tag;
CREATE POLICY "Allow all operations on color_tag" ON color_tag FOR ALL TO public USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all operations on category_tag" ON category_tag;
CREATE POLICY "Allow all operations on category_tag" ON category_tag FOR ALL TO public USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all operations on registration_product_information" ON registration_product_information;
CREATE POLICY "Allow all operations on registration_product_information" ON registration_product_information FOR ALL TO public USING (true) WITH CHECK (true);

-- ============================================
-- 6. 更新トリガーの作成
-- ============================================

-- 既存のトリガーを削除して再作成
DROP TRIGGER IF EXISTS update_works_series_updated_at ON works_series;
CREATE TRIGGER update_works_series_updated_at BEFORE UPDATE ON works_series FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_color_updated_at ON color;
CREATE TRIGGER update_color_updated_at BEFORE UPDATE ON color FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_copyright_source_updated_at ON copyright_source;
CREATE TRIGGER update_copyright_source_updated_at BEFORE UPDATE ON copyright_source FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_product_type_updated_at ON product_type;
CREATE TRIGGER update_product_type_updated_at BEFORE UPDATE ON product_type FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_receipt_location_updated_at ON receipt_location;
CREATE TRIGGER update_receipt_location_updated_at BEFORE UPDATE ON receipt_location FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_member_type_updated_at ON member_type;
CREATE TRIGGER update_member_type_updated_at BEFORE UPDATE ON member_type FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_currency_unit_updated_at ON currency_unit;
CREATE TRIGGER update_currency_unit_updated_at BEFORE UPDATE ON currency_unit FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_works_information_updated_at ON works_information;
CREATE TRIGGER update_works_information_updated_at BEFORE UPDATE ON works_information FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_product_regulations_size_updated_at ON product_regulations_size;
CREATE TRIGGER update_product_regulations_size_updated_at BEFORE UPDATE ON product_regulations_size FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_member_information_updated_at ON member_information;
CREATE TRIGGER update_member_information_updated_at BEFORE UPDATE ON member_information FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_photo_updated_at ON photo;
CREATE TRIGGER update_photo_updated_at BEFORE UPDATE ON photo FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_character_updated_at ON character;
CREATE TRIGGER update_character_updated_at BEFORE UPDATE ON character FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_color_tag_updated_at ON color_tag;
CREATE TRIGGER update_color_tag_updated_at BEFORE UPDATE ON color_tag FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_category_tag_updated_at ON category_tag;
CREATE TRIGGER update_category_tag_updated_at BEFORE UPDATE ON category_tag FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_registration_product_information_updated_at ON registration_product_information;
CREATE TRIGGER update_registration_product_information_updated_at BEFORE UPDATE ON registration_product_information FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- 完了メッセージ
-- ============================================
DO $$
BEGIN
  RAISE NOTICE 'すべてのテーブルが正常に作成されました！';
END $$;

