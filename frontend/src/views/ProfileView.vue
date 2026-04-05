<script setup>
import BottomNav from '../components/BottomNav.vue'
</script>

<template>
  <div class="container">
    <div class="header">我的</div>

    <div class="content">
      <div class="card">疾病：高血压</div>

      <div class="card">
        用药计划：<br>
        早 8:00<br>
        晚 8:00
      </div>

      <div class="card">
        检测计划：<br>
        每晚测一次血压
      </div>

      <div class="card">
        建议：<br>
        低盐饮食、规律作息、适量运动
      </div>
    </div>

    <BottomNav />
  </div>
</template>