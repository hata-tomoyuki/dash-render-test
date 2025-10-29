-- Create remaining tables as defined in spec.md and clear test data

-- Clear test data from registration_product_information table
DELETE FROM registration_product_information;

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

-- 色テーブル
CREATE TABLE IF NOT EXISTS color (
  color_group_id SERIAL PRIMARY KEY,
  color_group_name TEXT NOT NULL UNIQUE,
  color_preference TEXT, -- RGB value
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 作品情報テーブル (既に存在する場合はスキップ)
CREATE TABLE IF NOT EXISTS works_information (
  works_id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  works_series_id INTEGER REFERENCES works_series(works_series_id) ON DELETE SET NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 版権元テーブル (既に存在する場合はスキップ)
CREATE TABLE IF NOT EXISTS copyright_source (
  copyright_company_id SERIAL PRIMARY KEY,
  copyright_company_name TEXT NOT NULL UNIQUE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 製品種別テーブル (既に存在する場合はスキップ)
CREATE TABLE IF NOT EXISTS product_type (
  product_group_id SERIAL PRIMARY KEY,
  product_group_name TEXT NOT NULL UNIQUE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 製品規格サイズテーブル (既に存在する場合はスキップ)
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

-- 収納場所テーブル (既に存在する場合はスキップ)
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

-- 貨幣単位テーブル
CREATE TABLE IF NOT EXISTS currency_unit (
  currency_unit_id SERIAL PRIMARY KEY,
  currency_name TEXT NOT NULL UNIQUE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Update registration_product_information to include missing foreign keys
-- (Note: Some columns may need to be added based on spec.md)

-- Add missing columns to registration_product_information if they don't exist
DO $$
BEGIN
  -- Add columns that might be missing based on spec.md
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'registration_product_information' AND column_name = 'registration_quantity') THEN
    ALTER TABLE registration_product_information ADD COLUMN registration_quantity INTEGER DEFAULT 1;
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'registration_product_information' AND column_name = 'list_price') THEN
    ALTER TABLE registration_product_information ADD COLUMN list_price INTEGER;
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'registration_product_information' AND column_name = 'purchase_price') THEN
    ALTER TABLE registration_product_information ADD COLUMN purchase_price INTEGER;
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'registration_product_information' AND column_name = 'sales_desired_quantity') THEN
    ALTER TABLE registration_product_information ADD COLUMN sales_desired_quantity INTEGER;
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'registration_product_information' AND column_name = 'product_series_quantity') THEN
    ALTER TABLE registration_product_information ADD COLUMN product_series_quantity INTEGER;
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'registration_product_information' AND column_name = 'purchase_location') THEN
    ALTER TABLE registration_product_information ADD COLUMN purchase_location TEXT;
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'registration_product_information' AND column_name = 'freebie_name') THEN
    ALTER TABLE registration_product_information ADD COLUMN freebie_name TEXT;
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'registration_product_information' AND column_name = 'purchase_date') THEN
    ALTER TABLE registration_product_information ADD COLUMN purchase_date DATE;
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'registration_product_information' AND column_name = 'other_tag') THEN
    ALTER TABLE registration_product_information ADD COLUMN other_tag TEXT[];
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'registration_product_information' AND column_name = 'memo') THEN
    ALTER TABLE registration_product_information ADD COLUMN memo TEXT;
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'registration_product_information' AND column_name = 'product_series_flag') THEN
    ALTER TABLE registration_product_information ADD COLUMN product_series_flag INTEGER DEFAULT 0;
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'registration_product_information' AND column_name = 'commercial_product_flag') THEN
    ALTER TABLE registration_product_information ADD COLUMN commercial_product_flag INTEGER DEFAULT 1;
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'registration_product_information' AND column_name = 'personal_product_flag') THEN
    ALTER TABLE registration_product_information ADD COLUMN personal_product_flag INTEGER DEFAULT 0;
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'registration_product_information' AND column_name = 'digital_product_flag') THEN
    ALTER TABLE registration_product_information ADD COLUMN digital_product_flag INTEGER DEFAULT 0;
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'registration_product_information' AND column_name = 'sales_desired_flag') THEN
    ALTER TABLE registration_product_information ADD COLUMN sales_desired_flag INTEGER DEFAULT 0;
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'registration_product_information' AND column_name = 'want_object_flag') THEN
    ALTER TABLE registration_product_information ADD COLUMN want_object_flag INTEGER DEFAULT 0;
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'registration_product_information' AND column_name = 'flag_with_freebie') THEN
    ALTER TABLE registration_product_information ADD COLUMN flag_with_freebie INTEGER DEFAULT 0;
  END IF;
END $$;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_character_works ON character(works_id);
CREATE INDEX IF NOT EXISTS idx_character_works_series ON character(works_series_id);
CREATE INDEX IF NOT EXISTS idx_member_info_type ON member_information(members_type_name);
CREATE INDEX IF NOT EXISTS idx_photo_theme_color ON photo(photo_theme_color);
CREATE INDEX IF NOT EXISTS idx_color_tag_member ON color_tag(members_id);
CREATE INDEX IF NOT EXISTS idx_category_tag_member ON category_tag(members_id);

-- Enable Row Level Security for all new tables
ALTER TABLE character ENABLE ROW LEVEL SECURITY;
ALTER TABLE color ENABLE ROW LEVEL SECURITY;
ALTER TABLE works_information ENABLE ROW LEVEL SECURITY;
ALTER TABLE copyright_source ENABLE ROW LEVEL SECURITY;
ALTER TABLE product_type ENABLE ROW LEVEL SECURITY;
ALTER TABLE product_regulations_size ENABLE ROW LEVEL SECURITY;
ALTER TABLE receipt_location ENABLE ROW LEVEL SECURITY;
ALTER TABLE member_type ENABLE ROW LEVEL SECURITY;
ALTER TABLE member_information ENABLE ROW LEVEL SECURITY;
ALTER TABLE photo ENABLE ROW LEVEL SECURITY;
ALTER TABLE color_tag ENABLE ROW LEVEL SECURITY;
ALTER TABLE category_tag ENABLE ROW LEVEL SECURITY;
ALTER TABLE currency_unit ENABLE ROW LEVEL SECURITY;

-- Create policies for all tables (allow all operations for now)
CREATE POLICY "Allow all operations on character" ON character FOR ALL TO public USING (true) WITH CHECK (true);
CREATE POLICY "Allow all operations on color" ON color FOR ALL TO public USING (true) WITH CHECK (true);
CREATE POLICY "Allow all operations on works_information" ON works_information FOR ALL TO public USING (true) WITH CHECK (true);
CREATE POLICY "Allow all operations on copyright_source" ON copyright_source FOR ALL TO public USING (true) WITH CHECK (true);
CREATE POLICY "Allow all operations on product_type" ON product_type FOR ALL TO public USING (true) WITH CHECK (true);
CREATE POLICY "Allow all operations on product_regulations_size" ON product_regulations_size FOR ALL TO public USING (true) WITH CHECK (true);
CREATE POLICY "Allow all operations on receipt_location" ON receipt_location FOR ALL TO public USING (true) WITH CHECK (true);
CREATE POLICY "Allow all operations on member_type" ON member_type FOR ALL TO public USING (true) WITH CHECK (true);
CREATE POLICY "Allow all operations on member_information" ON member_information FOR ALL TO public USING (true) WITH CHECK (true);
CREATE POLICY "Allow all operations on photo" ON photo FOR ALL TO public USING (true) WITH CHECK (true);
CREATE POLICY "Allow all operations on color_tag" ON color_tag FOR ALL TO public USING (true) WITH CHECK (true);
CREATE POLICY "Allow all operations on category_tag" ON category_tag FOR ALL TO public USING (true) WITH CHECK (true);
CREATE POLICY "Allow all operations on currency_unit" ON currency_unit FOR ALL TO public USING (true) WITH CHECK (true);

-- Create updated_at triggers for all tables
CREATE TRIGGER update_character_updated_at BEFORE UPDATE ON character FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_color_updated_at BEFORE UPDATE ON color FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_works_information_updated_at BEFORE UPDATE ON works_information FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_copyright_source_updated_at BEFORE UPDATE ON copyright_source FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_product_type_updated_at BEFORE UPDATE ON product_type FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_product_regulations_size_updated_at BEFORE UPDATE ON product_regulations_size FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_receipt_location_updated_at BEFORE UPDATE ON receipt_location FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_member_type_updated_at BEFORE UPDATE ON member_type FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_member_information_updated_at BEFORE UPDATE ON member_information FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_photo_updated_at BEFORE UPDATE ON photo FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_color_tag_updated_at BEFORE UPDATE ON color_tag FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_category_tag_updated_at BEFORE UPDATE ON category_tag FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_currency_unit_updated_at BEFORE UPDATE ON currency_unit FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
