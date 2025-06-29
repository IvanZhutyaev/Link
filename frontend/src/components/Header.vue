<template>
  <header class="header">
    <div class="header-container">
      <div class="logo" @click="goHome">
        <img src="@/assets/logo.svg" alt="Логотип" class="logo-img" />
        
      </div>
      
      <nav class="nav">
        <button class="nav-link search-complexes-btn" @click="searchComplexes">
          Поиск ЖК
        </button>
        <a href="#" class="nav-link">Новостройки</a>
        <a href="#" class="nav-link">Застройщики</a>
        <a href="#" class="nav-link">Дома</a>
        <a href="#" class="nav-link">Управляющие компании</a>
        <a href="#" class="nav-link">Услуги</a>
      </nav>
      
      <div class="auth">
        <div v-if="isLoggedIn" class="user-menu">
          <button class="user-btn" @click="toggleUserMenu">
            <span class="user-status-indicator"></span>
            {{ userInfo.name }}
            <span class="user-icon">▼</span>
          </button>
          <div v-if="showUserMenu" class="user-dropdown">
            <button class="dropdown-item" @click="goToDashboard">
              Личный кабинет
            </button>
            <button class="dropdown-item" @click="logout">
              Выйти
            </button>
          </div>
        </div>
        <button v-else class="btn-login" @click="openLoginModal">
          Войти
        </button>
      </div>
    </div>
    
    <!-- Модальное окно входа -->
    <LoginModal 
      :is-open="isLoginModalOpen" 
      @close="closeLoginModal"
      @login-success="handleLoginSuccess"
    />
  </header>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import LoginModal from './LoginModal.vue'
import analytics from '../utils/analytics.js'

const emit = defineEmits(['login-success', 'go-to-dashboard', 'go-home', 'logout', 'search-complexes'])

const isLoginModalOpen = ref(false)
const isLoggedIn = ref(false)
const showUserMenu = ref(false)
const userInfo = ref({
  name: 'Пользователь',
  type: null
})

const openLoginModal = () => {
  // Отслеживаем открытие модального окна входа
  analytics.sendEvent(0, "open_login_modal")
  isLoginModalOpen.value = true
}

const closeLoginModal = () => {
  isLoginModalOpen.value = false
}

const handleLoginSuccess = (userData) => {
  isLoggedIn.value = true
  userInfo.value = {
    name: userData.name || 'Пользователь',
    type: userData.type
  }
  closeLoginModal()
  
  // Сохраняем информацию о пользователе в localStorage
  localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
  
  // Эмитим событие для родительского компонента
  emit('login-success', userData)
}

const toggleUserMenu = () => {
  // Отслеживаем открытие/закрытие меню пользователя
  analytics.sendEvent(0, "toggle_user_menu")
  showUserMenu.value = !showUserMenu.value
}

const goToDashboard = () => {
  // Отслеживаем переход в личный кабинет
  analytics.sendEvent(0, "go_to_dashboard", userInfo.value.type === 'developer' ? 2 : 1)
  showUserMenu.value = false
  // Переход к личному кабинету будет обработан в родительском компоненте
  emit('go-to-dashboard', userInfo.value.type)
}

const logout = () => {
  // Отслеживаем выход пользователя
  analytics.sendEvent(0, "header_logout")
  isLoggedIn.value = false
  userInfo.value = { name: 'Пользователь', type: null }
  showUserMenu.value = false
  
  // Очищаем данные из localStorage
  localStorage.removeItem('userInfo')
  localStorage.removeItem('userType')
  
  emit('logout')
}

const goHome = () => {
  // Отслеживаем переход на главную страницу через логотип
  analytics.sendEvent(0, "logo_click")
  emit('go-home')
}

const searchComplexes = () => {
  // Отслеживаем поиск ЖК
  analytics.sendEvent(0, "search_complexes")
  emit('search-complexes')
}

onMounted(() => {
  // Проверяем, есть ли сохраненные данные пользователя
  const savedUser = localStorage.getItem('userInfo')
  if (savedUser) {
    const user = JSON.parse(savedUser)
    isLoggedIn.value = true
    userInfo.value = user
  }
})
</script>

<style scoped>
.header {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 122, 255, 0.15);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.header-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 70px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.logo:hover {
  opacity: 0.8;
}

.logo-img {
  width: 40px;
  height: 40px;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 600;
  color: #007aff;
}

.nav {
  display: flex;
  gap: 2rem;
}

.nav-link {
  text-decoration: none;
  color: #2c3e50;
  font-weight: 500;
  transition: all 0.3s ease;
  padding: 8px 12px;
  border-radius: 6px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: inherit;
  font-family: inherit;
}

.nav-link:hover {
  color: #007aff;
  background: rgba(0, 122, 255, 0.1);
}

.search-complexes-btn {
  background: #007aff;
  color: white;
  font-weight: 600;
}

.search-complexes-btn:hover {
  background: #0056b3;
  color: white;
}

.auth {
  position: relative;
}

.btn-login {
  background: #007aff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-login:hover {
  background: #0056b3;
}

.user-menu {
  position: relative;
}

.user-btn {
  background: none;
  border: none;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  color: #2c3e50;
  transition: background 0.2s;
}

.user-btn:hover {
  background: rgba(0, 122, 255, 0.1);
}

.user-status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #28a745;
}

.user-icon {
  font-size: 12px;
  transition: transform 0.2s;
}

.user-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border: 1px solid #e1e5e9;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  min-width: 160px;
  z-index: 1001;
  margin-top: 4px;
}

.dropdown-item {
  display: block;
  width: 100%;
  padding: 12px 16px;
  border: none;
  background: none;
  text-align: left;
  cursor: pointer;
  font-size: 14px;
  color: #2c3e50;
  transition: background 0.2s;
}

.dropdown-item:hover {
  background: #f8f9fa;
}

.dropdown-item:first-child {
  border-radius: 8px 8px 0 0;
}

.dropdown-item:last-child {
  border-radius: 0 0 8px 8px;
}

@media (max-width: 768px) {
  .header-container {
    padding: 0 1rem;
  }
  
  .nav {
    display: none;
  }
  
  .logo-text {
    font-size: 1.2rem;
  }
}
</style> 