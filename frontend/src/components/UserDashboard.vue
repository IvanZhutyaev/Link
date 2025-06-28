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
          <div class="form-row">
            <input 
              v-model="searchFilters.city" 
              type="text" 
              placeholder="Город"
              class="form-input"
            />
            <input 
              v-model="searchFilters.minPrice" 
              type="number" 
              placeholder="Мин. цена"
              class="form-input"
            />
            <input 
              v-model="searchFilters.maxPrice" 
              type="number" 
              placeholder="Макс. цена"
              class="form-input"
            />
          </div>
          <div class="form-row">
            <select v-model="searchFilters.rooms" class="form-select">
              <option value="">Любое количество комнат</option>
              <option value="1">1 комната</option>
              <option value="2">2 комнаты</option>
              <option value="3">3 комнаты</option>
              <option value="4">4+ комнат</option>
            </select>
            <input 
              v-model="searchFilters.minArea" 
              type="number" 
              placeholder="Мин. площадь (м²)"
              class="form-input"
            />
            <input 
              v-model="searchFilters.maxArea" 
              type="number" 
              placeholder="Макс. площадь (м²)"
              class="form-input"
            />
          </div>
          <div class="form-actions">
            <button @click="searchProperties" class="search-btn">Найти квартиры</button>
            <button @click="clearFilters" class="clear-btn">Очистить</button>
          </div>
        </div>

        <div v-if="searchResults.length > 0" class="search-results">
          <h3>Результаты поиска</h3>
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
  color: #2c3e50;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
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
  padding: 3rem;
  color: #666;
}

.browse-btn {
  background: #007aff;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  margin-top: 1rem;
}

.properties-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.property-card {
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s;
}

.property-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.property-image {
  position: relative;
  height: 200px;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
}

.property-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.property-status {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
}

.property-status.booked {
  background: #ff9500;
  color: white;
}

.property-status.available {
  background: #34c759;
  color: white;
}

.property-status.purchased {
  background: #34c759;
  color: white;
}

.property-status.pending {
  background: #ff9500;
  color: white;
}

.property-status.approved {
  background: #34c759;
  color: white;
}

.property-status.rejected {
  background: #ff3b30;
  color: white;
}

.property-status.active {
  background: #34c759;
  color: white;
}

.property-status.closed {
  background: #ff3b30;
  color: white;
}

.property-info {
  padding: 1rem;
}

.property-info h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.property-address {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.property-price {
  font-size: 1.2rem;
  font-weight: 600;
  color: #007aff;
  margin-bottom: 0.5rem;
}

.property-payment {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.25rem;
}

.property-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
  flex-wrap: wrap;
}

.action-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: background-color 0.3s ease;
  flex: 1;
  min-width: 80px;
}

.action-btn.primary {
  background: #007aff;
  color: white;
}

.action-btn.primary:hover {
  background: #0056cc;
}

.action-btn.secondary {
  background: #f5f5f5;
  color: #2c3e50;
}

.action-btn.secondary:hover {
  background: #e5e5e5;
}

.action-btn.danger {
  background: #ff3b30;
  color: white;
}

.action-btn.danger:hover {
  background: #d70015;
}

.search-filters {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-group label {
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.9rem;
}

.filter-group input,
.filter-group select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
}

.search-btn,
.clear-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  align-self: end;
}

.search-btn {
  background: #007aff;
  color: white;
}

.search-btn:hover {
  background: #0056cc;
}

.clear-btn {
  background: #f5f5f5;
  color: #2c3e50;
}

.clear-btn:hover {
  background: #e5e5e5;
}

.search-results h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
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
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}

.mortgage-modal {
  max-width: 600px;
}

.modal-content h3 {
  margin-bottom: 1.5rem;
  color: #2c3e50;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #2c3e50;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #007aff;
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  justify-content: flex-end;
}

.btn-primary,
.btn-secondary {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s ease;
}

.btn-primary {
  background: #007aff;
  color: white;
}

.btn-primary:hover {
  background: #0056cc;
}

.btn-secondary {
  background: #f5f5f5;
  color: #2c3e50;
}

.btn-secondary:hover {
  background: #e5e5e5;
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 1rem;
  }
  
  .dashboard-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .header-actions {
    justify-content: center;
  }
  
  .properties-grid {
    grid-template-columns: 1fr;
  }
  
  .search-filters {
    grid-template-columns: 1fr;
  }
  
  .modal-content {
    margin: 1rem;
    min-width: auto;
  }
}
</style> 