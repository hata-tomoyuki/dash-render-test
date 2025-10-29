#!/usr/bin/env python3
"""
Supabaseデータベーステーブル作成スクリプト
"""

import os
from dotenv import load_dotenv
from services.supabase_client import get_supabase_client

load_dotenv()


def create_tables():
    """Supabaseにテーブルを作成"""
    print("🔧 Supabaseテーブル作成開始...")

    supabase = get_supabase_client()
    if supabase is None:
        print("❌ Supabase接続に失敗しました")
        return False

    sql_commands = [
        # 作品シリーズテーブル
        """
        CREATE TABLE IF NOT EXISTS works_series (
          works_series_id SERIAL PRIMARY KEY,
          works_series_name TEXT NOT NULL UNIQUE,
          created_at TIMESTAMPTZ DEFAULT NOW(),
          updated_at TIMESTAMPTZ DEFAULT NOW()
        );
        """,
        # 作品情報テーブル
        """
        CREATE TABLE IF NOT EXISTS works_information (
          works_id SERIAL PRIMARY KEY,
          title TEXT NOT NULL,
          works_series_id INTEGER REFERENCES works_series(works_series_id) ON DELETE SET NULL,
          created_at TIMESTAMPTZ DEFAULT NOW(),
          updated_at TIMESTAMPTZ DEFAULT NOW()
        );
        """,
        # 版權元テーブル
        """
        CREATE TABLE IF NOT EXISTS copyright_source (
          copyright_company_id SERIAL PRIMARY KEY,
          copyright_company_name TEXT NOT NULL UNIQUE,
          created_at TIMESTAMPTZ DEFAULT NOW(),
          updated_at TIMESTAMPTZ DEFAULT NOW()
        );
        """,
        # 製品種別テーブル
        """
        CREATE TABLE IF NOT EXISTS product_type (
          product_group_id SERIAL PRIMARY KEY,
          product_group_name TEXT NOT NULL UNIQUE,
          created_at TIMESTAMPTZ DEFAULT NOW(),
          updated_at TIMESTAMPTZ DEFAULT NOW()
        );
        """,
        # 製品規格サイズテーブル
        """
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
        """,
        # 収納場所テーブル
        """
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
        """,
        # 製品情報テーブル（拡張版）
        """
        CREATE TABLE IF NOT EXISTS products (
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
          additional_images TEXT[],

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
        """,
        # Row Level Securityの設定
        "ALTER TABLE works_series ENABLE ROW LEVEL SECURITY;",
        "ALTER TABLE works_information ENABLE ROW LEVEL SECURITY;",
        "ALTER TABLE copyright_source ENABLE ROW LEVEL SECURITY;",
        "ALTER TABLE product_type ENABLE ROW LEVEL SECURITY;",
        "ALTER TABLE product_regulations_size ENABLE ROW LEVEL SECURITY;",
        "ALTER TABLE receipt_location ENABLE ROW LEVEL SECURITY;",
        "ALTER TABLE products ENABLE ROW LEVEL SECURITY;",
        # RLSポリシー
        """
        CREATE POLICY "Anyone can view works_series" ON works_series
        FOR SELECT TO public USING (true);
        """,
        """
        CREATE POLICY "Anyone can insert works_series" ON works_series
        FOR INSERT TO public WITH CHECK (true);
        """,
        """
        CREATE POLICY "Anyone can update works_series" ON works_series
        FOR UPDATE TO public USING (true) WITH CHECK (true);
        """,
        """
        CREATE POLICY "Anyone can delete works_series" ON works_series
        FOR DELETE TO public USING (true);
        """,
        """
        CREATE POLICY "Anyone can view works_information" ON works_information
        FOR SELECT TO public USING (true);
        """,
        """
        CREATE POLICY "Anyone can insert works_information" ON works_information
        FOR INSERT TO public WITH CHECK (true);
        """,
        """
        CREATE POLICY "Anyone can update works_information" ON works_information
        FOR UPDATE TO public USING (true) WITH CHECK (true);
        """,
        """
        CREATE POLICY "Anyone can delete works_information" ON works_information
        FOR DELETE TO public USING (true);
        """,
        """
        CREATE POLICY "Anyone can view copyright_source" ON copyright_source
        FOR SELECT TO public USING (true);
        """,
        """
        CREATE POLICY "Anyone can insert copyright_source" ON copyright_source
        FOR INSERT TO public WITH CHECK (true);
        """,
        """
        CREATE POLICY "Anyone can update copyright_source" ON copyright_source
        FOR UPDATE TO public USING (true) WITH CHECK (true);
        """,
        """
        CREATE POLICY "Anyone can delete copyright_source" ON copyright_source
        FOR DELETE TO public USING (true);
        """,
        """
        CREATE POLICY "Anyone can view product_type" ON product_type
        FOR SELECT TO public USING (true);
        """,
        """
        CREATE POLICY "Anyone can insert product_type" ON product_type
        FOR INSERT TO public WITH CHECK (true);
        """,
        """
        CREATE POLICY "Anyone can update product_type" ON product_type
        FOR UPDATE TO public USING (true) WITH CHECK (true);
        """,
        """
        CREATE POLICY "Anyone can delete product_type" ON product_type
        FOR DELETE TO public USING (true);
        """,
        """
        CREATE POLICY "Anyone can view product_regulations_size" ON product_regulations_size
        FOR SELECT TO public USING (true);
        """,
        """
        CREATE POLICY "Anyone can insert product_regulations_size" ON product_regulations_size
        FOR INSERT TO public WITH CHECK (true);
        """,
        """
        CREATE POLICY "Anyone can update product_regulations_size" ON product_regulations_size
        FOR UPDATE TO public USING (true) WITH CHECK (true);
        """,
        """
        CREATE POLICY "Anyone can delete product_regulations_size" ON product_regulations_size
        FOR DELETE TO public USING (true);
        """,
        """
        CREATE POLICY "Anyone can view receipt_location" ON receipt_location
        FOR SELECT TO public USING (true);
        """,
        """
        CREATE POLICY "Anyone can insert receipt_location" ON receipt_location
        FOR INSERT TO public WITH CHECK (true);
        """,
        """
        CREATE POLICY "Anyone can update receipt_location" ON receipt_location
        FOR UPDATE TO public USING (true) WITH CHECK (true);
        """,
        """
        CREATE POLICY "Anyone can delete receipt_location" ON receipt_location
        FOR DELETE TO public USING (true);
        """,
        """
        CREATE POLICY "Anyone can view products" ON products
        FOR SELECT TO public USING (true);
        """,
        """
        CREATE POLICY "Anyone can insert products" ON products
        FOR INSERT TO public WITH CHECK (true);
        """,
        """
        CREATE POLICY "Anyone can update products" ON products
        FOR UPDATE TO public USING (true) WITH CHECK (true);
        """,
        """
        CREATE POLICY "Anyone can delete products" ON products
        FOR DELETE TO public USING (true);
        """,
        # インデックス
        "CREATE INDEX IF NOT EXISTS idx_works_series_name ON works_series(works_series_name);",
        "CREATE INDEX IF NOT EXISTS idx_works_information_title ON works_information(title);",
        "CREATE INDEX IF NOT EXISTS idx_works_information_series ON works_information(works_series_id);",
        "CREATE INDEX IF NOT EXISTS idx_copyright_source_name ON copyright_source(copyright_company_name);",
        "CREATE INDEX IF NOT EXISTS idx_product_type_name ON product_type(product_group_name);",
        "CREATE INDEX IF NOT EXISTS idx_product_regulations_size_group ON product_regulations_size(product_group_id);",
        "CREATE INDEX IF NOT EXISTS idx_receipt_location_name ON receipt_location(receipt_location_name);",
        "CREATE INDEX IF NOT EXISTS idx_products_barcode ON products(barcode);",
        "CREATE INDEX IF NOT EXISTS idx_products_works ON products(works_id);",
        "CREATE INDEX IF NOT EXISTS idx_products_copyright ON products(copyright_company_id);",
        "CREATE INDEX IF NOT EXISTS idx_products_type ON products(product_group_id);",
        "CREATE INDEX IF NOT EXISTS idx_products_size ON products(product_size_id);",
        "CREATE INDEX IF NOT EXISTS idx_products_location ON products(receipt_location_id);",
        "CREATE INDEX IF NOT EXISTS idx_products_created_at ON products(created_at DESC);",
        "CREATE INDEX IF NOT EXISTS idx_products_tags ON products USING GIN(tags);",
        "CREATE INDEX IF NOT EXISTS idx_products_custom_tags ON products USING GIN(custom_tags);",
        # 更新トリガー
        """
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE 'plpgsql';
        """,
        "CREATE TRIGGER update_works_series_updated_at BEFORE UPDATE ON works_series FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();",
        "CREATE TRIGGER update_works_information_updated_at BEFORE UPDATE ON works_information FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();",
        "CREATE TRIGGER update_copyright_source_updated_at BEFORE UPDATE ON copyright_source FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();",
        "CREATE TRIGGER update_product_type_updated_at BEFORE UPDATE ON product_type FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();",
        "CREATE TRIGGER update_product_regulations_size_updated_at BEFORE UPDATE ON product_regulations_size FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();",
        "CREATE TRIGGER update_receipt_location_updated_at BEFORE UPDATE ON receipt_location FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();",
        "CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON products FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();",
    ]

    success_count = 0
    for i, sql in enumerate(sql_commands, 1):
        sql = sql.strip()
        if not sql:
            continue

        try:
            print(f"📝 実行中... ({i}/{len(sql_commands)})")
            supabase.rpc("exec_sql", {"sql": sql}).execute()
            success_count += 1
        except Exception as exc:
            print(f"⚠️  SQL実行エラー: {str(exc)[:100]}...")
            # 一部のエラーは無視（既に存在する場合など）
            if "already exists" not in str(exc).lower():
                print(f"   SQL: {sql[:50]}...")

    print(f"✅ {success_count}/{len(sql_commands)} 個のSQL文を実行しました")
    return True


if __name__ == "__main__":
    success = create_tables()
    if success:
        print("\n🎉 データベーステーブル作成完了！")
        print("   写真の登録機能が利用可能です。")
    else:
        print("\n❌ テーブル作成に失敗しました。")
        print("   Supabaseダッシュボードで手動実行してください。")
