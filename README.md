# 📡 social-api-cheatsheet

> A community-maintained cheat sheet of **endpoints, key fields, versions and deprecation (sunset) dates** for major social-platform APIs — Facebook Graph, TikTok, Telegram Bot, and more. A bot watches the official changelogs daily and opens a PR when something upstream changes, so the data stays fresh.
>
> Bảng tra cứu cộng đồng về **endpoint, field chính, phiên bản và ngày khai tử (sunset)** của API các nền tảng social lớn — Facebook Graph, TikTok, Telegram Bot… Một bot theo dõi changelog chính thức mỗi ngày và tự mở PR khi nền tảng thay đổi, giúp dữ liệu luôn mới.

<p align="center">
  <img alt="last commit" src="https://img.shields.io/github/last-commit/tuanone123/social-api-cheatsheet">
  <img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen">
  <img alt="license" src="https://img.shields.io/badge/license-MIT-blue">
</p>

---

## 🇬🇧 English

**Why this exists.** Social APIs change constantly — new versions ship, fields get renamed, and old versions are sunset without much warning. This repo keeps a single, skimmable table per platform plus an automated watcher so you learn about breaking changes *before* they break your integration.

**How the automation works**
1. `scripts/watch.py` fetches each official changelog listed in [`sources.yml`](sources.yml), strips the noise, and diffs it against a saved snapshot.
2. When a page changes, a GitHub Action opens a **pull request** tagged `needs-curation` — a human then updates the matching `data/*.yml` entry. *(We never auto-merge parsed content — bad parses would poison the sheet.)*
3. A weekly job scans `sunset` dates and opens an **issue** for any API version expiring within 60 days.
4. Merging a change to `data/**` auto-rebuilds the tables below.

**Contribute** → see [CONTRIBUTING.md](CONTRIBUTING.md). Add a platform, fix a field, or update a version — it's just a YAML edit.

## 🇻🇳 Tiếng Việt

**Vì sao có repo này.** API social thay đổi liên tục — ra version mới, đổi tên field, khai tử version cũ mà báo trước rất ít. Repo này giữ mỗi nền tảng một bảng gọn + bot tự theo dõi để bạn biết breaking change *trước khi* nó làm hỏng tích hợp.

**Cơ chế tự động**
1. `scripts/watch.py` tải changelog chính thức khai báo trong [`sources.yml`](sources.yml), lọc nhiễu, rồi so với snapshot đã lưu.
2. Khi trang đổi, GitHub Action mở **pull request** gắn nhãn `needs-curation` — người duyệt cập nhật `data/*.yml` tương ứng. *(Không bao giờ auto-merge nội dung tự parse — parse sai sẽ làm bẩn bảng.)*
3. Job hằng tuần quét ngày `sunset`, mở **issue** cho mọi version sắp hết hạn trong 60 ngày.
4. Merge thay đổi vào `data/**` sẽ tự dựng lại các bảng bên dưới.

**Đóng góp** → xem [CONTRIBUTING.md](CONTRIBUTING.md). Thêm nền tảng, sửa field, cập nhật version — chỉ là sửa file YAML.

---

## 📚 Cheat sheet

<!-- AUTOGEN:START -->

**Platforms:** [Facebook Graph API](#facebook-graph-api) · [Telegram Bot API](#telegram-bot-api) · [TikTok for Developers](#tiktok-for-developers)

### Facebook Graph API
> Docs: <https://developers.facebook.com/docs/graph-api/> · Changelog: <https://developers.facebook.com/docs/graph-api/changelog/> · Auth: OAuth 2.0 Access Token (User / Page / App / Client Token)
>
> Base URL: `https://graph.facebook.com`

**Versions**

| Version | Released | Sunset |
|---|---|---|
| v21.0 | 2024-10-02 | 2026-10-02 |
| v20.0 | 2024-05-21 | 2026-05-21 |
| v19.0 | 2024-01-23 | 2026-01-23 |
| v18.0 | 2023-09-12 | 2025-09-12 |

**Endpoints**

| Endpoint | Method | Path | Scopes | Key fields | Notes |
|---|---|---|---|---|---|
| Get user profile | GET | `/{version}/{user-id}` | public_profile | id, name, picture | email requires the `email` scope + App Review |
| Publish page post | POST | `/{version}/{page-id}/feed` | pages_manage_posts | message, link, published | Needs a Page Access Token, not a User token |
| Debug token | GET | `/{version}/debug_token` | - | input_token, access_token | Inspect scopes / expiry of any token |

_Last verified: 2026-09-07_

### Telegram Bot API
> Docs: <https://core.telegram.org/bots/api> · Changelog: <https://core.telegram.org/bots/api-changelog> · Auth: Bot token from @BotFather (`https://api.telegram.org/bot<token>/METHOD`)
>
> Base URL: `https://api.telegram.org`

**Endpoints**

| Endpoint | Method | Path | Scopes | Key fields | Notes |
|---|---|---|---|---|---|
| getUpdates (long polling) | GET/POST | `/bot{token}/getUpdates` | - | offset, timeout, allowed_updates | Mutually exclusive with a set webhook |
| setWebhook | POST | `/bot{token}/setWebhook` | - | url, secret_token, allowed_updates | Use secret_token to verify incoming updates |
| sendMessage | POST | `/bot{token}/sendMessage` | - | chat_id, text, parse_mode, reply_markup | parse_mode: MarkdownV2 / HTML |

_Last verified: 2026-09-07_

### TikTok for Developers
> Docs: <https://developers.tiktok.com/doc/> · Changelog: <https://developers.tiktok.com/doc/changelog/> · Auth: OAuth 2.0 (Login Kit) — access_token + open_id
>
> Base URL: `https://open.tiktokapis.com`

**Versions**

| Version | Released |
|---|---|
| v2 | 2023-06-01 |

**Endpoints**

| Endpoint | Method | Path | Scopes | Key fields | Notes |
|---|---|---|---|---|---|
| Query user info | GET | `/v2/user/info/` | user.info.basic | open_id, display_name, avatar_url | Fields requested via `fields` query param |
| Init video publish | POST | `/v2/post/publish/video/init/` | video.publish | post_info, source_info | Content Posting API; returns publish_id |
| Query creator info | POST | `/v2/post/publish/creator_info/query/` | video.publish | creator_username, privacy_level_options | Call before publishing to get allowed settings |

_Last verified: 2026-09-07_

<!-- AUTOGEN:END -->

---

## ⚠️ Disclaimer

Data is community-contributed and provided **as-is** for quick reference. Always confirm against the official documentation before shipping — sunset dates in particular are estimates until verified. Not affiliated with or endorsed by any platform.

Dữ liệu do cộng đồng đóng góp, cung cấp **nguyên trạng** để tra cứu nhanh. Luôn đối chiếu tài liệu chính thức trước khi triển khai — đặc biệt ngày sunset chỉ là ước tính đến khi được xác minh. Không liên kết/đại diện cho bất kỳ nền tảng nào.

## 📄 License

[MIT](LICENSE) — free to use, share, and adapt.
