<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h1>Кабинет застройщика</h1>
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

      <!-- Рейтинг застройщика -->
      <div v-if="developerRating" class="dashboard-section rating-section">
        <h2>Рейтинг застройщика</h2>
        <div class="rating-card">
          <div class="rating-main">
            <div class="rating-score">
              <span class="rating-number">{{ developerRating.rating }}</span>
              <span class="rating-max">/10</span>
            </div>
            <div class="rating-stars">
              <span 
                v-for="i in 10" 
                :key="i" 
                class="star"
                :class="{ 'filled': i <= Math.round(developerRating.rating) }"
              >
                ★
              </span>
            </div>
          </div>
          <div class="rating-details">
            <div class="rating-stat">
              <span class="stat-label">Завершенных проектов:</span>
              <span class="stat-value">{{ developerRating.completed_projects }}</span>
            </div>
            <div class="rating-stat">
              <span class="stat-label">Лет на рынке:</span>
              <span class="stat-value">{{ developerRating.years_on_market }}</span>
            </div>
            <div class="rating-stat">
              <span class="stat-label">Последнее обновление:</span>
              <span class="stat-value">{{ formatDate(developerRating.last_updated) }}</span>
            </div>
          </div>
          <button class="recalculate-btn" @click="recalculateRating">
            Пересчитать рейтинг
          </button>
        </div>
      </div>

      <!-- Статистика застройщика -->
      <div v-if="developerStats" class="dashboard-section stats-section">
        <h2>Статистика</h2>
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">🏢</div>
            <div class="stat-content">
              <div class="stat-number">{{ developerStats.properties_count }}</div>
              <div class="stat-label">Объектов недвижимости</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">🏘️</div>
            <div class="stat-content">
              <div class="stat-number">{{ developerStats.complexes_count }}</div>
              <div class="stat-label">Жилых комплексов</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">⭐</div>
            <div class="stat-content">
              <div class="stat-number">{{ developerStats.avg_property_rating }}</div>
              <div class="stat-label">Средний рейтинг квартир</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">🏆</div>
            <div class="stat-content">
              <div class="stat-number">{{ developerStats.avg_complex_rating }}</div>
              <div class="stat-label">Средний рейтинг ЖК</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Аналитика -->
      <AnalyticsDashboard />

      <!-- ЖК застройщика -->
      <div class="dashboard-section">
        <div class="section-header">
          <h2>Жилые комплексы</h2>
          <button class="add-btn" @click="showAddComplexModal = true">
            + Добавить ЖК
          </button>
        </div>
        
        <div class="complexes-grid">
          <div 
            v-for="complex in complexes" 
            :key="complex.id"
            class="complex-card"
          >
            <div class="complex-image">
              <img :src="complex.image" :alt="complex.name" />
              <div class="complex-status" :class="complex.status">
                {{ complex.statusText }}
              </div>
            </div>
            <div class="complex-info">
              <h3>{{ complex.name }}</h3>
              <p class="complex-address">{{ complex.address }}</p>
              <p class="complex-city">Город: {{ complex.city }}</p>
              <p class="complex-class">Класс: {{ complex.housingClass || 'Не указан' }}</p>
              <p class="complex-date">Ввод в эксплуатацию: {{ complex.commissioningDate || 'Не указана' }}</p>
              
              <!-- Рейтинг ЖК -->
              <div v-if="complex.rating" class="complex-rating">
                <div class="rating-display">
                  <span class="rating-score">{{ complex.rating }}</span>
                  <span class="rating-max">/5</span>
                  <div class="rating-stars">
                    <span 
                      v-for="i in 5" 
                      :key="i" 
                      class="star"
                      :class="{ 'filled': i <= Math.round(complex.rating) }"
                    >
                      ★
                    </span>
                  </div>
                  <span class="rating-count">({{ complex.rating_count || 0 }} оценок)</span>
                </div>
              </div>
              
              <div class="complex-stats">
                <span>Квартир: {{ complex.apartmentsCount }}</span>
                <span>Продано: {{ complex.soldCount }}</span>
              </div>
              
              <!-- Список квартир в ЖК -->
              <div v-if="complex.apartments && complex.apartments.length > 0" class="apartments-list">
                <h4>Квартиры в ЖК:</h4>
                <div class="apartment-item" v-for="apartment in complex.apartments" :key="apartment.id">
                  <div class="apartment-info-mini">
                    <span class="apartment-name">{{ apartment.name }}</span>
                    <span class="apartment-price">{{ apartment.price }} ₽</span>
                    <span class="apartment-area">{{ apartment.area }} м²</span>
                    <span class="apartment-rooms">{{ apartment.rooms }} комн.</span>
                  </div>
                </div>
              </div>
              
              <div class="complex-actions">
                <button class="action-btn primary" @click="viewComplex(complex.id)">
                  Просмотр
                </button>
                <button class="action-btn secondary" @click="editComplex(complex.id)">
                  Редактировать
                </button>
                <button class="action-btn secondary" @click="addApartment(complex.id)">
                  + Квартира
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Забронированные квартиры -->
      <div class="dashboard-section">
        <h2>Забронированные квартиры</h2>
        <div v-if="bookedApartments.length === 0" class="empty-state">
          <p>Нет забронированных квартир</p>
        </div>
        <div v-else class="apartments-grid">
          <div 
            v-for="apartment in bookedApartments" 
            :key="apartment.id"
            class="apartment-card"
          >
            <div class="apartment-image">
              <img :src="apartment.image" :alt="apartment.name" />
              <div class="apartment-status booked">Забронировано</div>
            </div>
            <div class="apartment-info">
              <h3>{{ apartment.name }}</h3>
              <p class="apartment-address">{{ apartment.address }}</p>
              <p class="apartment-price">{{ apartment.price }} ₽</p>
              <p class="apartment-client">Клиент: {{ apartment.clientName }}</p>
              <div class="apartment-actions">
                <button class="action-btn primary" @click="confirmSale(apartment.id)">
                  Подтвердить продажу
                </button>
                <button class="action-btn secondary" @click="cancelBooking(apartment.id)">
                  Отменить бронь
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Проданные объекты -->
      <div class="dashboard-section">
        <h2>Проданные объекты</h2>
        <div v-if="soldApartments.length === 0" class="empty-state">
          <p>Нет проданных объектов</p>
        </div>
        <div v-else class="apartments-grid">
          <div 
            v-for="apartment in soldApartments" 
            :key="apartment.id"
            class="apartment-card"
          >
            <div class="apartment-image">
              <img :src="apartment.image" :alt="apartment.name" />
              <div class="apartment-status sold">Продано</div>
            </div>
            <div class="apartment-info">
              <h3>{{ apartment.name }}</h3>
              <p class="apartment-address">{{ apartment.address }}</p>
              <p class="apartment-price">{{ apartment.price }} ₽</p>
              <p class="apartment-client">Покупатель: {{ apartment.buyerName }}</p>
              <p class="apartment-date">Дата продажи: {{ apartment.saleDate }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Личная информация застройщика -->
      <div class="dashboard-section">
        <h2>Личная информация</h2>
        <div class="developer-info">
          <div class="info-item">
            <label>Название компании:</label>
            <span>{{ developerInfo.companyName }}</span>
          </div>
          <div class="info-item">
            <label>ИНН:</label>
            <span>{{ developerInfo.inn }}</span>
          </div>
          <div class="info-item">
            <label>ОГРН:</label>
            <span>{{ developerInfo.ogrn }}</span>
          </div>
          <div class="info-item">
            <label>Адрес:</label>
            <span>{{ developerInfo.address }}</span>
          </div>
          <div class="info-item">
            <label>Представитель:</label>
            <span>{{ developerInfo.representative }}</span>
          </div>
          <button class="edit-btn" @click="editDeveloperProfile">Редактировать</button>
        </div>
      </div>
    </div>

    <!-- Модальное окно добавления ЖК -->
    <div v-if="showAddComplexModal" class="modal-overlay" @click="closeAddComplexModal">
      <div class="modal-content" @click.stop>
        <h3>Добавить новый ЖК</h3>
        <div class="form-group">
          <label>Название ЖК:</label>
          <input v-model="newComplex.name" type="text" placeholder="Введите название" />
        </div>
        <div class="form-group">
          <label>Адрес:</label>
          <input v-model="newComplex.address" type="text" placeholder="Введите адрес" />
        </div>
        <div class="form-group">
          <label>Имя застройщика:</label>
          <input v-model="newComplex.developer_name" type="text" placeholder="Введите имя застройщика" />
        </div>
        <div class="form-group">
          <label>Город:</label>
          <select v-model="newComplex.city">
            <option value="">Выберите город</option>
            <option value="Москва">Москва</option>
            <option value="Санкт-Петербург">Санкт-Петербург</option>
            <option value="Краснодар">Краснодар</option>
            <option value="Адыгея">Адыгея</option>
          </select>
        </div>
        <div class="form-group">
          <label>Дата ввода в эксплуатацию:</label>
          <input v-model="newComplex.commissioning_date" type="text" placeholder="Например: 2025" />
        </div>
        <div class="form-group">
          <label>Класс жилья:</label>
          <select v-model="newComplex.housing_class">
            <option value="">Выберите класс</option>
            <option value="Эконом">Эконом</option>
            <option value="Комфорт">Комфорт</option>
            <option value="Бизнес">Бизнес</option>
            <option value="Премиум">Премиум</option>
          </select>
        </div>
        <div class="form-group">
          <label>Статус:</label>
          <select v-model="newComplex.status">
            <option value="">Выберите статус</option>
            <option value="Строится">Строится</option>
            <option value="Сдан">Сдан</option>
            <option value="Планируется">Планируется</option>
          </select>
        </div>
        <div class="modal-actions">
          <button class="btn secondary" @click="closeAddComplexModal">Отмена</button>
          <button class="btn primary" @click="addComplex">Добавить</button>
        </div>
      </div>
    </div>

    <!-- Модальное окно добавления квартиры -->
    <div v-if="showAddApartmentModal" class="modal-overlay" @click="closeAddApartmentModal">
      <div class="modal-content" @click.stop>
        <h3>Добавить квартиру в ЖК</h3>
        <div class="form-group">
          <label>Название квартиры:</label>
          <input v-model="newApartment.name" type="text" placeholder="Например: Квартира 45" />
        </div>
        <div class="form-group">
          <label>Адрес:</label>
          <input v-model="newApartment.address" type="text" placeholder="Полный адрес квартиры" />
        </div>
        <div class="form-group">
          <label>Площадь (м²):</label>
          <input v-model="newApartment.area" type="number" placeholder="75.5" />
        </div>
        <div class="form-group">
          <label>Количество комнат:</label>
          <select v-model="newApartment.rooms">
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4+</option>
          </select>
        </div>
        <div class="form-group">
          <label>Этаж:</label>
          <input v-model="newApartment.floor" type="number" placeholder="5" />
        </div>
        <div class="form-group">
          <label>Цена (₽):</label>
          <input v-model="newApartment.price" type="number" placeholder="3200000" />
        </div>
        <div class="form-group">
          <label>Описание:</label>
          <textarea v-model="newApartment.description" placeholder="Описание квартиры" rows="3"></textarea>
        </div>
        <div class="form-group">
          <label>Город:</label>
          <input v-model="newApartment.city" type="text" placeholder="Москва" />
        </div>
        <div class="form-group">
          <label>Изображение:</label>
          <input v-model="newApartment.image_url" type="url" placeholder="URL изображения" />
        </div>
        <div class="modal-actions">
          <button class="btn-secondary" @click="closeAddApartmentModal">Отмена</button>
          <button class="btn-primary" @click="addApartmentToComplex">Добавить квартиру</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { developerAPI } from '../utils/api.js'
import analytics from '../utils/analytics.js'
import AnalyticsDashboard from './AnalyticsDashboard.vue'

const emit = defineEmits(['logout', 'go-back'])

// Аналитика
const developerStats = ref({
  totalComplexes: 0,
  totalApartments: 0,
  soldApartments: 0,
  totalRevenue: 0
})

// ЖК застройщика
const complexes = ref([])

// Забронированные квартиры
const bookedApartments = ref([])

// Проданные объекты
const soldApartments = ref([])

// Личная информация застройщика
const developerInfo = ref({
  id: '',
  companyName: '',
  inn: '',
  ogrn: '',
  address: '',
  representative: ''
})

// Модальные окна
const showAddComplexModal = ref(false)
const showAddApartmentModal = ref(false)

// Формы
const newComplex = reactive({
  name: '',
  address: '',
  developer_name: '',
  city: '',
  commissioning_date: '',
  housing_class: '',
  status: '',
  avatar_url: ''
})

const newApartment = reactive({
  name: '',
  address: '',
  area: '',
  rooms: '1',
  floor: '',
  price: '',
  description: '',
  city: '',
  image_url: ''
})

// Переменная для хранения ID выбранного ЖК
const selectedComplexId = ref(null)

// Загрузка данных
const loading = ref(false)

const loadDeveloperData = async () => {
  loading.value = true
  try {
    console.log('Начинаем загрузку данных застройщика...')
    
    // Получаем ID застройщика из localStorage или используем первый доступный
    let developerId = 1
    
    // Попробуем получить из localStorage (если пользователь авторизован)
    const userInfo = localStorage.getItem('userInfo')
    if (userInfo) {
      const userData = JSON.parse(userInfo)
      if (userData.type === 'developer' && userData.id) {
        developerId = userData.id
      }
    }
    
    console.log('ID застройщика:', developerId)
    
    // Загружаем информацию о застройщике
    console.log('Загружаем информацию о застройщике...')
    const developer = await developerAPI.getDeveloper(developerId)
    console.log('Данные застройщика:', developer)
    
    developerInfo.value = {
      id: developer.id,
      companyName: developer.Company_name,
      inn: developer.INN,
      ogrn: developer.OGRN,
      address: developer.Adress,
      representative: developer.User_name
    }
    
    // Загружаем жилые комплексы застройщика из таблицы ResidentialComplex
    console.log('Загружаем жилые комплексы для:', developer.Company_name)
    try {
      const residentialComplexes = await developerAPI.getDeveloperResidentialComplexes(developer.id)
      console.log('Полученные ЖК:', residentialComplexes)
      
      // Загружаем квартиры для каждого ЖК
      const complexesWithApartments = await Promise.all(
        residentialComplexes.map(async (complex) => {
          try {
            // Загружаем квартиры для этого ЖК
            const apartments = await developerAPI.getComplexApartments(complex.id)
            return {
              id: complex.id,
              name: complex.name,
              address: complex.address,
              status: complex.status === 'Сдан' ? 'active' : 'inactive',
              statusText: complex.status || 'Неизвестно',
              apartmentsCount: apartments.length,
              soldCount: apartments.filter(apt => !apt.is_available).length,
              image: complex.avatar_url || 'https://via.placeholder.com/300x200/007aff/ffffff?text=ЖК',
              city: complex.city,
              housingClass: complex.housing_class,
              commissioningDate: complex.commissioning_date,
              apartments: apartments
            }
          } catch (error) {
            console.warn(`Не удалось загрузить квартиры для ЖК ${complex.name}:`, error)
            return {
              id: complex.id,
              name: complex.name,
              address: complex.address,
              status: complex.status === 'Сдан' ? 'active' : 'inactive',
              statusText: complex.status || 'Неизвестно',
              apartmentsCount: 0,
              soldCount: 0,
              image: complex.avatar_url || 'https://via.placeholder.com/300x200/007aff/ffffff?text=ЖК',
              city: complex.city,
              housingClass: complex.housing_class,
              commissioningDate: complex.commissioning_date,
              apartments: []
            }
          }
        })
      )
      
      complexes.value = complexesWithApartments
    } catch (complexError) {
      console.warn('Не удалось загрузить жилые комплексы:', complexError)
      console.log('Попробуем загрузить обычные объекты недвижимости...')
      
      // Fallback: загружаем обычные объекты недвижимости
      const properties = await developerAPI.getDeveloperProperties(developerId)
      complexes.value = properties.map(property => ({
        id: property.id,
        name: property.name,
        address: property.address,
        status: property.is_available ? 'active' : 'inactive',
        statusText: property.is_available ? 'Активен' : 'Неактивен',
        apartmentsCount: 0,
        soldCount: 0,
        image: property.image_url || 'https://via.placeholder.com/300x200/007aff/ffffff?text=ЖК',
        city: property.city,
        housingClass: 'Не указан',
        commissioningDate: 'Не указана',
        apartments: []
      }))
    }
    
    // Обновляем аналитику на основе реальных данных
    developerStats.value.totalComplexes = complexes.value.length
    developerStats.value.totalApartments = complexes.value.reduce((sum, complex) => sum + complex.apartmentsCount, 0)
    developerStats.value.soldApartments = complexes.value.reduce((sum, complex) => sum + complex.soldCount, 0)
    developerStats.value.totalRevenue = '0' // Пока нет данных о доходах
    
    console.log('Данные успешно загружены. Количество ЖК:', complexes.value.length)
    
  } catch (error) {
    console.error('Ошибка загрузки данных застройщика:', error)
    console.error('Детали ошибки:', error.message)
    console.error('Стек ошибки:', error.stack)
    alert('Ошибка загрузки данных: ' + (error.message || 'Неизвестная ошибка'))
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

const viewComplex = (complexId) => {
  // Отслеживаем просмотр ЖК
  analytics.sendEvent(complexId, "view_complex")
  console.log('Просмотр ЖК:', complexId)
}

const editComplex = (complexId) => {
  // Отслеживаем редактирование ЖК
  analytics.sendEvent(complexId, "edit_complex")
  console.log('Редактирование ЖК:', complexId)
}

const addApartment = (complexId) => {
  // Отслеживаем добавление квартиры
  analytics.sendEvent(complexId, "add_apartment")
  selectedComplexId.value = complexId
  showAddApartmentModal.value = true
}

const confirmSale = (apartmentId) => {
  // Отслеживаем подтверждение продажи
  analytics.sendEvent(apartmentId, "confirm_sale")
  console.log('Подтверждение продажи:', apartmentId)
}

const cancelBooking = (apartmentId) => {
  // Отслеживаем отмену брони
  analytics.sendEvent(apartmentId, "cancel_booking")
  console.log('Отмена брони:', apartmentId)
}

const editDeveloperProfile = () => {
  // Отслеживаем редактирование профиля
  analytics.sendEvent(0, "edit_developer_profile")
  console.log('Редактирование профиля застройщика')
}

const closeAddComplexModal = () => {
  showAddComplexModal.value = false
  Object.keys(newComplex).forEach(key => newComplex[key] = '')
}

const closeAddApartmentModal = () => {
  showAddApartmentModal.value = false
  Object.keys(newApartment).forEach(key => newApartment[key] = '')
}

const addComplex = async () => {
  try {
    await developerAPI.createResidentialComplex({
      ...newComplex,
      developer_name: developerInfo.value.companyName,
      zastroy_id: developerInfo.value.id
    })
    await loadDeveloperData()
    showAddComplexModal.value = false
  } catch (e) {
    alert('Ошибка при добавлении ЖК: ' + (e.message || 'Неизвестная ошибка'))
  }
}

const addApartmentToComplex = async () => {
  try {
    await developerAPI.createApartment({
      ...newApartment,
      complex_id: selectedComplexId.value,
      zastroy_id: developerInfo.value.id
    })
    await loadDeveloperData()
    showAddApartmentModal.value = false
  } catch (e) {
    alert('Ошибка при добавлении квартиры: ' + (e.message || 'Неизвестная ошибка'))
  }
}

onMounted(() => {
  console.log('Загрузка данных застройщика')
  loadDeveloperData()
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
}

.back-btn {
  background: #f5f5f5;
  color: #666;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
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

.dashboard-content {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-header h2 {
  margin: 0;
}

.add-btn {
  background: #34c759;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
}

.add-btn:hover {
  background: #28a745;
}

/* Аналитика */
.analytics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.analytics-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #007aff, #0056cc);
  color: white;
  border-radius: 8px;
}

.analytics-icon {
  font-size: 2rem;
  width: 50px;
  text-align: center;
}

.analytics-content h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  opacity: 0.9;
}

.analytics-number {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
}

/* ЖК */
.complexes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.complex-card {
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s;
}

.complex-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.complex-image {
  position: relative;
  height: 200px;
  background: #f5f5f5;
}

.complex-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.complex-status {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
}

.complex-status.active {
  background: #34c759;
  color: white;
}

.complex-status.construction {
  background: #ff9500;
  color: white;
}

.complex-info {
  padding: 1rem;
}

.complex-info h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.complex-address {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.complex-city {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.complex-class {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.complex-date {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.complex-stats {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: #666;
}

.complex-actions {
  display: flex;
  gap: 0.5rem;
}

/* Квартиры */
.apartments-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.apartment-card {
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s;
}

.apartment-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.apartment-image {
  position: relative;
  height: 200px;
  background: #f5f5f5;
}

.apartment-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.apartment-status {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
}

.apartment-status.booked {
  background: #ff9500;
  color: white;
}

.apartment-status.sold {
  background: #34c759;
  color: white;
}

.apartment-info {
  padding: 1rem;
}

.apartment-info h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.apartment-address {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.apartment-price {
  font-size: 1.2rem;
  font-weight: 700;
  color: #007aff;
  margin-bottom: 0.5rem;
}

.apartment-client,
.apartment-date {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.apartment-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.action-btn {
  flex: 1;
  padding: 0.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
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
  color: #666;
}

.action-btn.secondary:hover {
  background: #e5e5e5;
}

/* Личная информация */
.developer-info {
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
  min-width: 150px;
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

/* Модальные окна */
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
  padding: 2rem;
}

.modal-content h3 {
  margin: 0 0 1.5rem 0;
  color: #2c3e50;
  font-size: 1.5rem;
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

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #007aff;
  box-shadow: 0 0 0 2px rgba(0, 122, 255, 0.1);
}

.form-group select {
  background: white;
  cursor: pointer;
}

.form-group select option {
  padding: 0.5rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}

.btn-primary {
  background: #007aff;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background: #0056cc;
}

.btn-secondary {
  background: #f5f5f5;
  color: #666;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.btn-secondary:hover {
  background: #e5e5e5;
}

/* Индикатор загрузки */
.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
  text-align: center;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007aff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-indicator p {
  color: #666;
  font-size: 1.1rem;
  margin: 0;
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
  
  .analytics-grid {
    grid-template-columns: 1fr;
  }
  
  .complexes-grid,
  .apartments-grid {
    grid-template-columns: 1fr;
  }
  
  .section-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .modal-content {
    margin: 1rem;
    min-width: auto;
  }
}

.apartments-list {
  margin: 1rem 0;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.apartments-list h4 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
  font-size: 1rem;
}

.apartment-item {
  padding: 0.5rem;
  border-bottom: 1px solid #e9ecef;
  margin-bottom: 0.5rem;
}

.apartment-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.apartment-info-mini {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.apartment-name {
  font-weight: 600;
  color: #2c3e50;
  flex: 1;
  min-width: 120px;
}

.apartment-price {
  font-weight: 700;
  color: #007aff;
  font-size: 0.9rem;
}

.apartment-area,
.apartment-rooms {
  color: #666;
  font-size: 0.8rem;
  background: #e9ecef;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
}
</style> 