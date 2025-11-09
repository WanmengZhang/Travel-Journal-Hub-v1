# Vercel 云部署指南

将 Travel Journal Hub 部署到 Vercel 的完整教程。

---

## 🌟 为什么选择 Vercel

- ✅ **完全免费** - 个人项目无需付费
- ✅ **无需信用卡** - 注册即可使用
- ✅ **中国可访问** - 大部分地区可直接访问
- ✅ **自动部署** - 推送代码自动更新
- ✅ **全球 CDN** - 访问速度快
- ✅ **免费 HTTPS** - 自动配置 SSL 证书

---

## 📋 部署步骤

### 第一步：准备项目

项目已包含 `vercel.json` 配置文件：

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    },
    {
      "src": "static/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "USE_SQLITE": "true"
  }
}
```

### 第二步：推送代码到 GitHub

```bash
git add .
git commit -m "Ready for Vercel deployment"
git push origin main
```

### 第三步：注册 Vercel

1. 访问 **[vercel.com](https://vercel.com/)**
2. 点击 **"Sign Up"**（注册）
3. 选择 **"Continue with GitHub"**（推荐）
4. 授权 Vercel 访问你的 GitHub

### 第四步：导入项目

1. 登录后点击 **"Add New..."** → **"Project"**
2. 找到 **`Travel-Journal-Hub-v1`** 仓库
3. 点击 **"Import"**

### 第五步：配置项目

保持默认配置即可：

| 配置项 | 值 |
|--------|-----|
| **Project Name** | travel-journal-hub |
| **Framework Preset** | Other |
| **Root Directory** | ./ |
| **Build Command** | 留空 |
| **Output Directory** | 留空 |

### 第六步：部署

1. 点击 **"Deploy"** 按钮
2. 等待 2-3 分钟构建完成
3. 获取部署 URL（格式：`https://项目名.vercel.app`）

---

## ✅ 验证部署

访问以下页面确认部署成功：

- **首页**：`https://你的域名.vercel.app/`
- **日记列表**：`https://你的域名.vercel.app/journals`
- **编辑器**：`https://你的域名.vercel.app/editor`
- **API**：`https://你的域名.vercel.app/api/entries`

---

## 🔄 自动部署

配置成功后：
- ✅ 每次推送到 `main` 分支自动重新部署
- ✅ 其他分支推送创建预览部署
- ✅ Pull Request 自动生成预览链接

---

## 🔧 常见问题

### Q1: 部署失败怎么办？

**解决方案**：
1. 在 Vercel Dashboard 查看部署日志
2. 检查 `vercel.json` 配置
3. 确认 `requirements.txt` 包含所有依赖

### Q2: 如何查看部署日志？

**步骤**：
1. 登录 Vercel Dashboard
2. 选择你的项目
3. 点击 **"Deployments"** 标签
4. 点击具体部署查看日志

### Q3: 数据会丢失吗？

**说明**：
- ⚠️ Vercel 是无服务器环境，SQLite 数据会在每次部署后重置
- ✅ 适合演示和测试
- 💡 如需数据持久化，可使用外部数据库（PlanetScale、Supabase）

### Q4: 免费额度够用吗？

**额度说明**：
- ✅ 100 GB 带宽/月
- ✅ 无限次部署
- ✅ 免费 SSL 证书
- ✅ 全球 CDN

对于课程项目完全够用！

### Q5: 在中国能访问吗？

**访问情况**：
- ✅ 大部分地区可直接访问
- ⚠️ 部分地区可能较慢
- 💡 访问有问题可尝试更换网络

### Q6: 如何自定义域名？

**步骤**：
1. Vercel Dashboard → 项目 → **"Settings"**
2. 点击 **"Domains"**
3. 添加自定义域名
4. 按提示配置 DNS 记录

### Q7: 如何回滚版本？

**步骤**：
1. **"Deployments"** → 选择之前的部署
2. 点击 **"..."** → **"Promote to Production"**
3. 确认回滚

---

## 📊 性能优化（可选）

### 启用静态文件缓存

在 `vercel.json` 添加：

```json
{
  "headers": [
    {
      "source": "/static/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

### 配置环境变量

在 Vercel Dashboard：
1. 项目 → **"Settings"** → **"Environment Variables"**
2. 添加需要的环境变量
3. 在代码中使用 `os.environ.get('变量名')`

---

## 📝 部署完成后

在 `REPORT.md` 添加部署信息：

```markdown
### 7.4 云部署

**部署平台**：Vercel  
**部署 URL**：https://travel-journal-hub.vercel.app  
**部署时间**：2025年1月9日

**配置**：
- Framework: Flask (Python)
- Database: SQLite
- CDN: 全球加速
- HTTPS: 自动启用

**特性**：
- ✅ GitHub 自动部署
- ✅ 全球 CDN 加速
- ✅ 免费 HTTPS
- ✅ 零停机部署
```

---

## 🚀 快速开始

```bash
# 1. 提交代码
git add .
git commit -m "Ready for Vercel deployment"
git push origin main

# 2. 访问 Vercel
# https://vercel.com/

# 3. 导入项目并部署
# 完成！
```

---

## 🆘 需要帮助？

- **Vercel 文档**：[vercel.com/docs](https://vercel.com/docs)
- **部署日志**：Dashboard → Deployments
- **常见问题**：参见上方"常见问题"部分

---

**预计部署时间**：5-10 分钟（首次）

**成功标志**：获得 `.vercel.app` 域名，可以访问应用

**祝部署顺利！** 🎉
