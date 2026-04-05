<script setup>
import BottomNav from '../components/BottomNav.vue'
</script>

<template>
  <div class="container">
    <div class="header">健康助手</div>

    <div class="content">
      <div class="card">
        <b>早上好 👋</b><br>
        今天记得按时服药
      </div>

      <div class="card">
        <b>今日任务</b><br>
        08:00 服用降压药<br>
        20:00 测量血压
      </div>

      <div class="card">
        <b>AI提醒</b><br>
        你昨晚没有记录血压，今晚建议补测
      </div>

      <div class="card">
        <b>健康知识</b><br>
        高血压患者需要长期监测，而不是偶尔测一次
      </div>
    </div>

    <BottomNav />
  </div>
</template>