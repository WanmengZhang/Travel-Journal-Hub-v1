# 故障排除指南 (Troubleshooting Guide)

## 常见问题和解决方案

### 1. ❌ "Failed to load entries" 或 "Database connection failed"

**症状**:
- 浏览器显示 "Failed to load entries. Please try again later."
- 终端显示 "Error connecting to MySQL: 2003: Can't connect to MySQL server"

**原因**:
应用尝试连接 MySQL 数据库但本地没有运行 MySQL 服务器。

**解决方案**:
使用 SQLite 模式启动应用：

```bash
# 方法 1: 使用启动脚本（推荐）
./start.sh

# 方法 2: 手动设置环境变量
USE_SQLITE=true python app.py

# 方法 3: 创建 .env 文件
echo "USE_SQLITE=true" > .env
python app.py
```

---

### 2. ❌ "Port 5000 already in use"

**症状**:
```
OSError: [Errno 98] Address already in use
```

**解决方案**:
停止已运行的应用：

```bash
# 查找并停止运行中的 Python 进程
pkill -f "python app.py"

# 或者找到进程 ID 并手动停止
lsof -i :5000
kill -9 <PID>

# 然后重新启动
./start.sh
```

---

### 3. ❌ "ModuleNotFoundError: No module named 'flask'"

**症状**:
```
ModuleNotFoundError: No module named 'flask'
```

**解决方案**:
安装依赖：

```bash
pip install -r requirements.txt

# 如果上面不行，单独安装：
pip install flask flask-cors mysql-connector-python
```

---

### 4. ❌ SQLite 数据库锁定

**症状**:
```
sqlite3.OperationalError: database is locked
```

**解决方案**:
关闭所有访问数据库的连接：

```bash
# 停止应用
pkill -f "python app.py"

# 删除数据库文件（会丢失数据！）
rm travel_journal.db

# 重新启动
./start.sh
```

---

### 5. ❌ 页面显示但没有样式

**症状**:
页面加载了但看起来很丑，没有 CSS 样式。

**解决方案**:
检查静态文件是否存在：

```bash
# 验证文件存在
ls -la static/

# 应该看到：
# styles.css
# home.js
# journals.js
# editor.js

# 清除浏览器缓存并刷新
# Chrome/Edge: Ctrl+Shift+R
# Firefox: Ctrl+F5
# Safari: Cmd+Shift+R
```

---

### 6. ❌ CORS 错误

**症状**:
浏览器控制台显示：
```
Access to fetch at 'http://localhost:5000/api/entries' from origin 'null' has been blocked by CORS policy
```

**解决方案**:
确保 Flask-CORS 已安装并在 `app.py` 中启用：

```bash
# 重新安装 flask-cors
pip install flask-cors

# 验证 app.py 中有这一行：
grep "CORS(app)" app.py
```

---

### 7. ❌ 测试失败

**症状**:
运行 `python test_app.py` 时失败。

**解决方案**:

```bash
# 确保在项目根目录
cd /workspaces/Travel-Journal-Hub-v1

# 确保 USE_SQLITE 环境变量已设置
export USE_SQLITE=true

# 运行测试
python test_app.py

# 如果还是失败，查看具体错误信息
python test_app.py 2>&1 | more
```

---

### 8. ❌ 创建条目后刷新页面不显示

**症状**:
在 Editor 页面创建了条目，跳转到 Journals 页面但看不到。

**可能原因**:
1. 数据库写入失败
2. API 返回错误
3. 浏览器缓存问题

**解决方案**:

```bash
# 1. 检查数据库
sqlite3 travel_journal.db "SELECT * FROM journal_entries;"

# 2. 查看终端日志（应该没有错误）
# 检查是否有 "500 Internal Server Error"

# 3. 测试 API
curl http://localhost:5000/api/entries

# 4. 清除浏览器缓存
# Chrome DevTools: F12 → Application → Clear storage
```

---

### 9. ❌ 图片链接不显示

**症状**:
添加了 photo_links 但图片不显示。

**原因**:
图片 URL 可能无效或需要 CORS 支持。

**解决方案**:

1. 使用支持外链的图片托管服务：
   - Imgur: https://imgur.com/
   - Cloudinary: https://cloudinary.com/
   - ImgBB: https://imgbb.com/

2. 测试图片 URL：
   ```bash
   # 在浏览器直接访问图片 URL，看是否能加载
   ```

3. 图片格式示例：
   ```
   https://i.imgur.com/abc123.jpg
   https://res.cloudinary.com/demo/image/upload/sample.jpg
   ```

---

### 10. ❌ 日期验证错误

**症状**:
无法保存条目，提示 "End date must be after start date"。

**解决方案**:
确保 End Date 晚于 Start Date：
- ✅ Start: 2025-03-15, End: 2025-03-22 （正确）
- ❌ Start: 2025-03-22, End: 2025-03-15 （错误）

---

## 🔍 调试技巧

### 查看实时日志
```bash
# 启动应用时可以看到所有请求日志
./start.sh

# 或者启用 debug 模式（更详细的错误信息）
export FLASK_DEBUG=true
python app.py
```

### 测试 API 端点
```bash
# 获取所有条目
curl http://localhost:5000/api/entries

# 获取特定条目
curl http://localhost:5000/api/entries/1

# 创建新条目
curl -X POST http://localhost:5000/api/entries \
  -H "Content-Type: application/json" \
  -d '{"destination":"Tokyo","start_date":"2025-03-15","end_date":"2025-03-22"}'

# 删除条目
curl -X DELETE http://localhost:5000/api/entries/1
```

### 检查数据库内容
```bash
# 进入 SQLite 命令行
sqlite3 travel_journal.db

# 查看所有条目
SELECT * FROM journal_entries;

# 查看表结构
.schema journal_entries

# 退出
.quit
```

### 浏览器开发者工具
```
F12 打开开发者工具

1. Console 标签: 查看 JavaScript 错误
2. Network 标签: 查看 API 请求和响应
3. Application 标签: 清除缓存和存储
```

---

## 🆘 仍然有问题？

### 完全重置应用

```bash
# 1. 停止所有运行的实例
pkill -f "python app.py"

# 2. 删除数据库（会丢失所有数据！）
rm travel_journal.db

# 3. 重新安装依赖
pip install -r requirements.txt --force-reinstall

# 4. 运行测试
python test_app.py

# 5. 启动应用
./start.sh
```

### 验证环境

```bash
# 检查 Python 版本
python --version  # 应该是 3.7+

# 检查已安装的包
pip list | grep -E "flask|mysql|sqlite"

# 应该看到：
# Flask                 3.0.0
# Flask-Cors            4.0.0
# mysql-connector-python 8.2.0

# 检查文件完整性
python test_app.py  # 所有测试应该通过
```

---

## 📞 获取帮助

如果以上方法都不能解决问题：

1. **查看完整错误日志**:
   ```bash
   python app.py 2>&1 | tee error.log
   ```

2. **检查 GitHub Issues**: 
   https://github.com/WanmengZhang/Travel-Journal-Hub-v1/issues

3. **提供错误信息**:
   - 完整的错误消息
   - 操作系统和 Python 版本
   - 使用的数据库（MySQL 或 SQLite）
   - 复现步骤

---

## ✅ 快速检查清单

问题排查时按顺序检查：

- [ ] 应用是否在运行？(`ps aux | grep python`)
- [ ] 是否使用了正确的数据库模式？(`USE_SQLITE=true`)
- [ ] 端口 5000 是否被占用？(`lsof -i :5000`)
- [ ] 依赖是否都已安装？(`pip list`)
- [ ] 测试是否通过？(`python test_app.py`)
- [ ] 浏览器控制台是否有错误？(F12 → Console)
- [ ] API 是否可访问？(`curl http://localhost:5000/api/entries`)
- [ ] 数据库文件是否存在？(`ls -la travel_journal.db`)

---

**大部分问题都可以通过使用 SQLite 模式和清除缓存解决！** 🎯
