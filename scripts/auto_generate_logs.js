#!/usr/bin/env node
/**
 * 自动日志生成脚本
 * 每日自动生成金融市场日报和AI资讯日报
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// 配置
const CONFIG = {
  vaultPath: '/Users/fanshengxia/Library/Mobile Documents/iCloud~md~obsidian/Documents/工作/工作',
  logPath: '日志',
  wechatId: 'o9cq802mhu_ZgJtHr2xhUd624hZ4@im.wechat'
};

// 获取日期
const now = new Date();
const date = now.toISOString().split('T')[0];
const time = now.toLocaleString('zh-CN', { 
  year: 'numeric', 
  month: '2-digit', 
  day: '2-digit',
  hour: '2-digit',
  minute: '2-digit'
});

console.log(`[${time}] 开始生成 ${date} 的日志...`);

// 确保目录存在
const fullLogPath = path.join(CONFIG.vaultPath, CONFIG.logPath);
if (!fs.existsSync(fullLogPath)) {
  fs.mkdirSync(fullLogPath, { recursive: true });
}

// 生成金融市场日报模板
const financeTemplate = `# 金融市场日报 - ${date}

> 记录时间：${time}
> 来源：新浪财经、公开市场数据
> 生成方式：OpenClaw 自动整理

---

## 📊 市场概况

### A股主要指数
| 指数 | 收盘 | 涨跌 | 涨跌幅 |
|------|------|------|--------|
| 上证综指 | - | - | - |
| 深证成指 | - | - | - |
| 创业板指 | - | - | - |
| 科创综指 | - | - | - |
| 沪深300 | - | - | - |

**要点**：待更新

---

## 🔥 要闻速递

### 1. 政策动态
- 待更新

### 2. 市场热点
- 待更新

### 3. 资金流向
- 待更新

---

## 📝 投资思考

### 今日观察
1. 
2. 
3. 

### 明日关注
- [ ] 
- [ ] 
- [ ] 

---

## 🏷️ 标签
#金融市场 #A股 #投资日志 #${date.substring(0, 7)}

---

*由 OpenClaw 自动整理生成*
`;

// 生成AI资讯日报模板
const aiTemplate = `# AI 资讯日报 - ${date}

> 记录时间：${time}
> 来源：机器之心、行业动态
> 生成方式：OpenClaw 自动整理

---

## 🚀 重磅发布

### 1. 
- 

### 2. 
- 

### 3. 
- 

---

## 🔬 技术突破

### 1. 
- 

### 2. 
- 

---

## 🏢 大厂动态

### 
- 

---

## 📝 投资/应用思考

### 值得关注的方向
1. 
2. 
3. 

---

## 🏷️ 标签
#AI #大模型 #投资日志 #${date.substring(0, 7)}

---

*由 OpenClaw 自动整理生成*
`;

// 写入文件
const financePath = path.join(fullLogPath, `${date}-金融市场日报.md`);
const aiPath = path.join(fullLogPath, `${date}-AI资讯日报.md`);

fs.writeFileSync(financePath, financeTemplate);
fs.writeFileSync(aiPath, aiTemplate);

console.log(`✅ 日志模板已生成：`);
console.log(`  - ${financePath}`);
console.log(`  - ${aiPath}`);

// 发送通知（通过 OpenClaw）
try {
  const message = `📋 今日日志已生成！

${date} 的日志模板已创建：
✅ 金融市场日报
✅ AI资讯日报

请说"填充今日日志"让我自动获取资讯并填充内容。`;

  execSync(`openclaw message send --to "${CONFIG.wechatId}" --message "${message}"`, {
    stdio: 'inherit'
  });
} catch (e) {
  console.log('通知发送失败，但日志已生成');
}

console.log(`[${time}] 完成！`);
