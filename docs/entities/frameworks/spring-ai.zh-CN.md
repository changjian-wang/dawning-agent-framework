---
title: "Spring AI 详细分析"
type: entity
tags: [framework, spring-ai, java, enterprise, jvm]
status: active
created: 2026-04-22
subtype: framework
sources: []
updated: 2026-04-22
---

# Spring AI 详细分析

> Spring 官方出品，把 LangChain 的抽象搬到 JVM。**Java 企业生态的官方 LLM 框架**。

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **官方名称** | Spring AI |
| **维护者** | VMware / Broadcom（Spring 团队） |
| **仓库** | https://github.com/spring-projects/spring-ai |
| **文档** | https://docs.spring.io/spring-ai/reference/ |
| **语言** | Java（支持 Kotlin） |
| **许可证** | Apache 2.0 |
| **Stars** | 7k+ |
| **最新版本** | v1.0.x |
| **核心差异化** | Spring Boot 自动装配 + 企业级生态（Actuator / Observability / Security） |

---

## 1. 定位与背景

Spring AI 2024 年 11 月发布 v1.0.0-M1，2025 年 GA。目标是**给 Java 开发者一个官方、稳定、可维护的 LLM 框架**，对标 Python 的 LangChain。

**核心理念**：
- **POJO 优先**：Agent、Tool、Prompt 都是 Spring Bean
- **自动装配**：`spring-ai-openai-spring-boot-starter` → 配置 `application.yml` 即可
- **生态一等公民**：接入 Micrometer 指标、Spring Security、Actuator 健康检查

**关键差异**：不追求编排创新（Workflow 用 Spring Integration），专注**把 LLM 调用做成"平凡的 Bean 注入"**。

---

## 2. 架构设计

### 2.1 六大核心模块

````mermaid
graph TB
    subgraph APP["应用层（Spring Boot App）"]
        A1["@Service 业务代码"]
    end

    subgraph AI["Spring AI 核心"]
        M1["Chat Client<br/>（ChatModel）"]
        M2["Embedding"]
        M3["Image / Audio / Moderation"]
        M4["Vector Store"]
        M5["Function Calling"]
        M6["RAG Advisor"]
    end

    subgraph STARTERS["Starter（自动装配）"]
        S1["openai / anthropic / azure / ollama<br/>..."]
        S2["pgvector / pinecone / milvus / ..."]
    end

    subgraph ECO["Spring 生态"]
        E1["Spring Security"]
        E2["Micrometer Observability"]
        E3["Spring Data / Boot Actuator"]
    end

    APP --> AI
    AI --> STARTERS
    AI --> ECO

    style AI fill:#e8f5e9,stroke:#2e7d32,stroke-width:3px
    style APP fill:#e3f2fd,stroke:#1565c0
    style STARTERS fill:#fff3e0,stroke:#e65100
    style ECO fill:#f3e5f5,stroke:#6a1b9a
````

### 2.2 ChatClient 流式 API

```java
String answer = chatClient.prompt()
    .system("You are a helpful assistant.")
    .user("What is Spring AI?")
    .advisors(new QuestionAnswerAdvisor(vectorStore))  // RAG
    .tools(weatherTool, calendarTool)                   // Function Calling
    .call()
    .content();
```

对应到 Python 生态，这就是 `LCEL` 的 Java 版本。

---

## 3. 核心抽象

| 抽象 | 职责 | 类比 |
|------|------|------|
| **ChatModel** | LLM 调用（类似 OpenAI ChatCompletion） | LangChain `ChatModel` |
| **ChatClient** | 流式构造器 API（更友好） | LCEL 管道 |
| **Advisor** | 拦截器模式（RAG、Memory、Logging） | LangChain Callback |
| **FunctionCallback** | Tool 定义（`@Bean` 方法即工具） | LangChain Tool |
| **VectorStore** | 向量库统一接口 | LangChain VectorStore |
| **Prompt Template** | 模板变量替换 | LangChain PromptTemplate |

---

## 4. 代码示例

### 4.1 Tool Calling

```java
@Configuration
class ToolConfig {
    @Bean
    @Description("Get current weather for a city")
    public Function<WeatherRequest, WeatherResponse> weatherFunction() {
        return req -> new WeatherResponse(22, "sunny");
    }
}

@Service
class MyService {
    private final ChatClient chatClient;

    public String ask(String question) {
        return chatClient.prompt()
            .user(question)
            .functions("weatherFunction")  // 自动注入
            .call()
            .content();
    }
}
```

### 4.2 RAG via Advisor

```java
@Bean
public ChatClient chatClient(ChatClient.Builder builder, VectorStore vectorStore) {
    return builder
        .defaultAdvisors(
            new QuestionAnswerAdvisor(vectorStore, SearchRequest.defaults()),
            new MessageChatMemoryAdvisor(chatMemory())
        )
        .build();
}
```

---

## 5. 与其他框架对比

| 维度 | Spring AI | LangChain | Semantic Kernel | Dawning Agent OS |
|------|-----------|-----------|-----------------|-------------------|
| 语言 | Java/Kotlin | Python | .NET/Python/Java | .NET |
| 生态深度 | ⭐⭐⭐⭐⭐（Spring） | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| 多 Agent | ❌（用 Spring Integration） | LangGraph | MAF | ✅ 原生 |
| 企业就绪 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 学习曲线 | 低（Spring 用户） | 中 | 中 | 低 |
| 可观测 | ✅ Micrometer | ⚠️ LangSmith | ✅ OpenTelemetry | ✅ OpenTelemetry |

---

## 6. 对 Dawning Agent OS 的启示

1. **"框架 = Spring Boot Starter" 模式值得借鉴**：Dawning 应该做到 `AddDawningAgent()` 一行注入，配置走 `appsettings.json`——这与 Spring AI 的 Starter 理念完全一致
2. **Advisor 模式（拦截器链）**：`Advisor` 是 Spring AI 的神来之笔——把 RAG、Memory、Logging 都统一为可组合的拦截器。Dawning 可用 **中间件管道**（ASP.NET Core 风格）实现同等效果
3. **POJO/POCO 优先**：Agent、Tool 都是普通 Bean/类，不强制继承 → 这是 .NET 生态的优势，Dawning 应彻底贯彻
4. **"不做编排创新"也是策略**：Spring AI 故意不做 Agent 编排，把它交给 Spring Integration/State Machine。Dawning 选择**做**编排（多 Agent、Skill 路由），但要明白这是"产品定位"而非"必然"

---

## 7. 延伸阅读

- 官方文档：<https://docs.spring.io/spring-ai/reference/>
- Spring AI Workshop：<https://github.com/spring-projects/spring-ai-workshop>
- [comparisons/framework-modules-mapping.zh-CN.md](../../comparisons/framework-modules-mapping.zh-CN.md)
