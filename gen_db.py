# -*- coding: utf-8 -*-
import json
import collections
from pathlib import Path

# 定数（Unicodeエスケープで記述し、環境依存の文字化けを防止）
HEADER_ROLE = "\u5f79\u5272"           # 役割
HEADER_JP_NAME = "\u540d\u79f0\u65e5\u672c\u8a9e"  # 名称日本語
HEADER_METHOD = "\u30e1\u30bd\u30c3\u30c9\u540d"   # メソッド名
HEADER_TYPE = "\u30c7\u30fc\u30bf\u578b"           # データ型
HEADER_KEY = "\u30ad\u30fc\u8a2d\u5b9a"           # キー設定
HEADER_NOTNULL = "NOT NULL"
HEADER_FK = "\u5916\u90e8\u30ad\u30fc\u53c2\u7167"  # 外部キー参照
ENTITY = "\u30a8\u30f3\u30c6\u30a3\u30c6\u30a3\u540d"  # エンティティ名
ATTRIBUTE = "\u5c5e\u6027"                        # 属性

# 名称日本語のマッピング（database_configuration.md にある分のみ）
ENTITY_JP = {
    "works_series": "作品シリーズ",
    "works_information": "作品情報",
    "copyright_source": "版権元",
    "product_type": "製品種別",
    "product_regulations_size": "製品規格サイズ",
    "receipt_location": "収納場所",
    "icon_tag": "アイコンタグ",
    "member_information": "会員情報",
    "member_type": "会員種別",
    "photo": "写真",
    "color_tag": "カラータグ",
    "category_tag": "カテゴリータグ",
    "registration_product_information": "登録製品情報",
    "currency_unit": "貨幣単位",
    "character": "キャラクター情報",
    "color": "色",
}

COLUMN_JP = {
    "works_series": {
        "works_series_id": "作品シリーズ ID",
        "works_series_name": "作品シリーズ名",
    },
    "works_information": {
        "works_id": "作品 ID",
        "title": "作品名",
        "works_series_id": "作品シリーズ ID",
    },
    "copyright_source": {
        "copyright_company_id": "版権会社 ID",
        "copyright_company_name": "版権会社名",
    },
    "product_type": {
        "product_group_id": "製品グループ ID",
        "product_group_name": "製品グループ名",
    },
    "product_regulations_size": {
        "product_size_id": "製品サイズ ID",
        "product_group_id": "製品グループ ID",
        "product_type": "製品の形",
        "product_size_horizontal": "製品サイズ横",
        "product_size_depth": "製品サイズ奥行",
        "product_size_vertical": "製品サイズ縦",
    },
    "receipt_location": {
        "receipt_location_id": "収納場所 ID",
        "receipt_location_name": "収納場所名",
        "receipt_location_size_horizontal": "収納場所サイズ横",
        "receipt_location_size_depth": "収納場所サイズ奥行",
        "receipt_location_size_vertical": "収納場所サイズ縦",
        "receipt_count_per_1": "1 個あたりの収納数",
        "receipt_size_horizontal_per_1": "1 個あたりの収納サイズ横",
        "receipt_size_depth_per_1": "1 個あたりの収納サイズ奥行",
        "receipt_size_vertical_per_1": "1 個あたりの収納サイズ縦",
        "receipt_location_icon": "収納場所アイコン",
        "receipt_location_use_flag": "収納場所使用フラグ",
    },
    "icon_tag": {
        "icon": "アイコン",
        "icon_name": "アイコン名",
        "category_tag_use_flag": "カテゴリータグ使用フラグ",
        "receipt_location_use_flag": "収納場所使用フラグ",
    },
    "member_information": {
        "members_id": "会員 ID",
        "members_type_name": "会員種別名",
        "user_name": "ユーザ名",
        "email_address": "メールアドレス",
        "x_id": "X_ID",
        "instagram_id": "インスタグラム ID",
        "line_id": "LINE_ID",
    },
    "member_type": {
        "members_type_name": "会員種別名",
        "thumbnail_image_quality": "サムネイル画質",
        "registerable_number": "登録可能枚数",
        "number_registerable_high_resolution": "高解像度登録可能枚数",
    },
    "photo": {
        "photo_id": "写真 ID",
        "photo_theme_color": "写真のテーマ色",
        "front_flag": "正面フラグ",
        "photo_thumbnail": "写真サムネイル",
        "photo_thumbnail_image_quality": "写真サムネイル画質",
        "photo_high_resolution_flag": "写真高解像度フラグ",
        "photo_edited_flag": "写真編集済フラグ",
        "photo_registration_date": "写真登録日",
        "photo_edit_date": "写真編集日",
        "photo_thumbnail_url": "写真サムネイル URL",
        "photo_high_resolution_url": "写真高解像度 URL",
    },
    "color_tag": {
        "color_tag_id": "カラータグ ID",
        "members_id": "会員 ID",
        "color_tag_color": "カラータグ色",
        "color_tag_name": "カラータグ名",
    },
    "category_tag": {
        "category_tag_id": "カテゴリータグ ID",
        "members_id": "会員 ID",
        "category_tag_color": "カテゴリータグ色",
        "category_tag_name": "カテゴリータグ名",
        "category_tag_icon": "カテゴリータグアイコン",
        "category_tag_use_flag": "カテゴリータグ使用フラグ",
    },
    "registration_product_information": {
        "registration_product_id": "登録製品 ID",
        "photo_id": "写真 ID",
        "works_series_id": "作品シリーズ ID",
        "works_id": "作品 ID",
        "character_id": "キャラクター ID",
        "copyright_company_id": "版権会社 ID",
        "product_group_id": "製品グループ ID",
        "product_size_id": "製品サイズ ID",
        "receipt_location_id": "収納場所 ID",
        "receipt_location_tag_id": "収納場所タグ ID",
        "color_tag_id": "カラータグ ID",
        "category_tag_id": "カテゴリータグ ID",
        "campaign_id": "キャンペーン ID",
        "currency_unit_id": "貨幣単位 ID",
        "works_series_name": "作品シリーズ名",
        "title": "作品名",
        "character_name": "キャラクター名",
        "copyright_company_name": "版権会社名",
        "product_type": "製品の形",
        "product_size_horizontal": "製品サイズ横",
        "product_size_depth": "製品サイズ奥行",
        "product_size_vertical": "製品サイズ縦",
        "barcode_number": "バーコード番号",
        "barcode_type": "バーコードタイプ",
        "product_name": "製品名",
        "list_price": "定価",
        "purchase_price": "購入価格",
        "registration_quantity": "登録数量",
        "sales_desired_quantity": "販売希望数量",
        "product_series_quantity": "製品シリーズ数量",
        "purchase_location": "購入場所",
        "freebie_name": "おまけ名",
        "purchase_date": "購入日",
        "creation_date": "作成日",
        "updated_date": "更新日",
        "other_tag": "その他タグ",
        "memo": "メモ",
        "product_series_flag": "製品シリーズフラグ",
        "product_series_complete_flag": "製品シリーズコンプリートフラグ",
        "commercial_product_flag": "商用製品フラグ",
        "personal_product_flag": "同人製品フラグ",
        "digital_product_flag": "デジタル製品フラグ",
        "sales_desired_flag": "販売希望フラグ",
        "want_object_flag": "欲しい物フラグ",
        "flag_with_freebie": "おまけ付きフラグ",
        "product_group_name": "製品グループ名",
    },
    "currency_unit": {
        "currency_unit_id": "貨幣単位 ID",
        "currency_name": "貨幣名",
    },
    "character": {
        "character_id": "キャラクター ID",
        "works_id": "作品 ID",
        "works_series_id": "作品シリーズ ID",
        "theme_color": "テーマ色",
        "hair_color": "髪色",
        "eye_color": "目の色",
        "character_name": "キャラクター名",
        "nickname": "愛称",
        "sex": "性別",
        "person_flag": "人フラグ",
        "animal_flag": "動物フラグ",
        "existing_flag": "実在フラグ",
        "foot_number": "足数",
        "height": "身長",
        "weight": "体重",
        "birthday": "誕生日",
        "debut_date": "デビュー日",
        "age": "年齢",
        "student_flag": "学生フラグ",
    },
    "color": {
        "color_group_id": "色グループ ID",
        "color_group_name": "色グループ名",
        "color_preference": "色設定",
    },
}

# スキーマ情報の読み込み
with open('schema_info.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

cols = data['columns']
keys = data['keys']
fks = data['fks']

# 列情報をテーブル単位にまとめる
columns_by_table = collections.OrderedDict()
for schema, table, col, dtype, nullable, default, udt, charlen, numprec, numscale in cols:
    key = (schema, table)
    columns_by_table.setdefault(key, []).append(
        {
            'column': col,
            'data_type': dtype,
            'udt': udt,
            'nullable': nullable == 'YES',
            'default': default,
            'charlen': charlen,
            'numprec': numprec,
            'numscale': numscale,
        }
    )

# 主キーと外部キーの対応を準備
pk_by_table = collections.defaultdict(set)
fk_by_col = {}
for schema, table, col, ctype, cname in keys:
    if ctype == 'PRIMARY KEY':
        pk_by_table[(schema, table)].add(col)
for schema, table, col, f_schema, f_table, f_col, cname in fks:
    fk_by_col[(schema, table, col)] = (f_schema, f_table, f_col)

# Markdown生成
lines = []
for (schema, table), cols in columns_by_table.items():
    lines.append(f"## {schema}.{table}")
    lines.append("")
    lines.append(f"| {HEADER_ROLE} | {HEADER_JP_NAME} | {HEADER_METHOD} | {HEADER_TYPE} | {HEADER_KEY} | {HEADER_NOTNULL} | {HEADER_FK} |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    jp_entity = ENTITY_JP.get(table, "")
    lines.append(f"| {ENTITY} | {jp_entity} | {table} | - |  |  |  |")
    for c in cols:
        col = c['column']
        dtype = c['data_type']
        extra = []
        if c['charlen']:
            extra.append(f"len={c['charlen']}")
        if c['numprec']:
            extra.append(f"prec={c['numprec']}")
        if c['numscale']:
            extra.append(f"scale={c['numscale']}")
        detail = f" ({', '.join(extra)})" if extra else ""
        dt = f"{dtype}{detail}" if detail else dtype
        key_setting = []
        if col in pk_by_table[(schema, table)]:
            key_setting.append("Primary Key")
        if (schema, table, col) in fk_by_col:
            key_setting.append("Foreign Key")
        key_setting = ", ".join(key_setting)
        notnull = "YES" if not c['nullable'] else ""
        fkref = ""
        if (schema, table, col) in fk_by_col:
            f_schema, f_table, f_col = fk_by_col[(schema, table, col)]
            fkref = f"{f_schema}.{f_table}.{f_col}"
        jp_col = COLUMN_JP.get(table, {}).get(col, "")
        lines.append(f"| {ATTRIBUTE} | {jp_col} | {col} | {dt} | {key_setting} | {notnull} | {fkref} |")
    lines.append("")

Path('database.md').write_text("\n".join(lines), encoding='utf-8')
print("wrote database.md", len(columns_by_table))

