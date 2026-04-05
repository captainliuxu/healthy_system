<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
  <div class="navbar">
    <router-link to="/" :class="{ active: route.path === '/' }">首页</router-link>
    <router-link to="/chat" :class="{ active: route.path === '/chat' }">聊天</router-link>
    <router-link to="/record" :class="{ active: route.path === '/record' }">记录</router-link>
    <router-link to="/profile" :class="{ active: route.path === '/profile' }">我的</router-link>
  </div>
</template>