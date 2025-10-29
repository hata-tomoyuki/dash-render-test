-- Step 3: Add missing columns to registration_product_information table

-- Add missing columns based on spec.md
ALTER TABLE registration_product_information
ADD COLUMN IF NOT EXISTS registration_quantity INTEGER DEFAULT 1,
ADD COLUMN IF NOT EXISTS list_price INTEGER,
ADD COLUMN IF NOT EXISTS purchase_price INTEGER,
ADD COLUMN IF NOT EXISTS sales_desired_quantity INTEGER,
ADD COLUMN IF NOT EXISTS product_series_quantity INTEGER,
ADD COLUMN IF NOT EXISTS purchase_location TEXT,
ADD COLUMN IF NOT EXISTS freebie_name TEXT,
ADD COLUMN IF NOT EXISTS purchase_date DATE,
ADD COLUMN IF NOT EXISTS other_tag TEXT[],
ADD COLUMN IF NOT EXISTS memo TEXT,
ADD COLUMN IF NOT EXISTS product_series_flag INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS commercial_product_flag INTEGER DEFAULT 1,
ADD COLUMN IF NOT EXISTS personal_product_flag INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS digital_product_flag INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS sales_desired_flag INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS want_object_flag INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS flag_with_freebie INTEGER DEFAULT 0;
