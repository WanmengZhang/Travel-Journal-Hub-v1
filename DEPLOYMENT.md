# Vercel 云部署指南# 云部署指南 (Cloud Deployment Guide)



本指南展示如何将 Travel Journal Hub 部署到 Vercel。本指南展示如何将 Travel Journal Hub 部署到云端。



------



## 🌟 为什么选择 Vercel## � **中国用户请看这里！**



- ✅ **完全免费**（大额免费额度）**如果你在中国，推荐查看：[DEPLOYMENT_CHINA.md](DEPLOYMENT_CHINA.md)** 

- ✅ **全球 CDN**（访问速度快）- ✅ 中国可直接访问的平台

- ✅ **GitHub 自动部署**（推送代码自动更新）- ✅ 无需翻墙

- ✅ **自动 HTTPS**（免费 SSL 证书）- ✅ 无需信用卡

- ✅ **零配置**（自动检测项目类型）- ✅ 推荐使用 **Render.com**（在中国访问稳定）

- ✅ **中国可访问**（大部分地区可直接访问）

- ✅ **无需信用卡**（个人项目完全免费）---



---## � **无需信用卡的部署方案**



## 📋 部署步骤| 平台 | 中国访问 | 信用卡 | 难度 | 推荐指数 | 备注 |

|------|---------|--------|------|---------|------|

### 方法 1: 通过 Vercel 网站部署（推荐）| **Render** | ✅ 稳定 | ❌ 不需要 | ⭐⭐ 简单 | ⭐⭐⭐⭐⭐ | **中国用户首选** [详细教程](DEPLOYMENT_CHINA.md) |

| **PythonAnywhere** | ⚠️ 需翻墙 | ❌ 不需要 | ⭐ 简单 | ⭐⭐⭐⭐ | 国外用户推荐，[教程](DEPLOYMENT_PYTHONANYWHERE.md) |

#### 1. 准备配置文件| **Vercel** | ✅ 可访问 | ❌ 不需要 | ⭐⭐ 中等 | ⭐⭐⭐⭐ | 中国部分地区可用 |

| **Replit** | ⚠️ 不稳定 | ❌ 不需要 | ⭐ 最简单 | ⭐⭐⭐ | 在中国访问不稳定 |

首先需要在项目根目录创建 `vercel.json` 配置文件。| **Glitch** | ⚠️ 不稳定 | ❌ 不需要 | ⭐⭐ 简单 | ⭐⭐⭐ | 在中国访问不稳定 |

| Railway | ⚠️ 不稳定 | ⚠️ 试用需要 | ⭐ 简单 | ⭐⭐⭐⭐ | 试用期后需要信用卡 |

**已经准备好！** 项目中已包含 `vercel.json` 文件，内容如下：

---

```json

{## 🎯 **快速选择指南**

  "version": 2,

  "builds": [### 👉 如果你在中国

    {→ **使用 [Render](DEPLOYMENT_CHINA.md)** ✅（无需翻墙，无需信用卡）

      "src": "app.py",

      "use": "@vercel/python"### 👉 如果你在国外

    },→ **使用 [PythonAnywhere](DEPLOYMENT_PYTHONANYWHERE.md)** ✅（永久免费，无需信用卡）

    {

      "src": "static/**",### 👉 如果你想要最快部署

      "use": "@vercel/static"→ **使用 Replit**（5分钟搞定，但在中国可能不稳定）

    }

  ],### 👉 如果你有信用卡

  "routes": [→ **使用 Railway**（最佳体验）

    {

      "src": "/static/(.*)",---

      "dest": "/static/$1"

    },## 🌟 方法 1: PythonAnywhere（最推荐 - 无需信用卡）

    {

      "src": "/(.*)",**完全免费 | 无需信用卡 | 永久可用**

      "dest": "app.py"

    }详细教程请查看：**[DEPLOYMENT_PYTHONANYWHERE.md](DEPLOYMENT_PYTHONANYWHERE.md)**

  ],

  "env": {**快速步骤**：

    "USE_SQLITE": "true"1. 访问 [PythonAnywhere.com](https://www.pythonanywhere.com/) 注册

  }2. 克隆 GitHub 仓库

}3. 配置 WSGI 文件

```4. 启动应用



#### 2. 提交代码到 GitHub**优点**：

- ✅ 专为 Python 设计

```bash- ✅ Web 界面操作简单

cd /workspaces/Travel-Journal-Hub-v1- ✅ 包含免费 MySQL

git add .- ✅ 适合作业演示

git commit -m "Add Vercel deployment configuration"

git push origin main**URL 格式**：`https://你的用户名.pythonanywhere.com`

```

---

#### 3. 注册并登录 Vercel

## 🎮 方法 2: Replit（最简单 - 无需信用卡）

1. 访问 [Vercel.com](https://vercel.com/)

2. 点击 "Sign Up"（注册）或 "Log In"（登录）**完全免费 | 无需信用卡 | 5分钟部署**

3. 选择 "Continue with GitHub"（用 GitHub 账号登录最方便）

4. 授权 Vercel 访问你的 GitHub 账号### 快速部署步骤



#### 4. 导入项目1. **创建账号**

   - 访问 [Replit.com](https://replit.com/)

1. 登录后，点击右上角的 "Add New..." → "Project"   - 用 GitHub 账号登录（或邮箱注册）

2. 在项目列表中找到 `Travel-Journal-Hub-v1` 仓库

3. 点击 "Import"（导入）2. **导入项目**

   - 点击 "+ Create Repl"

#### 5. 配置项目   - 选择 "Import from GitHub"

   - 粘贴仓库 URL：`https://github.com/WanmengZhang/Travel-Journal-Hub-v1`

Vercel 会自动检测到这是一个 Python 项目：   - 点击 "Import from GitHub"



| 配置项 | 值 |3. **配置环境**

|--------|-----|   在 Replit 中创建 `.replit` 文件：

| Project Name | `travel-journal-hub`（或保持默认） |   ```toml

| Framework Preset | 选择 "Other" |   run = "USE_SQLITE=true python app.py"

| Root Directory | 保持默认 `./` |   language = "python3"

| Build Command | 留空（使用 vercel.json 配置） |   ```

| Output Directory | 留空 |

4. **点击 Run**

**环境变量**（可选，已在 vercel.json 中配置）：   - 点击顶部的绿色 "Run" 按钮

- 如果需要额外配置，可以在 "Environment Variables" 添加   - 等待依赖安装和启动

- 默认已设置 `USE_SQLITE=true`   - 应用会自动打开在右侧面板



#### 6. 部署5. **获取 URL**

   - 应用 URL 会显示在右侧预览窗口顶部

1. 确认配置无误   - 格式：`https://项目名.你的用户名.repl.co`

2. 点击 "Deploy"（部署）按钮

3. 等待 1-2 分钟（首次部署可能需要更长时间）**注意事项**：

- ⚠️ 不活跃时会自动休眠（访问时需要几秒唤醒）

#### 7. 查看部署结果- ⚠️ 免费版代码公开可见

- ✅ 适合快速演示和测试

部署成功后：

- 会自动跳转到项目 dashboard---

- 可以看到部署状态和访问 URL

- URL 格式：`https://travel-journal-hub.vercel.app` 或 `https://项目名-用户名.vercel.app`## 🌐 方法 3: Glitch（无需信用卡）



#### 8. 访问应用**完全免费 | 无需信用卡 | 在线编辑**



1. 点击生成的 URL### 快速部署步骤

2. 或者点击 "Visit" 按钮

3. 测试所有功能是否正常1. **创建账号**

   - 访问 [Glitch.com](https://glitch.com/)

---   - 用 GitHub 账号登录



### 方法 2: 通过命令行部署（可选）2. **导入项目**

   - 点击 "New Project" → "Import from GitHub"

如果你熟悉命令行，也可以使用 Vercel CLI：   - 输入：`https://github.com/WanmengZhang/Travel-Journal-Hub-v1`



#### 1. 安装 Vercel CLI3. **配置启动**

   在 `.env` 文件中添加：

```bash   ```

npm install -g vercel   USE_SQLITE=true

```   ```



#### 2. 登录 Vercel4. **自动启动**

   - Glitch 会自动检测 `app.py` 并启动

```bash   - 应用 URL 显示在顶部

vercel login   - 格式：`https://项目名.glitch.me`

```

**优点**：

按照提示登录你的 Vercel 账号。- ✅ 即时预览

- ✅ 在线编辑代码

#### 3. 部署项目- ✅ 自动备份



```bash**注意事项**：

cd /workspaces/Travel-Journal-Hub-v1- ⚠️ 项目默认公开（可设为私有）

vercel --prod- ⚠️ 不活跃时会休眠

```

---

按照提示确认配置，然后等待部署完成。

## 🚀 方法 4: Railway.app (推荐 - 但需要信用卡试用)

#### 4. 获取 URL

### 特点

部署成功后，命令行会显示生成的 URL。- ✅ **完全免费**（每月 $5 免费额度，够运行小项目）

- ✅ **零配置**：直接连接 GitHub 自动部署

---- ✅ **支持 SQLite**：数据持久化

- ✅ **自动 HTTPS**：免费提供安全域名

## ✅ 部署后验证- ✅ **自动重启**：应用崩溃自动恢复



访问以下 URL 确认应用正常工作：### 部署步骤（5分钟完成）



- **首页**: `https://你的域名.vercel.app/`#### 1. 提交代码到 GitHub

- **日记列表**: `https://你的域名.vercel.app/journals````bash

- **编辑器**: `https://你的域名.vercel.app/editor`# 在 VS Code 终端执行

- **API**: `https://你的域名.vercel.app/api/entries`cd /workspaces/Travel-Journal-Hub-v1

git add .

---git commit -m "Add cloud deployment configuration"

git push origin main

## 🔄 自动部署```



部署成功后，Vercel 会自动监控你的 GitHub 仓库：#### 2. 部署到 Railway

1. 访问 [Railway.app](https://railway.app/)

- **自动部署**: 每次推送到 `main` 分支，Vercel 会自动重新部署2. 点击 "Start a New Project"

- **预览部署**: 推送到其他分支会创建预览部署3. 选择 "Deploy from GitHub repo"

- **Pull Request 预览**: 创建 PR 时会自动生成预览链接4. 登录 GitHub 并授权 Railway

5. 选择 `WanmengZhang/Travel-Journal-Hub-v1` 仓库

---6. Railway 会自动检测到 Python 项目并开始部署



## 🔧 常见问题#### 3. 配置环境变量（自动使用 SQLite）

Railway 会自动设置 `PORT` 环境变量，应用会自动使用 SQLite。

### Q: 部署失败怎么办？

无需任何额外配置！

**解决方案**：

1. 在 Vercel Dashboard 查看部署日志#### 4. 获取部署 URL

2. 检查 `vercel.json` 配置是否正确- 部署完成后，点击 "Settings" → "Domains"

3. 确保 `requirements.txt` 包含所有依赖- Railway 会自动生成一个类似 `https://your-app-name.up.railway.app` 的域名

4. 常见错误：- 直接访问即可！

   - Python 版本不兼容：在 `runtime.txt` 中指定版本

   - 依赖安装失败：检查依赖名称和版本#### 5. 验证部署

访问你的域名，例如：

### Q: 如何查看部署日志？- 首页: `https://your-app-name.up.railway.app/`

- API: `https://your-app-name.up.railway.app/api/entries`

1. 登录 Vercel Dashboard

2. 选择你的项目---

3. 点击 "Deployments" 标签

4. 点击具体的部署记录## 🔵 方法 2: Render.com (免费且稳定)

5. 查看 "Building" 和 "Runtime Logs"

### 特点

### Q: 如何自定义域名？- ✅ **永久免费**层级（有休眠机制）

- ✅ **自动 SSL**

1. 在 Vercel Dashboard 选择项目- ✅ **支持 SQLite**（需要付费层才能持久化，但可以用 PostgreSQL）

2. 进入 "Settings" → "Domains"

3. 添加你的自定义域名### 快速部署步骤

4. 按照提示配置 DNS 记录

#### 1. 提交代码（同上）

### Q: 数据会丢失吗？

#### 2. 部署

Vercel 的无服务器环境是短暂的：1. 访问 [Render.com](https://render.com/)

- ⚠️ SQLite 数据库在部署后**会被重置**2. 注册/登录

- 💡 建议：如需持久化数据，考虑使用外部数据库（如 PlanetScale、Supabase）3. 点击 "New +" → "Web Service"

- ✅ 对于演示和测试，SQLite 完全够用4. 连接 GitHub 仓库 `WanmengZhang/Travel-Journal-Hub-v1`

5. 配置：

### Q: 如何回滚到之前的版本？   - **Name**: `travel-journal-hub`

   - **Environment**: `Python 3`

1. 在 "Deployments" 中找到之前的部署   - **Build Command**: `pip install -r requirements.txt`

2. 点击 "..." → "Promote to Production"   - **Start Command**: `python app.py`

3. 确认即可回滚6. 添加环境变量:

   - `USE_SQLITE` = `true`

### Q: Vercel 免费额度够用吗？   - `PORT` = `10000`（自动填充）

7. 点击 "Create Web Service"

**完全够用！** 免费额度包括：

- 100 GB 带宽/月#### 3. 等待部署（约 2-3 分钟）

- 无限次部署部署完成后会得到一个 `https://travel-journal-hub.onrender.com` 格式的 URL。

- 自动 SSL 证书

- 全球 CDN**注意**: Render 免费层会在 15 分钟不活跃后休眠，第一次访问需要等待 30 秒唤醒。



对于课程项目和个人演示，免费版本完全足够。---



### Q: 在中国能访问吗？## 🟢 方法 3: Vercel (前端推荐，需要小改动)



- ✅ 大部分地区可以直接访问Vercel 主要用于前端，但也可以部署 Flask：

- ⚠️ 部分地区可能速度较慢

- 💡 如果访问有问题，可以尝试更换网络或稍后再试### 额外需要的文件

创建 `vercel.json`:

---```json

{

## 📊 性能优化建议  "version": 2,

  "builds": [

### 1. 启用缓存    {

      "src": "app.py",

在 `vercel.json` 中配置静态文件缓存：      "use": "@vercel/python"

    }

```json  ],

{  "routes": [

  "headers": [    {

    {      "src": "/(.*)",

      "source": "/static/(.*)",      "dest": "app.py"

      "headers": [    }

        {  ]

          "key": "Cache-Control",}

          "value": "public, max-age=31536000, immutable"```

        }

      ]### 部署命令（在 VS Code 终端）

    }```bash

  ]# 安装 Vercel CLI（只需一次）

}npm install -g vercel

```

# 登录并部署

### 2. 压缩响应vercel login

vercel --prod

Vercel 自动启用 Gzip/Brotli 压缩，无需额外配置。```



### 3. 使用环境变量---



对于敏感信息（如 API 密钥），使用环境变量：## 🟡 方法 4: Heroku (传统选择)



1. 在 Vercel Dashboard → Settings → Environment Variables### 特点

2. 添加变量- ⚠️ **需要信用卡验证**（但不收费）

3. 在代码中使用 `os.environ.get('变量名')`- ✅ **稳定可靠**



---### 使用 GitHub 集成部署（无需本地 CLI）



## 📝 部署成功后#### 1. 访问 [Heroku Dashboard](https://dashboard.heroku.com/)



记得在 `REPORT.md` 中添加部署信息：#### 2. 创建新应用

- 点击 "New" → "Create new app"

```markdown- 输入应用名称（例如 `travel-journal-hub-2025`）

### 7.4 云部署- 选择地区（United States 或 Europe）



**部署平台**: Vercel  #### 3. 连接 GitHub

**部署 URL**: https://travel-journal-hub.vercel.app  - 进入 "Deploy" 标签

**部署时间**: 2025年1月9日  - 选择 "GitHub" 作为部署方法

- 搜索并连接 `WanmengZhang/Travel-Journal-Hub-v1`

**配置**:- 启用 "Automatic Deploys"（可选）

- Framework: Flask (Python)

- Database: SQLite (内存模式)#### 4. 配置环境变量

- CDN: 全球加速- 进入 "Settings" → "Config Vars"

- HTTPS: 自动启用- 添加:

  - `USE_SQLITE` = `true`

**特性**:

- ✅ 自动部署（GitHub 集成）#### 5. 手动部署

- ✅ 全球 CDN 加速- 回到 "Deploy" 标签

- ✅ 自动 HTTPS- 点击 "Deploy Branch"（选择 main 分支）

- ✅ 零停机部署

```#### 6. 访问应用

- 点击 "Open app" 按钮

---- URL 格式: `https://travel-journal-hub-2025.herokuapp.com/`



## 🎯 总结---



**Vercel 部署优势**：## 📊 部署方式对比

- ✅ 配置简单（只需 `vercel.json`）

- ✅ 自动部署（推送代码即更新）| 平台 | 需要信用卡 | 免费额度 | 速度 | SQLite支持 | 推荐指数 | 适用场景 |

- ✅ 全球 CDN（访问速度快）|------|-----------|---------|------|-----------|---------|---------|

- ✅ 完全免费（个人项目）| **PythonAnywhere** | ❌ 否 | 永久免费 | ⚡⚡ | ✅ 完美 | ⭐⭐⭐⭐⭐ | 学生作业、演示 |

- ✅ 自动 HTTPS| **Replit** | ❌ 否 | 永久免费 | ⚡⚡⚡ | ✅ 完美 | ⭐⭐⭐⭐ | 快速测试、演示 |

- ✅ 无需信用卡| **Glitch** | ❌ 否 | 永久免费 | ⚡⚡ | ✅ 可用 | ⭐⭐⭐⭐ | 在线编辑、协作 |

| **Railway** | ⚠️ 是 | $5/月 | ⚡⚡⚡ | ✅ 完美 | ⭐⭐⭐⭐⭐ | 最佳体验 |

**部署时间**：首次约 5-10 分钟，熟悉后 2 分钟内完成。| **Render** | ⚠️ 推荐 | 永久免费 | ⚡⚡ | ✅ 但有限制 | ⭐⭐⭐⭐ | 长期运行 |

| **Vercel** | ⚠️ 是 | 大额免费 | ⚡⚡⚡ | ⚠️ 不推荐 | ⭐⭐⭐ | 主要用前端 |

---| **Heroku** | ⚠️ 是 | 需验证 | ⚡⚡ | ✅ 可用 | ⭐⭐⭐ | 传统选择 |



## 🆘 需要帮助？### 🎓 学生推荐排序（无信用卡）

1. **PythonAnywhere** - 最稳定，专业

如果部署遇到问题：2. **Replit** - 最简单，5分钟搞定

3. **Glitch** - 在线编辑，适合调试

1. **查看 Vercel 文档**: [vercel.com/docs](https://vercel.com/docs)

2. **检查部署日志**: Dashboard → Deployments → 点击具体部署---

3. **常见问题**: 查看上面的"常见问题"部分

## ✅ 推荐流程（最快 5 分钟）

---

### 对于课程演示和作业展示：

**准备好了吗？现在就开始部署吧！** 🚀

```bash

```bash# 1. 提交所有代码

# 1. 提交代码git add .

git add .git commit -m "Add deployment configuration for Railway"

git commit -m "Ready for Vercel deployment"git push origin main

git push origin main

# 2. 访问 Railway.app

# 2. 访问 Vercel# - 注册/登录（用 GitHub 账号）

# https://vercel.com/# - "New Project" → "Deploy from GitHub repo"

# - 选择你的仓库

# 3. 导入项目并部署# - 等待 2-3 分钟自动部署

# 5-10 分钟后，你的应用就在线了！

```# 3. 获取 URL 并测试

# - Settings → Domains → 复制生成的 URL
# - 在浏览器打开测试

# 4. 更新 REPORT.md
# 在"部署"章节添加你的实际部署 URL
```

---

## 🔧 部署后验证清单

- [ ] 访问首页 `https://your-app.railway.app/`
- [ ] 测试创建条目功能
- [ ] 测试查看所有条目 `/journals`
- [ ] 测试编辑和删除功能
- [ ] 检查 API: `https://your-app.railway.app/api/entries`
- [ ] 在不同设备测试（手机、平板）
- [ ] 记录部署 URL 到 REPORT.md

---

## 📝 部署成功后更新文档

在 `REPORT.md` 的"部署"章节添加：

```markdown
### 7.4 Cloud Deployment (实际部署)

**Deployment Platform**: Railway.app

**Live URL**: https://travel-journal-hub.up.railway.app

**Deployment Date**: November 9, 2025

**Configuration**:
- Database: SQLite (persistent storage enabled)
- Environment: Production
- Auto-deployment: Enabled (GitHub main branch)

**Performance**:
- Response Time: < 200ms
- Uptime: 99.9%
- Database Size: < 1MB
```

---

## 🎯 常见问题

### Q: Railway 免费额度够用吗？
A: 够！$5/月的额度可以运行 500+ 小时，对于演示和课程项目完全足够。

### Q: 数据会丢失吗？
A: Railway 的 SQLite 数据会持久化存储，不会丢失。但建议定期备份。

### Q: 如何查看部署日志？
A: 在 Railway dashboard 点击你的项目 → "Deployments" → 查看实时日志。

### Q: 部署失败怎么办？
A: 
1. 检查 `requirements.txt` 是否包含所有依赖
2. 确保代码已推送到 GitHub
3. 查看 Railway 的部署日志找到错误信息
4. 确认 `PORT` 环境变量配置正确

### Q: 如何回滚到之前的版本？
A: Railway dashboard → "Deployments" → 选择之前的部署 → "Redeploy"

---

## 💡 额外加分项

部署成功后，你可以在作业中展示：

1. **实际的云端 URL**（可以写在报告封面）
2. **部署截图**（Railway dashboard、应用运行截图）
3. **性能指标**（响应时间、可用性）
4. **移动端适配**（用手机访问的截图）

这些会让你的项目显得更加专业和完整！

---

## 🚀 开始部署

选择一个平台（推荐 Railway），按照上面的步骤操作，5 分钟内就能完成部署！

有任何问题随时问我 😊
