<template>
  <div class="analytics-dashboard">
    <div class="analytics-header">
      <h2>Аналитика</h2>
      <div class="period-selector">
        <label>Период:</label>
        <select v-model="selectedPeriod" @change="loadAnalytics">
          <option value="7">7 дней</option>
          <option value="30">30 дней</option>
          <option value="90">90 дней</option>
        </select>
      </div>
    </div>

    <!-- Общая сводка -->
    <div class="analytics-summary">
      <div class="summary-card">
        <div class="summary-icon">📊</div>
        <div class="summary-content">
          <h3>Всего событий</h3>
          <p class="summary-number">{{ analyticsData.total_events || 0 }}</p>
        </div>
      </div>
      
      <div class="summary-card">
        <div class="summary-icon">👥</div>
        <div class="summary-content">
          <h3>Уникальных пользователей</h3>
          <p class="summary-number">{{ analyticsData.unique_users || 0 }}</p>
        </div>
      </div>
      
      <div class="summary-card">
        <div class="summary-icon">⏱️</div>
        <div class="summary-content">
          <h3>Среднее время на странице</h3>
          <p class="summary-number">{{ formatTime(analyticsData.average_time_on_page) }}</p>
        </div>
      </div>
      
      <div class="summary-card">
        <div class="summary-icon">🎯</div>
        <div class="summary-content">
          <h3>Конверсия</h3>
          <p class="summary-number">{{ analyticsData.conversion_rate ? analyticsData.conversion_rate.toFixed(1) : 0 }}%</p>
        </div>
      </div>
    </div>

    <!-- События по типам -->
    <div class="analytics-section">
      <h3>События по типам</h3>
      <div class="events-chart">
        <div 
          v-for="(count, eventType) in analyticsData.events_by_type" 
          :key="eventType"
          class="event-item"
        >
          <div class="event-info">
            <span class="event-type">{{ getEventTypeName(eventType) }}</span>
            <span class="event-count">{{ count }}</span>
          </div>
          <div class="event-bar">
            <div 
              class="event-progress" 
              :style="{ width: getEventPercentage(count) + '%' }"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Самые просматриваемые квартиры -->
    <div class="analytics-section">
      <h3>Самые просматриваемые квартиры</h3>
      <div class="apartments-list">
        <div 
          v-for="apartment in analyticsData.most_viewed_apartments" 
          :key="apartment.apartment_id"
          class="apartment-item"
        >
          <div class="apartment-info">
            <span class="apartment-id">Квартира #{{ apartment.apartment_id }}</span>
            <span class="apartment-views">{{ apartment.views }} просмотров</span>
          </div>
          <button 
            class="view-details-btn"
            @click="viewApartmentAnalytics(apartment.apartment_id)"
          >
            Детали
          </button>
        </div>
      </div>
    </div>

    <!-- Аналитика по квартирам -->
    <div v-if="selectedApartmentAnalytics" class="analytics-section">
      <h3>Аналитика квартиры #{{ selectedApartmentAnalytics.apartment_id }}</h3>
      <div class="apartment-analytics">
        <div class="apartment-stat">
          <span class="stat-label">Всего просмотров:</span>
          <span class="stat-value">{{ selectedApartmentAnalytics.total_views }}</span>
        </div>
        <div class="apartment-stat">
          <span class="stat-label">Уникальных посетителей:</span>
          <span class="stat-value">{{ selectedApartmentAnalytics.unique_visitors }}</span>
        </div>
        <div class="apartment-stat">
          <span class="stat-label">Кликов по 3D туру:</span>
          <span class="stat-value">{{ selectedApartmentAnalytics.clicks_3d_tour }}</span>
        </div>
        <div class="apartment-stat">
          <span class="stat-label">Кликов по бронированию:</span>
          <span class="stat-value">{{ selectedApartmentAnalytics.clicks_book }}</span>
        </div>
        <div class="apartment-stat">
          <span class="stat-label">Среднее время на странице:</span>
          <span class="stat-value">{{ formatTime(selectedApartmentAnalytics.average_time_on_page) }}</span>
        </div>
        <div class="apartment-stat">
          <span class="stat-label">Конверсия:</span>
          <span class="stat-value">{{ selectedApartmentAnalytics.conversion_rate ? selectedApartmentAnalytics.conversion_rate.toFixed(1) : 0 }}%</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import analytics from '../utils/analytics.js'

const selectedPeriod = ref(30)
const selectedApartmentAnalytics = ref(null)

const analyticsData = ref({
  total_events: 0,
  unique_users: 0,
  average_time_on_page: 0,
  conversion_rate: 0,
  events_by_type: {},
  most_viewed_apartments: []
})

const loadAnalytics = async () => {
  try {
    // Загружаем общую аналитику
    const summary = await analytics.getAnalyticsSummary(selectedPeriod.value)
    if (summary) {
      analyticsData.value = summary
    }
  } catch (error) {
    console.error('Ошибка загрузки аналитики:', error)
  }
}

const viewApartmentAnalytics = async (apartmentId) => {
  try {
    const apartmentAnalytics = await analytics.getApartmentAnalytics(apartmentId, selectedPeriod.value)
    if (apartmentAnalytics) {
      selectedApartmentAnalytics.value = apartmentAnalytics
    }
  } catch (error) {
    console.error('Ошибка загрузки аналитики квартиры:', error)
  }
}

const formatTime = (seconds) => {
  if (!seconds) return '0 сек'
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = Math.floor(seconds % 60)
  return minutes > 0 ? `${minutes}м ${remainingSeconds}с` : `${remainingSeconds}с`
}

const getEventTypeName = (eventType) => {
  const eventNames = {
    'view_apartment': 'Просмотр квартиры',
    'click_3d_tour': 'Клик по 3D туру',
    'click_book': 'Клик по бронированию',
    'time_on_page': 'Время на странице',
    'search_property': 'Поиск недвижимости',
    'filter_applied': 'Применение фильтров',
    'click_map': 'Клик по карте',
    'view_gallery': 'Просмотр галереи',
    'click_contact': 'Клик по контактам',
    'user_login': 'Вход пользователя',
    'user_logout': 'Выход пользователя',
    'create_complex': 'Создание ЖК',
    'create_apartment': 'Создание квартиры',
    'edit_complex': 'Редактирование ЖК',
    'add_apartment': 'Добавление квартиры',
    'confirm_sale': 'Подтверждение продажи',
    'cancel_booking': 'Отмена брони'
  }
  return eventNames[eventType] || eventType
}

const getEventPercentage = (count) => {
  const total = Object.values(analyticsData.value.events_by_type).reduce((sum, val) => sum + val, 0)
  return total > 0 ? (count / total) * 100 : 0
}

onMounted(() => {
  loadAnalytics()
})
</script>

<style scoped>
.analytics-dashboard {
  padding: 2rem;
  background: #f8f9fa;
  border-radius: 12px;
  margin-bottom: 2rem;
}

.analytics-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.analytics-header h2 {
  color: #007aff;
  margin: 0;
}

.period-selector {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.period-selector select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: white;
}

.analytics-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.summary-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.summary-icon {
  font-size: 2rem;
}

.summary-content h3 {
  margin: 0 0 0.5rem 0;
  font-size: 0.9rem;
  color: #666;
}

.summary-number {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: #007aff;
}

.analytics-section {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-bottom: 1.5rem;
}

.analytics-section h3 {
  color: #007aff;
  margin: 0 0 1rem 0;
}

.events-chart {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.event-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.event-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex: 1;
  min-width: 200px;
}

.event-type {
  font-weight: 500;
}

.event-count {
  color: #007aff;
  font-weight: 600;
}

.event-bar {
  flex: 2;
  height: 8px;
  background: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
}

.event-progress {
  height: 100%;
  background: #007aff;
  transition: width 0.3s ease;
}

.apartments-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.apartment-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 6px;
}

.apartment-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.apartment-id {
  font-weight: 600;
}

.apartment-views {
  color: #666;
  font-size: 0.9rem;
}

.view-details-btn {
  background: #007aff;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
}

.view-details-btn:hover {
  background: #0056cc;
}

.apartment-analytics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.apartment-stat {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 6px;
}

.stat-label {
  font-weight: 500;
}

.stat-value {
  color: #007aff;
  font-weight: 600;
}

@media (max-width: 768px) {
  .analytics-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .analytics-summary {
    grid-template-columns: 1fr;
  }
  
  .apartment-analytics {
    grid-template-columns: 1fr;
  }
}
</style> 