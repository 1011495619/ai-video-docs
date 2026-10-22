# AI Video 客户 API — Markdown 接口参考

接口版本：`1.0.0`。共 28 个客户接口。
本文件可独立阅读、下载或交给开发工具使用，由文档仓库的 `openapi.json` 生成。

## 连接配置

`API_BASE_URL` 是客户 API 的完整对外根地址，包含协议、域名、可选端口和 Nginx 对外路径前缀。末尾不加 `/`，也不包含 `/v1`、`/v1beta` 或具体接口路径。

将下面的占位值替换为所属站点的地址与密钥，在同一个终端设置一次即可：

```bash
export API_BASE_URL="YOUR_API_BASE_URL"
export PLATFORM_API_KEY="YOUR_API_KEY"
```

请求地址 = `API_BASE_URL` + 本文的接口路径。根路径、`/api`、`/gateway` 和多层前缀均按客户实际部署填写。若从工作台复制的 OpenAI SDK 地址末尾含 `/v1`，先移除该版本段。

正文命令读取终端环境变量；Mintlify 在线调试区则在 `Server → baseUrl` 填写相同根地址，两处分别保存。本文的请求示例不预设客户域名。

## 鉴权与请求约定

| 协议 | 请求头 | 说明 |
| --- | --- | --- |
| OpenAI / 文件 / 图片 / 视频 | `Authorization: Bearer $PLATFORM_API_KEY` | 密钥来自 API 请求所属站点 |
| Anthropic | `X-API-Key: $PLATFORM_API_KEY` | `anthropic-version: 2023-06-01` |
| Gemini | `x-goog-api-key: $PLATFORM_API_KEY` | 使用 `/v1beta` 接口路径 |

模型名与资源 ID 均为占位值。先查询模型目录，选择当前账户支持对应操作的模型；查询和删除时使用实际返回的 ID。文件上传使用 multipart，让 curl 自动生成 Content-Type 和 boundary。

生成接口会实际调用模型，并按站点规则消耗额度。示例仅说明参数结构；字段表标为可选的参数仍可能受到所选模型能力限制。

## 接口目录

| 分组 | 方法 | 路径 | 接口 |
| --- | --- | --- | --- |
| 账户与模型 | GET | `/v1/account` | [账户、额度与用量](#get_account) |
| 账户与模型 | GET | `/v1/catalog/models` | [图片与视频模型目录](#get_catalog) |
| 账户与模型 | GET | `/v1/models` | [对话模型列表](#get_models) |
| 账户与模型 | GET | `/v1beta/models` | [Gemini 模型列表](#get_gemini_models) |
| 素材文件 | POST | `/v1/files` | [上传图片、视频或音频](#upload_file) |
| 素材文件 | DELETE | `/v1/files/{fileId}` | [删除已上传素材](#delete_file) |
| 图片生成 | POST | `/v1/images` | [创建图片任务](#create_image) |
| 图片生成 | GET | `/v1/images/{taskId}` | [查询图片任务](#get_image) |
| OpenAI 图片兼容 | POST | `/v1/images/generations` | [OpenAI 图片生成](#image_generations) |
| OpenAI 图片兼容 | POST | `/v1/images/generations/async` | [OpenAI 图片生成（异步）](#image_generations_async) |
| OpenAI 图片兼容 | POST | `/v1/images/edits` | [OpenAI 图片编辑](#image_edits) |
| OpenAI 图片兼容 | POST | `/v1/images/edits/async` | [OpenAI 图片编辑（异步）](#image_edits_async) |
| OpenAI 图片兼容 | GET | `/v1/images/tasks/{taskId}` | [查询图片批次](#get_image_batch) |
| 视频生成 | POST | `/v1/videos` | [创建视频任务](#create_video) |
| 视频生成 | GET | `/v1/videos/{taskId}` | [查询视频任务](#get_video) |
| 对话协议 | POST | `/v1/chat/completions` | [Chat Completions](#chat_completions) |
| 对话协议 | POST | `/v1/responses` | [OpenAI Responses](#create_response) |
| 对话协议 | POST | `/v1/messages` | [Anthropic Messages](#anthropic_messages) |
| 对话协议 | POST | `/v1beta/models/{model}:generateContent` | [Gemini GenerateContent](#gemini_generate) |
| 对话协议 | POST | `/v1beta/models/{model}:streamGenerateContent` | [Gemini 流式生成](#gemini_stream) |
| Responses 资源 | GET | `/v1/responses/{responseId}` | [查询 Responses 响应](#get_response) |
| Responses 资源 | DELETE | `/v1/responses/{responseId}` | [删除 Responses 响应](#delete_response) |
| Responses 资源 | POST | `/v1/responses/{responseId}/cancel` | [取消 Responses 响应](#cancel_response) |
| Responses 资源 | GET | `/v1/responses/{responseId}/input_items` | [查询 Responses 输入项](#response_input_items) |
| Token 与上下文 | POST | `/v1/responses/compact` | [压缩 Responses 上下文](#compact_response) |
| Token 与上下文 | POST | `/v1/responses/input_tokens` | [统计 Responses 输入 Token](#response_input_tokens) |
| Token 与上下文 | POST | `/v1/messages/count_tokens` | [统计 Messages 输入 Token](#anthropic_count_tokens) |
| Token 与上下文 | POST | `/v1beta/models/{model}:countTokens` | [统计 Gemini 输入 Token](#gemini_count_tokens) |

## get_account

**账户、额度与用量**

`GET /v1/account`

查询当前平台 API Key 的额度和用户级限制。余额和账单在系统工作台查看。

**鉴权：** `Authorization: Bearer $PLATFORM_API_KEY`

### 路径、查询与请求头参数

无额外参数。

### 请求体

无请求体。

### 请求示例

```bash
curl --request GET "${API_BASE_URL}/v1/account" \
  -H "Authorization: Bearer $PLATFORM_API_KEY"
```

### 响应

| HTTP 状态 | 含义 | Content-Type | 响应结构 |
| --- | --- | --- | --- |
| 200 | 请求成功。 | `application/json` | [AccountEnvelope](#accountenvelope) |
| 400 | 参数或协议错误。 | `application/json` | [ApiError](#apierror) |
| 401 | 密钥缺失、无效、停用或跨站点使用。 | `application/json` | [ApiError](#apierror) |
| 402 | 余额或额度不足。 | `application/json` | [ApiError](#apierror) |
| 404 | 模型、任务或资源不存在。 | `application/json` | [ApiError](#apierror) |
| 429 | 频率或并发超过限制。 | `application/json` | [ApiError](#apierror) |
| 500 | 服务处理失败。 | `application/json` | [ApiError](#apierror) |

**HTTP 200 响应示例：**

```json
{
  "code": 200,
  "message": "查询成功",
  "data": {
    "account_id": "acct_example",
    "status": "active",
    "quota": {
      "daily_limit": 100,
      "daily_used": 7,
      "daily_remaining": 93
    },
    "rate_limit": {
      "requests_per_minute": 60
    },
    "concurrency": {
      "max_concurrent_tasks": 5
    },
    "created_at": 1776843503
  }
}
```

## get_catalog

**图片与视频模型目录**

`GET /v1/catalog/models`

查询账户可见的公开模型 ID、价格、能力及扩展参数。生成前以此结果选择模型。

**鉴权：** `Authorization: Bearer $PLATFORM_API_KEY`

### 路径、查询与请求头参数

无额外参数。

### 请求体

无请求体。

### 请求示例

```bash
curl --request GET "${API_BASE_URL}/v1/catalog/models" \
  -H "Authorization: Bearer $PLATFORM_API_KEY"
```

### 响应

| HTTP 状态 | 含义 | Content-Type | 响应结构 |
| --- | --- | --- | --- |
| 200 | 请求成功。 | `application/json` | [CatalogEnvelope](#catalogenvelope) |
| 400 | 参数或协议错误。 | `application/json` | [ApiError](#apierror) |
| 401 | 密钥缺失、无效、停用或跨站点使用。 | `application/json` | [ApiError](#apierror) |
| 402 | 余额或额度不足。 | `application/json` | [ApiError](#apierror) |
| 404 | 模型、任务或资源不存在。 | `application/json` | [ApiError](#apierror) |
| 429 | 频率或并发超过限制。 | `application/json` | [ApiError](#apierror) |
| 500 | 服务处理失败。 | `application/json` | [ApiError](#apierror) |

## get_models

**对话模型列表**

`GET /v1/models`

查询对话模型及 supported_operations。此页面使用 OpenAI 格式；Anthropic 或 Gemini 的列表格式见接入说明。

**鉴权：** `Authorization: Bearer $PLATFORM_API_KEY`

### 路径、查询与请求头参数

无额外参数。

### 请求体

无请求体。

### 请求示例

```bash
curl --request GET "${API_BASE_URL}/v1/models" \
  -H "Authorization: Bearer $PLATFORM_API_KEY"
```

### 响应

| HTTP 状态 | 含义 | Content-Type | 响应结构 |
| --- | --- | --- | --- |
| 200 | 请求成功。 | `application/json` | [ModelList](#modellist) |
| 400 | 参数或协议错误。 | `application/json` | [ProtocolError](#protocolerror) |
| 401 | 密钥缺失、无效、停用或跨站点使用。 | `application/json` | [ProtocolError](#protocolerror) |
| 402 | 余额或额度不足。 | `application/json` | [ProtocolError](#protocolerror) |
| 404 | 模型、任务或资源不存在。 | `application/json` | [ProtocolError](#protocolerror) |
| 429 | 频率或并发超过限制。 | `application/json` | [ProtocolError](#protocolerror) |
| 500 | 服务处理失败。 | `application/json` | [ProtocolError](#protocolerror) |

## get_gemini_models

**Gemini 模型列表**

`GET /v1beta/models`

查询 Gemini 资源名和 supportedGenerationMethods。生成路径中的模型只填写 ID，不重复 models/。

**鉴权：** `x-goog-api-key: $PLATFORM_API_KEY`

### 路径、查询与请求头参数

无额外参数。

### 请求体

无请求体。

### 请求示例

```bash
curl --request GET "${API_BASE_URL}/v1beta/models" \
  -H "x-goog-api-key: $PLATFORM_API_KEY"
```

### 响应

| HTTP 状态 | 含义 | Content-Type | 响应结构 |
| --- | --- | --- | --- |
| 200 | 请求成功。 | `application/json` | [GeminiModelList](#geminimodellist) |
| 400 | 参数或协议错误。 | `application/json` | [ProtocolError](#protocolerror) |
| 401 | 密钥缺失、无效、停用或跨站点使用。 | `application/json` | [ProtocolError](#protocolerror) |
| 402 | 余额或额度不足。 | `application/json` | [ProtocolError](#protocolerror) |
| 404 | 模型、任务或资源不存在。 | `application/json` | [ProtocolError](#protocolerror) |
| 429 | 频率或并发超过限制。 | `application/json` | [ProtocolError](#protocolerror) |
| 500 | 服务处理失败。 | `application/json` | [ProtocolError](#protocolerror) |

## upload_file

**上传图片、视频或音频**

`POST /v1/files`

上传素材后读取 url 用于生成，保存文件 UUID 用于删除。类型、大小和数量受平台配置限制，上传要求正余额。

**鉴权：** `Authorization: Bearer $PLATFORM_API_KEY`

### 路径、查询与请求头参数

无额外参数。

### 请求体

**Content-Type：** `multipart/form-data`；请求体必填：是。

**结构：** object。完整嵌套字段见同名数据结构。

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `file` | string (binary) | 是 | — | — |

### 请求示例：multipart/form-data

```bash
curl --request POST "${API_BASE_URL}/v1/files" \
  -H "Authorization: Bearer $PLATFORM_API_KEY" \
  -F "file=@/path/to/reference.mp4"
```

### 响应

| HTTP 状态 | 含义 | Content-Type | 响应结构 |
| --- | --- | --- | --- |
| 200 | 请求成功。 | `application/json` | [File](#file) |
| 400 | 参数或协议错误。 | `application/json` | [ApiError](#apierror) |
| 401 | 密钥缺失、无效、停用或跨站点使用。 | `application/json` | [ApiError](#apierror) |
| 402 | 余额或额度不足。 | `application/json` | [ApiError](#apierror) |
| 404 | 模型、任务或资源不存在。 | `application/json` | [ApiError](#apierror) |
| 429 | 频率或并发超过限制。 | `application/json` | [ApiError](#apierror) |
| 500 | 服务处理失败。 | `application/json` | [ApiError](#apierror) |
| 413 | 素材文件超过平台上传限制。 | `application/json` | [ApiError](#apierror) |

## delete_file

**删除已上传素材**

`DELETE /v1/files/{fileId}`

删除当前账户的素材。使用上传返回的文件 UUID。

**鉴权：** `Authorization: Bearer $PLATFORM_API_KEY`

### 路径、查询与请求头参数

| 位置 | 参数 | 类型 | 必填 | 说明与约束 |
| --- | --- | --- | --- | --- |
| path | `fileId` | string (uuid) | 是 | 上传结果的 id。 |

### 请求体

无请求体。

### 请求示例

```bash
curl --request DELETE "${API_BASE_URL}/v1/files/01234567-89ab-4cde-8f01-23456789abcd" \
  -H "Authorization: Bearer $PLATFORM_API_KEY"
```

### 响应

| HTTP 状态 | 含义 | Content-Type | 响应结构 |
| --- | --- | --- | --- |
| 200 | 请求成功。 | `application/json` | [FileDeleted](#filedeleted) |
| 400 | 参数或协议错误。 | `application/json` | [ApiError](#apierror) |
| 401 | 密钥缺失、无效、停用或跨站点使用。 | `application/json` | [ApiError](#apierror) |
| 402 | 余额或额度不足。 | `application/json` | [ApiError](#apierror) |
| 404 | 模型、任务或资源不存在。 | `application/json` | [ApiError](#apierror) |
| 429 | 频率或并发超过限制。 | `application/json` | [ApiError](#apierror) |
| 500 | 服务处理失败。 | `application/json` | [ApiError](#apierror) |

## create_image

**创建图片任务**

`POST /v1/images`

提交单个图片异步任务。保存 id 并通过查询接口读取最终结果。

**鉴权：** `Authorization: Bearer $PLATFORM_API_KEY`

### 路径、查询与请求头参数

无额外参数。

### 请求体

**Content-Type：** `application/json`；请求体必填：是。

**结构：** [CreateImage](#createimage)。完整嵌套字段见同名数据结构。

model、modelName、modelId 至少提供一项。JSON 参考媒体使用 URL。

至少满足一组：同时提供 `model`；或 同时提供 `modelName`；或 同时提供 `modelId`

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `model` | string | 否 | 查询模型目录，填写当前账户可用的公开模型 ID。 | 示例：`"YOUR_MODEL"` |
| `modelId` | string | 否 | 内部模型 ID 别名，优先于 modelName 和 model。 | — |
| `modelName` | string | 否 | 模型名称别名，优先于 model。 | — |
| `prompt` | string | 是 | 图片提示词，最大 10000 字符。 | 最长字符数：`10000` |
| `size` | string | 否 | 模型支持的尺寸或比例，如 1:1 或 1024x1024。 | — |
| `aspect_ratio` | string | 否 | 画面比例，如 16:9。 | — |
| `aspectRatio` | string | 否 | aspect_ratio 的兼容别名。 | — |
| `resolution` | string | 否 | 分辨率档位，如 2k。 | — |
| `quality` | string | 否 | 模型支持的质量档位。 | — |
| `style` | string | 否 | 模型支持的风格。 | — |
| `images` | array（string） | 否 | 参考素材 URL 数组；先上传素材可以取得可复用 URL。 | — |
| `image_urls` | array（string） | 否 | images 的兼容别名。 | — |
| `videos` | array（string） | 否 | 参考素材 URL 数组；先上传素材可以取得可复用 URL。 | — |
| `videoUrls` | array（string） | 否 | videos 的兼容别名。 | — |
| `audios` | array（string） | 否 | 参考素材 URL 数组；先上传素材可以取得可复用 URL。 | — |
| `audioUrls` | array（string） | 否 | audios 的兼容别名。 | — |
| `mask_url` | string | 否 | 局部重绘遮罩图 URL。 | — |
| `metadata` | object | 否 | 业务关联元数据。 | 允许额外字段 |
| `parameters` | object | 否 | 模型公开扩展参数；字段名与值以模型目录的 tasks[].parameters 为准。 | 允许额外字段 |
| `generationOptions` | object | 否 | 模型扩展参数兼容对象。 | 允许额外字段 |

### 请求示例：application/json

```bash
curl --request POST "${API_BASE_URL}/v1/images" \
  -H "Authorization: Bearer $PLATFORM_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
  "model": "YOUR_IMAGE_MODEL",
  "prompt": "一张咖啡产品海报，暖色自然光"
}'
```

### 响应

| HTTP 状态 | 含义 | Content-Type | 响应结构 |
| --- | --- | --- | --- |
| 200 | 请求成功。 | `application/json` | [Task](#task) |
| 400 | 参数或协议错误。 | `application/json` | [ApiError](#apierror) |
| 401 | 密钥缺失、无效、停用或跨站点使用。 | `application/json` | [ApiError](#apierror) |
| 402 | 余额或额度不足。 | `application/json` | [ApiError](#apierror) |
| 404 | 模型、任务或资源不存在。 | `application/json` | [ApiError](#apierror) |
| 429 | 频率或并发超过限制。 | `application/json` | [ApiError](#apierror) |
| 500 | 服务处理失败。 | `application/json` | [ApiError](#apierror) |

**HTTP 200 响应示例：**

```json
{
  "id": "task_example",
  "object": "image",
  "model": "YOUR_IMAGE_MODEL",
  "status": "queued",
  "progress": 0,
  "created_at": 1776843503
}
```

## get_image

**查询图片任务**

`GET /v1/images/{taskId}`

按 queued / processing / completed / failed 判断结果。完成后读取 url 或 images，失败读取 error。

**鉴权：** `Authorization: Bearer $PLATFORM_API_KEY`

### 路径、查询与请求头参数

| 位置 | 参数 | 类型 | 必填 | 说明与约束 |
| --- | --- | --- | --- | --- |
| path | `taskId` | string | 是 | 单个图片任务 id，来自 POST /v1/images。 |

### 请求体

无请求体。

### 请求示例

```bash
curl --request GET "${API_BASE_URL}/v1/images/YOUR_TASK_ID" \
  -H "Authorization: Bearer $PLATFORM_API_KEY"
```

### 响应

| HTTP 状态 | 含义 | Content-Type | 响应结构 |
| --- | --- | --- | --- |
| 200 | 请求成功。 | `application/json` | [Task](#task) |
| 400 | 参数或协议错误。 | `application/json` | [ApiError](#apierror) |
| 401 | 密钥缺失、无效、停用或跨站点使用。 | `application/json` | [ApiError](#apierror) |
| 402 | 余额或额度不足。 | `application/json` | [ApiError](#apierror) |
| 404 | 模型、任务或资源不存在。 | `application/json` | [ApiError](#apierror) |
| 429 | 频率或并发超过限制。 | `application/json` | [ApiError](#apierror) |
| 500 | 服务处理失败。 | `application/json` | [ApiError](#apierror) |

## image_generations

**OpenAI 图片生成**

`POST /v1/images/generations`

等待图片生成结束后返回 data[]。长时间生成建议使用 /async 接口，再轮询批次。

**鉴权：** `Authorization: Bearer $PLATFORM_API_KEY`

### 路径、查询与请求头参数

无额外参数。

### 请求体

**Content-Type：** `application/json`；请求体必填：是。

**结构：** [ImageGeneration](#imagegeneration)。完整嵌套字段见同名数据结构。

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `model` | string | 是 | 查询模型目录，填写当前账户可用的公开模型 ID。 | 示例：`"YOUR_MODEL"` |
| `prompt` | string | 是 | 非空提示词。 | 最短字符数：`1`；最长字符数：`10000` |
| `n` | integer | 否 | 生成数量，每张图片创建独立任务并计费。 | 默认：`1`；最小值：`1`；最大值：`128` |
| `response_format` | string | 否 | url 返回地址；b64_json 返回图片字节的 Base64。 | 枚举：`["url","b64_json"]`；默认：`"url"` |
| `size` | string | 否 | 模型支持的尺寸或比例。 | — |
| `quality` | string | 否 | — | — |
| `style` | string | 否 | — | — |
| `background` | string | 否 | — | — |
| `moderation` | string | 否 | — | — |
| `output_format` | string | 否 | — | — |
| `input_fidelity` | string | 否 | — | — |
| `output_compression` | integer | 否 | — | 最小值：`0`；最大值：`100` |
| `user` | string | 否 | — | — |
| `stream` | boolean | 否 | 此图片协议返回完整 JSON，使用 false。 | 默认：`false` |

### 请求示例：application/json

```bash
curl --request POST "${API_BASE_URL}/v1/images/generations" \
  -H "Authorization: Bearer $PLATFORM_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
  "model": "YOUR_IMAGE_MODEL",
  "prompt": "一张咖啡产品海报，暖色自然光",
  "n": 1,
  "response_format": "url"
}'
```

### 响应

| HTTP 状态 | 含义 | Content-Type | 响应结构 |
| --- | --- | --- | --- |
| 200 | 请求成功。 | `application/json` | [ImageResult](#imageresult) |
| 400 | 参数或协议错误。 | `application/json` | [ProtocolError](#protocolerror) |
| 401 | 密钥缺失、无效、停用或跨站点使用。 | `application/json` | [ProtocolError](#protocolerror) |
| 402 | 余额或额度不足。 | `application/json` | [ProtocolError](#protocolerror) |
| 404 | 模型、任务或资源不存在。 | `application/json` | [ProtocolError](#protocolerror) |
| 429 | 频率或并发超过限制。 | `application/json` | [ProtocolError](#protocolerror) |
| 500 | 服务处理失败。 | `application/json` | [ProtocolError](#protocolerror) |

## image_generations_async

**OpenAI 图片生成（异步）**

`POST /v1/images/generations/async`

返回 HTTP 202 和批次 UUID；按 Retry-After 轮询 /v1/images/tasks/\{taskId\}。批次与单个图片任务的 ID 和查询路径不同。

**鉴权：** `Authorization: Bearer $PLATFORM_API_KEY`

### 路径、查询与请求头参数

无额外参数。

### 请求体

**Content-Type：** `application/json`；请求体必填：是。

**结构：** [ImageGeneration](#imagegeneration)。完整嵌套字段见同名数据结构。

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `model` | string | 是 | 查询模型目录，填写当前账户可用的公开模型 ID。 | 示例：`"YOUR_MODEL"` |
| `prompt` | string | 是 | 非空提示词。 | 最短字符数：`1`；最长字符数：`10000` |
| `n` | integer | 否 | 生成数量，每张图片创建独立任务并计费。 | 默认：`1`；最小值：`1`；最大值：`128` |
| `response_format` | string | 否 | url 返回地址；b64_json 返回图片字节的 Base64。 | 枚举：`["url","b64_json"]`；默认：`"url"` |
| `size` | string | 否 | 模型支持的尺寸或比例。 | — |
| `quality` | string | 否 | — | — |
| `style` | string | 否 | — | — |
| `background` | string | 否 | — | — |
| `moderation` | string | 否 | — | — |
| `output_format` | string | 否 | — | — |
| `input_fidelity` | string | 否 | — | — |
| `output_compression` | integer | 否 | — | 最小值：`0`；最大值：`100` |
| `user` | string | 否 | — | — |
| `stream` | boolean | 否 | 此图片协议返回完整 JSON，使用 false。 | 默认：`false` |

### 请求示例：application/json

```bash
curl --request POST "${API_BASE_URL}/v1/images/generations/async" \
  -H "Authorization: Bearer $PLATFORM_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
  "model": "YOUR_IMAGE_MODEL",
  "prompt": "一张咖啡产品海报，暖色自然光",
  "n": 1,
  "response_format": "url"
}'
```

### 响应

| HTTP 状态 | 含义 | Content-Type | 响应结构 |
| --- | --- | --- | --- |
| 202 | 已接受异步批次。 | `application/json` | [ImageBatch](#imagebatch) |
| 400 | 参数或协议错误。 | `application/json` | [ProtocolError](#protocolerror) |
| 401 | 密钥缺失、无效、停用或跨站点使用。 | `application/json` | [ProtocolError](#protocolerror) |
| 402 | 余额或额度不足。 | `application/json` | [ProtocolError](#protocolerror) |
| 404 | 模型、任务或资源不存在。 | `application/json` | [ProtocolError](#protocolerror) |
| 429 | 频率或并发超过限制。 | `application/json` | [ProtocolError](#protocolerror) |
| 500 | 服务处理失败。 | `application/json` | [ProtocolError](#protocolerror) |

## image_edits

**OpenAI 图片编辑**

`POST /v1/images/edits`

等待图片生成结束后返回 data[]。长时间生成建议使用对应 /async 接口，再轮询批次。选择 multipart 可上传本地参考图。

**鉴权：** `Authorization: Bearer $PLATFORM_API_KEY`

### 路径、查询与请求头参数

无额外参数。

### 请求体

**Content-Type：** `application/json`；请求体必填：是。

**结构：** [ImageEdit](#imageedit)。完整嵌套字段见同名数据结构。

image 或 images 至少提供一项。

至少满足一组：同时提供 `image`；或 同时提供 `images`

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `model` | string | 是 | 查询模型目录，填写当前账户可用的公开模型 ID。 | 示例：`"YOUR_MODEL"` |
| `prompt` | string | 是 | 非空提示词。 | 最短字符数：`1`；最长字符数：`10000` |
| `n` | integer | 否 | 生成数量，每张图片创建独立任务并计费。 | 默认：`1`；最小值：`1`；最大值：`128` |
| `response_format` | string | 否 | url 返回地址；b64_json 返回图片字节的 Base64。 | 枚举：`["url","b64_json"]`；默认：`"url"` |
| `size` | string | 否 | 模型支持的尺寸或比例。 | — |
| `quality` | string | 否 | — | — |
| `style` | string | 否 | — | — |
| `background` | string | 否 | — | — |
| `moderation` | string | 否 | — | — |
| `output_format` | string | 否 | — | — |
| `input_fidelity` | string | 否 | — | — |
| `output_compression` | integer | 否 | — | 最小值：`0`；最大值：`100` |
| `user` | string | 否 | — | — |
| `stream` | boolean | 否 | 此图片协议返回完整 JSON，使用 false。 | 默认：`false` |
| `image` | string | 否 | 一张参考图的 HTTP(S) URL 或图片 Data URL。 | — |
| `images` | array（string） | 否 | 多张参考图 URL，最多 16 张，还受所选模型上限约束。 | 最多项数：`16` |
| `mask` | string | 否 | 遮罩图 URL 或图片 Data URL。 | — |

### 请求示例：application/json

```bash
curl --request POST "${API_BASE_URL}/v1/images/edits" \
  -H "Authorization: Bearer $PLATFORM_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
  "model": "YOUR_IMAGE_MODEL",
  "prompt": "保留主体，将背景换成浅灰色摄影棚",
  "n": 1,
  "response_format": "url",
  "image": "https://example.com/reference.png"
}'
```

**Content-Type：** `multipart/form-data`；请求体必填：是。

**结构：** [ImageEditUpload](#imageeditupload)。完整嵌套字段见同名数据结构。

image 或 image[] 至少提供一个文件。

至少满足一组：同时提供 `image`；或 同时提供 `image[]`

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `model` | string | 是 | 查询模型目录，填写当前账户可用的公开模型 ID。 | 示例：`"YOUR_MODEL"` |
| `prompt` | string | 是 | 非空提示词。 | 最短字符数：`1`；最长字符数：`10000` |
| `n` | integer | 否 | 生成数量，每张图片创建独立任务并计费。 | 默认：`1`；最小值：`1`；最大值：`128` |
| `response_format` | string | 否 | url 返回地址；b64_json 返回图片字节的 Base64。 | 枚举：`["url","b64_json"]`；默认：`"url"` |
| `size` | string | 否 | 模型支持的尺寸或比例。 | — |
| `quality` | string | 否 | — | — |
| `style` | string | 否 | — | — |
| `background` | string | 否 | — | — |
| `moderation` | string | 否 | — | — |
| `output_format` | string | 否 | — | — |
| `input_fidelity` | string | 否 | — | — |
| `output_compression` | integer | 否 | — | 最小值：`0`；最大值：`100` |
| `user` | string | 否 | — | — |
| `stream` | boolean | 否 | 此图片协议返回完整 JSON，使用 false。 | 默认：`false` |
| `image` | string (binary) | 否 | 单个参考图文件。 | — |
| `image[]` | array（string (binary)） | 否 | 多个参考图文件，可重复该字段。 | 最多项数：`16` |
| `mask` | string (binary) | 否 | 可选遮罩图文件。 | — |

### 请求示例：multipart/form-data

```bash
curl --request POST "${API_BASE_URL}/v1/images/edits" \
  -H "Authorization: Bearer $PLATFORM_API_KEY" \
  -F "model=YOUR_MODEL" \
  -F "prompt=用一句话描述你要生成的内容" \
  -F "image=@/path/to/reference.png"
```

### 响应

| HTTP 状态 | 含义 | Content-Type | 响应结构 |
| --- | --- | --- | --- |
| 200 | 请求成功。 | `application/json` | [ImageResult](#imageresult) |
| 400 | 参数或协议错误。 | `application/json` | [ProtocolError](#protocolerror) |
| 401 | 密钥缺失、无效、停用或跨站点使用。 | `application/json` | [ProtocolError](#protocolerror) |
| 402 | 余额或额度不足。 | `application/json` | [ProtocolError](#protocolerror) |
| 404 | 模型、任务或资源不存在。 | `application/json` | [ProtocolError](#protocolerror) |
| 429 | 频率或并发超过限制。 | `application/json` | [ProtocolError](#protocolerror) |
| 500 | 服务处理失败。 | `application/json` | [ProtocolError](#protocolerror) |

## image_edits_async

**OpenAI 图片编辑（异步）**

`POST /v1/images/edits/async`

返回 HTTP 202 和批次 UUID；按 Retry-After 轮询 /v1/images/tasks/\{taskId\}。批次与单个图片任务的 ID 和查询路径不同。

**鉴权：** `Authorization: Bearer $PLATFORM_API_KEY`

### 路径、查询与请求头参数

无额外参数。

### 请求体

**Content-Type：** `application/json`；请求体必填：是。

**结构：** [ImageEdit](#imageedit)。完整嵌套字段见同名数据结构。

image 或 images 至少提供一项。

至少满足一组：同时提供 `image`；或 同时提供 `images`

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `model` | string | 是 | 查询模型目录，填写当前账户可用的公开模型 ID。 | 示例：`"YOUR_MODEL"` |
| `prompt` | string | 是 | 非空提示词。 | 最短字符数：`1`；最长字符数：`10000` |
| `n` | integer | 否 | 生成数量，每张图片创建独立任务并计费。 | 默认：`1`；最小值：`1`；最大值：`128` |
| `response_format` | string | 否 | url 返回地址；b64_json 返回图片字节的 Base64。 | 枚举：`["url","b64_json"]`；默认：`"url"` |
| `size` | string | 否 | 模型支持的尺寸或比例。 | — |
| `quality` | string | 否 | — | — |
| `style` | string | 否 | — | — |
| `background` | string | 否 | — | — |
| `moderation` | string | 否 | — | — |
| `output_format` | string | 否 | — | — |
| `input_fidelity` | string | 否 | — | — |
| `output_compression` | integer | 否 | — | 最小值：`0`；最大值：`100` |
| `user` | string | 否 | — | — |
| `stream` | boolean | 否 | 此图片协议返回完整 JSON，使用 false。 | 默认：`false` |
| `image` | string | 否 | 一张参考图的 HTTP(S) URL 或图片 Data URL。 | — |
| `images` | array（string） | 否 | 多张参考图 URL，最多 16 张，还受所选模型上限约束。 | 最多项数：`16` |
| `mask` | string | 否 | 遮罩图 URL 或图片 Data URL。 | — |

### 请求示例：application/json

```bash
curl --request POST "${API_BASE_URL}/v1/images/edits/async" \
  -H "Authorization: Bearer $PLATFORM_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
  "model": "YOUR_IMAGE_MODEL",
  "prompt": "保留主体，将背景换成浅灰色摄影棚",
  "n": 1,
  "response_format": "url",
  "image": "https://example.com/reference.png"
}'
```

**Content-Type：** `multipart/form-data`；请求体必填：是。

**结构：** [ImageEditUpload](#imageeditupload)。完整嵌套字段见同名数据结构。

image 或 image[] 至少提供一个文件。

至少满足一组：同时提供 `image`；或 同时提供 `image[]`

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `model` | string | 是 | 查询模型目录，填写当前账户可用的公开模型 ID。 | 示例：`"YOUR_MODEL"` |
| `prompt` | string | 是 | 非空提示词。 | 最短字符数：`1`；最长字符数：`10000` |
| `n` | integer | 否 | 生成数量，每张图片创建独立任务并计费。 | 默认：`1`；最小值：`1`；最大值：`128` |
| `response_format` | string | 否 | url 返回地址；b64_json 返回图片字节的 Base64。 | 枚举：`["url","b64_json"]`；默认：`"url"` |
| `size` | string | 否 | 模型支持的尺寸或比例。 | — |
| `quality` | string | 否 | — | — |
| `style` | string | 否 | — | — |
| `background` | string | 否 | — | — |
| `moderation` | string | 否 | — | — |
| `output_format` | string | 否 | — | — |
| `input_fidelity` | string | 否 | — | — |
| `output_compression` | integer | 否 | — | 最小值：`0`；最大值：`100` |
| `user` | string | 否 | — | — |
| `stream` | boolean | 否 | 此图片协议返回完整 JSON，使用 false。 | 默认：`false` |
| `image` | string (binary) | 否 | 单个参考图文件。 | — |
| `image[]` | array（string (binary)） | 否 | 多个参考图文件，可重复该字段。 | 最多项数：`16` |
| `mask` | string (binary) | 否 | 可选遮罩图文件。 | — |

### 请求示例：multipart/form-data

```bash
curl --request POST "${API_BASE_URL}/v1/images/edits/async" \
  -H "Authorization: Bearer $PLATFORM_API_KEY" \
  -F "model=YOUR_MODEL" \
  -F "prompt=用一句话描述你要生成的内容" \
  -F "image=@/path/to/reference.png"
```

### 响应

| HTTP 状态 | 含义 | Content-Type | 响应结构 |
| --- | --- | --- | --- |
| 202 | 已接受异步批次。 | `application/json` | [ImageBatch](#imagebatch) |
| 400 | 参数或协议错误。 | `application/json` | [ProtocolError](#protocolerror) |
| 401 | 密钥缺失、无效、停用或跨站点使用。 | `application/json` | [ProtocolError](#protocolerror) |
| 402 | 余额或额度不足。 | `application/json` | [ProtocolError](#protocolerror) |
| 404 | 模型、任务或资源不存在。 | `application/json` | [ProtocolError](#protocolerror) |
| 429 | 频率或并发超过限制。 | `application/json` | [ProtocolError](#protocolerror) |
| 500 | 服务处理失败。 | `application/json` | [ProtocolError](#protocolerror) |

## get_image_batch

**查询图片批次**

`GET /v1/images/tasks/{taskId}`

读取 processing、completed 或 failed。完成时检查 result.data、partial 和 errors；查询 HTTP 200 仍可能表示生成失败。

**鉴权：** `Authorization: Bearer $PLATFORM_API_KEY`

### 路径、查询与请求头参数

| 位置 | 参数 | 类型 | 必填 | 说明与约束 |
| --- | --- | --- | --- | --- |
| path | `taskId` | string (uuid) | 是 | 异步批次返回的 id 或 task_id。 |

### 请求体

无请求体。

### 请求示例

```bash
curl --request GET "${API_BASE_URL}/v1/images/tasks/YOUR_TASK_ID" \
  -H "Authorization: Bearer $PLATFORM_API_KEY"
```

### 响应

| HTTP 状态 | 含义 | Content-Type | 响应结构 |
| --- | --- | --- | --- |
| 200 | 请求成功。 | `application/json` | [ImageBatch](#imagebatch) |
| 400 | 参数或协议错误。 | `application/json` | [ProtocolError](#protocolerror) |
| 401 | 密钥缺失、无效、停用或跨站点使用。 | `application/json` | [ProtocolError](#protocolerror) |
| 402 | 余额或额度不足。 | `application/json` | [ProtocolError](#protocolerror) |
| 404 | 模型、任务或资源不存在。 | `application/json` | [ProtocolError](#protocolerror) |
| 429 | 频率或并发超过限制。 | `application/json` | [ProtocolError](#protocolerror) |
| 500 | 服务处理失败。 | `application/json` | [ProtocolError](#protocolerror) |

## create_video

**创建视频任务**

`POST /v1/videos`

提交视频异步任务，按模型能力选择时长、比例和参考素材。JSON 使用素材 URL，multipart 可上传参考图。

**鉴权：** `Authorization: Bearer $PLATFORM_API_KEY`

### 路径、查询与请求头参数

无额外参数。

### 请求体

**Content-Type：** `application/json`；请求体必填：是。

**结构：** [CreateVideo](#createvideo)。完整嵌套字段见同名数据结构。

model、modelName、modelId 至少提供一项。所选模型决定支持的媒体、时长、比例和分辨率。

至少满足一组：同时提供 `model`；或 同时提供 `modelName`；或 同时提供 `modelId`

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `model` | string | 否 | 查询模型目录，填写当前账户可用的公开模型 ID。 | 示例：`"YOUR_MODEL"` |
| `modelId` | string | 否 | 内部模型 ID 别名，优先于 modelName 和 model。 | — |
| `modelName` | string | 否 | 模型名称别名，优先于 model。 | — |
| `prompt` | string | 是 | 视频生成提示词。 | — |
| `size` | string | 否 | 模型支持的尺寸或比例，如 1:1 或 1024x1024。 | — |
| `aspect_ratio` | string | 否 | 画面比例，如 16:9。 | — |
| `aspectRatio` | string | 否 | aspect_ratio 的兼容别名。 | — |
| `resolution` | string | 否 | 分辨率档位，如 2k。 | — |
| `images` | array（string） | 否 | 参考素材 URL 数组；先上传素材可以取得可复用 URL。 | — |
| `videos` | array（string） | 否 | 参考素材 URL 数组；先上传素材可以取得可复用 URL。 | — |
| `videoUrls` | array（string） | 否 | videos 的兼容别名。 | — |
| `audios` | array（string） | 否 | 参考素材 URL 数组；先上传素材可以取得可复用 URL。 | — |
| `audioUrls` | array（string） | 否 | audios 的兼容别名。 | — |
| `metadata` | object | 否 | 业务关联元数据。 | 允许额外字段 |
| `parameters` | object | 否 | 模型公开扩展参数；字段名与值以模型目录的 tasks[].parameters 为准。 | 允许额外字段 |
| `generationOptions` | object | 否 | 模型扩展参数兼容对象。 | 允许额外字段 |
| `seconds` | string | 否 | 正数时长，单位秒。JSON 同样接受数字；multipart 使用文本。 | 示例：`"10"` |
| `duration` | string | 否 | seconds 的兼容别名，选择其中一个。 | — |
| `mode` | string | 否 | 模型支持的生成模式。 | — |
| `video_urls` | array（string） | 否 | videos 的兼容别名。 | — |
| `video_url` | string | 否 | 单个参考视频 URL。 | — |
| `audio_urls` | array（string） | 否 | audios 的兼容别名。 | — |
| `audio_url` | string | 否 | 单个参考音频 URL。 | — |
| `upload_method` | string | 否 | — | 枚举：`["s3","oss"]` |

### 请求示例：application/json

```bash
curl --request POST "${API_BASE_URL}/v1/videos" \
  -H "Authorization: Bearer $PLATFORM_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
  "model": "YOUR_VIDEO_MODEL",
  "prompt": "一只小猫在阳光下玩耍，电影感"
}'
```

**Content-Type：** `multipart/form-data`；请求体必填：是。

**结构：** [CreateVideoUpload](#createvideoupload)。完整嵌套字段见同名数据结构。

至少满足一组：同时提供 `model`；或 同时提供 `modelName`；或 同时提供 `modelId`

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `model` | string | 否 | 查询模型目录，填写当前账户可用的公开模型 ID。 | 示例：`"YOUR_MODEL"` |
| `modelId` | string | 否 | 内部模型 ID 别名，优先于 modelName 和 model。 | — |
| `modelName` | string | 否 | 模型名称别名，优先于 model。 | — |
| `prompt` | string | 是 | 视频生成提示词。 | — |
| `size` | string | 否 | 模型支持的尺寸或比例，如 1:1 或 1024x1024。 | — |
| `aspect_ratio` | string | 否 | 画面比例，如 16:9。 | — |
| `aspectRatio` | string | 否 | aspect_ratio 的兼容别名。 | — |
| `resolution` | string | 否 | 分辨率档位，如 2k。 | — |
| `images` | array（string） | 否 | 参考素材 URL 数组；先上传素材可以取得可复用 URL。 | — |
| `videos` | array（string） | 否 | 参考素材 URL 数组；先上传素材可以取得可复用 URL。 | — |
| `videoUrls` | array（string） | 否 | videos 的兼容别名。 | — |
| `audios` | array（string） | 否 | 参考素材 URL 数组；先上传素材可以取得可复用 URL。 | — |
| `audioUrls` | array（string） | 否 | audios 的兼容别名。 | — |
| `metadata` | string | 否 | JSON 文本，例如 \{"order_id":"order_123"\}。 | — |
| `parameters` | string | 否 | JSON 文本，例如 \{"order_id":"order_123"\}。 | — |
| `generationOptions` | string | 否 | JSON 文本，例如 \{"order_id":"order_123"\}。 | — |
| `seconds` | string | 否 | 正数时长，单位秒。JSON 同样接受数字；multipart 使用文本。 | 示例：`"10"` |
| `duration` | string | 否 | seconds 的兼容别名，选择其中一个。 | — |
| `mode` | string | 否 | 模型支持的生成模式。 | — |
| `video_urls` | array（string） | 否 | videos 的兼容别名。 | — |
| `video_url` | string | 否 | 单个参考视频 URL。 | — |
| `audio_urls` | array（string） | 否 | audios 的兼容别名。 | — |
| `audio_url` | string | 否 | 单个参考音频 URL。 | — |
| `upload_method` | string | 否 | — | 枚举：`["s3","oss"]` |
| `input_reference` | array（string (binary)） | 否 | 参考图片文件，多图重复同一字段。 | — |

### 请求示例：multipart/form-data

```bash
curl --request POST "${API_BASE_URL}/v1/videos" \
  -H "Authorization: Bearer $PLATFORM_API_KEY" \
  -F "model=YOUR_MODEL" \
  -F "prompt=用一句话描述你要生成的内容"
```

### 响应

| HTTP 状态 | 含义 | Content-Type | 响应结构 |
| --- | --- | --- | --- |
| 200 | 请求成功。 | `application/json` | [Task](#task) |
| 400 | 参数或协议错误。 | `application/json` | [ApiError](#apierror) |
| 401 | 密钥缺失、无效、停用或跨站点使用。 | `application/json` | [ApiError](#apierror) |
| 402 | 余额或额度不足。 | `application/json` | [ApiError](#apierror) |
| 404 | 模型、任务或资源不存在。 | `application/json` | [ApiError](#apierror) |
| 429 | 频率或并发超过限制。 | `application/json` | [ApiError](#apierror) |
| 500 | 服务处理失败。 | `application/json` | [ApiError](#apierror) |

**HTTP 200 响应示例：**

```json
{
  "id": "task_example",
  "object": "video",
  "model": "YOUR_VIDEO_MODEL",
  "status": "queued",
  "progress": 0,
  "created_at": 1776843503
}
```

## get_video

**查询视频任务**

`GET /v1/videos/{taskId}`

完成后读取 video_url；失败时读取 error。created_at 等时间戳使用 Unix 秒，processing_time 为毫秒。

**鉴权：** `Authorization: Bearer $PLATFORM_API_KEY`

### 路径、查询与请求头参数

| 位置 | 参数 | 类型 | 必填 | 说明与约束 |
| --- | --- | --- | --- | --- |
| path | `taskId` | string | 是 | 视频创建接口实际返回的 id。 |

### 请求体

无请求体。

### 请求示例

```bash
curl --request GET "${API_BASE_URL}/v1/videos/YOUR_TASK_ID" \
  -H "Authorization: Bearer $PLATFORM_API_KEY"
```

### 响应

| HTTP 状态 | 含义 | Content-Type | 响应结构 |
| --- | --- | --- | --- |
| 200 | 请求成功。 | `application/json` | [Task](#task) |
| 400 | 参数或协议错误。 | `application/json` | [ApiError](#apierror) |
| 401 | 密钥缺失、无效、停用或跨站点使用。 | `application/json` | [ApiError](#apierror) |
| 402 | 余额或额度不足。 | `application/json` | [ApiError](#apierror) |
| 404 | 模型、任务或资源不存在。 | `application/json` | [ApiError](#apierror) |
| 429 | 频率或并发超过限制。 | `application/json` | [ApiError](#apierror) |
| 500 | 服务处理失败。 | `application/json` | [ApiError](#apierror) |

## chat_completions

**Chat Completions**

`POST /v1/chat/completions`

发送 messages，读取 choices[].message。stream=true 时返回 SSE；先查询模型支持的操作。

**鉴权：** `Authorization: Bearer $PLATFORM_API_KEY`

### 路径、查询与请求头参数

无额外参数。

### 请求体

**Content-Type：** `application/json`；请求体必填：是。

**结构：** [ChatRequest](#chatrequest)。完整嵌套字段见同名数据结构。

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `model` | string | 是 | 查询模型目录，填写当前账户可用的公开模型 ID。 | 示例：`"YOUR_MODEL"` |
| `messages` | array（[ChatMessage](#chatmessage)） | 是 | — | 最少项数：`1` |
| `stream` | boolean | 否 | true 使用 SSE。 | 默认：`false` |
| `stream_options` | object | 否 | — | — |
| `stream_options.include_usage` | boolean | 否 | — | — |
| `max_tokens` | integer | 否 | 输出上限；与 max_completion_tokens 按模型支持选择。 | 最小值：`1` |
| `max_completion_tokens` | integer | 否 | — | 最小值：`1` |
| `temperature` | number | 否 | — | — |
| `top_p` | number | 否 | — | — |
| `stop` | string oneOf array（string） | 否 | — | 恰好满足一组：string；或 array（string） |
| `tools` | array（object） | 否 | — | — |
| `tool_choice` | 任意 JSON | 否 | — | — |
| `response_format` | object | 否 | — | 允许额外字段 |

### 请求示例：application/json

```bash
curl --request POST "${API_BASE_URL}/v1/chat/completions" \
  -H "Authorization: Bearer $PLATFORM_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
  "model": "YOUR_CHAT_MODEL",
  "messages": [
    {
      "role": "user",
      "content": "用一句话解释异步任务"
    }
  ],
  "stream": false
}'
```

### 响应

| HTTP 状态 | 含义 | Content-Type | 响应结构 |
| --- | --- | --- | --- |
| 200 | 请求成功。 | `application/json` | [ChatResponse](#chatresponse) |
| 200 | 请求成功。 | `text/event-stream` | string |
| 400 | 参数或协议错误。 | `application/json` | [ProtocolError](#protocolerror) |
| 401 | 密钥缺失、无效、停用或跨站点使用。 | `application/json` | [ProtocolError](#protocolerror) |
| 402 | 余额或额度不足。 | `application/json` | [ProtocolError](#protocolerror) |
| 404 | 模型、任务或资源不存在。 | `application/json` | [ProtocolError](#protocolerror) |
| 429 | 频率或并发超过限制。 | `application/json` | [ProtocolError](#protocolerror) |
| 500 | 服务处理失败。 | `application/json` | [ProtocolError](#protocolerror) |

**HTTP 200 SSE：** SSE 事件流；将请求的 stream 设为 true。

## create_response

**OpenAI Responses**

`POST /v1/responses`

发送 input，读取 output。续接、存储和后台响应依赖原生上游能力及当前模型配置。

**鉴权：** `Authorization: Bearer $PLATFORM_API_KEY`

### 路径、查询与请求头参数

无额外参数。

### 请求体

**Content-Type：** `application/json`；请求体必填：是。

**结构：** [ResponsesRequest](#responsesrequest)。完整嵌套字段见同名数据结构。

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `model` | string | 是 | 查询模型目录，填写当前账户可用的公开模型 ID。 | 示例：`"YOUR_MODEL"` |
| `input` | string oneOf array（object） | 是 | 文本或 Responses 原生输入项。 | 恰好满足一组：string；或 array（object） |
| `instructions` | string | 否 | — | — |
| `max_output_tokens` | integer | 否 | — | 最小值：`1` |
| `stream` | boolean | 否 | — | 默认：`false` |
| `previous_response_id` | string | 否 | 同账户已保存的响应 ID；上游需支持续接。 | — |
| `tools` | array（object） | 否 | — | — |
| `tool_choice` | 任意 JSON | 否 | — | — |
| `store` | boolean | 否 | — | — |
| `background` | boolean | 否 | 仅在上游支持后台响应时启用。 | — |
| `temperature` | number | 否 | — | — |
| `text` | object | 否 | — | 允许额外字段 |
| `reasoning` | object | 否 | — | 允许额外字段 |

### 请求示例：application/json

```bash
curl --request POST "${API_BASE_URL}/v1/responses" \
  -H "Authorization: Bearer $PLATFORM_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
  "model": "YOUR_RESPONSES_MODEL",
  "input": "用一句话解释异步任务",
  "max_output_tokens": 512,
  "stream": false
}'
```

### 响应

| HTTP 状态 | 含义 | Content-Type | 响应结构 |
| --- | --- | --- | --- |
| 200 | 请求成功。 | `application/json` | [ResponsesResponse](#responsesresponse) |
| 200 | 请求成功。 | `text/event-stream` | string |
| 400 | 参数或协议错误。 | `application/json` | [ProtocolError](#protocolerror) |
| 401 | 密钥缺失、无效、停用或跨站点使用。 | `application/json` | [ProtocolError](#protocolerror) |
| 402 | 余额或额度不足。 | `application/json` | [ProtocolError](#protocolerror) |
| 404 | 模型、任务或资源不存在。 | `application/json` | [ProtocolError](#protocolerror) |
| 429 | 频率或并发超过限制。 | `application/json` | [ProtocolError](#protocolerror) |
| 500 | 服务处理失败。 | `application/json` | [ProtocolError](#protocolerror) |

**HTTP 200 SSE：** SSE 事件流；将请求的 stream 设为 true。

## anthropic_messages

**Anthropic Messages**

`POST /v1/messages`

系统指令放在顶层 system。max_tokens 必填；读取 content 中的 text 块。stream=true 使用 SSE。

**鉴权：** `X-API-Key: $PLATFORM_API_KEY`

### 路径、查询与请求头参数

| 位置 | 参数 | 类型 | 必填 | 说明与约束 |
| --- | --- | --- | --- | --- |
| header | `anthropic-version` | string | 是 | Anthropic 协议版本。；默认：`"2023-06-01"` |

### 请求体

**Content-Type：** `application/json`；请求体必填：是。

**结构：** [AnthropicRequest](#anthropicrequest)。完整嵌套字段见同名数据结构。

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `model` | string | 是 | 查询模型目录，填写当前账户可用的公开模型 ID。 | 示例：`"YOUR_MODEL"` |
| `messages` | array（[AnthropicMessage](#anthropicmessage)） | 是 | — | 最少项数：`1` |
| `system` | string oneOf array（object） | 否 | — | 恰好满足一组：string；或 array（object） |
| `tools` | array（object） | 否 | — | — |
| `tool_choice` | object | 否 | — | 允许额外字段 |
| `thinking` | object | 否 | — | 允许额外字段 |
| `max_tokens` | integer | 是 | 必填输出上限，遵守模型限制。 | 最小值：`1` |
| `stream` | boolean | 否 | — | 默认：`false` |
| `temperature` | number | 否 | — | — |
| `top_p` | number | 否 | — | — |
| `stop_sequences` | array（string） | 否 | — | — |

### 请求示例：application/json

```bash
curl --request POST "${API_BASE_URL}/v1/messages" \
  -H "X-API-Key: $PLATFORM_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  --data '{
  "model": "YOUR_MESSAGES_MODEL",
  "messages": [
    {
      "role": "user",
      "content": "用一句话解释异步任务"
    }
  ],
  "max_tokens": 512,
  "stream": false
}'
```

### 响应

| HTTP 状态 | 含义 | Content-Type | 响应结构 |
| --- | --- | --- | --- |
| 200 | 请求成功。 | `application/json` | [AnthropicResponse](#anthropicresponse) |
| 200 | 请求成功。 | `text/event-stream` | string |
| 400 | 参数或协议错误。 | `application/json` | [ProtocolError](#protocolerror) |
| 401 | 密钥缺失、无效、停用或跨站点使用。 | `application/json` | [ProtocolError](#protocolerror) |
| 402 | 余额或额度不足。 | `application/json` | [ProtocolError](#protocolerror) |
| 404 | 模型、任务或资源不存在。 | `application/json` | [ProtocolError](#protocolerror) |
| 429 | 频率或并发超过限制。 | `application/json` | [ProtocolError](#protocolerror) |
| 500 | 服务处理失败。 | `application/json` | [ProtocolError](#protocolerror) |

**HTTP 200 SSE：** SSE 事件流；将请求的 stream 设为 true。

## gemini_generate

**Gemini GenerateContent**

`POST /v1beta/models/{model}:generateContent`

模型名在 URL 中。发送 contents，读取 candidates[].content.parts；用量来自 usageMetadata。

**鉴权：** `x-goog-api-key: $PLATFORM_API_KEY`

### 路径、查询与请求头参数

| 位置 | 参数 | 类型 | 必填 | 说明与约束 |
| --- | --- | --- | --- | --- |
| path | `model` | string | 是 | Gemini 公开模型 ID，不含 models/ 前缀。；示例：`"YOUR_GEMINI_MODEL"` |

### 请求体

**Content-Type：** `application/json`；请求体必填：是。

**结构：** [GeminiRequest](#geminirequest)。完整嵌套字段见同名数据结构。

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `contents` | array（[GeminiContent](#geminicontent)） | 是 | — | 最少项数：`1` |
| `systemInstruction` | [GeminiContent](#geminicontent) | 否 | — | — |
| `generationConfig` | object | 否 | — | 允许额外字段 |
| `generationConfig.maxOutputTokens` | integer | 否 | — | 最小值：`1` |
| `generationConfig.temperature` | number | 否 | — | — |
| `generationConfig.topP` | number | 否 | — | — |
| `generationConfig.responseMimeType` | string | 否 | — | — |
| `generationConfig.responseSchema` | object | 否 | — | 允许额外字段 |
| `tools` | array（object） | 否 | — | — |
| `toolConfig` | object | 否 | — | 允许额外字段 |
| `safetySettings` | array（object） | 否 | — | — |

### 请求示例：application/json

```bash
curl --request POST "${API_BASE_URL}/v1beta/models/YOUR_GEMINI_MODEL:generateContent" \
  -H "x-goog-api-key: $PLATFORM_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": "用一句话解释异步任务"
        }
      ]
    }
  ],
  "generationConfig": {
    "maxOutputTokens": 512
  }
}'
```

### 响应

| HTTP 状态 | 含义 | Content-Type | 响应结构 |
| --- | --- | --- | --- |
| 200 | 请求成功。 | `application/json` | [GeminiResponse](#geminiresponse) |
| 400 | 参数或协议错误。 | `application/json` | [ProtocolError](#protocolerror) |
| 401 | 密钥缺失、无效、停用或跨站点使用。 | `application/json` | [ProtocolError](#protocolerror) |
| 402 | 余额或额度不足。 | `application/json` | [ProtocolError](#protocolerror) |
| 404 | 模型、任务或资源不存在。 | `application/json` | [ProtocolError](#protocolerror) |
| 429 | 频率或并发超过限制。 | `application/json` | [ProtocolError](#protocolerror) |
| 500 | 服务处理失败。 | `application/json` | [ProtocolError](#protocolerror) |

## gemini_stream

**Gemini 流式生成**

`POST /v1beta/models/{model}:streamGenerateContent`

使用 alt=sse，按 data: JSON 事件读取文本增量及最终用量。

**鉴权：** `x-goog-api-key: $PLATFORM_API_KEY`

### 路径、查询与请求头参数

| 位置 | 参数 | 类型 | 必填 | 说明与约束 |
| --- | --- | --- | --- | --- |
| path | `model` | string | 是 | Gemini 公开模型 ID，不含 models/ 前缀。；示例：`"YOUR_GEMINI_MODEL"` |
| query | `alt` | string | 是 | 枚举：`["sse"]`；默认：`"sse"` |

### 请求体

**Content-Type：** `application/json`；请求体必填：是。

**结构：** [GeminiRequest](#geminirequest)。完整嵌套字段见同名数据结构。

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `contents` | array（[GeminiContent](#geminicontent)） | 是 | — | 最少项数：`1` |
| `systemInstruction` | [GeminiContent](#geminicontent) | 否 | — | — |
| `generationConfig` | object | 否 | — | 允许额外字段 |
| `generationConfig.maxOutputTokens` | integer | 否 | — | 最小值：`1` |
| `generationConfig.temperature` | number | 否 | — | — |
| `generationConfig.topP` | number | 否 | — | — |
| `generationConfig.responseMimeType` | string | 否 | — | — |
| `generationConfig.responseSchema` | object | 否 | — | 允许额外字段 |
| `tools` | array（object） | 否 | — | — |
| `toolConfig` | object | 否 | — | 允许额外字段 |
| `safetySettings` | array（object） | 否 | — | — |

### 请求示例：application/json

```bash
curl -N --request POST "${API_BASE_URL}/v1beta/models/YOUR_GEMINI_MODEL:streamGenerateContent?alt=sse" \
  -H "x-goog-api-key: $PLATFORM_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": "用一句话解释异步任务"
        }
      ]
    }
  ],
  "generationConfig": {
    "maxOutputTokens": 512
  }
}'
```

### 响应

| HTTP 状态 | 含义 | Content-Type | 响应结构 |
| --- | --- | --- | --- |
| 200 | 请求成功。 | `text/event-stream` | string |
| 400 | 参数或协议错误。 | `application/json` | [ProtocolError](#protocolerror) |
| 401 | 密钥缺失、无效、停用或跨站点使用。 | `application/json` | [ProtocolError](#protocolerror) |
| 402 | 余额或额度不足。 | `application/json` | [ProtocolError](#protocolerror) |
| 404 | 模型、任务或资源不存在。 | `application/json` | [ProtocolError](#protocolerror) |
| 429 | 频率或并发超过限制。 | `application/json` | [ProtocolError](#protocolerror) |
| 500 | 服务处理失败。 | `application/json` | [ProtocolError](#protocolerror) |

**HTTP 200 SSE：** Gemini SSE JSON 事件流。

## get_response

**查询 Responses 响应**

`GET /v1/responses/{responseId}`

使用原创建请求的账户与路由访问资源；查询、取消及输入项依赖上游原生 Responses 和存储能力。

**鉴权：** `Authorization: Bearer $PLATFORM_API_KEY`

### 路径、查询与请求头参数

| 位置 | 参数 | 类型 | 必填 | 说明与约束 |
| --- | --- | --- | --- | --- |
| path | `responseId` | string | 是 | 同账户通过 Responses 创建获得的实际响应 ID。；示例：`"resp_example"` |

### 请求体

无请求体。

### 请求示例

```bash
curl --request GET "${API_BASE_URL}/v1/responses/resp_example" \
  -H "Authorization: Bearer $PLATFORM_API_KEY"
```

### 响应

| HTTP 状态 | 含义 | Content-Type | 响应结构 |
| --- | --- | --- | --- |
| 200 | 请求成功。 | `application/json` | [ResponsesResponse](#responsesresponse) |
| 400 | 参数或协议错误。 | `application/json` | [ProtocolError](#protocolerror) |
| 401 | 密钥缺失、无效、停用或跨站点使用。 | `application/json` | [ProtocolError](#protocolerror) |
| 402 | 余额或额度不足。 | `application/json` | [ProtocolError](#protocolerror) |
| 404 | 模型、任务或资源不存在。 | `application/json` | [ProtocolError](#protocolerror) |
| 429 | 频率或并发超过限制。 | `application/json` | [ProtocolError](#protocolerror) |
| 500 | 服务处理失败。 | `application/json` | [ProtocolError](#protocolerror) |

## delete_response

**删除 Responses 响应**

`DELETE /v1/responses/{responseId}`

使用原创建请求的账户与路由访问资源；依赖原生 Responses 存储能力。删除前需确认账务已完成，usage_pending 时返回 409。

**鉴权：** `Authorization: Bearer $PLATFORM_API_KEY`

### 路径、查询与请求头参数

| 位置 | 参数 | 类型 | 必填 | 说明与约束 |
| --- | --- | --- | --- | --- |
| path | `responseId` | string | 是 | 同账户通过 Responses 创建获得的实际响应 ID。；示例：`"resp_example"` |

### 请求体

无请求体。

### 请求示例

```bash
curl --request DELETE "${API_BASE_URL}/v1/responses/resp_example" \
  -H "Authorization: Bearer $PLATFORM_API_KEY"
```

### 响应

| HTTP 状态 | 含义 | Content-Type | 响应结构 |
| --- | --- | --- | --- |
| 200 | 请求成功。 | `application/json` | [ResponseDeleted](#responsedeleted) |
| 400 | 参数或协议错误。 | `application/json` | [ProtocolError](#protocolerror) |
| 401 | 密钥缺失、无效、停用或跨站点使用。 | `application/json` | [ProtocolError](#protocolerror) |
| 402 | 余额或额度不足。 | `application/json` | [ProtocolError](#protocolerror) |
| 404 | 模型、任务或资源不存在。 | `application/json` | [ProtocolError](#protocolerror) |
| 429 | 频率或并发超过限制。 | `application/json` | [ProtocolError](#protocolerror) |
| 500 | 服务处理失败。 | `application/json` | [ProtocolError](#protocolerror) |
| 409 | usage_pending：账务尚未核对完成，请保留响应资源。 | `application/json` | [ProtocolError](#protocolerror) |

## cancel_response

**取消 Responses 响应**

`POST /v1/responses/{responseId}/cancel`

使用原创建请求的账户与路由访问资源；查询、取消及输入项依赖上游原生 Responses 和存储能力。

**鉴权：** `Authorization: Bearer $PLATFORM_API_KEY`

### 路径、查询与请求头参数

| 位置 | 参数 | 类型 | 必填 | 说明与约束 |
| --- | --- | --- | --- | --- |
| path | `responseId` | string | 是 | 同账户通过 Responses 创建获得的实际响应 ID。；示例：`"resp_example"` |

### 请求体

无请求体。

### 请求示例

```bash
curl --request POST "${API_BASE_URL}/v1/responses/resp_example/cancel" \
  -H "Authorization: Bearer $PLATFORM_API_KEY"
```

### 响应

| HTTP 状态 | 含义 | Content-Type | 响应结构 |
| --- | --- | --- | --- |
| 200 | 请求成功。 | `application/json` | [ResponsesResponse](#responsesresponse) |
| 400 | 参数或协议错误。 | `application/json` | [ProtocolError](#protocolerror) |
| 401 | 密钥缺失、无效、停用或跨站点使用。 | `application/json` | [ProtocolError](#protocolerror) |
| 402 | 余额或额度不足。 | `application/json` | [ProtocolError](#protocolerror) |
| 404 | 模型、任务或资源不存在。 | `application/json` | [ProtocolError](#protocolerror) |
| 429 | 频率或并发超过限制。 | `application/json` | [ProtocolError](#protocolerror) |
| 500 | 服务处理失败。 | `application/json` | [ProtocolError](#protocolerror) |

## response_input_items

**查询 Responses 输入项**

`GET /v1/responses/{responseId}/input_items`

使用原创建请求的账户与路由访问资源；查询、取消及输入项依赖上游原生 Responses 和存储能力。

**鉴权：** `Authorization: Bearer $PLATFORM_API_KEY`

### 路径、查询与请求头参数

| 位置 | 参数 | 类型 | 必填 | 说明与约束 |
| --- | --- | --- | --- | --- |
| path | `responseId` | string | 是 | 同账户通过 Responses 创建获得的实际响应 ID。；示例：`"resp_example"` |
| query | `limit` | integer | 否 | 最小值：`1`；最大值：`100` |
| query | `after` | string | 否 | — |
| query | `before` | string | 否 | — |
| query | `order` | string | 否 | 枚举：`["asc","desc"]` |

### 请求体

无请求体。

### 请求示例

```bash
curl --request GET "${API_BASE_URL}/v1/responses/resp_example/input_items" \
  -H "Authorization: Bearer $PLATFORM_API_KEY"
```

### 响应

| HTTP 状态 | 含义 | Content-Type | 响应结构 |
| --- | --- | --- | --- |
| 200 | 请求成功。 | `application/json` | [ResponseInputItems](#responseinputitems) |
| 400 | 参数或协议错误。 | `application/json` | [ProtocolError](#protocolerror) |
| 401 | 密钥缺失、无效、停用或跨站点使用。 | `application/json` | [ProtocolError](#protocolerror) |
| 402 | 余额或额度不足。 | `application/json` | [ProtocolError](#protocolerror) |
| 404 | 模型、任务或资源不存在。 | `application/json` | [ProtocolError](#protocolerror) |
| 429 | 频率或并发超过限制。 | `application/json` | [ProtocolError](#protocolerror) |
| 500 | 服务处理失败。 | `application/json` | [ProtocolError](#protocolerror) |

## compact_response

**压缩 Responses 上下文**

`POST /v1/responses/compact`

仅用于声明支持对应操作的模型和供应商。返回完整 JSON。

**鉴权：** `Authorization: Bearer $PLATFORM_API_KEY`

### 路径、查询与请求头参数

无额外参数。

### 请求体

**Content-Type：** `application/json`；请求体必填：是。

**结构：** [ResponsesCompactRequest](#responsescompactrequest)。完整嵌套字段见同名数据结构。

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `model` | string | 是 | 查询模型目录，填写当前账户可用的公开模型 ID。 | 示例：`"YOUR_MODEL"` |
| `input` | string oneOf array（object） | 是 | 文本或 Responses 原生输入项。 | 恰好满足一组：string；或 array（object） |
| `instructions` | string | 否 | — | — |
| `previous_response_id` | string | 否 | 同账户已保存的响应 ID；上游需支持续接。 | — |
| `tools` | array（object） | 否 | — | — |
| `tool_choice` | 任意 JSON | 否 | — | — |
| `store` | boolean | 否 | — | — |
| `background` | boolean | 否 | 仅在上游支持后台响应时启用。 | — |
| `temperature` | number | 否 | — | — |
| `text` | object | 否 | — | 允许额外字段 |
| `reasoning` | object | 否 | — | 允许额外字段 |

### 请求示例：application/json

```bash
curl --request POST "${API_BASE_URL}/v1/responses/compact" \
  -H "Authorization: Bearer $PLATFORM_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
  "model": "YOUR_RESPONSES_MODEL",
  "input": "用一句话解释异步任务"
}'
```

### 响应

| HTTP 状态 | 含义 | Content-Type | 响应结构 |
| --- | --- | --- | --- |
| 200 | 请求成功。 | `application/json` | [ResponsesResponse](#responsesresponse) |
| 400 | 参数或协议错误。 | `application/json` | [ProtocolError](#protocolerror) |
| 401 | 密钥缺失、无效、停用或跨站点使用。 | `application/json` | [ProtocolError](#protocolerror) |
| 402 | 余额或额度不足。 | `application/json` | [ProtocolError](#protocolerror) |
| 404 | 模型、任务或资源不存在。 | `application/json` | [ProtocolError](#protocolerror) |
| 429 | 频率或并发超过限制。 | `application/json` | [ProtocolError](#protocolerror) |
| 500 | 服务处理失败。 | `application/json` | [ProtocolError](#protocolerror) |

## response_input_tokens

**统计 Responses 输入 Token**

`POST /v1/responses/input_tokens`

仅用于声明支持对应操作的模型和供应商。返回完整 JSON。

**鉴权：** `Authorization: Bearer $PLATFORM_API_KEY`

### 路径、查询与请求头参数

无额外参数。

### 请求体

**Content-Type：** `application/json`；请求体必填：是。

**结构：** [ResponsesInputTokensRequest](#responsesinputtokensrequest)。完整嵌套字段见同名数据结构。

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `model` | string | 是 | 查询模型目录，填写当前账户可用的公开模型 ID。 | 示例：`"YOUR_MODEL"` |
| `input` | string oneOf array（object） | 是 | 文本或 Responses 原生输入项。 | 恰好满足一组：string；或 array（object） |
| `instructions` | string | 否 | — | — |
| `previous_response_id` | string | 否 | 同账户已保存的响应 ID；上游需支持续接。 | — |
| `tools` | array（object） | 否 | — | — |
| `tool_choice` | 任意 JSON | 否 | — | — |
| `store` | boolean | 否 | — | — |
| `background` | boolean | 否 | 仅在上游支持后台响应时启用。 | — |
| `temperature` | number | 否 | — | — |
| `text` | object | 否 | — | 允许额外字段 |
| `reasoning` | object | 否 | — | 允许额外字段 |

### 请求示例：application/json

```bash
curl --request POST "${API_BASE_URL}/v1/responses/input_tokens" \
  -H "Authorization: Bearer $PLATFORM_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
  "model": "YOUR_RESPONSES_MODEL",
  "input": "用一句话解释异步任务"
}'
```

### 响应

| HTTP 状态 | 含义 | Content-Type | 响应结构 |
| --- | --- | --- | --- |
| 200 | 请求成功。 | `application/json` | [InputTokens](#inputtokens) |
| 400 | 参数或协议错误。 | `application/json` | [ProtocolError](#protocolerror) |
| 401 | 密钥缺失、无效、停用或跨站点使用。 | `application/json` | [ProtocolError](#protocolerror) |
| 402 | 余额或额度不足。 | `application/json` | [ProtocolError](#protocolerror) |
| 404 | 模型、任务或资源不存在。 | `application/json` | [ProtocolError](#protocolerror) |
| 429 | 频率或并发超过限制。 | `application/json` | [ProtocolError](#protocolerror) |
| 500 | 服务处理失败。 | `application/json` | [ProtocolError](#protocolerror) |

## anthropic_count_tokens

**统计 Messages 输入 Token**

`POST /v1/messages/count_tokens`

模型需支持 messagesCountTokens。统计请求无需 max_tokens；生成实际计费以最终用量为准。

**鉴权：** `X-API-Key: $PLATFORM_API_KEY`

### 路径、查询与请求头参数

| 位置 | 参数 | 类型 | 必填 | 说明与约束 |
| --- | --- | --- | --- | --- |
| header | `anthropic-version` | string | 是 | Anthropic 协议版本。；默认：`"2023-06-01"` |

### 请求体

**Content-Type：** `application/json`；请求体必填：是。

**结构：** [AnthropicCountRequest](#anthropiccountrequest)。完整嵌套字段见同名数据结构。

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `model` | string | 是 | 查询模型目录，填写当前账户可用的公开模型 ID。 | 示例：`"YOUR_MODEL"` |
| `messages` | array（[AnthropicMessage](#anthropicmessage)） | 是 | — | 最少项数：`1` |
| `system` | string oneOf array（object） | 否 | — | 恰好满足一组：string；或 array（object） |
| `tools` | array（object） | 否 | — | — |
| `tool_choice` | object | 否 | — | 允许额外字段 |
| `thinking` | object | 否 | — | 允许额外字段 |

### 请求示例：application/json

```bash
curl --request POST "${API_BASE_URL}/v1/messages/count_tokens" \
  -H "X-API-Key: $PLATFORM_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  --data '{
  "model": "YOUR_MESSAGES_MODEL",
  "messages": [
    {
      "role": "user",
      "content": "你好"
    }
  ]
}'
```

### 响应

| HTTP 状态 | 含义 | Content-Type | 响应结构 |
| --- | --- | --- | --- |
| 200 | 请求成功。 | `application/json` | [InputTokens](#inputtokens) |
| 400 | 参数或协议错误。 | `application/json` | [ProtocolError](#protocolerror) |
| 401 | 密钥缺失、无效、停用或跨站点使用。 | `application/json` | [ProtocolError](#protocolerror) |
| 402 | 余额或额度不足。 | `application/json` | [ProtocolError](#protocolerror) |
| 404 | 模型、任务或资源不存在。 | `application/json` | [ProtocolError](#protocolerror) |
| 429 | 频率或并发超过限制。 | `application/json` | [ProtocolError](#protocolerror) |
| 500 | 服务处理失败。 | `application/json` | [ProtocolError](#protocolerror) |

## gemini_count_tokens

**统计 Gemini 输入 Token**

`POST /v1beta/models/{model}:countTokens`

选择 supportedGenerationMethods 包含 countTokens 的模型，发送原生 contents。

**鉴权：** `x-goog-api-key: $PLATFORM_API_KEY`

### 路径、查询与请求头参数

| 位置 | 参数 | 类型 | 必填 | 说明与约束 |
| --- | --- | --- | --- | --- |
| path | `model` | string | 是 | Gemini 公开模型 ID，不含 models/ 前缀。；示例：`"YOUR_GEMINI_MODEL"` |

### 请求体

**Content-Type：** `application/json`；请求体必填：是。

**结构：** [GeminiRequest](#geminirequest)。完整嵌套字段见同名数据结构。

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `contents` | array（[GeminiContent](#geminicontent)） | 是 | — | 最少项数：`1` |
| `systemInstruction` | [GeminiContent](#geminicontent) | 否 | — | — |
| `generationConfig` | object | 否 | — | 允许额外字段 |
| `generationConfig.maxOutputTokens` | integer | 否 | — | 最小值：`1` |
| `generationConfig.temperature` | number | 否 | — | — |
| `generationConfig.topP` | number | 否 | — | — |
| `generationConfig.responseMimeType` | string | 否 | — | — |
| `generationConfig.responseSchema` | object | 否 | — | 允许额外字段 |
| `tools` | array（object） | 否 | — | — |
| `toolConfig` | object | 否 | — | 允许额外字段 |
| `safetySettings` | array（object） | 否 | — | — |

### 请求示例：application/json

```bash
curl --request POST "${API_BASE_URL}/v1beta/models/YOUR_GEMINI_MODEL:countTokens" \
  -H "x-goog-api-key: $PLATFORM_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": "你好"
        }
      ]
    }
  ]
}'
```

### 响应

| HTTP 状态 | 含义 | Content-Type | 响应结构 |
| --- | --- | --- | --- |
| 200 | 请求成功。 | `application/json` | [GeminiTokens](#geminitokens) |
| 400 | 参数或协议错误。 | `application/json` | [ProtocolError](#protocolerror) |
| 401 | 密钥缺失、无效、停用或跨站点使用。 | `application/json` | [ProtocolError](#protocolerror) |
| 402 | 余额或额度不足。 | `application/json` | [ProtocolError](#protocolerror) |
| 404 | 模型、任务或资源不存在。 | `application/json` | [ProtocolError](#protocolerror) |
| 429 | 频率或并发超过限制。 | `application/json` | [ProtocolError](#protocolerror) |
| 500 | 服务处理失败。 | `application/json` | [ProtocolError](#protocolerror) |

## 数据结构

下表的必填标记以当前对象为作用范围；可选父对象存在时，其内部必填字段仍需提供。引用类型链接到本文同名结构。`anyOf` 的条件必填规则单独列出。

### ApiError

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `code` | integer oneOf string | 否 | — | 恰好满足一组：integer；或 string |
| `message` | string | 否 | — | — |
| `error` | object | 否 | — | 允许额外字段 |
| `requestId` | string | 否 | — | — |

### ProtocolError

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `type` | string | 否 | Anthropic 错误类型，部分协议省略 | — |
| `error` | object | 是 | — | 允许额外字段 |
| `error.message` | string | 否 | — | — |
| `error.type` | string | 否 | — | — |
| `error.code` | string | 否 | — | — |
| `error.param` | string / null | 否 | — | — |

### TaskError

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `message` | string | 否 | 任务失败原因 | — |
| `code` | string | 否 | 错误码 | — |

### TaskUsage

仅在取得有效最终用量时出现。

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `totalTokens` | integer | 否 | — | 最小值：`0` |
| `inputTokens` | integer | 否 | — | 最小值：`0` |
| `outputTokens` | integer | 否 | — | 最小值：`0` |
| `cachedInputTokens` | integer | 否 | — | 最小值：`0` |

### Task

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `id` | string | 是 | 保存此 ID，用于对应的图片或视频任务查询。 | — |
| `object` | string | 是 | — | 枚举：`["image","video"]` |
| `model` | string | 是 | 公开模型名 | — |
| `status` | string | 是 | 查询 HTTP 200 仍可能是 failed；按状态决定是否结束。 | 枚举：`["queued","processing","completed","failed"]` |
| `progress` | number | 是 | 进度百分比 | 最小值：`0`；最大值：`100` |
| `created_at` | integer | 是 | 创建时间，Unix 秒 | — |
| `completed_at` | integer | 否 | 完成时间，Unix 秒 | — |
| `failed_at` | integer | 否 | 失败时间，Unix 秒 | — |
| `aspectRatio` | string | 否 | 画面比例 | — |
| `size` | string | 否 | 图片或视频尺寸 | — |
| `seconds` | string | 否 | 视频时长，单位秒 | — |
| `url` | string | 否 | 完成时的图片 URL | — |
| `video_url` | string | 否 | 完成时的视频 URL | — |
| `images` | array（string oneOf object） | 否 | 供应商返回的图片结果列表，项目结构随模型而异。 | — |
| `result` | object | 否 | 供应商结果，可包含图片或视频地址。 | 允许额外字段 |
| `processing_time` | number | 否 | 处理耗时，毫秒 | — |
| `usage` | [TaskUsage](#taskusage) | 否 | — | — |
| `error` | [TaskError](#taskerror) | 否 | — | — |

### Account

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `account_id` | string | 否 | — | — |
| `status` | string | 否 | — | — |
| `quota` | object | 否 | — | — |
| `quota.daily_limit` | number / null | 否 | — | — |
| `quota.daily_used` | number | 否 | — | — |
| `quota.daily_remaining` | number / null | 否 | — | — |
| `quota.reset_at` | integer | 否 | Unix 秒 | — |
| `rate_limit` | object | 否 | — | — |
| `rate_limit.requests_per_minute` | integer | 否 | 用户级每分钟限制 | — |
| `concurrency` | object | 否 | — | — |
| `concurrency.max_concurrent_tasks` | integer | 否 | 用户级最大任务并发 | — |
| `created_at` | integer | 否 | Unix 秒 | — |

### AccountEnvelope

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `code` | integer | 是 | — | — |
| `message` | string | 是 | — | — |
| `data` | [Account](#account) | 是 | — | — |
| `requestId` | string | 否 | — | — |

### ModelParameter

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `name` | string | 否 | — | — |
| `label` | string | 否 | — | — |
| `type` | string | 否 | — | — |
| `required` | boolean | 否 | — | — |
| `default` | 任意 JSON | 否 | — | — |
| `options` | array（任意 JSON） | 否 | — | — |
| `min` | number | 否 | — | — |
| `max` | number | 否 | — | — |

### CatalogModel

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `id` | string | 否 | 用于生成请求的公开模型 ID | — |
| `name` | string | 否 | — | — |
| `displayName` | string | 否 | — | — |
| `type` | string | 否 | — | 枚举：`["image_generation","video_generation"]` |
| `pricing` | object | 否 | — | — |
| `pricing.type` | string | 否 | per_call、per_second 等实际计费方式 | — |
| `pricing.amount` | number | 否 | — | — |
| `pricing.currency` | string | 否 | — | 枚举：`["CNY"]` |
| `status` | string | 否 | — | — |
| `capabilities` | object | 否 | — | 允许额外字段 |
| `tasks` | array（object） | 否 | — | — |
| `tasks[].parameters` | array（[ModelParameter](#modelparameter)） | 否 | — | — |

### CatalogEnvelope

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `code` | integer | 是 | — | — |
| `message` | string | 是 | — | — |
| `data` | object | 是 | — | — |
| `data.models` | array（[CatalogModel](#catalogmodel)） | 是 | — | — |
| `requestId` | string | 否 | — | — |

### ConversationModel

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `id` | string | 是 | — | — |
| `object` | string | 否 | — | — |
| `created` | integer | 否 | Unix 秒 | — |
| `owned_by` | string | 否 | — | — |
| `supported_operations` | array（string） | 否 | — | — |
| `context_window` | integer | 否 | — | — |
| `max_output_tokens` | integer | 否 | — | — |
| `supported_transports` | array（string） | 否 | — | — |
| `pricing` | object | 否 | — | 允许额外字段 |

### ModelList

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `object` | string | 否 | — | — |
| `data` | array（[ConversationModel](#conversationmodel)） | 是 | — | — |

### File

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `id` | string (uuid) | 是 | 文件 UUID；删除时使用此 ID。 | — |
| `object` | string | 是 | — | 枚举：`["file"]` |
| `type` | string | 是 | — | 枚举：`["image","video","audio"]` |
| `url` | string | 是 | — | — |
| `mime_type` | string | 否 | — | — |
| `size` | integer | 否 | 字节数 | — |
| `created_at` | integer | 否 | Unix 秒 | — |

### FileDeleted

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `id` | string (uuid) | 是 | — | — |
| `object` | string | 是 | — | 枚举：`["file"]` |
| `deleted` | boolean | 是 | — | — |

### CreateImage

model、modelName、modelId 至少提供一项。JSON 参考媒体使用 URL。

至少满足一组：同时提供 `model`；或 同时提供 `modelName`；或 同时提供 `modelId`

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `model` | string | 否 | 查询模型目录，填写当前账户可用的公开模型 ID。 | 示例：`"YOUR_MODEL"` |
| `modelId` | string | 否 | 内部模型 ID 别名，优先于 modelName 和 model。 | — |
| `modelName` | string | 否 | 模型名称别名，优先于 model。 | — |
| `prompt` | string | 是 | 图片提示词，最大 10000 字符。 | 最长字符数：`10000` |
| `size` | string | 否 | 模型支持的尺寸或比例，如 1:1 或 1024x1024。 | — |
| `aspect_ratio` | string | 否 | 画面比例，如 16:9。 | — |
| `aspectRatio` | string | 否 | aspect_ratio 的兼容别名。 | — |
| `resolution` | string | 否 | 分辨率档位，如 2k。 | — |
| `quality` | string | 否 | 模型支持的质量档位。 | — |
| `style` | string | 否 | 模型支持的风格。 | — |
| `images` | array（string） | 否 | 参考素材 URL 数组；先上传素材可以取得可复用 URL。 | — |
| `image_urls` | array（string） | 否 | images 的兼容别名。 | — |
| `videos` | array（string） | 否 | 参考素材 URL 数组；先上传素材可以取得可复用 URL。 | — |
| `videoUrls` | array（string） | 否 | videos 的兼容别名。 | — |
| `audios` | array（string） | 否 | 参考素材 URL 数组；先上传素材可以取得可复用 URL。 | — |
| `audioUrls` | array（string） | 否 | audios 的兼容别名。 | — |
| `mask_url` | string | 否 | 局部重绘遮罩图 URL。 | — |
| `metadata` | object | 否 | 业务关联元数据。 | 允许额外字段 |
| `parameters` | object | 否 | 模型公开扩展参数；字段名与值以模型目录的 tasks[].parameters 为准。 | 允许额外字段 |
| `generationOptions` | object | 否 | 模型扩展参数兼容对象。 | 允许额外字段 |

### CreateVideo

model、modelName、modelId 至少提供一项。所选模型决定支持的媒体、时长、比例和分辨率。

至少满足一组：同时提供 `model`；或 同时提供 `modelName`；或 同时提供 `modelId`

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `model` | string | 否 | 查询模型目录，填写当前账户可用的公开模型 ID。 | 示例：`"YOUR_MODEL"` |
| `modelId` | string | 否 | 内部模型 ID 别名，优先于 modelName 和 model。 | — |
| `modelName` | string | 否 | 模型名称别名，优先于 model。 | — |
| `prompt` | string | 是 | 视频生成提示词。 | — |
| `size` | string | 否 | 模型支持的尺寸或比例，如 1:1 或 1024x1024。 | — |
| `aspect_ratio` | string | 否 | 画面比例，如 16:9。 | — |
| `aspectRatio` | string | 否 | aspect_ratio 的兼容别名。 | — |
| `resolution` | string | 否 | 分辨率档位，如 2k。 | — |
| `images` | array（string） | 否 | 参考素材 URL 数组；先上传素材可以取得可复用 URL。 | — |
| `videos` | array（string） | 否 | 参考素材 URL 数组；先上传素材可以取得可复用 URL。 | — |
| `videoUrls` | array（string） | 否 | videos 的兼容别名。 | — |
| `audios` | array（string） | 否 | 参考素材 URL 数组；先上传素材可以取得可复用 URL。 | — |
| `audioUrls` | array（string） | 否 | audios 的兼容别名。 | — |
| `metadata` | object | 否 | 业务关联元数据。 | 允许额外字段 |
| `parameters` | object | 否 | 模型公开扩展参数；字段名与值以模型目录的 tasks[].parameters 为准。 | 允许额外字段 |
| `generationOptions` | object | 否 | 模型扩展参数兼容对象。 | 允许额外字段 |
| `seconds` | string | 否 | 正数时长，单位秒。JSON 同样接受数字；multipart 使用文本。 | 示例：`"10"` |
| `duration` | string | 否 | seconds 的兼容别名，选择其中一个。 | — |
| `mode` | string | 否 | 模型支持的生成模式。 | — |
| `video_urls` | array（string） | 否 | videos 的兼容别名。 | — |
| `video_url` | string | 否 | 单个参考视频 URL。 | — |
| `audio_urls` | array（string） | 否 | audios 的兼容别名。 | — |
| `audio_url` | string | 否 | 单个参考音频 URL。 | — |
| `upload_method` | string | 否 | — | 枚举：`["s3","oss"]` |

### CreateVideoUpload

至少满足一组：同时提供 `model`；或 同时提供 `modelName`；或 同时提供 `modelId`

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `model` | string | 否 | 查询模型目录，填写当前账户可用的公开模型 ID。 | 示例：`"YOUR_MODEL"` |
| `modelId` | string | 否 | 内部模型 ID 别名，优先于 modelName 和 model。 | — |
| `modelName` | string | 否 | 模型名称别名，优先于 model。 | — |
| `prompt` | string | 是 | 视频生成提示词。 | — |
| `size` | string | 否 | 模型支持的尺寸或比例，如 1:1 或 1024x1024。 | — |
| `aspect_ratio` | string | 否 | 画面比例，如 16:9。 | — |
| `aspectRatio` | string | 否 | aspect_ratio 的兼容别名。 | — |
| `resolution` | string | 否 | 分辨率档位，如 2k。 | — |
| `images` | array（string） | 否 | 参考素材 URL 数组；先上传素材可以取得可复用 URL。 | — |
| `videos` | array（string） | 否 | 参考素材 URL 数组；先上传素材可以取得可复用 URL。 | — |
| `videoUrls` | array（string） | 否 | videos 的兼容别名。 | — |
| `audios` | array（string） | 否 | 参考素材 URL 数组；先上传素材可以取得可复用 URL。 | — |
| `audioUrls` | array（string） | 否 | audios 的兼容别名。 | — |
| `metadata` | string | 否 | JSON 文本，例如 \{"order_id":"order_123"\}。 | — |
| `parameters` | string | 否 | JSON 文本，例如 \{"order_id":"order_123"\}。 | — |
| `generationOptions` | string | 否 | JSON 文本，例如 \{"order_id":"order_123"\}。 | — |
| `seconds` | string | 否 | 正数时长，单位秒。JSON 同样接受数字；multipart 使用文本。 | 示例：`"10"` |
| `duration` | string | 否 | seconds 的兼容别名，选择其中一个。 | — |
| `mode` | string | 否 | 模型支持的生成模式。 | — |
| `video_urls` | array（string） | 否 | videos 的兼容别名。 | — |
| `video_url` | string | 否 | 单个参考视频 URL。 | — |
| `audio_urls` | array（string） | 否 | audios 的兼容别名。 | — |
| `audio_url` | string | 否 | 单个参考音频 URL。 | — |
| `upload_method` | string | 否 | — | 枚举：`["s3","oss"]` |
| `input_reference` | array（string (binary)） | 否 | 参考图片文件，多图重复同一字段。 | — |

### ImageGeneration

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `model` | string | 是 | 查询模型目录，填写当前账户可用的公开模型 ID。 | 示例：`"YOUR_MODEL"` |
| `prompt` | string | 是 | 非空提示词。 | 最短字符数：`1`；最长字符数：`10000` |
| `n` | integer | 否 | 生成数量，每张图片创建独立任务并计费。 | 默认：`1`；最小值：`1`；最大值：`128` |
| `response_format` | string | 否 | url 返回地址；b64_json 返回图片字节的 Base64。 | 枚举：`["url","b64_json"]`；默认：`"url"` |
| `size` | string | 否 | 模型支持的尺寸或比例。 | — |
| `quality` | string | 否 | — | — |
| `style` | string | 否 | — | — |
| `background` | string | 否 | — | — |
| `moderation` | string | 否 | — | — |
| `output_format` | string | 否 | — | — |
| `input_fidelity` | string | 否 | — | — |
| `output_compression` | integer | 否 | — | 最小值：`0`；最大值：`100` |
| `user` | string | 否 | — | — |
| `stream` | boolean | 否 | 此图片协议返回完整 JSON，使用 false。 | 默认：`false` |

### ImageEdit

image 或 images 至少提供一项。

至少满足一组：同时提供 `image`；或 同时提供 `images`

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `model` | string | 是 | 查询模型目录，填写当前账户可用的公开模型 ID。 | 示例：`"YOUR_MODEL"` |
| `prompt` | string | 是 | 非空提示词。 | 最短字符数：`1`；最长字符数：`10000` |
| `n` | integer | 否 | 生成数量，每张图片创建独立任务并计费。 | 默认：`1`；最小值：`1`；最大值：`128` |
| `response_format` | string | 否 | url 返回地址；b64_json 返回图片字节的 Base64。 | 枚举：`["url","b64_json"]`；默认：`"url"` |
| `size` | string | 否 | 模型支持的尺寸或比例。 | — |
| `quality` | string | 否 | — | — |
| `style` | string | 否 | — | — |
| `background` | string | 否 | — | — |
| `moderation` | string | 否 | — | — |
| `output_format` | string | 否 | — | — |
| `input_fidelity` | string | 否 | — | — |
| `output_compression` | integer | 否 | — | 最小值：`0`；最大值：`100` |
| `user` | string | 否 | — | — |
| `stream` | boolean | 否 | 此图片协议返回完整 JSON，使用 false。 | 默认：`false` |
| `image` | string | 否 | 一张参考图的 HTTP(S) URL 或图片 Data URL。 | — |
| `images` | array（string） | 否 | 多张参考图 URL，最多 16 张，还受所选模型上限约束。 | 最多项数：`16` |
| `mask` | string | 否 | 遮罩图 URL 或图片 Data URL。 | — |

### ImageEditUpload

image 或 image[] 至少提供一个文件。

至少满足一组：同时提供 `image`；或 同时提供 `image[]`

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `model` | string | 是 | 查询模型目录，填写当前账户可用的公开模型 ID。 | 示例：`"YOUR_MODEL"` |
| `prompt` | string | 是 | 非空提示词。 | 最短字符数：`1`；最长字符数：`10000` |
| `n` | integer | 否 | 生成数量，每张图片创建独立任务并计费。 | 默认：`1`；最小值：`1`；最大值：`128` |
| `response_format` | string | 否 | url 返回地址；b64_json 返回图片字节的 Base64。 | 枚举：`["url","b64_json"]`；默认：`"url"` |
| `size` | string | 否 | 模型支持的尺寸或比例。 | — |
| `quality` | string | 否 | — | — |
| `style` | string | 否 | — | — |
| `background` | string | 否 | — | — |
| `moderation` | string | 否 | — | — |
| `output_format` | string | 否 | — | — |
| `input_fidelity` | string | 否 | — | — |
| `output_compression` | integer | 否 | — | 最小值：`0`；最大值：`100` |
| `user` | string | 否 | — | — |
| `stream` | boolean | 否 | 此图片协议返回完整 JSON，使用 false。 | 默认：`false` |
| `image` | string (binary) | 否 | 单个参考图文件。 | — |
| `image[]` | array（string (binary)） | 否 | 多个参考图文件，可重复该字段。 | 最多项数：`16` |
| `mask` | string (binary) | 否 | 可选遮罩图文件。 | — |

### ImageResult

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `created` | integer | 是 | Unix 秒 | — |
| `data` | array（object） | 是 | — | — |
| `data[].url` | string | 否 | — | — |
| `data[].b64_json` | string | 否 | — | — |
| `data[].revised_prompt` | string | 否 | — | — |
| `task_ids` | array（string） | 否 | — | — |
| `partial` | boolean | 否 | — | — |
| `requested` | integer | 否 | — | — |
| `submitted` | integer | 否 | — | — |
| `errors` | array（object） | 否 | — | — |
| `errors[].index` | integer | 否 | — | — |
| `errors[].task_id` | string | 否 | — | — |
| `errors[].code` | string | 否 | — | — |
| `errors[].message` | string | 否 | — | — |

### ImageBatch

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `id` | string (uuid) | 是 | — | — |
| `task_id` | string (uuid) | 否 | — | — |
| `object` | string | 否 | — | 枚举：`["image.generation.task"]` |
| `status` | string | 是 | — | 枚举：`["processing","completed","failed"]` |
| `created_at` | integer | 否 | Unix 秒 | — |
| `expires_at` | integer | 否 | Unix 秒，默认有效期约 24 小时。 | — |
| `completed_at` | integer | 否 | Unix 秒 | — |
| `failed_at` | integer | 否 | Unix 秒 | — |
| `poll_url` | string | 否 | — | — |
| `http_status` | integer | 否 | — | — |
| `image_url` | string | 否 | — | — |
| `result` | [ImageResult](#imageresult) | 否 | — | — |
| `error` | [TaskError](#taskerror) | 否 | — | — |

### ChatMessage

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `role` | string | 是 | 按模型支持的协议角色填写。 | 枚举：`["system","developer","user","assistant","tool"]` |
| `content` | string oneOf array（object） | 否 | 文本或包含图片、音频等的原生内容块。 | 恰好满足一组：string；或 array（object） |
| `name` | string | 否 | — | — |
| `tool_call_id` | string | 否 | — | — |
| `tool_calls` | array（object） | 否 | — | — |

### TokenUsage

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `prompt_tokens` | integer | 否 | — | — |
| `completion_tokens` | integer | 否 | — | — |
| `total_tokens` | integer | 否 | — | — |
| `input_tokens` | integer | 否 | — | — |
| `output_tokens` | integer | 否 | — | — |
| `cached_tokens` | integer | 否 | — | — |

### ChatRequest

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `model` | string | 是 | 查询模型目录，填写当前账户可用的公开模型 ID。 | 示例：`"YOUR_MODEL"` |
| `messages` | array（[ChatMessage](#chatmessage)） | 是 | — | 最少项数：`1` |
| `stream` | boolean | 否 | true 使用 SSE。 | 默认：`false` |
| `stream_options` | object | 否 | — | — |
| `stream_options.include_usage` | boolean | 否 | — | — |
| `max_tokens` | integer | 否 | 输出上限；与 max_completion_tokens 按模型支持选择。 | 最小值：`1` |
| `max_completion_tokens` | integer | 否 | — | 最小值：`1` |
| `temperature` | number | 否 | — | — |
| `top_p` | number | 否 | — | — |
| `stop` | string oneOf array（string） | 否 | — | 恰好满足一组：string；或 array（string） |
| `tools` | array（object） | 否 | — | — |
| `tool_choice` | 任意 JSON | 否 | — | — |
| `response_format` | object | 否 | — | 允许额外字段 |

### ChatResponse

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `id` | string | 否 | — | — |
| `object` | string | 否 | — | — |
| `created` | integer | 否 | Unix 秒 | — |
| `model` | string | 否 | — | — |
| `choices` | array（object） | 是 | — | — |
| `choices[].index` | integer | 否 | — | — |
| `choices[].message` | [ChatMessage](#chatmessage) | 否 | — | — |
| `choices[].finish_reason` | string / null | 否 | — | — |
| `usage` | [TokenUsage](#tokenusage) | 否 | — | — |

### ResponsesRequest

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `model` | string | 是 | 查询模型目录，填写当前账户可用的公开模型 ID。 | 示例：`"YOUR_MODEL"` |
| `input` | string oneOf array（object） | 是 | 文本或 Responses 原生输入项。 | 恰好满足一组：string；或 array（object） |
| `instructions` | string | 否 | — | — |
| `max_output_tokens` | integer | 否 | — | 最小值：`1` |
| `stream` | boolean | 否 | — | 默认：`false` |
| `previous_response_id` | string | 否 | 同账户已保存的响应 ID；上游需支持续接。 | — |
| `tools` | array（object） | 否 | — | — |
| `tool_choice` | 任意 JSON | 否 | — | — |
| `store` | boolean | 否 | — | — |
| `background` | boolean | 否 | 仅在上游支持后台响应时启用。 | — |
| `temperature` | number | 否 | — | — |
| `text` | object | 否 | — | 允许额外字段 |
| `reasoning` | object | 否 | — | 允许额外字段 |

### ResponsesResponse

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `id` | string | 否 | — | — |
| `object` | string | 否 | — | — |
| `status` | string | 否 | — | — |
| `model` | string | 否 | — | — |
| `output` | array（object） | 否 | — | — |
| `output[].type` | string | 否 | — | — |
| `output[].id` | string | 否 | — | — |
| `output[].role` | string | 否 | — | — |
| `output[].status` | string | 否 | — | — |
| `output[].content` | array（object） | 否 | — | — |
| `output[].content[].type` | string | 否 | — | — |
| `output[].content[].text` | string | 否 | — | — |
| `usage` | [TokenUsage](#tokenusage) | 否 | — | — |
| `error` | [TaskError](#taskerror) | 否 | — | — |
| `incomplete_details` | object / null | 否 | — | 允许额外字段 |

### AnthropicMessage

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `role` | string | 是 | — | 枚举：`["user","assistant"]` |
| `content` | string oneOf array（object） | 是 | — | 恰好满足一组：string；或 array（object） |

### AnthropicRequest

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `model` | string | 是 | 查询模型目录，填写当前账户可用的公开模型 ID。 | 示例：`"YOUR_MODEL"` |
| `messages` | array（[AnthropicMessage](#anthropicmessage)） | 是 | — | 最少项数：`1` |
| `system` | string oneOf array（object） | 否 | — | 恰好满足一组：string；或 array（object） |
| `tools` | array（object） | 否 | — | — |
| `tool_choice` | object | 否 | — | 允许额外字段 |
| `thinking` | object | 否 | — | 允许额外字段 |
| `max_tokens` | integer | 是 | 必填输出上限，遵守模型限制。 | 最小值：`1` |
| `stream` | boolean | 否 | — | 默认：`false` |
| `temperature` | number | 否 | — | — |
| `top_p` | number | 否 | — | — |
| `stop_sequences` | array（string） | 否 | — | — |

### AnthropicCountRequest

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `model` | string | 是 | 查询模型目录，填写当前账户可用的公开模型 ID。 | 示例：`"YOUR_MODEL"` |
| `messages` | array（[AnthropicMessage](#anthropicmessage)） | 是 | — | 最少项数：`1` |
| `system` | string oneOf array（object） | 否 | — | 恰好满足一组：string；或 array（object） |
| `tools` | array（object） | 否 | — | — |
| `tool_choice` | object | 否 | — | 允许额外字段 |
| `thinking` | object | 否 | — | 允许额外字段 |

### AnthropicResponse

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `id` | string | 否 | — | — |
| `type` | string | 否 | — | — |
| `role` | string | 否 | — | — |
| `model` | string | 否 | — | — |
| `content` | array（object） | 是 | — | — |
| `content[].type` | string | 否 | — | — |
| `content[].text` | string | 否 | — | — |
| `stop_reason` | string / null | 否 | — | — |
| `stop_sequence` | string / null | 否 | — | — |
| `usage` | [TokenUsage](#tokenusage) | 否 | — | — |

### GeminiContent

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `role` | string | 否 | — | 枚举：`["user","model"]` |
| `parts` | array（object） | 是 | — | 最少项数：`1` |
| `parts[].text` | string | 否 | — | — |
| `parts[].inlineData` | object | 否 | — | — |
| `parts[].inlineData.mimeType` | string | 否 | — | — |
| `parts[].inlineData.data` | string | 否 | Base64 编码 | — |
| `parts[].fileData` | object | 否 | — | — |
| `parts[].fileData.mimeType` | string | 否 | — | — |
| `parts[].fileData.fileUri` | string | 否 | — | — |

### GeminiRequest

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `contents` | array（[GeminiContent](#geminicontent)） | 是 | — | 最少项数：`1` |
| `systemInstruction` | [GeminiContent](#geminicontent) | 否 | — | — |
| `generationConfig` | object | 否 | — | 允许额外字段 |
| `generationConfig.maxOutputTokens` | integer | 否 | — | 最小值：`1` |
| `generationConfig.temperature` | number | 否 | — | — |
| `generationConfig.topP` | number | 否 | — | — |
| `generationConfig.responseMimeType` | string | 否 | — | — |
| `generationConfig.responseSchema` | object | 否 | — | 允许额外字段 |
| `tools` | array（object） | 否 | — | — |
| `toolConfig` | object | 否 | — | 允许额外字段 |
| `safetySettings` | array（object） | 否 | — | — |

### GeminiResponse

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `candidates` | array（object） | 否 | — | — |
| `candidates[].content` | [GeminiContent](#geminicontent) | 否 | — | — |
| `candidates[].finishReason` | string | 否 | — | — |
| `candidates[].index` | integer | 否 | — | — |
| `usageMetadata` | object | 否 | — | 允许额外字段 |
| `usageMetadata.promptTokenCount` | integer | 否 | — | — |
| `usageMetadata.candidatesTokenCount` | integer | 否 | — | — |
| `usageMetadata.totalTokenCount` | integer | 否 | — | — |
| `promptFeedback` | object | 否 | — | 允许额外字段 |

### GeminiModelList

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `models` | array（object） | 否 | — | — |
| `models[].name` | string | 否 | models/ 前缀的资源名 | — |
| `models[].baseModelId` | string | 否 | — | — |
| `models[].displayName` | string | 否 | — | — |
| `models[].supportedGenerationMethods` | array（string） | 否 | — | — |

### ResponseDeleted

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `id` | string | 否 | — | — |
| `object` | string | 否 | — | — |
| `deleted` | boolean | 否 | — | — |

### ResponseInputItems

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `object` | string | 否 | — | — |
| `data` | array（object） | 否 | — | — |
| `has_more` | boolean | 否 | — | — |
| `first_id` | string | 否 | — | — |
| `last_id` | string | 否 | — | — |

### InputTokens

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `input_tokens` | integer | 否 | — | 最小值：`0` |

### ResponsesCompactRequest

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `model` | string | 是 | 查询模型目录，填写当前账户可用的公开模型 ID。 | 示例：`"YOUR_MODEL"` |
| `input` | string oneOf array（object） | 是 | 文本或 Responses 原生输入项。 | 恰好满足一组：string；或 array（object） |
| `instructions` | string | 否 | — | — |
| `previous_response_id` | string | 否 | 同账户已保存的响应 ID；上游需支持续接。 | — |
| `tools` | array（object） | 否 | — | — |
| `tool_choice` | 任意 JSON | 否 | — | — |
| `store` | boolean | 否 | — | — |
| `background` | boolean | 否 | 仅在上游支持后台响应时启用。 | — |
| `temperature` | number | 否 | — | — |
| `text` | object | 否 | — | 允许额外字段 |
| `reasoning` | object | 否 | — | 允许额外字段 |

### ResponsesInputTokensRequest

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `model` | string | 是 | 查询模型目录，填写当前账户可用的公开模型 ID。 | 示例：`"YOUR_MODEL"` |
| `input` | string oneOf array（object） | 是 | 文本或 Responses 原生输入项。 | 恰好满足一组：string；或 array（object） |
| `instructions` | string | 否 | — | — |
| `previous_response_id` | string | 否 | 同账户已保存的响应 ID；上游需支持续接。 | — |
| `tools` | array（object） | 否 | — | — |
| `tool_choice` | 任意 JSON | 否 | — | — |
| `store` | boolean | 否 | — | — |
| `background` | boolean | 否 | 仅在上游支持后台响应时启用。 | — |
| `temperature` | number | 否 | — | — |
| `text` | object | 否 | — | 允许额外字段 |
| `reasoning` | object | 否 | — | 允许额外字段 |

### GeminiTokens

允许额外字段

| 字段 | 类型 | 必填 | 说明 | 约束 |
| --- | --- | --- | --- | --- |
| `totalTokens` | integer | 否 | — | — |

## 流式、异步与错误处理

- Chat Completions、Responses、Messages 将 `stream` 设为 `true` 时使用 SSE；读取完整结束事件与用量。Gemini 使用独立流式接口并带 `alt=sse`。
- 单个图片或视频任务创建后保存 `id`，查询到 `completed` 再读取结果；`failed` 时检查 `error`。HTTP 200 的任务查询仍需检查任务状态。
- OpenAI 图片异步批次返回 HTTP 202，按批次 `id` 查询 `/v1/images/tasks/{taskId}`，与单图片任务 ID 分开保存。建议轮询间隔至少约 3 秒，遇到 429 时遵循 Retry-After。
- Nginx 重写前缀时，响应中的 `poll_url` 或 Location 可能包含后端路径；按客户的完整 `API_BASE_URL` 与接口路径自行拼接轮询地址。
- 创建请求超时先核对已有任务和账单，避免重复提交；查询请求遇到临时网络故障可退避重试。
- 响应字段和示例依协议而异：账户、目录可带 `code/data` 包装；对话兼容协议按原生结构读取，勿套用统一包装。

本文件仅包含 OpenAPI 中登记的客户 HTTP 接口。WebSocket 接入、SDK 代码和管理操作另见文档仓库的对应指南。
