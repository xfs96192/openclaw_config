---
name: photo-snap
description: 自动化拍照流程。打开 Photo Booth → 截图 → 上传到飞书云盘 → 发送链接给用户。当用户说"拍照"、"截图"、"拍张照"、"截个图"时触发此技能。
---

# 自动化拍照技能 - Photo Snap

## 功能描述

一键完成拍照并分享到飞书云盘的完整流程：
1. 打开 Photo Booth 应用
2. 截取屏幕截图
3. 上传到飞书云盘（创建文档并插入图片）
4. 将云盘链接发送给用户

## 触发条件

当用户提到以下关键词时触发：
- "拍照"
- "截图"
- "拍张照"
- "截个图"
- "打开摄像头拍照"
- "截图发给我"

## 执行流程

### 步骤 1: 打开 Photo Booth

```bash
open -a "Photo Booth"
```

**说明：** Photo Booth 是 macOS 自带的相机应用，打开后可以手动拍照或用于提示用户相机已就绪。

### 步骤 2: 执行屏幕截图

```bash
/usr/sbin/screencapture -x ~/Desktop/screenshot_$(date +%Y%m%d_%H%M%S).png
```

**参数说明：**
- `-x`: 不播放快门声音
- 输出路径：`~/Desktop/screenshot_YYYYMMDD_HHMMSS.png`

**验证截图成功：**
```bash
ls -lt ~/Desktop/screenshot_*.png | head -1
```

### 步骤 3: 创建飞书文档并上传图片

**3.1 创建新文档：**
```
action: create
title: 截图 - YYYYMMDD_HHMMSS
```

**3.2 上传图片到文档：**
```
action: upload_image
doc_token: [上一步返回的 document_id]
file_path: [截图文件路径]
```

**3.3 获取云盘链接：**
文档 URL 格式：`https://feishu.cn/docx/{document_id}`

### 步骤 4: 发送云盘链接给用户

通过飞书消息发送：
- 文件名称和大小
- 云盘链接
- 简洁的说明文字

## 完整执行示例

```python
# 伪代码示例
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
screenshot_path = f"~/Desktop/screenshot_{timestamp}.png"

# 1. 打开 Photo Booth
exec('open -a "Photo Booth"')

# 2. 截图
result = exec(f'/usr/sbin/screencapture -x {screenshot_path}')
if result.status != 0:
    return "截图失败，请检查屏幕录制权限"

# 3. 创建飞书文档
doc = feishu_doc(action='create', title=f'截图 - {timestamp}')

# 4. 上传图片
upload = feishu_doc(
    action='upload_image',
    doc_token=doc.document_id,
    file_path=screenshot_path
)

# 5. 发送消息
message.send(
    message=f"📸 截图已上传到飞书云盘！\n\n**文件：** screenshot_{timestamp}.png\n**大小：** {upload.size} bytes\n\n📎 云盘链接：https://feishu.cn/docx/{doc.document_id}",
    target=user_id
)
```

## 错误处理

### 常见错误及解决方案

**1. 截图失败 - "could not create image from display"**
- **原因：** 缺少屏幕录制权限
- **解决：** 引导用户前往「系统设置 → 隐私与安全性 → 屏幕录制」授权终端

**2. Photo Booth 无法打开**
- **原因：** 系统限制或应用损坏
- **解决：** 尝试使用系统截图快捷键 `Command + Shift + 3`

**3. 飞书上传失败**
- **原因：** 文件过大或网络问题
- **解决：** 检查文件大小，重试上传

## 文件管理

**截图保存位置：** `~/Desktop/screenshot_YYYYMMDD_HHMMSS.png`

**清理建议：** 
- 上传成功后可保留截图（用户可能需要本地备份）
- 如需清理，可删除 7 天前的截图文件

## 权限要求

1. **macOS 屏幕录制权限** - 必须授权终端应用
2. **飞书文档写入权限** - 需要文档创建和图片上传权限
3. **飞书消息发送权限** - 需要联系人消息发送权限

## 使用示例

**用户：** "拍照"
**小梦：** 执行完整流程 → 返回云盘链接

**用户：** "截个图发给我"
**小梦：** 执行完整流程 → 返回云盘链接

**用户：** "打开摄像头拍照"
**小梦：** 执行完整流程 → 返回云盘链接

## 注意事项

1. 首次使用前需确保已获得屏幕录制权限
2. 截图文件会保存到桌面，注意定期清理
3. 飞书文档默认创建在根目录，用户可后续移动
4. 整个过程约 5-10 秒，无需用户干预

---

*🐱 小梦的拍照技能 - 一键截图，自动上传，随时分享！*
