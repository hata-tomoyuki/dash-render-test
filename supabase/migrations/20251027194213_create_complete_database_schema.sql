/*
  # 推し活グッズ管理アプリの完全なデータベーススキーマ作成

  以下のテーブルを作成：
  1. works_series (作品シリーズ)
  2. works_information (作品情報)
  3. copyright_source (版権元)
  4. product_type (製品種別)
  5. product_regulations_size (製品規格サイズ)
  6. receipt_location (収納場所)
  7. registration_product_information (製品情報 - 拡張版)

  既存のphotosテーブルをregistration_product_informationテーブルに統合・拡張
*/

-- 作品シリーズテーブル
CREATE TABLE IF NOT EXISTS works_series (
  works_series_id SERIAL PRIMARY KEY,
  works_series_name TEXT NOT NULL UNIQUE,
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
  product_type TEXT NOT NULL,
  product_size_horizontal INTEGER,
  product_size_depth INTEGER,
  product_size_vertical INTEGER,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 収納場所テーブル
CREATE TABLE IF NOT EXISTS receipt_location (
  receipt_location_id SERIAL PRIMARY KEY,
  receipt_location_name TEXT NOT NULL UNIQUE,
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

-- 製品情報テーブル（拡張版）
CREATE TABLE IF NOT EXISTS registration_product_information (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  -- 基本情報
  barcode TEXT,
  barcode_type TEXT DEFAULT 'unknown',
  product_name TEXT,
  description TEXT DEFAULT '',

  -- 関連情報
  works_id INTEGER REFERENCES works_information(works_id) ON DELETE SET NULL,
  copyright_company_id INTEGER REFERENCES copyright_source(copyright_company_id) ON DELETE SET NULL,
  product_group_id INTEGER REFERENCES product_type(product_group_id) ON DELETE SET NULL,
  product_size_id INTEGER REFERENCES product_regulations_size(product_size_id) ON DELETE SET NULL,

  -- 画像関連
  image_url TEXT,
  additional_images TEXT[], -- 追加画像URLの配列

  -- タグ関連
  tags TEXT[] DEFAULT '{}',
  custom_tags TEXT[] DEFAULT '{}',

  -- 収納関連
  receipt_location_id INTEGER REFERENCES receipt_location(receipt_location_id) ON DELETE SET NULL,

  -- 価格・数量情報
  price INTEGER,
  quantity INTEGER DEFAULT 1,
  purchase_date DATE,

  -- メモ・備考
  notes TEXT,
  memo TEXT,

  -- タイムスタンプ
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 既存のphotosテーブルデータを移行
INSERT INTO registration_product_information (
  id,
  barcode,
  barcode_type,
  image_url,
  description,
  created_at,
  updated_at
)
SELECT
  id,
  barcode,
  COALESCE(barcode_type, 'unknown'),
  image_url,
  description,
  created_at,
  updated_at
FROM photos
ON CONFLICT (id) DO NOTHING;

-- photosテーブルを削除（データ移行後）
DROP TABLE IF EXISTS photos CASCADE;

-- Row Level Securityの設定
ALTER TABLE works_series ENABLE ROW LEVEL SECURITY;
ALTER TABLE works_information ENABLE ROW LEVEL SECURITY;
ALTER TABLE copyright_source ENABLE ROW LEVEL SECURITY;
ALTER TABLE product_type ENABLE ROW LEVEL SECURITY;
ALTER TABLE product_regulations_size ENABLE ROW LEVEL SECURITY;
ALTER TABLE receipt_location ENABLE ROW LEVEL SECURITY;
ALTER TABLE registration_product_information ENABLE ROW LEVEL SECURITY;

-- RLSポリシー（全テーブルで同様）
CREATE POLICY "Anyone can view works_series" ON works_series FOR SELECT TO public USING (true);
CREATE POLICY "Anyone can insert works_series" ON works_series FOR INSERT TO public WITH CHECK (true);
CREATE POLICY "Anyone can update works_series" ON works_series FOR UPDATE TO public USING (true) WITH CHECK (true);
CREATE POLICY "Anyone can delete works_series" ON works_series FOR DELETE TO public USING (true);

CREATE POLICY "Anyone can view works_information" ON works_information FOR SELECT TO public USING (true);
CREATE POLICY "Anyone can insert works_information" ON works_information FOR INSERT TO public WITH CHECK (true);
CREATE POLICY "Anyone can update works_information" ON works_information FOR UPDATE TO public USING (true) WITH CHECK (true);
CREATE POLICY "Anyone can delete works_information" ON works_information FOR DELETE TO public USING (true);

CREATE POLICY "Anyone can view copyright_source" ON copyright_source FOR SELECT TO public USING (true);
CREATE POLICY "Anyone can insert copyright_source" ON copyright_source FOR INSERT TO public WITH CHECK (true);
CREATE POLICY "Anyone can update copyright_source" ON copyright_source FOR UPDATE TO public USING (true) WITH CHECK (true);
CREATE POLICY "Anyone can delete copyright_source" ON copyright_source FOR DELETE TO public USING (true);

CREATE POLICY "Anyone can view product_type" ON product_type FOR SELECT TO public USING (true);
CREATE POLICY "Anyone can insert product_type" ON product_type FOR INSERT TO public WITH CHECK (true);
CREATE POLICY "Anyone can update product_type" ON product_type FOR UPDATE TO public USING (true) WITH CHECK (true);
CREATE POLICY "Anyone can delete product_type" ON product_type FOR DELETE TO public USING (true);

CREATE POLICY "Anyone can view product_regulations_size" ON product_regulations_size FOR SELECT TO public USING (true);
CREATE POLICY "Anyone can insert product_regulations_size" ON product_regulations_size FOR INSERT TO public WITH CHECK (true);
CREATE POLICY "Anyone can update product_regulations_size" ON product_regulations_size FOR UPDATE TO public USING (true) WITH CHECK (true);
CREATE POLICY "Anyone can delete product_regulations_size" ON product_regulations_size FOR DELETE TO public USING (true);

CREATE POLICY "Anyone can view receipt_location" ON receipt_location FOR SELECT TO public USING (true);
CREATE POLICY "Anyone can insert receipt_location" ON receipt_location FOR INSERT TO public WITH CHECK (true);
CREATE POLICY "Anyone can update receipt_location" ON receipt_location FOR UPDATE TO public USING (true) WITH CHECK (true);
CREATE POLICY "Anyone can delete receipt_location" ON receipt_location FOR DELETE TO public USING (true);

CREATE POLICY "Anyone can view registration_product_information" ON registration_product_information FOR SELECT TO public USING (true);
CREATE POLICY "Anyone can insert registration_product_information" ON registration_product_information FOR INSERT TO public WITH CHECK (true);
CREATE POLICY "Anyone can update registration_product_information" ON registration_product_information FOR UPDATE TO public USING (true) WITH CHECK (true);
CREATE POLICY "Anyone can delete registration_product_information" ON registration_product_information FOR DELETE TO public USING (true);

-- インデックスの作成
CREATE INDEX IF NOT EXISTS idx_works_series_name ON works_series(works_series_name);
CREATE INDEX IF NOT EXISTS idx_works_information_title ON works_information(title);
CREATE INDEX IF NOT EXISTS idx_works_information_series ON works_information(works_series_id);
CREATE INDEX IF NOT EXISTS idx_copyright_source_name ON copyright_source(copyright_company_name);
CREATE INDEX IF NOT EXISTS idx_product_type_name ON product_type(product_group_name);
CREATE INDEX IF NOT EXISTS idx_product_regulations_size_group ON product_regulations_size(product_group_id);
CREATE INDEX IF NOT EXISTS idx_receipt_location_name ON receipt_location(receipt_location_name);
CREATE INDEX IF NOT EXISTS idx_registration_product_information_barcode ON registration_product_information(barcode);
CREATE INDEX IF NOT EXISTS idx_registration_product_information_works ON registration_product_information(works_id);
CREATE INDEX IF NOT EXISTS idx_registration_product_information_copyright ON registration_product_information(copyright_company_id);
CREATE INDEX IF NOT EXISTS idx_registration_product_information_type ON registration_product_information(product_group_id);
CREATE INDEX IF NOT EXISTS idx_registration_product_information_size ON registration_product_information(product_size_id);
CREATE INDEX IF NOT EXISTS idx_registration_product_information_location ON registration_product_information(receipt_location_id);
CREATE INDEX IF NOT EXISTS idx_registration_product_information_created_at ON registration_product_information(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_registration_product_information_tags ON registration_product_information USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_registration_product_information_custom_tags ON registration_product_information USING GIN(custom_tags);

-- 更新トリガーの作成
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER update_works_series_updated_at BEFORE UPDATE ON works_series
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_works_information_updated_at BEFORE UPDATE ON works_information
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_copyright_source_updated_at BEFORE UPDATE ON copyright_source
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_product_type_updated_at BEFORE UPDATE ON product_type
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_product_regulations_size_updated_at BEFORE UPDATE ON product_regulations_size
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_receipt_location_updated_at BEFORE UPDATE ON receipt_location
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_registration_product_information_updated_at BEFORE UPDATE ON registration_product_information
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
