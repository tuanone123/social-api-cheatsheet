# Contributing / Đóng góp

Thanks for helping keep the cheat sheet accurate! Cảm ơn bạn đã góp phần giữ bảng tra cứu chính xác!

## 🇬🇧 English

Everything lives in **`data/*.yml`** — one file per platform. The README tables are generated from these files, so you never edit the README directly.

### Add or fix a platform
1. Copy an existing file in `data/` (e.g. `data/telegram.yml`) or edit the one you want to fix.
2. Follow the schema below. Every field is a plain string.
3. Set `last_checked` to today's date (`YYYY-MM-DD`) and cite the official docs in your PR.
4. Open a pull request. A maintainer merges it; the README rebuilds automatically.

```yaml
platform: "Platform display name"
slug: shortname            # lowercase, matches the filename
docs: "https://..."         # official docs URL
changelog: "https://..."    # official changelog URL (also add to sources.yml to auto-watch)
auth: "How auth works in one line"
base_url: "https://api.example.com"
current_version: "v2"
versioning: true            # false if the platform has no versioned URLs
versions:
  - version: "v2"
    released: "2024-01-01"
    sunset: "2026-01-01"    # leave "" if the platform never sunsets
endpoints:
  - name: "Human-readable name"
    method: "GET"           # GET / POST / ...
    path: "/{version}/resource"
    scopes: "scope.name"    # "-" if none
    key_fields: "field1, field2"
    notes: "Anything worth a warning"
last_checked: "2026-09-07"
```

### To auto-watch a new platform
Add its changelog page to [`sources.yml`](sources.yml) with an optional CSS `selector`. The daily bot will then diff it and open a PR when it changes.

### Rules
- **Only public, official documentation** as sources. No scraping behind logins, no private/reverse-engineered endpoints.
- Keep entries concise — this is a cheat sheet, not full docs.
- One platform per PR when possible.

## 🇻🇳 Tiếng Việt

Toàn bộ dữ liệu nằm trong **`data/*.yml`** — mỗi nền tảng một file. Bảng trong README được sinh tự động từ các file này, nên bạn **không sửa README trực tiếp**.

### Thêm hoặc sửa một nền tảng
1. Copy một file có sẵn trong `data/` (vd `data/telegram.yml`) hoặc sửa file cần chỉnh.
2. Theo đúng schema ở trên. Mọi trường đều là chuỗi.
3. Đặt `last_checked` = ngày hôm nay (`YYYY-MM-DD`) và dẫn link tài liệu chính thức trong PR.
4. Mở pull request. Maintainer merge; README tự dựng lại.

### Bật auto-theo-dõi nền tảng mới
Thêm URL changelog vào [`sources.yml`](sources.yml) kèm `selector` CSS (tuỳ chọn). Bot hằng ngày sẽ diff và tự mở PR khi trang đổi.

### Quy tắc
- **Chỉ dùng tài liệu công khai, chính thức** làm nguồn. Không cào dữ liệu sau đăng nhập, không dùng endpoint riêng tư/reverse-engineer.
- Viết ngắn gọn — đây là cheat sheet, không phải tài liệu đầy đủ.
- Mỗi PR nên chỉ một nền tảng khi có thể.
