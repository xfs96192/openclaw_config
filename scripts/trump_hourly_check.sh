#!/bin/bash
# TrumpDailyPosts 每小时监控脚本
# 只获取最近1小时的新推文，无新内容则不发送

set -e

USERNAME="TrumpDailyPosts"
MAX_RESULTS=20
STATE_FILE="/Users/fanshengxia/clawd/cron/.trump_daily_last_check"

# 获取当前时间戳（毫秒）
CURRENT_TIME=$(date +%s000)

# 读取上次检查时间（默认为1小时前）
if [ -f "$STATE_FILE" ]; then
    LAST_CHECK=$(cat "$STATE_FILE")
else
    LAST_CHECK=$((CURRENT_TIME - 3600000))
fi

# 获取推文
echo "正在检查 @${USERNAME} 的新推文..."
RESPONSE=$(curl -s -X POST "https://ai.6551.io/open/twitter_user_tweets" \
  -H "Authorization: Bearer ${TWITTER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"${USERNAME}\", \"maxResults\": ${MAX_RESULTS}, \"product\": \"Latest\", \"includeReplies\": true, \"includeRetweets\": true}")

# 检查API响应
if [ -z "$RESPONSE" ] || [ "$RESPONSE" = "null" ]; then
    echo "API响应为空"
    exit 0
fi

# 筛选过去1小时内的推文（将Twitter时间转换为时间戳比较）
# Twitter格式: Thu Mar 26 04:25:59 +0000 2026
NEW_TWEETS=$(echo "$RESPONSE" | jq -r --arg last_check "$LAST_CHECK" '
  .data // [] | map(select(.createdAt != null)) | map(select(
    (.createdAt | capture("(?<day>\\w+) (?<month>\\w+) (?<date>\\d+) (?<time>\\d+:\\d+:\\d+) (?<tz>[+-]\\d+) (?<year>\\d+)") | 
    "\(.year)-\(.month)-\(.date)T\(.time)\(.tz[0:3]):\(.tz[3:5])" | 
    fromdateiso8601 * 1000 | tonumber) > ($last_check | tonumber)
  ))
')

TWEET_COUNT=$(echo "$NEW_TWEETS" | jq 'length')

if [ "$TWEET_COUNT" -eq 0 ] || [ "$TWEET_COUNT" = "null" ]; then
    echo "过去1小时内没有新推文"
    # 更新检查时间
    echo "$CURRENT_TIME" > "$STATE_FILE"
    exit 0
fi

echo "发现 ${TWEET_COUNT} 条新推文"

# 格式化输出
echo "$NEW_TWEETS" | jq -r '.[] | "\n═══════════════════════════════════════════════════════════════\n🕐 发布时间: \(.createdAt)\n💬 转发: \(.retweetCount) | ❤️ 点赞: \(.favoriteCount)\n\n🇺🇸 原文 (English):\n\(.text)\n\n🇨🇳 中文翻译:\n[请手动翻译或等待AI处理]\n"'

# 更新检查时间
echo "$CURRENT_TIME" > "$STATE_FILE"

echo "处理完成，已更新检查时间戳"
