## auth.audit_log_entries

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 |  | audit_log_entries | - |  |  |  |
| 属性 |  | instance_id | uuid |  |  |  |
| 属性 |  | id | uuid | Primary Key | YES |  |
| 属性 |  | payload | json |  |  |  |
| 属性 |  | created_at | timestamp with time zone |  |  |  |
| 属性 |  | ip_address | character varying (len=64) |  | YES |  |

## auth.flow_state

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 |  | flow_state | - |  |  |  |
| 属性 |  | id | uuid | Primary Key | YES |  |
| 属性 |  | user_id | uuid |  |  |  |
| 属性 |  | auth_code | text |  | YES |  |
| 属性 |  | code_challenge_method | USER-DEFINED |  | YES |  |
| 属性 |  | code_challenge | text |  | YES |  |
| 属性 |  | provider_type | text |  | YES |  |
| 属性 |  | provider_access_token | text |  |  |  |
| 属性 |  | provider_refresh_token | text |  |  |  |
| 属性 |  | created_at | timestamp with time zone |  |  |  |
| 属性 |  | updated_at | timestamp with time zone |  |  |  |
| 属性 |  | authentication_method | text |  | YES |  |
| 属性 |  | auth_code_issued_at | timestamp with time zone |  |  |  |

## auth.identities

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 |  | identities | - |  |  |  |
| 属性 |  | provider_id | text |  | YES |  |
| 属性 |  | user_id | uuid |  | YES |  |
| 属性 |  | identity_data | jsonb |  | YES |  |
| 属性 |  | provider | text |  | YES |  |
| 属性 |  | last_sign_in_at | timestamp with time zone |  |  |  |
| 属性 |  | created_at | timestamp with time zone |  |  |  |
| 属性 |  | updated_at | timestamp with time zone |  |  |  |
| 属性 |  | email | text |  |  |  |
| 属性 |  | id | uuid | Primary Key | YES |  |

## auth.instances

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 |  | instances | - |  |  |  |
| 属性 |  | id | uuid | Primary Key | YES |  |
| 属性 |  | uuid | uuid |  |  |  |
| 属性 |  | raw_base_config | text |  |  |  |
| 属性 |  | created_at | timestamp with time zone |  |  |  |
| 属性 |  | updated_at | timestamp with time zone |  |  |  |

## auth.mfa_amr_claims

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 |  | mfa_amr_claims | - |  |  |  |
| 属性 |  | session_id | uuid |  | YES |  |
| 属性 |  | created_at | timestamp with time zone |  | YES |  |
| 属性 |  | updated_at | timestamp with time zone |  | YES |  |
| 属性 |  | authentication_method | text |  | YES |  |
| 属性 |  | id | uuid | Primary Key | YES |  |

## auth.mfa_challenges

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 |  | mfa_challenges | - |  |  |  |
| 属性 |  | id | uuid | Primary Key | YES |  |
| 属性 |  | factor_id | uuid |  | YES |  |
| 属性 |  | created_at | timestamp with time zone |  | YES |  |
| 属性 |  | verified_at | timestamp with time zone |  |  |  |
| 属性 |  | ip_address | inet |  | YES |  |
| 属性 |  | otp_code | text |  |  |  |
| 属性 |  | web_authn_session_data | jsonb |  |  |  |

## auth.mfa_factors

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 |  | mfa_factors | - |  |  |  |
| 属性 |  | id | uuid | Primary Key | YES |  |
| 属性 |  | user_id | uuid |  | YES |  |
| 属性 |  | friendly_name | text |  |  |  |
| 属性 |  | factor_type | USER-DEFINED |  | YES |  |
| 属性 |  | status | USER-DEFINED |  | YES |  |
| 属性 |  | created_at | timestamp with time zone |  | YES |  |
| 属性 |  | updated_at | timestamp with time zone |  | YES |  |
| 属性 |  | secret | text |  |  |  |
| 属性 |  | phone | text |  |  |  |
| 属性 |  | last_challenged_at | timestamp with time zone |  |  |  |
| 属性 |  | web_authn_credential | jsonb |  |  |  |
| 属性 |  | web_authn_aaguid | uuid |  |  |  |
| 属性 |  | last_webauthn_challenge_data | jsonb |  |  |  |

## auth.oauth_authorizations

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 |  | oauth_authorizations | - |  |  |  |
| 属性 |  | id | uuid | Primary Key | YES |  |
| 属性 |  | authorization_id | text |  | YES |  |
| 属性 |  | client_id | uuid |  | YES |  |
| 属性 |  | user_id | uuid |  |  |  |
| 属性 |  | redirect_uri | text |  | YES |  |
| 属性 |  | scope | text |  | YES |  |
| 属性 |  | state | text |  |  |  |
| 属性 |  | resource | text |  |  |  |
| 属性 |  | code_challenge | text |  |  |  |
| 属性 |  | code_challenge_method | USER-DEFINED |  |  |  |
| 属性 |  | response_type | USER-DEFINED |  | YES |  |
| 属性 |  | status | USER-DEFINED |  | YES |  |
| 属性 |  | authorization_code | text |  |  |  |
| 属性 |  | created_at | timestamp with time zone |  | YES |  |
| 属性 |  | expires_at | timestamp with time zone |  | YES |  |
| 属性 |  | approved_at | timestamp with time zone |  |  |  |
| 属性 |  | nonce | text |  |  |  |

## auth.oauth_client_states

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 |  | oauth_client_states | - |  |  |  |
| 属性 |  | id | uuid | Primary Key | YES |  |
| 属性 |  | provider_type | text |  | YES |  |
| 属性 |  | code_verifier | text |  |  |  |
| 属性 |  | created_at | timestamp with time zone |  | YES |  |

## auth.oauth_clients

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 |  | oauth_clients | - |  |  |  |
| 属性 |  | id | uuid | Primary Key | YES |  |
| 属性 |  | client_secret_hash | text |  |  |  |
| 属性 |  | registration_type | USER-DEFINED |  | YES |  |
| 属性 |  | redirect_uris | text |  | YES |  |
| 属性 |  | grant_types | text |  | YES |  |
| 属性 |  | client_name | text |  |  |  |
| 属性 |  | client_uri | text |  |  |  |
| 属性 |  | logo_uri | text |  |  |  |
| 属性 |  | created_at | timestamp with time zone |  | YES |  |
| 属性 |  | updated_at | timestamp with time zone |  | YES |  |
| 属性 |  | deleted_at | timestamp with time zone |  |  |  |
| 属性 |  | client_type | USER-DEFINED |  | YES |  |

## auth.oauth_consents

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 |  | oauth_consents | - |  |  |  |
| 属性 |  | id | uuid | Primary Key | YES |  |
| 属性 |  | user_id | uuid |  | YES |  |
| 属性 |  | client_id | uuid |  | YES |  |
| 属性 |  | scopes | text |  | YES |  |
| 属性 |  | granted_at | timestamp with time zone |  | YES |  |
| 属性 |  | revoked_at | timestamp with time zone |  |  |  |

## auth.one_time_tokens

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 |  | one_time_tokens | - |  |  |  |
| 属性 |  | id | uuid | Primary Key | YES |  |
| 属性 |  | user_id | uuid |  | YES |  |
| 属性 |  | token_type | USER-DEFINED |  | YES |  |
| 属性 |  | token_hash | text |  | YES |  |
| 属性 |  | relates_to | text |  | YES |  |
| 属性 |  | created_at | timestamp without time zone |  | YES |  |
| 属性 |  | updated_at | timestamp without time zone |  | YES |  |

## auth.refresh_tokens

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 |  | refresh_tokens | - |  |  |  |
| 属性 |  | instance_id | uuid |  |  |  |
| 属性 |  | id | bigint (prec=64) | Primary Key | YES |  |
| 属性 |  | token | character varying (len=255) |  |  |  |
| 属性 |  | user_id | character varying (len=255) |  |  |  |
| 属性 |  | revoked | boolean |  |  |  |
| 属性 |  | created_at | timestamp with time zone |  |  |  |
| 属性 |  | updated_at | timestamp with time zone |  |  |  |
| 属性 |  | parent | character varying (len=255) |  |  |  |
| 属性 |  | session_id | uuid |  |  |  |

## auth.saml_providers

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 |  | saml_providers | - |  |  |  |
| 属性 |  | id | uuid | Primary Key | YES |  |
| 属性 |  | sso_provider_id | uuid |  | YES |  |
| 属性 |  | entity_id | text |  | YES |  |
| 属性 |  | metadata_xml | text |  | YES |  |
| 属性 |  | metadata_url | text |  |  |  |
| 属性 |  | attribute_mapping | jsonb |  |  |  |
| 属性 |  | created_at | timestamp with time zone |  |  |  |
| 属性 |  | updated_at | timestamp with time zone |  |  |  |
| 属性 |  | name_id_format | text |  |  |  |

## auth.saml_relay_states

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 |  | saml_relay_states | - |  |  |  |
| 属性 |  | id | uuid | Primary Key | YES |  |
| 属性 |  | sso_provider_id | uuid |  | YES |  |
| 属性 |  | request_id | text |  | YES |  |
| 属性 |  | for_email | text |  |  |  |
| 属性 |  | redirect_to | text |  |  |  |
| 属性 |  | created_at | timestamp with time zone |  |  |  |
| 属性 |  | updated_at | timestamp with time zone |  |  |  |
| 属性 |  | flow_state_id | uuid |  |  |  |

## auth.schema_migrations

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 |  | schema_migrations | - |  |  |  |
| 属性 |  | version | character varying (len=255) |  | YES |  |

## auth.sessions

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 |  | sessions | - |  |  |  |
| 属性 |  | id | uuid | Primary Key | YES |  |
| 属性 |  | user_id | uuid |  | YES |  |
| 属性 |  | created_at | timestamp with time zone |  |  |  |
| 属性 |  | updated_at | timestamp with time zone |  |  |  |
| 属性 |  | factor_id | uuid |  |  |  |
| 属性 |  | aal | USER-DEFINED |  |  |  |
| 属性 |  | not_after | timestamp with time zone |  |  |  |
| 属性 |  | refreshed_at | timestamp without time zone |  |  |  |
| 属性 |  | user_agent | text |  |  |  |
| 属性 |  | ip | inet |  |  |  |
| 属性 |  | tag | text |  |  |  |
| 属性 |  | oauth_client_id | uuid |  |  |  |
| 属性 |  | refresh_token_hmac_key | text |  |  |  |
| 属性 |  | refresh_token_counter | bigint (prec=64) |  |  |  |
| 属性 |  | scopes | text |  |  |  |

## auth.sso_domains

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 |  | sso_domains | - |  |  |  |
| 属性 |  | id | uuid | Primary Key | YES |  |
| 属性 |  | sso_provider_id | uuid |  | YES |  |
| 属性 |  | domain | text |  | YES |  |
| 属性 |  | created_at | timestamp with time zone |  |  |  |
| 属性 |  | updated_at | timestamp with time zone |  |  |  |

## auth.sso_providers

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 |  | sso_providers | - |  |  |  |
| 属性 |  | id | uuid | Primary Key | YES |  |
| 属性 |  | resource_id | text |  |  |  |
| 属性 |  | created_at | timestamp with time zone |  |  |  |
| 属性 |  | updated_at | timestamp with time zone |  |  |  |
| 属性 |  | disabled | boolean |  |  |  |

## auth.users

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 |  | users | - |  |  |  |
| 属性 |  | instance_id | uuid |  |  |  |
| 属性 |  | id | uuid | Primary Key | YES |  |
| 属性 |  | aud | character varying (len=255) |  |  |  |
| 属性 |  | role | character varying (len=255) |  |  |  |
| 属性 |  | email | character varying (len=255) |  |  |  |
| 属性 |  | encrypted_password | character varying (len=255) |  |  |  |
| 属性 |  | email_confirmed_at | timestamp with time zone |  |  |  |
| 属性 |  | invited_at | timestamp with time zone |  |  |  |
| 属性 |  | confirmation_token | character varying (len=255) |  |  |  |
| 属性 |  | confirmation_sent_at | timestamp with time zone |  |  |  |
| 属性 |  | recovery_token | character varying (len=255) |  |  |  |
| 属性 |  | recovery_sent_at | timestamp with time zone |  |  |  |
| 属性 |  | email_change_token_new | character varying (len=255) |  |  |  |
| 属性 |  | email_change | character varying (len=255) |  |  |  |
| 属性 |  | email_change_sent_at | timestamp with time zone |  |  |  |
| 属性 |  | last_sign_in_at | timestamp with time zone |  |  |  |
| 属性 |  | raw_app_meta_data | jsonb |  |  |  |
| 属性 |  | raw_user_meta_data | jsonb |  |  |  |
| 属性 |  | is_super_admin | boolean |  |  |  |
| 属性 |  | created_at | timestamp with time zone |  |  |  |
| 属性 |  | updated_at | timestamp with time zone |  |  |  |
| 属性 |  | phone | text |  |  |  |
| 属性 |  | phone_confirmed_at | timestamp with time zone |  |  |  |
| 属性 |  | phone_change | text |  |  |  |
| 属性 |  | phone_change_token | character varying (len=255) |  |  |  |
| 属性 |  | phone_change_sent_at | timestamp with time zone |  |  |  |
| 属性 |  | confirmed_at | timestamp with time zone |  |  |  |
| 属性 |  | email_change_token_current | character varying (len=255) |  |  |  |
| 属性 |  | email_change_confirm_status | smallint (prec=16) |  |  |  |
| 属性 |  | banned_until | timestamp with time zone |  |  |  |
| 属性 |  | reauthentication_token | character varying (len=255) |  |  |  |
| 属性 |  | reauthentication_sent_at | timestamp with time zone |  |  |  |
| 属性 |  | is_sso_user | boolean |  | YES |  |
| 属性 |  | deleted_at | timestamp with time zone |  |  |  |
| 属性 |  | is_anonymous | boolean |  | YES |  |

## public.category_tag

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 | カテゴリータグ | category_tag | - |  |  |  |
| 属性 | カテゴリータグ ID | category_tag_id | integer (prec=32) | Primary Key | YES |  |
| 属性 | 会員 ID | members_id | integer (prec=32) | Foreign Key |  | public.member_information.members_id |
| 属性 | カテゴリータグ色 | category_tag_color | text |  |  |  |
| 属性 | カテゴリータグ名 | category_tag_name | text |  | YES |  |
| 属性 |  | created_at | timestamp with time zone |  |  |  |
| 属性 |  | updated_at | timestamp with time zone |  |  |  |
| 属性 | カテゴリータグアイコン | category_tag_icon | text |  |  |  |
| 属性 | カテゴリータグ使用フラグ | category_tag_use_flag | integer (prec=32) |  |  |  |

## public.character

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 | キャラクター情報 | character | - |  |  |  |
| 属性 | キャラクター ID | character_id | integer (prec=32) | Primary Key | YES |  |
| 属性 | 作品 ID | works_id | integer (prec=32) | Foreign Key |  | public.works_information.works_id |
| 属性 | 作品シリーズ ID | works_series_id | integer (prec=32) | Foreign Key |  | public.works_series.works_series_id |
| 属性 | テーマ色 | theme_color | integer (prec=32) | Foreign Key |  | public.color.color_group_id |
| 属性 | 髪色 | hair_color | integer (prec=32) | Foreign Key |  | public.color.color_group_id |
| 属性 | 目の色 | eye_color | integer (prec=32) | Foreign Key |  | public.color.color_group_id |
| 属性 | キャラクター名 | character_name | text |  |  |  |
| 属性 | 愛称 | nickname | text |  |  |  |
| 属性 | 性別 | sex | text |  |  |  |
| 属性 | 人フラグ | person_flag | integer (prec=32) |  |  |  |
| 属性 | 動物フラグ | animal_flag | integer (prec=32) |  |  |  |
| 属性 | 実在フラグ | existing_flag | integer (prec=32) |  |  |  |
| 属性 | 足数 | foot_number | integer (prec=32) |  |  |  |
| 属性 | 身長 | height | integer (prec=32) |  |  |  |
| 属性 | 体重 | weight | integer (prec=32) |  |  |  |
| 属性 | 誕生日 | birthday | date |  |  |  |
| 属性 | デビュー日 | debut_date | date |  |  |  |
| 属性 | 年齢 | age | integer (prec=32) |  |  |  |
| 属性 | 学生フラグ | student_flag | integer (prec=32) |  |  |  |
| 属性 |  | created_at | timestamp with time zone |  |  |  |
| 属性 |  | updated_at | timestamp with time zone |  |  |  |

## public.color

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 | 色 | color | - |  |  |  |
| 属性 | 色グループ ID | color_group_id | integer (prec=32) | Primary Key | YES |  |
| 属性 | 色グループ名 | color_group_name | text |  | YES |  |
| 属性 | 色設定 | color_preference | text |  |  |  |
| 属性 |  | created_at | timestamp with time zone |  |  |  |
| 属性 |  | updated_at | timestamp with time zone |  |  |  |

## public.color_tag

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 | カラータグ | color_tag | - |  |  |  |
| 属性 | カラータグ ID | color_tag_id | integer (prec=32) | Primary Key | YES |  |
| 属性 | 会員 ID | members_id | integer (prec=32) | Foreign Key |  | public.member_information.members_id |
| 属性 | カラータグ色 | color_tag_color | text |  |  |  |
| 属性 | カラータグ名 | color_tag_name | text |  | YES |  |
| 属性 |  | created_at | timestamp with time zone |  |  |  |
| 属性 |  | updated_at | timestamp with time zone |  |  |  |

## public.copyright_source

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 | 版権元 | copyright_source | - |  |  |  |
| 属性 | 版権会社 ID | copyright_company_id | integer (prec=32) | Primary Key | YES |  |
| 属性 | 版権会社名 | copyright_company_name | text |  | YES |  |
| 属性 |  | created_at | timestamp with time zone |  |  |  |
| 属性 |  | updated_at | timestamp with time zone |  |  |  |

## public.currency_unit

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 | 貨幣単位 | currency_unit | - |  |  |  |
| 属性 | 貨幣単位 ID | currency_unit_id | integer (prec=32) | Primary Key | YES |  |
| 属性 | 貨幣名 | currency_name | text |  | YES |  |
| 属性 |  | created_at | timestamp with time zone |  |  |  |
| 属性 |  | updated_at | timestamp with time zone |  |  |  |

## public.icon_tag

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 | アイコンタグ | icon_tag | - |  |  |  |
| 属性 | アイコン | icon | text | Primary Key | YES |  |
| 属性 | アイコン名 | icon_name | text |  | YES |  |
| 属性 | カテゴリータグ使用フラグ | category_tag_use_flag | integer (prec=32) |  |  |  |
| 属性 | 収納場所使用フラグ | receipt_location_use_flag | integer (prec=32) |  |  |  |

## public.member_information

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 | 会員情報 | member_information | - |  |  |  |
| 属性 | 会員 ID | members_id | integer (prec=32) | Primary Key | YES |  |
| 属性 | 会員種別名 | members_type_name | text | Foreign Key |  | public.member_type.members_type_name |
| 属性 | ユーザ名 | user_name | text |  |  |  |
| 属性 | メールアドレス | email_address | text |  |  |  |
| 属性 | X_ID | x_id | text |  |  |  |
| 属性 | インスタグラム ID | instagram_id | text |  |  |  |
| 属性 | LINE_ID | line_id | text |  |  |  |
| 属性 |  | created_at | timestamp with time zone |  |  |  |
| 属性 |  | updated_at | timestamp with time zone |  |  |  |

## public.member_type

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 | 会員種別 | member_type | - |  |  |  |
| 属性 | 会員種別名 | members_type_name | text | Primary Key | YES |  |
| 属性 | サムネイル画質 | thumbnail_image_quality | integer (prec=32) |  |  |  |
| 属性 | 登録可能枚数 | registerable_number | integer (prec=32) |  |  |  |
| 属性 | 高解像度登録可能枚数 | number_registerable_high_resolution | integer (prec=32) |  |  |  |
| 属性 |  | created_at | timestamp with time zone |  |  |  |
| 属性 |  | updated_at | timestamp with time zone |  |  |  |

## public.photo

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 | 写真 | photo | - |  |  |  |
| 属性 | 写真 ID | photo_id | integer (prec=32) | Primary Key | YES |  |
| 属性 | 写真のテーマ色 | photo_theme_color | integer (prec=32) | Foreign Key |  | public.color.color_group_id |
| 属性 | 正面フラグ | front_flag | integer (prec=32) |  |  |  |
| 属性 | 写真サムネイル | photo_thumbnail | bytea |  |  |  |
| 属性 | 写真サムネイル画質 | photo_thumbnail_image_quality | integer (prec=32) |  |  |  |
| 属性 | 写真高解像度フラグ | photo_high_resolution_flag | integer (prec=32) |  |  |  |
| 属性 | 写真編集済フラグ | photo_edited_flag | integer (prec=32) |  |  |  |
| 属性 | 写真登録日 | photo_registration_date | timestamp with time zone |  |  |  |
| 属性 | 写真編集日 | photo_edit_date | timestamp with time zone |  |  |  |
| 属性 | 写真サムネイル URL | photo_thumbnail_url | text |  |  |  |
| 属性 | 写真高解像度 URL | photo_high_resolution_url | text |  |  |  |
| 属性 |  | created_at | timestamp with time zone |  |  |  |
| 属性 |  | updated_at | timestamp with time zone |  |  |  |

## public.product_regulations_size

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 | 製品規格サイズ | product_regulations_size | - |  |  |  |
| 属性 | 製品サイズ ID | product_size_id | integer (prec=32) | Primary Key | YES |  |
| 属性 | 製品グループ ID | product_group_id | integer (prec=32) | Foreign Key |  | public.product_type.product_group_id |
| 属性 | 製品の形 | product_type | text |  | YES |  |
| 属性 | 製品サイズ横 | product_size_horizontal | integer (prec=32) |  |  |  |
| 属性 | 製品サイズ奥行 | product_size_depth | integer (prec=32) |  |  |  |
| 属性 | 製品サイズ縦 | product_size_vertical | integer (prec=32) |  |  |  |
| 属性 |  | created_at | timestamp with time zone |  |  |  |
| 属性 |  | updated_at | timestamp with time zone |  |  |  |

## public.product_type

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 | 製品種別 | product_type | - |  |  |  |
| 属性 | 製品グループ ID | product_group_id | integer (prec=32) | Primary Key | YES |  |
| 属性 | 製品グループ名 | product_group_name | text |  | YES |  |
| 属性 |  | created_at | timestamp with time zone |  |  |  |
| 属性 |  | updated_at | timestamp with time zone |  |  |  |

## public.receipt_location

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 | 収納場所 | receipt_location | - |  |  |  |
| 属性 | 収納場所 ID | receipt_location_id | integer (prec=32) | Primary Key | YES |  |
| 属性 | 収納場所名 | receipt_location_name | text |  | YES |  |
| 属性 | 収納場所サイズ横 | receipt_location_size_horizontal | integer (prec=32) |  |  |  |
| 属性 | 収納場所サイズ奥行 | receipt_location_size_depth | integer (prec=32) |  |  |  |
| 属性 | 収納場所サイズ縦 | receipt_location_size_vertical | integer (prec=32) |  |  |  |
| 属性 | 1 個あたりの収納数 | receipt_count_per_1 | integer (prec=32) |  |  |  |
| 属性 | 1 個あたりの収納サイズ横 | receipt_size_horizontal_per_1 | integer (prec=32) |  |  |  |
| 属性 | 1 個あたりの収納サイズ奥行 | receipt_size_depth_per_1 | integer (prec=32) |  |  |  |
| 属性 | 1 個あたりの収納サイズ縦 | receipt_size_vertical_per_1 | integer (prec=32) |  |  |  |
| 属性 |  | created_at | timestamp with time zone |  |  |  |
| 属性 |  | updated_at | timestamp with time zone |  |  |  |
| 属性 | 収納場所アイコン | receipt_location_icon | text |  |  |  |
| 属性 | 収納場所使用フラグ | receipt_location_use_flag | integer (prec=32) |  |  |  |

## public.registration_product_information

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 | 登録製品情報 | registration_product_information | - |  |  |  |
| 属性 | 登録製品 ID | registration_product_id | integer (prec=32) | Primary Key | YES |  |
| 属性 | 写真 ID | photo_id | integer (prec=32) | Foreign Key |  | public.photo.photo_id |
| 属性 | 作品シリーズ ID | works_series_id | integer (prec=32) | Foreign Key |  | public.works_series.works_series_id |
| 属性 | 作品 ID | works_id | integer (prec=32) | Foreign Key |  | public.works_information.works_id |
| 属性 | キャラクター ID | character_id | integer (prec=32) | Foreign Key |  | public.character.character_id |
| 属性 | 版権会社 ID | copyright_company_id | integer (prec=32) | Foreign Key |  | public.copyright_source.copyright_company_id |
| 属性 | 製品グループ ID | product_group_id | integer (prec=32) | Foreign Key |  | public.product_type.product_group_id |
| 属性 | 製品サイズ ID | product_size_id | integer (prec=32) | Foreign Key |  | public.product_regulations_size.product_size_id |
| 属性 | 収納場所 ID | receipt_location_id | integer (prec=32) | Foreign Key |  | public.receipt_location.receipt_location_id |
| 属性 | 収納場所タグ ID | receipt_location_tag_id | integer (prec=32) |  |  |  |
| 属性 | カラータグ ID | color_tag_id | integer (prec=32) | Foreign Key |  | public.color_tag.color_tag_id |
| 属性 | カテゴリータグ ID | category_tag_id | integer (prec=32) | Foreign Key |  | public.category_tag.category_tag_id |
| 属性 | キャンペーン ID | campaign_id | integer (prec=32) |  |  |  |
| 属性 | 貨幣単位 ID | currency_unit_id | integer (prec=32) | Foreign Key |  | public.currency_unit.currency_unit_id |
| 属性 | 作品シリーズ名 | works_series_name | text |  |  |  |
| 属性 | 作品名 | title | text |  |  |  |
| 属性 | キャラクター名 | character_name | text |  |  |  |
| 属性 | 版権会社名 | copyright_company_name | text |  |  |  |
| 属性 | 製品の形 | product_type | text |  |  |  |
| 属性 | 製品サイズ横 | product_size_horizontal | integer (prec=32) |  |  |  |
| 属性 | 製品サイズ奥行 | product_size_depth | integer (prec=32) |  |  |  |
| 属性 | 製品サイズ縦 | product_size_vertical | integer (prec=32) |  |  |  |
| 属性 | バーコード番号 | barcode_number | text |  |  |  |
| 属性 | バーコードタイプ | barcode_type | text |  |  |  |
| 属性 | 製品名 | product_name | text |  |  |  |
| 属性 | 定価 | list_price | integer (prec=32) |  |  |  |
| 属性 | 購入価格 | purchase_price | integer (prec=32) |  |  |  |
| 属性 | 登録数量 | registration_quantity | integer (prec=32) |  |  |  |
| 属性 | 販売希望数量 | sales_desired_quantity | integer (prec=32) |  |  |  |
| 属性 | 製品シリーズ数量 | product_series_quantity | integer (prec=32) |  |  |  |
| 属性 | 購入場所 | purchase_location | text |  |  |  |
| 属性 | おまけ名 | freebie_name | text |  |  |  |
| 属性 | 購入日 | purchase_date | date |  |  |  |
| 属性 | 作成日 | creation_date | timestamp with time zone |  |  |  |
| 属性 | 更新日 | updated_date | timestamp with time zone |  |  |  |
| 属性 | その他タグ | other_tag | text |  |  |  |
| 属性 | メモ | memo | text |  |  |  |
| 属性 | 製品シリーズフラグ | product_series_flag | integer (prec=32) |  |  |  |
| 属性 | 商用製品フラグ | commercial_product_flag | integer (prec=32) |  |  |  |
| 属性 | 同人製品フラグ | personal_product_flag | integer (prec=32) |  |  |  |
| 属性 | デジタル製品フラグ | digital_product_flag | integer (prec=32) |  |  |  |
| 属性 | 販売希望フラグ | sales_desired_flag | integer (prec=32) |  |  |  |
| 属性 | 欲しい物フラグ | want_object_flag | integer (prec=32) |  |  |  |
| 属性 | おまけ付きフラグ | flag_with_freebie | integer (prec=32) |  |  |  |
| 属性 | 製品シリーズコンプリートフラグ | product_series_complete_flag | integer (prec=32) |  |  |  |
| 属性 | 製品グループ名 | product_group_name | text |  |  |  |

## public.theme_settings

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 |  | theme_settings | - |  |  |  |
| 属性 |  | members_id | integer (prec=32) | Primary Key | YES |  |
| 属性 |  | members_type_name | text | Primary Key | YES |  |
| 属性 |  | theme | text |  | YES |  |
| 属性 |  | created_at | timestamp with time zone |  |  |  |
| 属性 |  | updated_at | timestamp with time zone |  |  |  |

## public.works_information

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 | 作品情報 | works_information | - |  |  |  |
| 属性 | 作品 ID | works_id | integer (prec=32) | Primary Key | YES |  |
| 属性 | 作品名 | title | text |  | YES |  |
| 属性 | 作品シリーズ ID | works_series_id | integer (prec=32) | Foreign Key |  | public.works_series.works_series_id |
| 属性 |  | created_at | timestamp with time zone |  |  |  |
| 属性 |  | updated_at | timestamp with time zone |  |  |  |
| 属性 |  | copyright_company_name | text |  |  |  |

## public.works_series

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 | 作品シリーズ | works_series | - |  |  |  |
| 属性 | 作品シリーズ ID | works_series_id | integer (prec=32) | Primary Key | YES |  |
| 属性 | 作品シリーズ名 | works_series_name | text |  | YES |  |
| 属性 |  | created_at | timestamp with time zone |  |  |  |
| 属性 |  | updated_at | timestamp with time zone |  |  |  |

## storage.buckets

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 |  | buckets | - |  |  |  |
| 属性 |  | id | text | Primary Key | YES |  |
| 属性 |  | name | text |  | YES |  |
| 属性 |  | owner | uuid |  |  |  |
| 属性 |  | created_at | timestamp with time zone |  |  |  |
| 属性 |  | updated_at | timestamp with time zone |  |  |  |
| 属性 |  | public | boolean |  |  |  |
| 属性 |  | avif_autodetection | boolean |  |  |  |
| 属性 |  | file_size_limit | bigint (prec=64) |  |  |  |
| 属性 |  | allowed_mime_types | ARRAY |  |  |  |
| 属性 |  | owner_id | text |  |  |  |
| 属性 |  | type | USER-DEFINED |  | YES |  |

## storage.buckets_analytics

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 |  | buckets_analytics | - |  |  |  |
| 属性 |  | name | text |  | YES |  |
| 属性 |  | type | USER-DEFINED |  | YES |  |
| 属性 |  | format | text |  | YES |  |
| 属性 |  | created_at | timestamp with time zone |  | YES |  |
| 属性 |  | updated_at | timestamp with time zone |  | YES |  |
| 属性 |  | id | uuid | Primary Key | YES |  |
| 属性 |  | deleted_at | timestamp with time zone |  |  |  |

## storage.buckets_vectors

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 |  | buckets_vectors | - |  |  |  |
| 属性 |  | id | text |  | YES |  |
| 属性 |  | type | USER-DEFINED |  | YES |  |
| 属性 |  | created_at | timestamp with time zone |  | YES |  |
| 属性 |  | updated_at | timestamp with time zone |  | YES |  |

## storage.migrations

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 |  | migrations | - |  |  |  |
| 属性 |  | id | integer (prec=32) |  | YES |  |
| 属性 |  | name | character varying (len=100) |  | YES |  |
| 属性 |  | hash | character varying (len=40) |  | YES |  |
| 属性 |  | executed_at | timestamp without time zone |  |  |  |

## storage.objects

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 |  | objects | - |  |  |  |
| 属性 |  | id | uuid | Primary Key | YES |  |
| 属性 |  | bucket_id | text |  |  |  |
| 属性 |  | name | text |  |  |  |
| 属性 |  | owner | uuid |  |  |  |
| 属性 |  | created_at | timestamp with time zone |  |  |  |
| 属性 |  | updated_at | timestamp with time zone |  |  |  |
| 属性 |  | last_accessed_at | timestamp with time zone |  |  |  |
| 属性 |  | metadata | jsonb |  |  |  |
| 属性 |  | path_tokens | ARRAY |  |  |  |
| 属性 |  | version | text |  |  |  |
| 属性 |  | owner_id | text |  |  |  |
| 属性 |  | user_metadata | jsonb |  |  |  |
| 属性 |  | level | integer (prec=32) |  |  |  |

## storage.prefixes

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 |  | prefixes | - |  |  |  |
| 属性 |  | bucket_id | text | Primary Key | YES |  |
| 属性 |  | name | text | Primary Key | YES |  |
| 属性 |  | level | integer (prec=32) | Primary Key | YES |  |
| 属性 |  | created_at | timestamp with time zone |  |  |  |
| 属性 |  | updated_at | timestamp with time zone |  |  |  |

## storage.s3_multipart_uploads

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 |  | s3_multipart_uploads | - |  |  |  |
| 属性 |  | id | text | Primary Key | YES |  |
| 属性 |  | in_progress_size | bigint (prec=64) |  | YES |  |
| 属性 |  | upload_signature | text |  | YES |  |
| 属性 |  | bucket_id | text |  | YES |  |
| 属性 |  | key | text |  | YES |  |
| 属性 |  | version | text |  | YES |  |
| 属性 |  | owner_id | text |  |  |  |
| 属性 |  | created_at | timestamp with time zone |  | YES |  |
| 属性 |  | user_metadata | jsonb |  |  |  |

## storage.s3_multipart_uploads_parts

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 |  | s3_multipart_uploads_parts | - |  |  |  |
| 属性 |  | id | uuid | Primary Key | YES |  |
| 属性 |  | upload_id | text |  | YES |  |
| 属性 |  | size | bigint (prec=64) |  | YES |  |
| 属性 |  | part_number | integer (prec=32) |  | YES |  |
| 属性 |  | bucket_id | text |  | YES |  |
| 属性 |  | key | text |  | YES |  |
| 属性 |  | etag | text |  | YES |  |
| 属性 |  | owner_id | text |  |  |  |
| 属性 |  | version | text |  | YES |  |
| 属性 |  | created_at | timestamp with time zone |  | YES |  |

## storage.vector_indexes

| 役割 | 名称日本語 | メソッド名 | データ型 | キー設定 | NOT NULL | 外部キー参照 |
| --- | --- | --- | --- | --- | --- | --- |
| エンティティ名 |  | vector_indexes | - |  |  |  |
| 属性 |  | id | text |  | YES |  |
| 属性 |  | name | text |  | YES |  |
| 属性 |  | bucket_id | text |  | YES |  |
| 属性 |  | data_type | text |  | YES |  |
| 属性 |  | dimension | integer (prec=32) |  | YES |  |
| 属性 |  | distance_metric | text |  | YES |  |
| 属性 |  | metadata_configuration | jsonb |  |  |  |
| 属性 |  | created_at | timestamp with time zone |  | YES |  |
| 属性 |  | updated_at | timestamp with time zone |  | YES |  |
