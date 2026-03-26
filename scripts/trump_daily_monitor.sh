#!/bin/bash
# TrumpDailyPosts 监控脚本 - 每小时执行
# 获取最新推文，翻译并发送

set -e

# 配置
USERNAME="TrumpDailyPosts"
MAX_RESULTS=20
WEBHOOK_URL="https://gateway.openclaw.ai/webhook/..."  # 需要配置

# 获取推文
echo "正在获取 @${USERNAME} 的最新推文..."
RESPONSE=$(curl -s -X POST "https://ai.6551.io/open/twitter_user_tweets" \
  -H "Authorization: Bearer ${TWITTER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"${USERNAME}\", \"maxResults\": ${MAX_RESULTS}, \"product\": \"Latest\", \"includeReplies\": true, \"includeRetweets\": true}")

# 检查是否有新推文
TWEET_COUNT=$(echo "$RESPONSE" | jq '.data | length')
if [ "$TWEET_COUNT" -eq 0 ]; then
    echo "没有新推文"
    exit 0
fi

echo "获取到 ${TWEET_COUNT} 条推文，正在处理..."

# 处理每条推文
echo "$RESPONSE" | jq -c '.data[]' | while read -r tweet; do
    CREATED_AT=$(echo "$tweet" | jq -r '.createdAt')
    TEXT=$(echo "$tweet" | jq -r '.text')
    RETWEETS=$(echo "$tweet" | jq -r '.retweetCount')
    LIKES=$(echo "$tweet" | jq -r '.favoriteCount')
    
    # 跳过空内容
    if [ -z "$TEXT" ] || [ "$TEXT" = "null" ]; then
        continue
    fi
    
    # 构建消息
    MESSAGE=$(cat <<EOF
🕐 ${CREATED_AT}
💬 转发: ${RETWEETS} | ❤️ 点赞: ${LIKES}

🇺🇸 原文:
${TEXT}

🇨🇳 中文翻译:
[待翻译]
EOF
)
    
    echo "$MESSAGE"
    echo "---"
done

echo "处理完成"
