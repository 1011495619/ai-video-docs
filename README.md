# AI Video 文档

AI Video 客户 API 接入与供应商管理指南的唯一维护仓库。页面正文维护在 `.mdx`，导航、主题与旧页面重定向维护在根目录 `docs.json`。

- 文档仓库：[1011495619/ai-video-docs](https://github.com/1011495619/ai-video-docs)
- 应用源码：[1011495619/ai-video](https://github.com/1011495619/ai-video)
- 在线文档：[AI Video 文档](https://as-aed1f270.mintlify.site)

应用仓库中的 `docs/` 保留研发计划、审计和运维资料；公开接入文档与管理操作指南统一在本仓库维护。

## 本地预览

使用 Node.js 20.17.0 或更高版本。推荐将应用仓库 `aiVideo/` 与文档仓库 `ai-video-docs/` 放在同级目录。

```bash
npm install -g mint
cd ai-video-docs
mint dev --port 3333 --no-open
```

从应用仓库根目录可使用 `cd ../ai-video-docs`。预览地址为 `http://localhost:3333`。

## 发布检查

在文档仓库根目录执行：

```bash
mint validate
mint broken-links
```

新增页面后，在 `docs.json` 的导航中登记。修改调用示例时核对应用的公开控制器、DTO、协议与响应映射，尤其注意 Base URL 版本前缀、时间单位、文件 UUID、上传限制及各协议的结果结构。

## GitHub 与 Mintlify 发布

现有 Mintlify Git 配置：

| 配置项 | 值 |
| --- | --- |
| GitHub 仓库 | `1011495619/ai-video-docs` |
| 发布分支 | `main` |
| 文档目录 | 仓库根目录 |
| 当前托管地址 | `https://as-aed1f270.mintlify.site` |

文档变更在本仓库独立提交。检查通过后，将变更合并并推送到 `main`，Mintlify 自动构建发布；在 Mintlify 控制台查看部署状态，再核对线上页面。

主项目的提交与应用构建独立进行。自定义域名在 Mintlify 控制台配置，并按提示添加 DNS 记录。

## 应用文档链接

管理后台 → 系统配置 → 基础信息 → 文档链接，填写 `https://as-aed1f270.mintlify.site` 或已配置的自定义域名。对应系统配置键为 `site_documentation_url`，客户端刷新后读取新地址，无需重新构建应用。

链接留空时隐藏 API 工作台文档入口。旧客户端文档路径通过 `/documentation` 获取最新配置并跳转，后端 API Key 的文档元数据也使用该配置。

完整子路径 URL 也可作为入口，但 DNS、HTTPS 和子路径代理需要按 Mintlify 指引配置。

## 内容迁移与接口参考

原应用仓库 `client/public/docs/openapi-integration-guide.md` 已拆分为快速开始、鉴权、模型、账户、上传、对话协议、SDK、图像、视频、任务状态和错误处理页面。原供应商说明位于 `administration/provider-routes.mdx`。应用仓库内的 `mintlify/` 副本已移除，后续内容变更统一在此维护。

`openapi.json` 维护客户 API 的请求、响应和认证结构。`API 参考` 页面通过 `openapi: "openapi.json METHOD /path"` 绑定接口，在保留正文的同时展示 Mintlify 交互式调试区。

当前包含 28 个客户接口，覆盖账户与模型、素材上传删除、对话协议、图片和视频任务、OpenAI 图片批次、Responses 资源和 Token 统计。默认 API 服务根地址为 `https://ai.moyinai.com/api`，路径中已包含 `/v1` 或 `/v1beta`，避免重复拼接版本前缀。

调试区使用 Mintlify API 代理，并提供 cURL、Python 和 JavaScript 示例。修改接口时同步维护 `openapi.json` 和对应 MDX 页面；不要直接发布包含后台接口的完整 Swagger 导出。

官方说明：[GitHub 部署](https://www.mintlify.com/docs/deploy/github)、[自定义域名](https://www.mintlify.com/docs/customize/custom-domain)、[子路径部署](https://www.mintlify.com/docs/deploy/docs-subpath)。
