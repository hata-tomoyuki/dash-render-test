-- Step 2: Create missing tables from spec.md

-- 色テーブル
CREATE TABLE IF NOT EXISTS color (
  color_group_id SERIAL PRIMARY KEY,
  color_group_name TEXT NOT NULL UNIQUE,
  color_preference TEXT, -- RGB value
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 作品情報テーブル
CREATE TABLE IF NOT EXISTS works_information (
  works_id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  works_series_id INTEGER REFERENCES works_series(works_series_id) ON DELETE SET NULL,
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

-- 貨幣単位テーブル
CREATE TABLE IF NOT EXISTS currency_unit (
  currency_unit_id SERIAL PRIMARY KEY,
  currency_name TEXT NOT NULL UNIQUE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
