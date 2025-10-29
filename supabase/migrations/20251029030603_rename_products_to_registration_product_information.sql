-- Rename products table to registration_product_information
-- This migration renames the products table to match the new naming convention

-- Rename the table
ALTER TABLE products RENAME TO registration_product_information;

-- Rename the primary key constraint
ALTER TABLE registration_product_information RENAME CONSTRAINT products_pkey TO registration_product_information_pkey;

-- Rename indexes
ALTER INDEX IF EXISTS idx_products_barcode RENAME TO idx_registration_product_information_barcode;
ALTER INDEX IF EXISTS idx_products_works RENAME TO idx_registration_product_information_works;
ALTER INDEX IF EXISTS idx_products_copyright RENAME TO idx_registration_product_information_copyright;
ALTER INDEX IF EXISTS idx_products_type RENAME TO idx_registration_product_information_type;
ALTER INDEX IF EXISTS idx_products_size RENAME TO idx_registration_product_information_size;
ALTER INDEX IF EXISTS idx_products_location RENAME TO idx_registration_product_information_location;
ALTER INDEX IF EXISTS idx_products_created_at RENAME TO idx_registration_product_information_created_at;
ALTER INDEX IF EXISTS idx_products_tags RENAME TO idx_registration_product_information_tags;
ALTER INDEX IF EXISTS idx_products_custom_tags RENAME TO idx_registration_product_information_custom_tags;

-- Rename policies
ALTER POLICY "Anyone can view products" ON registration_product_information RENAME TO "Anyone can view registration_product_information";
ALTER POLICY "Anyone can insert products" ON registration_product_information RENAME TO "Anyone can insert registration_product_information";
ALTER POLICY "Anyone can update products" ON registration_product_information RENAME TO "Anyone can update registration_product_information";
ALTER POLICY "Anyone can delete products" ON registration_product_information RENAME TO "Anyone can delete registration_product_information";

-- Rename trigger
ALTER TRIGGER update_products_updated_at ON registration_product_information RENAME TO update_registration_product_information_updated_at;
