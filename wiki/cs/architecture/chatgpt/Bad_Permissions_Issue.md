---
type: Concept
title: "Bad Permissions Issue"
description: "CS - Software Architecture - ChatGPT 대화 추출 노트 (2026-06-25)"
tags: [cs, chatgpt-export]
timestamp: 2026-06-25
status: active
---

# Bad Permissions Issue

> **카테고리**: `CS - Software Architecture`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-06-25

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
Bad permissions. Try removing permissions for user: ..\\{GUEST} (S-1-5-21-2363085722-1329486135-1710076284-1042) on file ../../../.ssh/config.

### 💡 답변 (Assistant)
OpenSSH가 `~/.ssh/config`의 Windows ACL에 Guest 계정 접근 권한이 있어 거부하는 상황입니다. 표시 이름보다 오류의 SID를 기준으로 해당 ACL 항목을 제거하는 방향으로 진행하겠습니다.

---

### 💡 답변 (Assistant)
Run this in **PowerShell**:

```powershell
$config = (Resolve-Path "../../../.ssh/config").Path

# Remove inherited permissions from the file
icacls $config /inheritance:r

# Remove the bad Guest/user SID from the ACL
icacls $config /remove:g "*S-1-5-21-2363085722-1329486135-1710076284-1042"

# Optional but usually helpful: remove broad Windows principals that OpenSSH dislikes
icacls $config /remove:g "*S-1-1-0" "*S-1-5-11" "*S-1-5-32-545" "*S-1-5-32-546"

# Ensure only you, SYSTEM, and Administrators have access
$me = [System.Security.Principal.WindowsIdentity]::GetCurrent().User.Value
icacls $config /grant:r "*${me}:F" "*S-1-5-18:F" "*S-1-5-32-544:F"
```

Then verify:

```powershell
icacls $config
```

You should **not** see that `...{GUEST}` / `S-1-5-21-2363085722-1329486135-1710076284-1042` entry anymore.

If you know the file is actually your normal SSH config, this simpler path is often better:

```powershell
$config = "$HOME\.ssh\config"
```

rather than using `../../../.ssh/config`.

---

### ❓ 질문 (User)
1 파일을 처리했으며 0 파일은 처리하지 못했습니다.

### 💡 답변 (Assistant)
좋습니다. 그 메시지는 **권한 수정 명령이 정상적으로 적용됐다**는 뜻입니다.

`1 파일을 처리했으며 0 파일은 처리하지 못했습니다.`  
= **1개 파일 처리 성공, 실패 0개**

이제 아래로 확인하세요.

```powershell
icacls $config
```

출력에 아래 SID가 더 이상 없어야 합니다.

```text
S-1-5-21-2363085722-1329486135-1710076284-1042
```

그리고 SSH를 다시 실행해 보세요.

```powershell
ssh -v <사용자명>@<호스트>
```

또는 GitHub 확인이면:

```powershell
ssh -T git@github.com
```

아직도 `Bad permissions`가 나오면, 다음 단계는 **현재 ACL 출력 전체**를 봐야 합니다. 특히 `Everyone`, `Users`, `Authenticated Users`, `Guests` 같은 항목이 남아 있으면 OpenSSH가 계속 거부할 수 있습니다.

---

### ❓ 질문 (User)
Permissions for '{key}' are too open. 
> It is required that your private key files are NOT accessible by others.
> This private key will be ignored.
> Load key "{key}": bad permissions 
>{name}@{Port}: Permission denied (publickey).

### 💡 답변 (Assistant)
이번 오류는 `config`가 아니라 개인키 파일 자체의 권한 문제입니다. 에러에 나온 `{key}` 경로의 ACL을 더 좁혀야 OpenSSH가 키를 사용합니다.

---

### 💡 답변 (Assistant)
이번 오류는 **개인키 파일 `{key}`의 권한이 너무 넓다**는 뜻입니다. 앞에서 고친 것은 `~/.ssh/config`였고, 이번에는 실제 private key 파일, 예를 들면 `id_rsa`, `id_ed25519`, `.pem` 같은 파일을 고쳐야 합니다.

PowerShell에서 `{key}` 자리에 오류에 나온 실제 키 경로를 넣고 실행하세요.

```powershell
$key = "C:\Users\사용자명\.ssh\id_ed25519"
$key = (Resolve-Path $key).Path

$me = [System.Security.Principal.WindowsIdentity]::GetCurrent().User.Value

# 상속 권한 제거
icacls $key /inheritance:r

# 넓은 권한 제거: Everyone, Authenticated Users, Users, Guests
icacls $key /remove:g "*S-1-1-0" "*S-1-5-11" "*S-1-5-32-545" "*S-1-5-32-546"

# 앞에서 문제였던 Guest SID도 제거
icacls $key /remove:g "*S-1-5-21-2363085722-1329486135-1710076284-1042"

# 현재 사용자에게만 읽기 권한 부여
icacls $key /grant:r "*${me}:R"
```

만약 키 파일 경로가 오류에 이렇게 나왔다면:

```text
Permissions for 'C:\Users\abc\.ssh\mykey.pem' are too open.
```

이렇게 넣으면 됩니다.

```powershell
$key = "C:\Users\abc\.ssh\mykey.pem"
```

그다음 확인:

```powershell
icacls $key
```

정상적인 형태는 대략 이렇게 **현재 사용자만** 보이면 됩니다.

```text
C:\Users\사용자명\.ssh\id_ed25519
    사용자SID:(R)
```

또는 `SYSTEM`, `Administrators`가 남아 있어도 보통 괜찮습니다. 하지만 아래 항목이 있으면 안 됩니다.

```text
Everyone
Users
Authenticated Users
Guests
S-1-5-21-2363085722-1329486135-1710076284-1042
```

그 후 다시 접속하세요.

```powershell
ssh -i $key -v 사용자명@호스트
```

포트를 따로 지정해야 하는 경우는 `@{Port}`가 아니라 `-p`를 써야 합니다.

```powershell
ssh -i $key -p 포트번호 사용자명@호스트
```

예:

```powershell
ssh -i $key -p 2222 ubuntu@example.com
```

GitHub라면:

```powershell
ssh -i $key -T git@github.com
```

---

### ❓ 질문 (User)
계정 이름과 보안 식별자 사이에 매핑이 이루어지지 않았습니다.

### 💡 답변 (Assistant)
이 오류는 `icacls`가 입력한 계정명이나 SID를 해석하지 못했다는 뜻입니다. 계정 이름은 피하고, 현재 사용자 SID처럼 필요한 SID에는 `*`를 붙여 처리하는 쪽으로 가겠습니다.

---

### 💡 답변 (Assistant)
그 오류는 보통 `icacls /grant` 또는 `/remove`에 들어간 **계정 이름/SID 문자열을 Windows가 해석하지 못했을 때** 납니다. 이번에는 `icacls`로 계정 이름을 해석시키지 말고, PowerShell의 `.NET ACL` API로 **현재 사용자 SID만 남기는 방식**으로 처리하세요.

`{key}`를 그대로 쓰면 안 되고, SSH 오류에 나온 **실제 private key 경로**로 바꿔야 합니다.

예를 들어 오류가 이렇게 나왔다면:

```text
Permissions for 'C:\Users\me\.ssh\id_ed25519' are too open.
```

아래에서 `$key`만 그 경로로 바꿔 실행하세요.

```powershell
$key = "C:\Users\me\.ssh\id_ed25519"
$key = (Resolve-Path -LiteralPath $key).Path

$meSid = [System.Security.Principal.WindowsIdentity]::GetCurrent().User

# 파일 소유권을 현재 사용자로 가져오기
takeown.exe /F "$key" | Out-Null

# ACL을 직접 재구성: 상속 제거 + 기존 권한 제거 + 현재 사용자 Read만 부여
$acl = Get-Acl -LiteralPath $key
$acl.SetOwner($meSid)
$acl.SetAccessRuleProtection($true, $false)

foreach ($rule in @($acl.Access)) {
    $acl.RemoveAccessRuleAll($rule)
}

$readRule = [System.Security.AccessControl.FileSystemAccessRule]::new(
    $meSid,
    [System.Security.AccessControl.FileSystemRights]::Read,
    [System.Security.AccessControl.AccessControlType]::Allow
)

$acl.AddAccessRule($readRule)
Set-Acl -LiteralPath $key -AclObject $acl
```

확인:

```powershell
icacls $key
```

출력에 `Everyone`, `Users`, `Authenticated Users`, `Guests` 같은 항목이 없어야 합니다. 현재 사용자 SID 또는 현재 사용자 계정만 보이면 좋습니다.

그다음 SSH를 다시 실행하세요.

```powershell
ssh -i $key -p 포트번호 사용자명@호스트
```

예:

```powershell
ssh -i $key -p 2222 ubuntu@example.com
```

중요한 점 하나: `{name}@{Port}` 형식은 SSH 문법이 아닙니다. 포트는 반드시 `-p`로 줘야 합니다.

```powershell
ssh -i $key -p 22 name@example.com
```

---

### ❓ 질문 (User)
[16:13:10.638] > Host key verification failed.
> 프로세스에서 없는 파이프에 쓰려고 했습니다.
[16:13:20.568] > 
[16:13:24.362] "install" terminal command done
[16:13:24.364] Install terminal quit with output: 프로세스에서 없는 파이프에 쓰려고 했습니다.
[16:13:24.364] Received install output: 프로세스에서 없는 파이프에 쓰려고 했습니다.

### 💡 답변 (Assistant)
이번에는 키 권한 문제가 아니라 원격 서버의 host key 검증 실패로 넘어간 상태입니다. `없는 파이프` 메시지는 VS Code Remote-SSH가 뒤따라 낸 부가 오류로 보입니다.

---

### 💡 답변 (Assistant)
이제 오류 포인트가 바뀌었습니다.

```text
Host key verification failed.
프로세스에서 없는 파이프에 쓰려고 했습니다.
```

핵심은 **`Host key verification failed`** 입니다.  
뒤의 **“없는 파이프”** 메시지는 VS Code Remote-SSH 설치 터미널이 SSH 실패 이후 같이 종료되면서 나온 부수 오류에 가깝습니다.

## 원인

Windows의 SSH 클라이언트가 원격 서버를 접속할 때 `known_hosts` 파일을 확인합니다.

그런데 다음 중 하나가 발생하면 접속을 막습니다.

1. 서버가 재설치되어 host key가 바뀜
2. 같은 IP에 다른 서버가 붙음
3. 포트가 바뀌었는데 기존 known_hosts 기록과 충돌함
4. 처음 접속인데 VS Code Remote-SSH가 `yes` 입력 프롬프트를 처리하지 못함
5. `~/.ssh/known_hosts`에 잘못된 기존 기록이 남아 있음

가장 흔한 경우는 **서버 재설치/초기화/컨테이너 변경/클라우드 인스턴스 교체로 host key가 바뀐 경우**입니다.

---

## 1단계: VS Code가 쓰는 실제 Host 확인

VS Code에서 접속하는 이름이 예를 들어 `myserver`라면 PowerShell에서 먼저 확인하세요.

```powershell
ssh -G myserver | findstr /I "hostname port user identityfile knownhosts strict"
```

예상 출력은 대략 이런 식입니다.

```text
user ubuntu
hostname 192.168.0.10
port 22
identityfile C:\Users\me\.ssh\id_ed25519
userknownhostsfile C:\Users\me\.ssh\known_hosts
stricthostkeychecking ask
```

여기서 중요한 건 `hostname`과 `port`입니다.

---

## 2단계: 기존 known_hosts 기록 삭제

`hostname`이 `192.168.0.10`, 포트가 `22`라면:

```powershell
ssh-keygen -R 192.168.0.10
```

포트가 `22`가 아니라 예를 들어 `2222`라면 이 형식도 같이 지우세요.

```powershell
ssh-keygen -R "[192.168.0.10]:2222"
```

도메인으로 접속 중이면 도메인도 지우세요.

```powershell
ssh-keygen -R example.com
ssh-keygen -R "[example.com]:2222"
```

즉, 안전하게 하려면 이런 식입니다.

```powershell
ssh-keygen -R 192.168.0.10
ssh-keygen -R "[192.168.0.10]:22"
ssh-keygen -R "[192.168.0.10]:2222"
```

삭제가 되면 보통 `known_hosts.old` 백업이 생깁니다.

---

## 3단계: VS Code 말고 PowerShell에서 먼저 직접 접속

VS Code Remote-SSH로 바로 하지 말고, PowerShell에서 먼저 수동 접속하세요.

```powershell
ssh -i "C:\Users\사용자명\.ssh\id_ed25519" -p 22 사용자명@192.168.0.10
```

포트가 `2222`라면:

```powershell
ssh -i "C:\Users\사용자명\.ssh\id_ed25519" -p 2222 사용자명@192.168.0.10
```

처음 접속이면 이런 질문이 나올 수 있습니다.

```text
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

여기서 서버가 맞다면:

```text
yes
```

입력하세요.

이 과정이 성공하면 `known_hosts`에 새 host key가 등록됩니다. 그다음 VS Code Remote-SSH를 다시 시도하면 됩니다.

---

## 4단계: 여전히 프롬프트가 안 나오고 바로 실패하면

임시로 한 번만 이렇게 접속해 보세요.

```powershell
ssh -o StrictHostKeyChecking=accept-new -i "C:\Users\사용자명\.ssh\id_ed25519" -p 22 사용자명@192.168.0.10
```

포트가 다르면 바꿔주세요.

```powershell
ssh -o StrictHostKeyChecking=accept-new -i "C:\Users\사용자명\.ssh\id_ed25519" -p 2222 사용자명@192.168.0.10
```

이 옵션은 **새 서버 host key는 자동 등록**하지만, 이미 등록된 host key와 충돌하는 경우까지 무시하지는 않습니다. 충돌이면 위의 `ssh-keygen -R`로 기존 기록을 지우는 게 먼저입니다.

---

## 5단계: VS Code SSH config 예시

`C:\Users\사용자명\.ssh\config`에 이런 식으로 되어 있어야 합니다.

```sshconfig
Host myserver
    HostName 192.168.0.10
    User ubuntu
    Port 22
    IdentityFile C:\Users\사용자명\.ssh\id_ed25519
    IdentitiesOnly yes
```

포트가 `2222`라면:

```sshconfig
Host myserver
    HostName 192.168.0.10
    User ubuntu
    Port 2222
    IdentityFile C:\Users\사용자명\.ssh\id_ed25519
    IdentitiesOnly yes
```

그 후 PowerShell에서:

```powershell
ssh myserver
```

이게 성공해야 VS Code Remote-SSH도 보통 성공합니다.

---

## 주의할 점

`Host key verification failed`는 단순 오류일 수도 있지만, 원칙적으로는 **“내가 알던 서버와 지금 접속한 서버의 신원이 다르다”**는 경고입니다.

서버를 재설치했거나 IP를 새로 할당했거나 포트를 바꾼 게 맞다면 `known_hosts` 삭제 후 재등록하면 됩니다.  
그런 변경을 한 적이 전혀 없는데 갑자기 이 오류가 떴다면, 접속 대상 IP/도메인/포트가 맞는지 먼저 확인하는 게 좋습니다.

지금은 이 순서로 가면 됩니다.

```powershell
ssh-keygen -R 원격IP
ssh-keygen -R "[원격IP]:포트"
ssh -i "키파일경로" -p 포트 사용자명@원격IP
```

수동 SSH가 성공한 뒤에 VS Code Remote-SSH를 다시 연결하세요.

---

### ❓ 질문 (User)
Host key for [59.150.33.1]:55104 has changed and you have requested strict checking.
Host key verification failed.

### 💡 답변 (Assistant)
원인이 명확합니다. `59.150.33.1:55104`에 대해 저장된 기존 서버 키와 현재 서버 키가 달라졌습니다.

PowerShell에서 기존 기록을 제거하세요.

```powershell
ssh-keygen -R "[59.150.33.1]:55104"
```

정상적으로 삭제되면 다음처럼 다시 직접 접속합니다.

```powershell
ssh -p 55104 사용자명@59.150.33.1
```

새 키 확인 메시지가 나오면, 서버가 실제로 재설치됐거나 SSH 설정이 변경된 것이 맞는지 확인한 뒤:

```text
yes
```

를 입력하세요. 이후 VS Code Remote-SSH로 다시 연결하면 됩니다.

### 삭제되지 않을 때

VS Code가 별도의 `known_hosts`를 사용하는지 확인합니다.

```powershell
ssh -G 사용자명@59.150.33.1 -p 55104 | findstr /I "userknownhostsfile"
```

예를 들어 출력 경로가 다음과 같다면:

```text
userknownhostsfile C:\Users\사용자명\.ssh\known_hosts
```

명시적으로 삭제하세요.

```powershell
ssh-keygen -f "C:\Users\사용자명\.ssh\known_hosts" -R "[59.150.33.1]:55104"
```

주의할 점은, 서버를 재설치하거나 교체한 사실이 없는데 갑자기 키가 바뀌었다면 무작정 승인하지 않는 것입니다. 서버 관리자에게 새 SSH host key fingerprint가 맞는지 확인하는 것이 안전합니다. 서버 콘솔에서 확인할 수 있다면 Ubuntu 기준:

```bash
sudo ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```

여기에 표시되는 fingerprint와 Windows에서 새로 접속할 때 보이는 fingerprint가 같아야 합니다.

---
