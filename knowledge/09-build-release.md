# 09 构建与发布

## 已确认结论

### 1. 本地最小构建命令是 `go build -o octo-server .`
README quickstart 给出的本地启动流程是 clone、`go build -o octo-server .`、再用 `./octo-server --config ./configs/tsdd.yaml` 启动。

来源: README.md#L50-L55

### 2. 本仓依赖 octo-lib，私有预览阶段可能需要本地 replace
`BUILDING.md` 说明依赖 sibling repo `octo-lib`，私有预览阶段 `go build ./...` 可能因 go.sum 缺失失败，可 clone sibling repo 并加 replace。

来源: BUILDING.md#L3-L27

### 3. Dockerfile 是源码内构建的多阶段镜像
`Dockerfile` 使用 `golang:1.25` build stage，执行 `go mod download`，再用 `CGO_ENABLED=0 GOOS=linux go build` 编译，并通过 ldflags 写入 Commit、CommitDate、Version、TreeState；prod stage 用 alpine，拷贝 app/assets/configs。

来源: Dockerfile#L11-L20
来源: Dockerfile#L22-L33
来源: Dockerfile#L35-L48

### 4. Dockerfile.ghcr 是预构建二进制镜像形态
`Dockerfile.ghcr` 基于 debian slim，按 `TARGETARCH` 拷贝 `linux_${TARGETARCH}` 为 `/app/main`，并拷贝 assets/configs。

来源: Dockerfile.ghcr#L1-L17

### 5. 官方完整 OOTB 部署已迁到 octo-deployment
README 和 BUILDING 都说明完整 stack（server + admin + web + matter + smart-summary + WuKongIM + MySQL + Redis + MinIO + nginx）在 `Mininglamp-OSS/octo-deployment`，本仓旧 compose 已退役。

来源: README.md#L59-L66
来源: BUILDING.md#L33-L41
来源: BUILDING.md#L49-L55

### 6. Makefile 中仍有历史私有 registry push/deploy，非 canonical release surface
BUILDING 明确说 `push` / `deploy` / `deploy-v2` 是旧私有 Aliyun registry 路径，不应作为 canonical release surface。

来源: BUILDING.md#L57-L62
来源: Makefile#L1-L13
