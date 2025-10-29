-- Step 4: Setup RLS, indexes and triggers

-- Enable Row Level Security for all new tables
ALTER TABLE color ENABLE ROW LEVEL SECURITY;
ALTER TABLE works_information ENABLE ROW LEVEL SECURITY;
ALTER TABLE copyright_source ENABLE ROW LEVEL SECURITY;
ALTER TABLE product_type ENABLE ROW LEVEL SECURITY;
ALTER TABLE product_regulations_size ENABLE ROW LEVEL SECURITY;
ALTER TABLE receipt_location ENABLE ROW LEVEL SECURITY;
ALTER TABLE member_type ENABLE ROW LEVEL SECURITY;
ALTER TABLE member_information ENABLE ROW LEVEL SECURITY;
ALTER TABLE photo ENABLE ROW LEVEL SECURITY;
ALTER TABLE character ENABLE ROW LEVEL SECURITY;
ALTER TABLE color_tag ENABLE ROW LEVEL SECURITY;
ALTER TABLE category_tag ENABLE ROW LEVEL SECURITY;
ALTER TABLE currency_unit ENABLE ROW LEVEL SECURITY;

-- Create policies for all tables (allow all operations for now)
CREATE POLICY "Allow all operations on color" ON color FOR ALL TO public USING (true) WITH CHECK (true);
CREATE POLICY "Allow all operations on works_information" ON works_information FOR ALL TO public USING (true) WITH CHECK (true);
CREATE POLICY "Allow all operations on copyright_source" ON copyright_source FOR ALL TO public USING (true) WITH CHECK (true);
CREATE POLICY "Allow all operations on product_type" ON product_type FOR ALL TO public USING (true) WITH CHECK (true);
CREATE POLICY "Allow all operations on product_regulations_size" ON product_regulations_size FOR ALL TO public USING (true) WITH CHECK (true);
CREATE POLICY "Allow all operations on receipt_location" ON receipt_location FOR ALL TO public USING (true) WITH CHECK (true);
CREATE POLICY "Allow all operations on member_type" ON member_type FOR ALL TO public USING (true) WITH CHECK (true);
CREATE POLICY "Allow all operations on member_information" ON member_information FOR ALL TO public USING (true) WITH CHECK (true);
CREATE POLICY "Allow all operations on photo" ON photo FOR ALL TO public USING (true) WITH CHECK (true);
CREATE POLICY "Allow all operations on character" ON character FOR ALL TO public USING (true) WITH CHECK (true);
CREATE POLICY "Allow all operations on color_tag" ON color_tag FOR ALL TO public USING (true) WITH CHECK (true);
CREATE POLICY "Allow all operations on category_tag" ON category_tag FOR ALL TO public USING (true) WITH CHECK (true);
CREATE POLICY "Allow all operations on currency_unit" ON currency_unit FOR ALL TO public USING (true) WITH CHECK (true);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_character_works ON character(works_id);
CREATE INDEX IF NOT EXISTS idx_character_works_series ON character(works_series_id);
CREATE INDEX IF NOT EXISTS idx_member_info_type ON member_information(members_type_name);
CREATE INDEX IF NOT EXISTS idx_photo_theme_color ON photo(photo_theme_color);
CREATE INDEX IF NOT EXISTS idx_color_tag_member ON color_tag(members_id);
CREATE INDEX IF NOT EXISTS idx_category_tag_member ON category_tag(members_id);

-- Create updated_at triggers for all tables
CREATE TRIGGER update_color_updated_at BEFORE UPDATE ON color FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_works_information_updated_at BEFORE UPDATE ON works_information FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_copyright_source_updated_at BEFORE UPDATE ON copyright_source FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_product_type_updated_at BEFORE UPDATE ON product_type FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_product_regulations_size_updated_at BEFORE UPDATE ON product_regulations_size FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_receipt_location_updated_at BEFORE UPDATE ON receipt_location FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_member_type_updated_at BEFORE UPDATE ON member_type FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_member_information_updated_at BEFORE UPDATE ON member_information FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_photo_updated_at BEFORE UPDATE ON photo FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_character_updated_at BEFORE UPDATE ON character FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_color_tag_updated_at BEFORE UPDATE ON color_tag FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_category_tag_updated_at BEFORE UPDATE ON category_tag FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_currency_unit_updated_at BEFORE UPDATE ON currency_unit FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
