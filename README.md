# AI Video 文档

独立 Mintlify 文档仓库。页面内容维护在 `.mdx`，导航和默认主题维护在 `docs.json`。

## 本地预览

```bash
npm install -g mint
mint dev --port 3333 --no-open
```

## 发布检查

```bash
mint validate
mint broken-links
```

## 托管

已上线：[AI Video 文档](https://as-aed1f270.mintlify.site)。

Mintlify 已连接 `1011495619/ai-video-docs`，发布分支为 `main`，文档目录为仓库根目录。推送到 `main` 后自动构建发布。

主系统「系统配置 → 基础信息 → 文档链接」填写 `https://as-aed1f270.mintlify.site`。自定义域名在 Mintlify 控制台配置，并按提示添加 DNS 记录。
