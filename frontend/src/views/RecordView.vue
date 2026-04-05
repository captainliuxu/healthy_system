<script setup>
import { ref } from 'vue'
import BottomNav from '../components/BottomNav.vue'
import '../assets/styles/record.css'

const medication = ref('')
const systolic = ref('')
const diastolic = ref('')
const symptom = ref('')
const saveResult = ref('')

function saveRecord() {
  const recordData = {
    medication: medication.value,
    systolic: systolic.value,
    diastolic: diastolic.value,
    symptom: symptom.value,
    time: new Date().toLocaleString()
  }

  localStorage.setItem('healthRecord', JSON.stringify(recordData))
  saveResult.value = '今日记录已保存'
}
</script>

<template>
  <div class="container">
    <div class="header">健康记录</div>

    <div class="content">
      <div class="page-tip">
        今天也要记得关注自己的身体状态
      </div>

      <div class="card">
        <div class="card-title">今日服药情况</div>
        <div class="card-desc">请记录今天是否已按时服药</div>
        <div class="btn-group">
          <button type="button" @click="medication = '已服用'">已服用</button>
          <button type="button" @click="medication = '未服用'">未服用</button>
        </div>
      </div>

      <div class="card">
        <div class="card-title">血压记录</div>
        <div class="card-desc">输入本次测量结果，方便后续趋势分析</div>
        <div class="input-group">
          <input v-model="systolic" type="text" placeholder="请输入收缩压（高压）" />
          <input v-model="diastolic" type="text" placeholder="请输入舒张压（低压）" />
        </div>
      </div>

      <div class="card">
        <div class="card-title">今日身体状态</div>
        <div class="card-desc">请选择今天最接近的身体感受</div>
        <div class="btn-group">
          <button type="button" @click="symptom = '正常'">正常</button>
          <button type="button" @click="symptom = '头晕'">头晕</button>
          <button type="button" @click="symptom = '乏力'">乏力</button>
        </div>
      </div>

      <div class="card">
        <button type="button" @click="saveRecord">保存今日记录</button>
        <div v-if="saveResult">{{ saveResult }}</div>
      </div>
    </div>

    <BottomNav />
  </div>
</template>