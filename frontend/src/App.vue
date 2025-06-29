<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import analytics from './utils/analytics.js';
import Header from './components/Header.vue'
import HeroGallery from './components/HeroGallery.vue'
import ComplexSearch from './components/ComplexSearch.vue'
import UserDashboard from './components/UserDashboard.vue'
import DeveloperDashboard from './components/DeveloperDashboard.vue'
import PromotionBlock from './components/PromotionBlock.vue'
import TopDevelopers from './components/TopDevelopers.vue'
import MapYandex from './components/MapYandex.vue'
import ChatAssistant from './components/ChatAssistant.vue'

const apartmentId = 123; // Можно заменить на актуальный id
let startTime = 0;

// Состояние приложения
const currentView = ref('home') // 'home', 'complex-search', 'user-dashboard', 'developer-dashboard'
const userType = ref(null) // 'user', 'developer'
const selectedComplex = ref(null)

onMounted(() => {
  startTime = Date.now();
  
  // Очищаем старые данные о текущем представлении
  localStorage.removeItem('currentView')
  
  // По умолчанию показываем главную страницу
  currentView.value = 'home'
  
  // Проверяем, есть ли сохраненный тип пользователя (только для данных пользователя)
  const savedUserType = localStorage.getItem('userType')
  
  if (savedUserType) {
    userType.value = savedUserType
  }
  
  // Отслеживаем загрузку главной страницы
  analytics.sendEvent(0, "page_load", 1)
});

onBeforeUnmount(() => {
  const duration = (Date.now() - startTime) / 1000;
  analytics.sendEvent(apartmentId, "time_on_page", duration);
});

// Методы для переключения между представлениями
const showHome = () => {
  currentView.value = 'home'
  analytics.sendEvent(0, "navigate_home")
}

const showComplexSearch = () => {
  currentView.value = 'complex-search'
  analytics.sendEvent(0, "navigate_complex_search")
}

const showUserDashboard = () => {
  currentView.value = 'user-dashboard'
  userType.value = 'user'
  localStorage.setItem('userType', 'user')
  analytics.sendEvent(0, "navigate_user_dashboard")
}

const showDeveloperDashboard = () => {
  currentView.value = 'developer-dashboard'
  userType.value = 'developer'
  localStorage.setItem('userType', 'developer')
  analytics.sendEvent(0, "navigate_developer_dashboard")
}

const logout = () => {
  analytics.sendEvent(0, "user_logout")
  currentView.value = 'home'
  userType.value = null
  localStorage.removeItem('userType')
  localStorage.removeItem('userInfo')
}

const handleLoginSuccess = (userData) => {
  // Отслеживаем успешный вход
  analytics.sendEvent(0, "user_login", userData.type === 'developer' ? 2 : 1)
  
  // Сохраняем информацию о пользователе
  localStorage.setItem('userInfo', JSON.stringify(userData))
  
  // НЕ переходим автоматически в личный кабинет
  // Пользователь остается на главной странице
  // Личный кабинет доступен через меню в хедере
}

const handleGoToDashboard = (userType) => {
  if (userType === 'user') {
    showUserDashboard()
  } else if (userType === 'developer') {
    showDeveloperDashboard()
  }
}

const handleGoHome = () => {
  showHome()
}

const handleComplexSelected = (complex) => {
  selectedComplex.value = complex
  // Можно добавить дополнительную логику при выборе ЖК
}

const handleDeveloperSelected = (developerId) => {
  // Можно добавить логику для перехода к странице застройщика
  console.log('Выбран застройщик:', developerId)
  analytics.sendEvent(developerId, "developer_selected")
}
</script>

<template>
  <div id="app">
    <!-- Главная страница -->
    <div v-if="currentView === 'home'">
      <Header 
        @login-success="handleLoginSuccess"
        @go-to-dashboard="handleGoToDashboard"
        @go-home="handleGoHome"
        @logout="logout"
        @search-complexes="showComplexSearch"
      />
      <HeroGallery @search-complexes="showComplexSearch" />
      <PromotionBlock />
      <TopDevelopers @developer-selected="handleDeveloperSelected" />
      <MapYandex />
    </div>

    <!-- Поиск ЖК -->
    <div v-else-if="currentView === 'complex-search'">
      <Header 
        @login-success="handleLoginSuccess"
        @go-to-dashboard="handleGoToDashboard"
        @go-home="handleGoHome"
        @logout="logout"
        @search-complexes="showComplexSearch"
      />
      <ComplexSearch 
        @complex-selected="handleComplexSelected"
        @go-back="showHome"
      />
    </div>

    <!-- Личный кабинет пользователя -->
    <div v-else-if="currentView === 'user-dashboard'">
      <UserDashboard @logout="logout" @go-back="showHome" />
    </div>

    <!-- Личный кабинет застройщика -->
    <div v-else-if="currentView === 'developer-dashboard'">
      <DeveloperDashboard @logout="logout" @go-back="showHome" />
    </div>
    <ChatAssistant />
  </div>
</template>

<style scoped>
#app {
  margin: 0;
  padding: 0;
  font-weight: normal;
}
</style>
