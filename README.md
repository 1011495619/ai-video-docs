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

在 Mintlify 中连接 `1011495619/ai-video-docs`，发布分支选择 `main`，文档目录使用仓库根目录。推送到 `main` 后触发文档部署。

生成的站点地址填写到主系统「系统配置 → 基础信息 → 文档链接」。自定义域名在 Mintlify 控制台配置，并按提示添加 DNS 记录。
