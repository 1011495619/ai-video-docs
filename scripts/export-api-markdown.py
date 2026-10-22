#!/usr/bin/env python3
"""Export the customer OpenAPI contract as a standalone Markdown reference."""

import argparse
import json
import re
import shlex
from pathlib import Path
from urllib.parse import urlencode


ROOT = Path(__file__).resolve().parents[1]
METHODS = {"get", "post", "put", "patch", "delete", "head", "options"}


def compact(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def prose(value):
    return str(value).replace("{", "\\{").replace("}", "\\}").replace("<", "&lt;").replace(">", "&gt;")


def table(headers, rows):
    return "\n".join([
        "| " + " | ".join(map(cell, headers)) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
        *("| " + " | ".join(map(cell, row)) + " |" for row in rows),
    ])


def schema_type(schema):
    if "$ref" in schema:
        name = schema["$ref"].rsplit("/", 1)[-1]
        return f"[{name}](#{name.lower()})"
    for keyword in ("oneOf", "anyOf", "allOf"):
        if keyword in schema and any("type" in item or "$ref" in item for item in schema[keyword]):
            return f" {keyword} ".join(schema_type(item) for item in schema[keyword])
    kind = schema.get("type", "任意 JSON")
    if kind == "array":
        kind = f"array（{schema_type(schema.get('items', {}))}）"
    if schema.get("format"):
        kind += f" ({schema['format']})"
    if schema.get("nullable"):
        kind += " / null"
    return kind


def constraints(schema):
    parts = []
    for key, label in (
        ("enum", "枚举"), ("default", "默认"), ("example", "示例"),
        ("minimum", "最小值"), ("maximum", "最大值"),
        ("exclusiveMinimum", "exclusiveMinimum"), ("exclusiveMaximum", "exclusiveMaximum"),
        ("minLength", "最短字符数"), ("maxLength", "最长字符数"),
        ("minItems", "最少项数"), ("maxItems", "最多项数"), ("pattern", "格式约束"),
    ):
        if key in schema:
            parts.append(f"{label}：`{compact(schema[key])}`")
    if "additionalProperties" in schema:
        extra = schema["additionalProperties"]
        parts.append("允许额外字段" if extra is True else "仅允许声明字段" if extra is False else f"额外字段类型：{schema_type(extra)}")
    for keyword in ("anyOf", "oneOf", "allOf"):
        if keyword in schema:
            groups = []
            for branch in schema[keyword]:
                if branch.get("required"):
                    groups.append("同时提供 " + "、".join(f"`{key}`" for key in branch["required"]))
                else:
                    groups.append(schema_type(branch))
            meaning = {"anyOf": "至少满足一组", "oneOf": "恰好满足一组", "allOf": "满足全部组合"}[keyword]
            parts.append(meaning + "：" + "；或 ".join(groups))
    return "；".join(parts)


def field_rows(schema, prefix="", parent_optional=False):
    required = set(schema.get("required", []))
    for name, value in schema.get("properties", {}).items():
        path = f"{prefix}.{name}" if prefix else name
        needed = "是" if name in required else "否"
        if parent_optional and name in required:
            needed = "父对象存在时必填"
        yield (f"`{path}`", schema_type(value), needed, prose(value.get("description", "—")), constraints(value) or "—")
        if "$ref" not in value:
            nested = value.get("items", {}) if value.get("type") == "array" else value
            nested_prefix = path + ("[]" if value.get("type") == "array" else "")
            yield from field_rows(nested, nested_prefix, parent_optional or name not in required)


def resolve(spec, schema):
    while "$ref" in schema:
        node = spec
        for part in schema["$ref"].removeprefix("#/").split("/"):
            node = node[part.replace("~1", "/").replace("~0", "~")]
        schema = node
    return schema


def parameter_value(parameter):
    schema = parameter.get("schema", {})
    for item in (parameter, schema):
        for key in ("example", "default"):
            if key in item:
                return str(item[key])
    if schema.get("enum"):
        return str(schema["enum"][0])
    return {
        "fileId": "01234567-89ab-4cde-8f01-23456789abcd",
        "taskId": "YOUR_TASK_ID", "responseId": "YOUR_RESPONSE_ID", "model": "YOUR_GEMINI_MODEL",
    }.get(parameter["name"], "YOUR_VALUE")


def auth_headers(spec, operation):
    security = operation.get("security", spec.get("security", []))
    if not security:
        return []
    headers = []
    # Security requirement entries are alternatives; use the first documented option.
    for name in security[0]:
        scheme = spec["components"]["securitySchemes"][name]
        headers.append("Authorization: Bearer $PLATFORM_API_KEY" if scheme["type"] == "http"
                       else f"{scheme['name']}: $PLATFORM_API_KEY")
    return headers


def curl_example(spec, path, method, operation, media_type=None, media=None):
    parameters = operation.get("parameters", [])
    for parameter in parameters:
        if parameter["in"] == "path":
            path = path.replace("{" + parameter["name"] + "}", parameter_value(parameter))
    query = {p["name"]: parameter_value(p) for p in parameters if p["in"] == "query" and p.get("required")}
    if query:
        path += "?" + urlencode(query)
    flags = " -N" if path.split("?", 1)[0].endswith(":streamGenerateContent") else ""
    lines = [f'curl{flags} --request {method.upper()} "${{API_BASE_URL}}{path}"']
    for header in auth_headers(spec, operation):
        lines.append(f'-H "{header}"')
    for parameter in parameters:
        if parameter["in"] == "header" and parameter.get("required"):
            lines.append(f'-H "{parameter["name"]}: {parameter_value(parameter)}"')
    if media_type == "application/json":
        lines.append('-H "Content-Type: application/json"')
        lines.append("--data " + shlex.quote(json.dumps(media["example"], ensure_ascii=False, indent=2)))
    elif media_type == "multipart/form-data":
        schema = resolve(spec, media["schema"])
        required = set(schema.get("required", []))
        for branch in schema.get("anyOf", [])[:1]:
            required.update(branch.get("required", []))
        for name, value in schema.get("properties", {}).items():
            binary = value.get("format") == "binary" or value.get("items", {}).get("format") == "binary"
            if name not in required:
                continue
            sample = "@/path/to/reference.png" if binary else value.get("example", {
                "model": "YOUR_MODEL", "prompt": "用一句话描述你要生成的内容",
            }.get(name, "YOUR_VALUE"))
            if name == "file":
                sample = "@/path/to/reference.mp4"
            lines.append(f'-F "{name}={sample}"')
    return (" " + "\\" + "\n  ").join(lines)


def generate(spec):
    operations = [(path, method, op) for path, methods in spec["paths"].items()
                  for method, op in methods.items() if method in METHODS]
    out = [f"# {spec['info']['title']} — Markdown 接口参考", "",
           f"接口版本：`{spec['info']['version']}`。共 {len(operations)} 个客户接口。",
           "本文件可独立阅读、下载或交给开发工具使用，由文档仓库的 `openapi.json` 生成。", "",
           "## 连接配置", "",
           "`API_BASE_URL` 是客户 API 的完整对外根地址，包含协议、域名、可选端口和 Nginx 对外路径前缀。末尾不加 `/`，也不包含 `/v1`、`/v1beta` 或具体接口路径。", "",
           "将下面的占位值替换为所属站点的地址与密钥，在同一个终端设置一次即可：", "",
           '```bash\nexport API_BASE_URL="YOUR_API_BASE_URL"\nexport PLATFORM_API_KEY="YOUR_API_KEY"\n```', "",
           "请求地址 = `API_BASE_URL` + 本文的接口路径。根路径、`/api`、`/gateway` 和多层前缀均按客户实际部署填写。若从工作台复制的 OpenAI SDK 地址末尾含 `/v1`，先移除该版本段。", "",
           "正文命令读取终端环境变量；Mintlify 在线调试区则在 `Server → baseUrl` 填写相同根地址，两处分别保存。本文的请求示例不预设客户域名。", "",
           "## 鉴权与请求约定", "",
           table(["协议", "请求头", "说明"], [
               ["OpenAI / 文件 / 图片 / 视频", '`Authorization: Bearer $PLATFORM_API_KEY`', "密钥来自 API 请求所属站点"],
               ["Anthropic", '`X-API-Key: $PLATFORM_API_KEY`', '`anthropic-version: 2023-06-01`'],
               ["Gemini", '`x-goog-api-key: $PLATFORM_API_KEY`', "使用 `/v1beta` 接口路径"],
           ]), "",
           "模型名与资源 ID 均为占位值。先查询模型目录，选择当前账户支持对应操作的模型；查询和删除时使用实际返回的 ID。文件上传使用 multipart，让 curl 自动生成 Content-Type 和 boundary。", "",
           "生成接口会实际调用模型，并按站点规则消耗额度。示例仅说明参数结构；字段表标为可选的参数仍可能受到所选模型能力限制。", "",
           "## 接口目录", "",
           table(["分组", "方法", "路径", "接口"], [
               ["、".join(op.get("tags", [])), method.upper(), f"`{path}`", f"[{op['summary']}](#{op['operationId'].lower()})"]
               for path, method, op in operations
           ]), ""]

    for path, method, operation in operations:
        out += [f"## {operation['operationId']}", "", f"**{operation['summary']}**", "",
                f"`{method.upper()} {path}`", "", prose(operation.get("description", "")), "",
                "**鉴权：** " + "；".join(f"`{h}`" for h in auth_headers(spec, operation)), ""]
        params = operation.get("parameters", [])
        out += ["### 路径、查询与请求头参数", ""]
        out += [table(["位置", "参数", "类型", "必填", "说明与约束"], [
            [p["in"], f"`{p['name']}`", schema_type(p.get("schema", {})), "是" if p.get("required") else "否",
             "；".join(filter(None, [prose(p.get("description", "")), constraints(p.get("schema", {}))])) or "—"]
            for p in params
        ]) if params else "无额外参数。", ""]
        body = operation.get("requestBody")
        media_types = body.get("content", {}) if body else {}
        out += ["### 请求体", ""]
        if not body:
            out += ["无请求体。", "", "### 请求示例", "", "```bash", curl_example(spec, path, method, operation), "```", ""]
        for media_type, media in media_types.items():
            schema = media.get("schema", {})
            definition = resolve(spec, schema)
            out += [f"**Content-Type：** `{media_type}`；请求体必填：{'是' if body.get('required') else '否'}。", "",
                    f"**结构：** {schema_type(schema)}。完整嵌套字段见同名数据结构。", ""]
            if definition.get("description"):
                out += [prose(definition["description"]), ""]
            if constraints(definition):
                out += [constraints(definition), ""]
            rows = list(field_rows(definition))
            if rows:
                out += [table(["字段", "类型", "必填", "说明", "约束"], rows), ""]
            out += [f"### 请求示例：{media_type}", "", "```bash",
                    curl_example(spec, path, method, operation, media_type, media), "```", ""]
        out += ["### 响应", ""]
        response_rows = []
        for status, response in operation.get("responses", {}).items():
            for media_type, media in response.get("content", {}).items():
                response_rows.append([status, prose(response.get("description", "—")), f"`{media_type}`", schema_type(media.get("schema", {}))])
            if not response.get("content"):
                response_rows.append([status, prose(response.get("description", "—")), "—", "—"])
        out += [table(["HTTP 状态", "含义", "Content-Type", "响应结构"], response_rows), ""]
        for status, response in operation.get("responses", {}).items():
            for media_type, media in response.get("content", {}).items():
                if "example" in media:
                    out += [f"**HTTP {status} 响应示例：**", "", "```json",
                            json.dumps(media["example"], ensure_ascii=False, indent=2), "```", ""]
                elif media_type == "text/event-stream":
                    out += [f"**HTTP {status} SSE：** " + prose(media.get("schema", {}).get("description", "按 SSE 事件流读取。")), ""]

    out += ["## 数据结构", "",
            "下表的必填标记以当前对象为作用范围；可选父对象存在时，其内部必填字段仍需提供。引用类型链接到本文同名结构。`anyOf` 的条件必填规则单独列出。", ""]
    for name, schema in spec.get("components", {}).get("schemas", {}).items():
        out += [f"### {name}", ""]
        if schema.get("description"):
            out += [prose(schema["description"]), ""]
        if constraints(schema):
            out += [constraints(schema), ""]
        out += [table(["字段", "类型", "必填", "说明", "约束"], list(field_rows(schema))), ""]
    out += ["## 流式、异步与错误处理", "",
            "- Chat Completions、Responses、Messages 将 `stream` 设为 `true` 时使用 SSE；读取完整结束事件与用量。Gemini 使用独立流式接口并带 `alt=sse`。",
            "- 单个图片或视频任务创建后保存 `id`，查询到 `completed` 再读取结果；`failed` 时检查 `error`。HTTP 200 的任务查询仍需检查任务状态。",
            "- OpenAI 图片异步批次返回 HTTP 202，按批次 `id` 查询 `/v1/images/tasks/{taskId}`，与单图片任务 ID 分开保存。建议轮询间隔至少约 3 秒，遇到 429 时遵循 Retry-After。",
            "- Nginx 重写前缀时，响应中的 `poll_url` 或 Location 可能包含后端路径；按客户的完整 `API_BASE_URL` 与接口路径自行拼接轮询地址。",
            "- 创建请求超时先核对已有任务和账单，避免重复提交；查询请求遇到临时网络故障可退避重试。",
            "- 响应字段和示例依协议而异：账户、目录可带 `code/data` 包装；对话兼容协议按原生结构读取，勿套用统一包装。", "",
            "本文件仅包含 OpenAPI 中登记的客户 HTTP 接口。WebSocket 接入、SDK 代码和管理操作另见文档仓库的对应指南。", ""]
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail when the committed Markdown export is stale")
    args = parser.parse_args()
    spec = json.loads((ROOT / "openapi.json").read_text())
    output = ROOT / "exports" / "customer-api-reference.md"
    content = generate(spec)
    if args.check:
        if not output.exists() or output.read_text() != content:
            raise SystemExit("Markdown export is stale. Run: python3 scripts/export-api-markdown.py")
        print("Markdown export is current.")
    else:
        output.parent.mkdir(exist_ok=True)
        output.write_text(content)
        print(f"Generated {output}")


if __name__ == "__main__":
    main()
