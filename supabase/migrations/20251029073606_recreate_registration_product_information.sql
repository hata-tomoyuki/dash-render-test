-- Recreate registration_product_information table according to spec.md

-- Drop existing table
DROP TABLE IF EXISTS registration_product_information CASCADE;

-- Create new registration_product_information table according to spec.md
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
  flag_with_freebie INTEGER DEFAULT 0
);

-- Create indexes for better performance
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

-- Enable Row Level Security
ALTER TABLE registration_product_information ENABLE ROW LEVEL SECURITY;

-- Create policies
DROP POLICY IF EXISTS "Anyone can view registration_product_information" ON registration_product_information;
DROP POLICY IF EXISTS "Anyone can insert registration_product_information" ON registration_product_information;
DROP POLICY IF EXISTS "Anyone can update registration_product_information" ON registration_product_information;
DROP POLICY IF EXISTS "Anyone can delete registration_product_information" ON registration_product_information;

CREATE POLICY "Anyone can view registration_product_information" ON registration_product_information FOR SELECT TO public USING (true);
CREATE POLICY "Anyone can insert registration_product_information" ON registration_product_information FOR INSERT TO public WITH CHECK (true);
CREATE POLICY "Anyone can update registration_product_information" ON registration_product_information FOR UPDATE TO public USING (true) WITH CHECK (true);
CREATE POLICY "Anyone can delete registration_product_information" ON registration_product_information FOR DELETE TO public USING (true);

-- Create trigger for updated_at
DROP TRIGGER IF EXISTS update_registration_product_information_updated_at ON registration_product_information;
CREATE TRIGGER update_registration_product_information_updated_at BEFORE UPDATE ON registration_product_information FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
