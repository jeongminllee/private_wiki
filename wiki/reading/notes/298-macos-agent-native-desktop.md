---
type: Reference
title: "Agent! for macOS: accessibility·shell·Xcode를 연결하는 native desktop agent"
description: "local·cloud LLM을 macOS application, codebase와 privileged command에 연결하는 Swift 기반 agent harness"
resource: https://github.com/macOS26/Agent
notion: https://app.notion.com/p/d961a73cf20b82cdb150819806e02fcb
tags: [reading, ai-agents, macos, desktop-automation]
timestamp: 2026-07-24
status: summarized
---

# 범위

Agent!는 macOS 26을 대상으로 만든 native desktop agent다. Accessibility API와 app scripting으로 Safari, Music, Photo Booth와 다른 application을 조작하고, file edit, shell, Git, Xcode build와 test를 수행한다. Voice와 iMessage를 통한 remote request, parallel subagent, repository map과 대화 기억도 제공한다.

Claude, GPT, Gemini, Mistral, DeepSeek, Qwen, OpenRouter 등 cloud provider뿐 아니라 Ollama, vLLM, LM Studio와 Apple Foundation Models를 연결한다. Apple Intelligence가 처리할 수 있는 tool call은 device 안에서 실행하고 실패할 때 cloud model로 넘기는 구성을 지원한다고 설명한다. File edit마다 rollback 가능한 snapshot을 남기는 점은 desktop automation의 복구성을 높인다.

# 가장 큰 위험

이 도구의 능력은 곧 권한의 크기다. Accessibility 권한은 다른 app의 UI와 text를 읽고 조작할 수 있고, shell은 사용자 권한으로 실행된다. 선택적으로 설치하는 Launch Daemon을 승인하면 root command도 가능하다. iMessage remote control까지 열면 발신자 인증과 prompt injection이 machine compromise의 경계가 된다.

따라서 처음에는 privileged helper 없이 별도 macOS account와 test repository에서 실행하고, cloud provider에 보낼 수 없는 folder·application을 제외한다. API key는 최소 권한으로 분리하고 iMessage sender allowlist, confirmation, command log와 snapshot 복구를 실제로 시험한다. “no telemetry”라는 project 설명과 별개로 선택한 cloud provider에는 prompt와 tool result가 전송될 수 있다.

# 구현 관점

Repository는 Swift·SwiftUI 기반이며 application을 hard-code하기보다 SDEF와 `/Applications`를 runtime에 찾아 tool 범위를 넓힌다. 확장성은 높지만 새 app이 자동으로 실행 대상이 된다는 뜻이므로 tool discovery와 execution permission을 분리해 검토하는 편이 안전하다. MIT license다.

# 출처

- [Agent! 저장소](https://github.com/macOS26/Agent)
- [보안 설계 문서](https://github.com/macOS26/Agent/blob/main/docs/SECURITY.md)

