-- Create icon_tag table for centralized icon management

CREATE TABLE IF NOT EXISTS icon_tag (
  icon TEXT PRIMARY KEY,
  icon_name TEXT NOT NULL,
  category_tag_use_flag INTEGER DEFAULT 1,
  receipt_location_use_flag INTEGER DEFAULT 1
);

-- Enable Row Level Security
ALTER TABLE icon_tag ENABLE ROW LEVEL SECURITY;

-- Create policies
DROP POLICY IF EXISTS "Anyone can view icon_tag" ON icon_tag;
DROP POLICY IF EXISTS "Anyone can insert icon_tag" ON icon_tag;
DROP POLICY IF EXISTS "Anyone can update icon_tag" ON icon_tag;
DROP POLICY IF EXISTS "Anyone can delete icon_tag" ON icon_tag;

CREATE POLICY "Anyone can view icon_tag" ON icon_tag FOR SELECT TO public USING (true);
CREATE POLICY "Anyone can insert icon_tag" ON icon_tag FOR INSERT TO public WITH CHECK (true);
CREATE POLICY "Anyone can update icon_tag" ON icon_tag FOR UPDATE TO public USING (true) WITH CHECK (true);
CREATE POLICY "Anyone can delete icon_tag" ON icon_tag FOR DELETE TO public USING (true);
