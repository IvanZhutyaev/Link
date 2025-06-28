<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h1>Личный кабинет</h1>
      <div class="header-actions">
        <button class="back-btn" @click="goBack">← Вернуться</button>
        <button class="logout-btn" @click="logout">Выйти</button>
      </div>
    </div>

    <div class="dashboard-content">
      <!-- Индикатор загрузки -->
      <div v-if="loading" class="loading-indicator">
        <div class="loading-spinner"></div>
        <p>Загрузка данных...</p>
      </div>

      <!-- Личная информация -->
      <div v-else class="dashboard-section">
        <h2>Личная информация</h2>
        <div class="user-info">
          <div class="info-item">
            <label>Имя:</label>
            <span>{{ userInfo.name }}</span>
          </div>
          <div class="info-item">
            <label>Телефон:</label>
            <span>{{ userInfo.phone }}</span>
          </div>
          <button class="edit-btn" @click="editProfile">Редактировать</button>
        </div>
      </div>

      <!-- Забронированные объекты -->
      <div v-if="!loading" class="dashboard-section">
        <h2>Забронированные квартиры</h2>
        <div v-if="bookedProperties.length === 0" class="empty-state">
          <p>У вас пока нет забронированных квартир</p>
          <button class="browse-btn" @click="browseProperties">Найти квартиру</button>
        </div>
        <div v-else class="properties-grid">
          <div 
            v-for="property in bookedProperties" 
            :key="property.id"
            class="property-card"
          >
            <div class="property-image">
              <img :src="property.image" :alt="property.name" />
              <div class="property-status booked">Забронировано</div>
            </div>
            <div class="property-info">
              <h3>{{ property.name }}</h3>
              <p class="property-address">{{ property.address }}</p>
              <p class="property-price">{{ property.price }} ₽</p>
              <div class="property-actions">
                <button class="action-btn primary" @click="buyProperty(property.id)">
                  Купить
                </button>
                <button class="action-btn secondary" @click="applyMortgage(property.id)">
                  Ипотека
                </button>
                <button class="action-btn danger" @click="cancelBooking(property.id)">
                  Отменить бронь
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Купленные объекты -->
      <div v-if="!loading" class="dashboard-section">
        <h2>Купленные квартиры</h2>
        <div v-if="purchasedProperties.length === 0" class="empty-state">
          <p>У вас пока нет купленных квартир</p>
        </div>
        <div v-else class="properties-grid">
          <div 
            v-for="property in purchasedProperties" 
            :key="property.id"
            class="property-card"
          >
            <div class="property-image">
              <img :src="property.image" :alt="property.name" />
              <div class="property-status purchased">Куплено</div>
            </div>
            <div class="property-info">
              <h3>{{ property.name }}</h3>
              <p class="property-address">{{ property.address }}</p>
              <p class="property-price">{{ property.price }} ₽</p>
              <p class="property-payment">Способ оплаты: {{ getPaymentMethodText(property.payment_method) }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Ипотечные заявки -->
      <div v-if="!loading" class="dashboard-section">
        <h2>Ипотечные заявки</h2>
        <div v-if="mortgages.length === 0" class="empty-state">
          <p>У вас пока нет ипотечных заявок</p>
        </div>
        <div v-else class="mortgages-list">
          <div 
            v-for="mortgage in mortgages" 
            :key="mortgage.id"
            class="mortgage-card"
          >
            <div class="mortgage-info">
              <h3>{{ mortgage.property_name }}</h3>
              <p class="mortgage-amount">Сумма кредита: {{ mortgage.loan_amount.toLocaleString() }} ₽</p>
              <p class="mortgage-rate">Ставка: {{ mortgage.interest_rate }}%</p>
              <p class="mortgage-term">Срок: {{ mortgage.loan_term_years }} лет</p>
              <p class="mortgage-status">Статус: {{ mortgage.status }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Поиск недвижимости -->
      <div class="dashboard-section">
        <h2>Поиск квартир</h2>
        <div class="search-form">
          <!-- Основные фильтры -->
          <div class="search-filters-grid">
            <div class="filter-group">
              <label class="filter-label">Город</label>
              <input 
                v-model="searchFilters.city" 
                type="text" 
                placeholder="Введите город"
                class="filter-input"
              />
            </div>
            
            <div class="filter-group">
              <label class="filter-label">Цена</label>
              <div class="price-range">
                <input 
                  v-model="searchFilters.minPrice" 
                  type="number" 
                  placeholder="От"
                  class="filter-input price-input"
                />
                <span class="price-separator">—</span>
                <input 
                  v-model="searchFilters.maxPrice" 
                  type="number" 
                  placeholder="До"
                  class="filter-input price-input"
                />
              </div>
            </div>
            
            <div class="filter-group">
              <label class="filter-label">Площадь</label>
              <div class="area-range">
                <input 
                  v-model="searchFilters.minArea" 
                  type="number" 
                  placeholder="От"
                  class="filter-input area-input"
                />
                <span class="area-separator">—</span>
                <input 
                  v-model="searchFilters.maxArea" 
                  type="number" 
                  placeholder="До"
                  class="filter-input area-input"
                />
                <span class="area-unit">м²</span>
              </div>
            </div>
          </div>
          
          <!-- Фильтр по комнатам -->
          <div class="rooms-filter">
            <label class="filter-label">Количество комнат</label>
            <div class="rooms-buttons">
              <button 
                @click="searchFilters.rooms = ''" 
                :class="['room-btn', { active: searchFilters.rooms === '' }]"
              >
                Все
              </button>
              <button 
                @click="searchFilters.rooms = '1'" 
                :class="['room-btn', { active: searchFilters.rooms === '1' }]"
              >
                1
              </button>
              <button 
                @click="searchFilters.rooms = '2'" 
                :class="['room-btn', { active: searchFilters.rooms === '2' }]"
              >
                2
              </button>
              <button 
                @click="searchFilters.rooms = '3'" 
                :class="['room-btn', { active: searchFilters.rooms === '3' }]"
              >
                3
              </button>
              <button 
                @click="searchFilters.rooms = '4'" 
                :class="['room-btn', { active: searchFilters.rooms === '4' }]"
              >
                4+
              </button>
            </div>
          </div>
          
          <!-- Кнопки действий -->
          <div class="search-actions">
            <button @click="searchProperties" class="search-btn">
              <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"></circle>
                <path d="m21 21-4.35-4.35"></path>
              </svg>
              Найти квартиры
            </button>
            <button @click="clearFilters" class="clear-btn">
              <svg class="clear-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 6h18"></path>
                <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path>
                <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
              </svg>
              Очистить
            </button>
          </div>
        </div>

        <div v-if="searchResults.length > 0" class="search-results">
          <h3>Результаты поиска ({{ searchResults.length }})</h3>
          <div class="properties-grid">
            <div 
              v-for="property in searchResults" 
              :key="property.id"
              class="property-card"
            >
              <div class="property-image">
                <img :src="property.image" :alt="property.name" />
                <div class="property-status available">Доступно</div>
              </div>
              <div class="property-info">
                <h3>{{ property.name }}</h3>
                <p class="property-address">{{ property.address }}</p>
                <p class="property-price">{{ property.price }} ₽</p>
                <div class="property-actions">
                  <button class="action-btn primary" @click="bookProperty(property.id)">
                    Забронировать
                  </button>
                  <button class="action-btn secondary" @click="buyPropertyDirect(property.id)">
                    Купить
                  </button>
                  <button class="action-btn secondary" @click="viewDetails(property.id)">
                    Подробнее
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно редактирования профиля -->
    <div v-if="showEditModal" class="modal-overlay" @click="closeEditModal">
      <div class="modal-content" @click.stop>
        <h3>Редактировать профиль</h3>
        <div class="form-group">
          <label>Имя:</label>
          <input v-model="editForm.name" type="text" />
        </div>
        <div class="form-group">
          <label>Телефон:</label>
          <input v-model="editForm.phone" type="tel" />
        </div>
        <div class="modal-actions">
          <button class="btn-secondary" @click="closeEditModal">Отмена</button>
          <button class="btn-primary" @click="saveProfile">Сохранить</button>
        </div>
      </div>
    </div>

    <!-- Модальное окно покупки -->
    <div v-if="showPurchaseModal" class="modal-overlay" @click="closePurchaseModal">
      <div class="modal-content" @click.stop>
        <h3>Купить квартиру</h3>
        <div class="form-group">
          <label>Цена покупки (₽):</label>
          <input v-model="purchaseForm.price" type="number" placeholder="Введите цену" />
        </div>
        <div class="form-group">
          <label>Способ оплаты:</label>
          <select v-model="purchaseForm.payment_method">
            <option value="cash">Наличные</option>
            <option value="installment">Рассрочка</option>
            <option value="mortgage">Ипотека</option>
          </select>
        </div>
        <div class="modal-actions">
          <button class="btn secondary" @click="closePurchaseModal">Отмена</button>
          <button class="btn primary" @click="confirmPurchase">Купить</button>
        </div>
      </div>
    </div>

    <!-- Модальное окно ипотеки -->
    <div v-if="showMortgageModal" class="modal-overlay" @click="closeMortgageModal">
      <div class="modal-content" @click.stop>
        <h3>Оформить ипотеку на квартиру</h3>
        <div class="form-group">
          <label>Сумма кредита (₽):</label>
          <input v-model="mortgageForm.loan_amount" type="number" placeholder="Введите сумму кредита" />
        </div>
        <div class="form-group">
          <label>Первоначальный взнос (₽):</label>
          <input v-model="mortgageForm.down_payment" type="number" placeholder="Введите первоначальный взнос" />
        </div>
        <div class="form-group">
          <label>Процентная ставка (%):</label>
          <input v-model="mortgageForm.interest_rate" type="number" step="0.1" placeholder="Например: 7.5" />
        </div>
        <div class="form-group">
          <label>Срок кредита (лет):</label>
          <select v-model="mortgageForm.loan_term_years">
            <option value="10">10 лет</option>
            <option value="15">15 лет</option>
            <option value="20">20 лет</option>
            <option value="25">25 лет</option>
            <option value="30">30 лет</option>
          </select>
        </div>
        <div class="form-group">
          <label>Банк:</label>
          <input v-model="mortgageForm.bank_name" type="text" placeholder="Название банка" />
        </div>
        <div class="form-group">
          <label>Примечания:</label>
          <textarea v-model="mortgageForm.application_notes" placeholder="Дополнительная информация"></textarea>
        </div>
        <div class="modal-actions">
          <button class="btn secondary" @click="closeMortgageModal">Отмена</button>
          <button class="btn primary" @click="confirmMortgage">Подать заявку</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { userAPI, propertyAPI } from '../utils/api.js'
import analytics from '../utils/analytics.js'

const emit = defineEmits(['logout', 'go-back'])

// Данные пользователя
const userInfo = ref({
  name: '',
  phone: ''
})

// Забронированные объекты
const bookedProperties = ref([])

// Купленные объекты
const purchasedProperties = ref([])

// Ипотечные заявки
const mortgages = ref([])

// Поиск недвижимости
const searchFilters = reactive({
  city: '',
  minPrice: '',
  maxPrice: '',
  rooms: '',
  minArea: '',
  maxArea: ''
})

const searchResults = ref([])

// Модальные окна
const showEditModal = ref(false)
const showPurchaseModal = ref(false)
const showMortgageModal = ref(false)

const editForm = reactive({
  name: '',
  phone: ''
})

const purchaseForm = reactive({
  property_id: null,
  price: '',
  payment_method: 'cash'
})

const mortgageForm = reactive({
  property_id: null,
  loan_amount: '',
  down_payment: '',
  interest_rate: '',
  loan_term_years: 20,
  bank_name: '',
  application_notes: ''
})

// Загрузка данных пользователя
const loading = ref(false)

const loadUserData = async () => {
  loading.value = true
  try {
    // Получаем ID пользователя из localStorage или используем первый доступный
    let userId = 1
    
    // Попробуем получить из localStorage (если пользователь авторизован)
    const userInfoRaw = localStorage.getItem('userInfo')
    if (userInfoRaw) {
      const userData = JSON.parse(userInfoRaw)
      if (userData.type === 'user' && userData.id) {
        userId = userData.id
      }
    }
    
    // Загружаем информацию о пользователе
    const user = await userAPI.getUser(userId)
    userInfo.value = {
      name: user.User_name,
      phone: user.Phone_number || 'Не указан'
    }
    
    // Загружаем забронированные объекты
    const bookings = await propertyAPI.getUserBookings(userId)
    bookedProperties.value = bookings.map(booking => ({
      id: booking.property.id,
      name: booking.property.name,
      address: booking.property.address,
      price: booking.property.price.toLocaleString(),
      image: booking.property.image_url || 'https://via.placeholder.com/300x200/007aff/ffffff?text=Квартира',
      booking_id: booking.id
    }))
    
    // Загружаем купленные объекты
    const purchases = await propertyAPI.getUserPurchases(userId)
    purchasedProperties.value = purchases.map(purchase => ({
      id: purchase.property.id,
      name: purchase.property.name,
      address: purchase.property.address,
      price: purchase.purchase_price.toLocaleString(),
      image: purchase.property.image_url || 'https://via.placeholder.com/300x200/007aff/ffffff?text=Квартира',
      payment_method: getPaymentMethodText(purchase.payment_method)
    }))
    
    // Загружаем ипотечные заявки
    const mortgageApplications = await propertyAPI.getUserMortgages(userId)
    mortgages.value = mortgageApplications.map(mortgage => ({
      ...mortgage,
      property: {
        ...mortgage.property,
        image: mortgage.property.image_url || 'https://via.placeholder.com/300x200/007aff/ffffff?text=Квартира'
      }
    }))
    
  } catch (error) {
    console.error('Ошибка загрузки данных пользователя:', error)
    alert('Ошибка загрузки данных. Проверьте подключение к серверу.')
  } finally {
    loading.value = false
  }
}

// Методы
const logout = () => {
  // Эмитим событие для родительского компонента
  emit('logout')
}

const goBack = () => {
  // Эмитим событие для возврата на главную страницу
  emit('go-back')
}

const editProfile = () => {
  editForm.name = userInfo.value.name
  editForm.phone = userInfo.value.phone
  showEditModal.value = true
}

const closeEditModal = () => {
  showEditModal.value = false
}

const saveProfile = async () => {
  try {
    // Получаем ID пользователя
    let userId = 1
    const userInfoRaw = localStorage.getItem('userInfo')
    if (userInfoRaw) {
      const userData = JSON.parse(userInfoRaw)
      if (userData.type === 'user' && userData.id) {
        userId = userData.id
      }
    }
    
    await userAPI.updateProfile(userId, editForm.name, editForm.phone)
    userInfo.value.name = editForm.name
    userInfo.value.phone = editForm.phone
    closeEditModal()
    alert('Профиль успешно обновлен!')
  } catch (error) {
    console.error('Ошибка обновления профиля:', error)
    alert('Ошибка при обновлении профиля')
  }
}

const browseProperties = () => {
  // Переход к поиску квартир
  console.log('Поиск квартир')
}

const searchProperties = async () => {
  try {
    // Отслеживаем поиск
    analytics.trackSearch(searchFilters)
    
    const results = await propertyAPI.searchProperties(searchFilters)
    searchResults.value = results.map(property => ({
      id: property.id,
      name: property.name,
      address: property.address,
      price: property.price.toLocaleString(),
      image: property.image_url || 'https://via.placeholder.com/300x200/007aff/ffffff?text=Квартира'
    }))
  } catch (error) {
    console.error('Ошибка поиска квартир:', error)
  }
}

const bookProperty = async (propertyId) => {
  try {
    // Отслеживаем клик по бронированию
    analytics.trackBookClick(propertyId)
    
    // Получаем ID пользователя
    let userId = 1
    const userInfoRaw = localStorage.getItem('userInfo')
    if (userInfoRaw) {
      const userData = JSON.parse(userInfoRaw)
      if (userData.type === 'user' && userData.id) {
        userId = userData.id
      }
    }
    
    await propertyAPI.bookProperty(propertyId, userId)
    alert('Квартира забронирована!')
    // Перезагружаем данные
    await loadUserData()
  } catch (error) {
    console.error('Ошибка бронирования:', error)
    alert('Ошибка при бронировании квартиры')
  }
}

const buyProperty = async (propertyId) => {
  // Открываем модальное окно покупки
  purchaseForm.property_id = propertyId
  showPurchaseModal.value = true
}

const buyPropertyDirect = async (propertyId) => {
  // Покупка напрямую без бронирования
  purchaseForm.property_id = propertyId
  showPurchaseModal.value = true
}

const confirmPurchase = async () => {
  try {
    // Получаем ID пользователя
    let userId = 1
    const userInfoRaw = localStorage.getItem('userInfo')
    if (userInfoRaw) {
      const userData = JSON.parse(userInfoRaw)
      if (userData.type === 'user' && userData.id) {
        userId = userData.id
      }
    }
    
    await propertyAPI.purchasePropertyDirect({
      property_id: purchaseForm.property_id,
      purchase_price: parseInt(purchaseForm.price),
      payment_method: purchaseForm.payment_method
    }, userId)
    
    alert('Квартира успешно куплена!')
    closePurchaseModal()
    await loadUserData()
  } catch (error) {
    console.error('Ошибка покупки:', error)
    alert('Ошибка при покупке квартиры')
  }
}

const closePurchaseModal = () => {
  showPurchaseModal.value = false
  purchaseForm.property_id = null
  purchaseForm.price = ''
  purchaseForm.payment_method = 'cash'
}

const applyMortgage = async (propertyId) => {
  // Открываем модальное окно ипотеки
  mortgageForm.property_id = propertyId
  showMortgageModal.value = true
}

const confirmMortgage = async () => {
  try {
    // Получаем ID пользователя
    let userId = 1
    const userInfoRaw = localStorage.getItem('userInfo')
    if (userInfoRaw) {
      const userData = JSON.parse(userInfoRaw)
      if (userData.type === 'user' && userData.id) {
        userId = userData.id
      }
    }
    
    await propertyAPI.applyMortgage({
      property_id: mortgageForm.property_id,
      loan_amount: parseInt(mortgageForm.loan_amount),
      down_payment: parseInt(mortgageForm.down_payment),
      interest_rate: parseFloat(mortgageForm.interest_rate),
      loan_term_years: parseInt(mortgageForm.loan_term_years),
      bank_name: mortgageForm.bank_name,
      application_notes: mortgageForm.application_notes
    }, userId)
    
    alert('Заявка на ипотеку подана!')
    closeMortgageModal()
    await loadUserData()
  } catch (error) {
    console.error('Ошибка подачи заявки на ипотеку:', error)
    alert('Ошибка при подаче заявки на ипотеку')
  }
}

const closeMortgageModal = () => {
  showMortgageModal.value = false
  mortgageForm.property_id = null
  mortgageForm.loan_amount = ''
  mortgageForm.down_payment = ''
  mortgageForm.interest_rate = ''
  mortgageForm.loan_term_years = 20
  mortgageForm.bank_name = ''
  mortgageForm.application_notes = ''
}

const cancelBooking = async (propertyId) => {
  try {
    // Получаем ID пользователя
    let userId = 1
    const userInfoRaw = localStorage.getItem('userInfo')
    if (userInfoRaw) {
      const userData = JSON.parse(userInfoRaw)
      if (userData.type === 'user' && userData.id) {
        userId = userData.id
      }
    }
    
    // Находим ID брони
    const booking = bookedProperties.value.find(p => p.id === propertyId)
    if (booking) {
      await propertyAPI.cancelBooking(booking.booking_id, userId)
      alert('Бронь отменена!')
      await loadUserData()
    }
  } catch (error) {
    console.error('Ошибка отмены брони:', error)
    alert('Ошибка при отмене брони')
  }
}

const viewDetails = (propertyId) => {
  // Отслеживаем просмотр деталей квартиры
  analytics.trackApartmentView(propertyId)
  
  // Просмотр деталей квартиры
  console.log('Детали квартиры:', propertyId)
}

const clearFilters = () => {
  // Отслеживаем очистку фильтров
  analytics.trackFilterApplied(0)
  
  // Логика очистки фильтров
  searchFilters.city = ''
  searchFilters.minPrice = ''
  searchFilters.maxPrice = ''
  searchFilters.rooms = ''
  searchFilters.minArea = ''
  searchFilters.maxArea = ''
}

// Вспомогательные функции
const getPaymentMethodText = (method) => {
  const methods = {
    'cash': 'Наличные',
    'installment': 'Рассрочка',
    'mortgage': 'Ипотека'
  }
  return methods[method] || method
}

const getMortgageStatusText = (status) => {
  const statuses = {
    'pending': 'На рассмотрении',
    'approved': 'Одобрено',
    'rejected': 'Отклонено',
    'active': 'Активно',
    'closed': 'Закрыто'
  }
  return statuses[status] || status
}

const getMortgageStatusClass = (status) => {
  const classes = {
    'pending': 'pending',
    'approved': 'approved',
    'rejected': 'rejected',
    'active': 'active',
    'closed': 'closed'
  }
  return classes[status] || 'pending'
}

onMounted(() => {
  console.log('Загрузка данных пользователя')
  loadUserData()
})
</script>

<style scoped>
.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #007aff;
}

.dashboard-header h1 {
  color: #007aff;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.back-btn {
  background: #f5f5f5;
  color: #2c3e50;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s ease;
}

.back-btn:hover {
  background: #e5e5e5;
}

.logout-btn {
  background: #ff3b30;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
}

.logout-btn:hover {
  background: #d70015;
}

.dashboard-section {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.dashboard-section h2 {
  margin-bottom: 1.5rem;
  color: #2c3e50;
  font-size: 1.5rem;
  font-weight: 700;
  position: relative;
  padding-bottom: 0.5rem;
}

.dashboard-section h2::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 3px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 2px;
}

.dashboard-section h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
  font-size: 1.2rem;
  font-weight: 600;
}

.user-info {
  display: grid;
  gap: 1rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.info-item label {
  font-weight: 600;
  color: #666;
  min-width: 100px;
}

.edit-btn {
  background: #007aff;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  width: fit-content;
}

.edit-btn:hover {
  background: #0056cc;
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  border-radius: 12px;
  border: 2px dashed #ced4da;
}

.empty-state p {
  color: #6c757d;
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
}

.browse-btn {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.browse-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

.properties-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.property-card {
  border: 1px solid #e1e8ed;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.property-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  border-color: #667eea;
}

.property-image {
  position: relative;
  height: 200px;
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.property-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.property-card:hover .property-image img {
  transform: scale(1.05);
}

.property-status {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.property-status.booked {
  background: linear-gradient(135deg, #ff9500, #ff6b35);
  color: white;
}

.property-status.available {
  background: linear-gradient(135deg, #34c759, #30d158);
  color: white;
}

.property-status.purchased {
  background: linear-gradient(135deg, #34c759, #30d158);
  color: white;
}

.property-status.pending {
  background: linear-gradient(135deg, #ff9500, #ff6b35);
  color: white;
}

.property-status.approved {
  background: linear-gradient(135deg, #34c759, #30d158);
  color: white;
}

.property-status.rejected {
  background: linear-gradient(135deg, #ff3b30, #ff453a);
  color: white;
}

.property-status.active {
  background: linear-gradient(135deg, #34c759, #30d158);
  color: white;
}

.property-status.closed {
  background: linear-gradient(135deg, #ff3b30, #ff453a);
  color: white;
}

.property-info {
  padding: 1.5rem;
}

.property-info h3 {
  margin: 0 0 0.75rem 0;
  color: #2c3e50;
  font-size: 1.1rem;
  font-weight: 600;
  line-height: 1.3;
}

.property-address {
  color: #6c757d;
  font-size: 0.9rem;
  margin-bottom: 0.75rem;
  line-height: 1.4;
}

.property-price {
  font-size: 1.3rem;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 0.75rem;
}

.property-payment {
  font-size: 0.9rem;
  color: #6c757d;
  margin-bottom: 0.5rem;
  font-style: italic;
}

.property-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
  flex-wrap: wrap;
}

.action-btn {
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.3s ease;
  flex: 1;
  min-width: 80px;
  text-align: center;
}

.action-btn.primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.action-btn.primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.action-btn.secondary {
  background: #f8f9fa;
  color: #2c3e50;
  border: 2px solid #e1e8ed;
}

.action-btn.secondary:hover {
  background: #e9ecef;
  border-color: #ced4da;
  transform: translateY(-1px);
}

.action-btn.danger {
  background: linear-gradient(135deg, #ff6b6b, #ee5a24);
  color: white;
  box-shadow: 0 2px 8px rgba(255, 107, 107, 0.3);
}

.action-btn.danger:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 107, 107, 0.4);
}

/* Форма поиска */
.search-form {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.search-filters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-label {
  font-weight: 600;
  color: white;
  font-size: 0.9rem;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.filter-input {
  padding: 0.75rem 1rem;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  font-size: 0.9rem;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  color: #2c3e50;
}

.filter-input:focus {
  outline: none;
  border-color: rgba(255, 255, 255, 0.8);
  background: rgba(255, 255, 255, 1);
  box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.2);
}

.filter-input::placeholder {
  color: #7f8c8d;
}

/* Диапазоны цен и площади */
.price-range,
.area-range {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.price-input,
.area-input {
  flex: 1;
  min-width: 0;
}

.price-separator,
.area-separator {
  color: white;
  font-weight: 600;
  font-size: 1.1rem;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.area-unit {
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  white-space: nowrap;
}

/* Фильтр по комнатам */
.rooms-filter {
  margin-bottom: 2rem;
}

.rooms-buttons {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.room-btn {
  padding: 0.75rem 1.5rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 25px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  min-width: 60px;
  text-align: center;
}

.room-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-1px);
}

.room-btn.active {
  background: white;
  color: #667eea;
  border-color: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Кнопки действий */
.search-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.search-btn,
.clear-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 160px;
  justify-content: center;
}

.search-btn {
  background: linear-gradient(135deg, #ff6b6b, #ee5a24);
  color: white;
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
}

.search-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 107, 107, 0.6);
}

.clear-btn {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(10px);
}

.clear-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-1px);
}

.search-icon,
.clear-icon {
  width: 18px;
  height: 18px;
}

/* Результаты поиска */
.search-results h3 {
  margin-bottom: 1.5rem;
  color: #2c3e50;
  font-size: 1.3rem;
  font-weight: 600;
}

/* Адаптивность */
@media (max-width: 768px) {
  .search-form {
    padding: 1.5rem;
  }
  
  .search-filters-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .rooms-buttons {
    justify-content: center;
  }
  
  .search-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .search-btn,
  .clear-btn {
    width: 100%;
    max-width: 300px;
  }
}

@media (max-width: 480px) {
  .price-range,
  .area-range {
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .price-separator,
  .area-separator {
    display: none;
  }
  
  .area-unit {
    align-self: flex-end;
    margin-top: -2.5rem;
    margin-right: 0.5rem;
  }
}

.loading-indicator {
  text-align: center;
  padding: 3rem;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007aff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Модальные окна */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.modal-content {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-content h3 {
  margin: 0 0 1.5rem 0;
  color: #2c3e50;
  font-size: 1.4rem;
  font-weight: 600;
  text-align: center;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.9rem;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #e1e8ed;
  border-radius: 8px;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  background: #f8f9fa;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
  background: white;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 120px;
}

.btn.primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn.primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

.btn.secondary {
  background: #f8f9fa;
  color: #2c3e50;
  border: 2px solid #e1e8ed;
}

.btn.secondary:hover {
  background: #e9ecef;
  border-color: #ced4da;
}
</style> 