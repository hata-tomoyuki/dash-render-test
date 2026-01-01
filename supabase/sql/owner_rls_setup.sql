-- ユーザー毎のデータ分離: owner_id + RLS
-- 既存データがある場合は、owner_id を手動で埋めてから RLS を有効化してください。

-- registration_product_information
alter table if exists public.registration_product_information
    add column if not exists owner_id uuid default auth.uid();

-- photo
alter table if exists public.photo
    add column if not exists owner_id uuid default auth.uid();

-- theme_settings
alter table if exists public.theme_settings
    add column if not exists owner_id uuid default auth.uid();

-- color_tag
alter table if exists public.color_tag
    add column if not exists owner_id uuid default auth.uid();

-- category_tag
alter table if exists public.category_tag
    add column if not exists owner_id uuid default auth.uid();

-- RLS 有効化
alter table if exists public.registration_product_information enable row level security;
alter table if exists public.photo enable row level security;
alter table if exists public.theme_settings enable row level security;
alter table if exists public.color_tag enable row level security;
alter table if exists public.category_tag enable row level security;

-- ポリシー（自分の行のみ）
create policy if not exists rpi_select_self on public.registration_product_information
    for select using (owner_id = auth.uid());
create policy if not exists rpi_insert_self on public.registration_product_information
    for insert with check (owner_id = auth.uid());
create policy if not exists rpi_update_self on public.registration_product_information
    for update using (owner_id = auth.uid());
create policy if not exists rpi_delete_self on public.registration_product_information
    for delete using (owner_id = auth.uid());

create policy if not exists photo_select_self on public.photo
    for select using (owner_id = auth.uid());
create policy if not exists photo_insert_self on public.photo
    for insert with check (owner_id = auth.uid());
create policy if not exists photo_update_self on public.photo
    for update using (owner_id = auth.uid());
create policy if not exists photo_delete_self on public.photo
    for delete using (owner_id = auth.uid());

create policy if not exists theme_select_self on public.theme_settings
    for select using (owner_id = auth.uid());
create policy if not exists theme_upsert_self on public.theme_settings
    for all using (owner_id = auth.uid()) with check (owner_id = auth.uid());

create policy if not exists color_tag_select_self on public.color_tag
    for select using (owner_id = auth.uid());
create policy if not exists color_tag_mutate_self on public.color_tag
    for all using (owner_id = auth.uid()) with check (owner_id = auth.uid());

create policy if not exists category_tag_select_self on public.category_tag
    for select using (owner_id = auth.uid());
create policy if not exists category_tag_mutate_self on public.category_tag
    for all using (owner_id = auth.uid()) with check (owner_id = auth.uid());

-- Storage ポリシー例（photos bucket）
-- name が auth.uid() で始まるオブジェクトのみ許可する想定
-- adjust your bucket name/path as needed
-- create policy "photos select own" on storage.objects
--   for select using (bucket_id = 'photos' and position(auth.uid()::text in name) = 1);


