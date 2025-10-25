/*
  # 写真管理アプリのデータベーススキーマ作成

  1. 新規テーブル
    - `photos`
      - `id` (uuid, primary key) - 写真レコードの一意識別子
      - `barcode` (text, not null) - バーコード情報
      - `barcode_type` (text) - バーコードの種類（EAN-13, QR Code等）
      - `image_url` (text, not null) - 写真のURL（Supabase Storageパス）
      - `description` (text) - 写真の説明（オプション）
      - `created_at` (timestamptz) - 作成日時
      - `updated_at` (timestamptz) - 更新日時

  2. セキュリティ
    - `photos`テーブルでRLSを有効化
    - 全ユーザーが読み取り可能（公開アプリとして）
    - 全ユーザーが挿入・更新・削除可能（認証なしアプリとして）

  3. インデックス
    - バーコードでの検索を高速化するためのインデックス
    - 作成日時でのソートを高速化するためのインデックス
*/

CREATE TABLE IF NOT EXISTS photos (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  barcode text NOT NULL,
  barcode_type text DEFAULT 'unknown',
  image_url text NOT NULL,
  description text DEFAULT '',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

ALTER TABLE photos ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can view photos"
  ON photos
  FOR SELECT
  TO public
  USING (true);

CREATE POLICY "Anyone can insert photos"
  ON photos
  FOR INSERT
  TO public
  WITH CHECK (true);

CREATE POLICY "Anyone can update photos"
  ON photos
  FOR UPDATE
  TO public
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Anyone can delete photos"
  ON photos
  FOR DELETE
  TO public
  USING (true);

CREATE INDEX IF NOT EXISTS idx_photos_barcode ON photos(barcode);
CREATE INDEX IF NOT EXISTS idx_photos_created_at ON photos(created_at DESC);

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_photos_updated_at BEFORE UPDATE ON photos
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();