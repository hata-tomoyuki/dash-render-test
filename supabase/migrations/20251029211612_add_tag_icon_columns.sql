-- Add icon and use_flag columns to tag tables

-- Add columns to category_tag table
ALTER TABLE category_tag
ADD COLUMN IF NOT EXISTS category_tag_icon TEXT,
ADD COLUMN IF NOT EXISTS category_tag_use_flag INTEGER DEFAULT 1;

-- Add columns to receipt_location table
ALTER TABLE receipt_location
ADD COLUMN IF NOT EXISTS receipt_location_icon TEXT,
ADD COLUMN IF NOT EXISTS receipt_location_use_flag INTEGER DEFAULT 1;
