<template>
  <div class="container">
    <div class="header">健康助手</div>

    <div class="content">
      <div class="messages">
        <div 
          v-for="(msg, index) in messages" 
          :key="index" 
          :class="['message', msg.role === 'user' ? 'user-message' : 'ai-message']"
        >
          {{ msg.text }}
        </div>
      </div>

      <div class="input-area">
        <input 
          v-model="inputText" 
          @keyup.enter="handleSend" 
          placeholder="输入消息..." 
          class="input"
        />
        <button @click="handleSend" class="send-btn">发送</button>
      </div>

      <button @click="triggerProactiveMessage" class="proactive-btn">主动提醒</button>
    </div>

    <BottomNav />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import BottomNav from '../components/BottomNav.vue'
import { sendChatMessage } from '../api/chat'

const inputText = ref('')
const messages = ref([
  { role: 'ai', text: '你好，我是你的健康助手。今天感觉怎么样？' },
  { role: 'ai', text: '如果你有头晕、乏力、忘记服药等情况，可以直接告诉我。' },
])

const proactiveMessages = [
  '现在是晚间服药时间，记得按计划完成用药。',
  '你今天还没有记录血压，建议今晚尽快测量一次。',
  '你最近提到过头晕，今晚注意休息，并留意身体状态。',
  '慢病管理最重要的是长期规律，坚持记录会更有帮助。'
]

function triggerProactiveMessage() {
  const randomIndex = Math.floor(Math.random() * proactiveMessages.length)
  messages.value.push({ role: 'ai', text: proactiveMessages[randomIndex] })
}

async function handleSend() {
  const text = inputText.value.trim()
  if (!text) return

  messages.value.push({ role: 'user', text })
  inputText.value = ''

  try {
    const data = await sendChatMessage(text)
    messages.value.push({ role: 'ai', text: data.reply })
  } catch (error) {
    messages.value.push({ role: 'ai', text: '后端连接失败，请确认 FastAPI 已启动' })
  }
}
</script>

<style scoped>
.messages {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 15px;
}

.message {
  padding: 10px 15px;
  margin-bottom: 10px;
  border-radius: 18px;
  max-width: 80%;
  word-wrap: break-word;
}

.ai-message {
  background: #e3f2fd;
  align-self: flex-start;
  border-bottom-left-radius: 5px;
}

.user-message {
  background: #c8e6c9;
  align-self: flex-end;
  margin-left: auto;
  border-bottom-right-radius: 5px;
}

.input-area {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.input {
  flex: 1;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 20px;
  font-size: 16px;
}

.send-btn {
  padding: 12px 20px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
}

.proactive-btn {
  width: 100%;
  padding: 12px;
  background: #ff9800;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 16px;
}
</style>