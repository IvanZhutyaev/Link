<template>
  <div v-if="isOpen" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>{{ isLogin ? 'Вход' : 'Регистрация' }}</h2>
        <button class="close-btn" @click="closeModal">&times;</button>
      </div>

      <!-- Выбор типа пользователя -->
      <div v-if="!userType" class="user-type-selection">
        <h3>Выберите тип пользователя</h3>
        <div class="type-buttons">
          <button class="type-btn" @click="selectUserType('user')">
            <div class="type-icon">👤</div>
            <div class="type-info">
              <h4>Пользователь</h4>
              <p>Поиск и покупка недвижимости</p>
            </div>
          </button>
          <button class="type-btn" @click="selectUserType('developer')">
            <div class="type-icon">🏢</div>
            <div class="type-info">
              <h4>Застройщик</h4>
              <p>Размещение объектов недвижимости</p>
            </div>
          </button>
        </div>
      </div>

      <!-- Форма входа -->
      <div v-else-if="isLogin" class="login-form">
        <div class="form-group">
          <label v-if="userType === 'user'">Телефон</label>
          <label v-else>ИНН</label>
          <input 
            v-if="userType === 'user'"
            type="tel" 
            v-model="loginData.identifier"
            placeholder="Введите номер телефона"
            class="form-input"
          />
          <input 
            v-else
            type="text" 
            v-model="loginData.identifier"
            placeholder="Введите ИНН"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label>Пароль</label>
          <input 
            type="password" 
            v-model="loginData.password"
            placeholder="Введите пароль"
            class="form-input"
          />
        </div>

        <button class="submit-btn" @click="handleLogin">
          Войти
        </button>

        <div class="form-footer">
          <span>Нет аккаунта? </span>
          <button class="link-btn" @click="switchToRegister">Зарегистрироваться</button>
        </div>
      </div>

      <!-- Форма регистрации -->
      <div v-else class="register-form">
        <!-- Форма для пользователя -->
        <div v-if="userType === 'user'">
          <div class="form-group">
            <label>Имя</label>
            <input 
              type="text" 
              v-model="registerData.name"
              placeholder="Введите ваше имя"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label>Телефон</label>
            <input 
              type="tel" 
              v-model="registerData.phone"
              placeholder="Введите номер телефона"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label>Пароль</label>
            <input 
              type="password" 
              v-model="registerData.password"
              placeholder="Придумайте пароль"
              class="form-input"
            />
          </div>
        </div>

        <!-- Форма для застройщика -->
        <div v-else>
          <div class="form-group">
            <label>Название компании</label>
            <input 
              type="text" 
              v-model="registerData.companyName"
              placeholder="Введите название компании"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label>ИНН</label>
            <input 
              type="text" 
              v-model="registerData.inn"
              placeholder="Введите ИНН"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label>ОГРН</label>
            <input 
              type="text" 
              v-model="registerData.ogrn"
              placeholder="Введите ОГРН"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label>Юридический адрес</label>
            <textarea 
              v-model="registerData.address"
              placeholder="Введите юридический адрес"
              class="form-textarea"
              rows="3"
            ></textarea>
          </div>

          <div class="form-group">
            <label>ФИО и должность представителя</label>
            <input 
              type="text" 
              v-model="registerData.representative"
              placeholder="ФИО и должность"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label>Пароль</label>
            <input 
              type="password" 
              v-model="registerData.password"
              placeholder="Придумайте пароль"
              class="form-input"
            />
          </div>
        </div>

        <button class="submit-btn" @click="handleRegister">
          Зарегистрироваться
        </button>

        <div class="form-footer">
          <span>Уже есть аккаунт? </span>
          <button class="link-btn" @click="switchToLogin">Войти</button>
        </div>
      </div>

      <!-- Кнопка возврата к выбору типа -->
      <div class="back-btn-container">
        <button class="back-btn" @click="backToTypeSelection">
          ← Назад к выбору типа
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { userAPI, developerAPI } from '../utils/api.js'
import analytics from '../utils/analytics.js'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'login-success'])

const isLogin = ref(true)
const userType = ref(null)

const loginData = reactive({
  identifier: '',
  password: ''
})

const registerData = reactive({
  // Для пользователя
  name: '',
  phone: '',
  password: '',
  // Для застройщика
  companyName: '',
  inn: '',
  ogrn: '',
  address: '',
  representative: '',
})

const selectUserType = (type) => {
  // Отслеживаем выбор типа пользователя
  analytics.sendEvent(0, "select_user_type", type === 'developer' ? 2 : 1)
  userType.value = type
}

const switchToLogin = () => {
  // Отслеживаем переключение на форму входа
  analytics.sendEvent(0, "switch_to_login")
  isLogin.value = true
  clearFormData()
}

const switchToRegister = () => {
  // Отслеживаем переключение на форму регистрации
  analytics.sendEvent(0, "switch_to_register")
  isLogin.value = false
  clearFormData()
}

const backToTypeSelection = () => {
  // Отслеживаем возврат к выбору типа
  analytics.sendEvent(0, "back_to_type_selection")
  userType.value = null
  clearFormData()
}

const clearFormData = () => {
  Object.keys(loginData).forEach(key => loginData[key] = '')
  Object.keys(registerData).forEach(key => registerData[key] = '')
}

const closeModal = () => {
  // Отслеживаем закрытие модального окна
  analytics.sendEvent(0, "close_login_modal")
  emit('close')
  userType.value = null
  isLogin.value = true
  clearFormData()
}

const handleLogin = async () => {
  if (userType.value === 'user') {
    if (!loginData.identifier || !loginData.password) {
      alert('Заполните все поля')
      return
    }
    
    try {
      // Отслеживаем попытку входа пользователя
      analytics.sendEvent(0, "login_attempt", 1)
      
      const response = await userAPI.login({
        phone: loginData.identifier,
        password: loginData.password
      })
      
      // Отслеживаем успешный вход пользователя
      analytics.sendEvent(0, "login_success", 1)
      
      emit('login-success', {
        type: 'user',
        name: loginData.identifier,
        ...response
      })
      alert('Вход выполнен успешно! Теперь вы можете перейти в личный кабинет через меню.')
    } catch (e) {
      // Отслеживаем ошибку входа
      analytics.sendEvent(0, "login_error", 1)
      alert('Ошибка входа: ' + (e.message || 'Неизвестная ошибка'))
    }
  } else {
    if (!loginData.identifier || !loginData.password) {
      alert('Заполните все поля')
      return
    }
    
    try {
      // Отслеживаем попытку входа застройщика
      analytics.sendEvent(0, "login_attempt", 2)
      
      const response = await developerAPI.login({
        inn: parseInt(loginData.identifier),
        password: loginData.password
      })
      
      // Отслеживаем успешный вход застройщика
      analytics.sendEvent(0, "login_success", 2)
      
      emit('login-success', {
        type: 'developer',
        name: `Застройщик ${loginData.identifier}`,
        ...response
      })
      alert('Вход выполнен успешно! Теперь вы можете перейти в личный кабинет через меню.')
    } catch (e) {
      // Отслеживаем ошибку входа
      analytics.sendEvent(0, "login_error", 2)
      alert('Ошибка входа: ' + (e.message || 'Неизвестная ошибка'))
    }
  }
  closeModal()
}

const handleRegister = async () => {
  if (userType.value === 'user') {
    if (!registerData.name || !registerData.phone || !registerData.password) {
      alert('Заполните все поля')
      return
    }
    
    // Формируем данные для пользователя
    const userData = {
      "User_name": registerData.name,
      "Phone_number": registerData.phone,
      "password": registerData.password
    }
    try {
      // Отслеживаем попытку регистрации пользователя
      analytics.sendEvent(0, "register_attempt", 1)
      
      const response = await userAPI.register(userData)
      
      // Отслеживаем успешную регистрацию пользователя
      analytics.sendEvent(0, "register_success", 1)
      
      emit('login-success', {
        type: 'user',
        name: registerData.name,
        ...response
      })
      alert('Регистрация выполнена успешно! Теперь вы можете перейти в личный кабинет через меню.')
    } catch (e) {
      // Отслеживаем ошибку регистрации
      analytics.sendEvent(0, "register_error", 1)
      alert('Ошибка регистрации: ' + (e.message || 'Неизвестная ошибка'))
    }
  } else {
    if (!registerData.companyName || !registerData.inn || !registerData.ogrn || 
        !registerData.address || !registerData.representative || !registerData.password) {
      alert('Заполните все поля')
      return
    }
    
    // Формируем данные для застройщика
    const developerData = {
      "Company_name": registerData.companyName,
      "INN": parseInt(registerData.inn),
      "OGRN": parseInt(registerData.ogrn),
      "Adress": registerData.address,
      "User_name": registerData.representative,
      "password": registerData.password
    }
    try {
      // Отслеживаем попытку регистрации застройщика
      analytics.sendEvent(0, "register_attempt", 2)
      
      const response = await developerAPI.register(developerData)
      
      // Отслеживаем успешную регистрацию застройщика
      analytics.sendEvent(0, "register_success", 2)
      
      emit('login-success', {
        type: 'developer',
        name: registerData.companyName,
        ...response
      })
      alert('Регистрация выполнена успешно! Теперь вы можете перейти в личный кабинет через меню.')
    } catch (e) {
      // Отслеживаем ошибку регистрации
      analytics.sendEvent(0, "register_error", 2)
      alert('Ошибка регистрации: ' + (e.message || 'Неизвестная ошибка'))
    }
  }
  closeModal()
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
}

.modal-header h2 {
  margin: 0;
  color: #007aff;
  font-size: 1.5rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.3s ease;
}

.close-btn:hover {
  background: #f5f5f5;
}

.user-type-selection {
  padding: 2rem;
}

.user-type-selection h3 {
  text-align: center;
  margin-bottom: 2rem;
  color: #007aff;
}

.type-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.type-btn {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  border: 2px solid #eee;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
}

.type-btn:hover {
  border-color: #007aff;
  background: rgba(0, 122, 255, 0.05);
}

.type-icon {
  font-size: 2rem;
  width: 50px;
  text-align: center;
}

.type-info h4 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.type-info p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.login-form,
.register-form {
  padding: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 500;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #007aff;
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.submit-btn {
  width: 100%;
  background: #007aff;
  color: white;
  border: none;
  padding: 12px;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-bottom: 1rem;
}

.submit-btn:hover {
  background: #0056cc;
}

.form-footer {
  text-align: center;
  color: #666;
}

.link-btn {
  background: none;
  border: none;
  color: #007aff;
  cursor: pointer;
  font-weight: 500;
  text-decoration: underline;
}

.link-btn:hover {
  color: #0056cc;
}

.back-btn-container {
  padding: 1rem 2rem 2rem;
  text-align: center;
}

.back-btn {
  background: none;
  border: none;
  color: #666;
  cursor: pointer;
  font-size: 0.9rem;
  text-decoration: underline;
}

.back-btn:hover {
  color: #007aff;
}

@media (max-width: 768px) {
  .modal-content {
    margin: 1rem;
    max-height: calc(100vh - 2rem);
  }
  
  .type-btn {
    padding: 1rem;
  }
  
  .type-icon {
    font-size: 1.5rem;
    width: 40px;
  }
}
</style> 