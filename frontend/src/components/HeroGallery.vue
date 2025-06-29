<template>
  <section class="hero-gallery">
    <!-- LogoSlider сверху по всей ширине -->
    <div class="logo-slider-container">
      <div class="logo-track">
        <!-- Первый набор логотипов -->
        <div
          v-for="(logo, index) in logos"
          :key="`first-${index}`"
          class="logo-item"
        >
          <img :src="logo" alt="Logo" />
        </div>
        <!-- Второй набор для плавного перехода -->
        <div
          v-for="(logo, index) in logos"
          :key="`second-${index}`"
          class="logo-item"
        >
          <img :src="logo" alt="Logo" />
        </div>
        <!-- Третий набор для полной бесконечности -->
        <div
          v-for="(logo, index) in logos"
          :key="`third-${index}`"
          class="logo-item"
        >
          <img :src="logo" alt="Logo" />
        </div>
      </div>
    </div>
    
    <!-- Основной контент по центру -->
    <div class="hero-main-content">
      <div class="hero-container">
        <div class="hero-content">
          <h1 class="hero-title">
            Найдите свой идеальный дом
          </h1>
          <p class="hero-subtitle">
            Более 50 000 новостроек по всей России. Проверенные застройщики, 
            прозрачные условия и выгодные цены.
          </p>
          <div class="hero-filters">
            <!-- Фильтр Город -->
            <div class="filter-dropdown" @click="toggleDropdown('city')">
              <button class="filter-btn">
                {{ selectedCity || 'Город' }}
                <span class="dropdown-arrow">▼</span>
              </button>
              <div class="dropdown-menu" v-if="activeDropdown === 'city'">
                <div 
                  v-for="city in cities" 
                  :key="city"
                  class="dropdown-item"
                  @click="selectCity(city)"
                >
                  {{ city }}
                </div>
              </div>
            </div>

            <!-- Фильтр Тип -->
            <div class="filter-dropdown" @click="toggleDropdown('type')">
              <button class="filter-btn">
                {{ selectedType || 'Тип' }}
                <span class="dropdown-arrow">▼</span>
              </button>
              <div class="dropdown-menu" v-if="activeDropdown === 'type'">
                <div 
                  v-for="type in propertyTypes" 
                  :key="type"
                  class="dropdown-item"
                  @click="selectType(type)"
                >
                  {{ type }}
                </div>
              </div>
            </div>

            <!-- Фильтр Сроки -->
            <div class="filter-dropdown" @click="toggleDropdown('timeline')">
              <button class="filter-btn">
                {{ selectedTimeline || 'Сроки' }}
                <span class="dropdown-arrow">▼</span>
              </button>
              <div class="dropdown-menu" v-if="activeDropdown === 'timeline'">
                <div 
                  v-for="timeline in timelines" 
                  :key="timeline"
                  class="dropdown-item"
                  @click="selectTimeline(timeline)"
                >
                  {{ timeline }}
                </div>
              </div>
            </div>

            <!-- Фильтр Статус -->
            <div class="filter-dropdown" @click="toggleDropdown('status')">
              <button class="filter-btn">
                {{ selectedStatus || 'Статус' }}
                <span class="dropdown-arrow">▼</span>
              </button>
              <div class="dropdown-menu" v-if="activeDropdown === 'status'">
                <div 
                  v-for="status in statuses" 
                  :key="status"
                  class="dropdown-item"
                  @click="selectStatus(status)"
                >
                  {{ status }}
                </div>
              </div>
            </div>

            <button class="search-btn" @click="handleSearch">Найти</button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { propertyAPI } from '../utils/api.js'
import analytics from '../utils/analytics.js'

const emit = defineEmits(['search-complexes'])

// Логотипы застройщиков
const logos = [
  '/logos/art.svg',
  '/logos/ava.svg',
  '/logos/bel_Development.svg',
  '/logos/deco.svg',
  '/logos/neometria.svg',
  '/logos/developmentYoug.svg',
  '/logos/dogma.svg',
  '/logos/evropea.svg',
  '/logos/insiti.svg',
  '/logos/kub.svg',
  '/logos/lendex.svg',
  '/logos/livingston.svg',
  '/logos/SSK.svg',
  '/logos/tochno.svg',
  '/logos/pobeda.svg',
  '/logos/semiya.svg',
]

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

// Состояние фильтров
const activeDropdown = ref(null)
const selectedCity = ref('')
const selectedType = ref('')
const selectedTimeline = ref('')
const selectedStatus = ref('')

// Опции для фильтров
const cities = ref([
  'Москва',
  'Санкт-Петербург',
  'Новосибирск',
  'Екатеринбург',
  'Казань',
  'Нижний Новгород',
  'Челябинск',
  'Самара',
  'Уфа',
  'Ростов-на-Дону'
])

const propertyTypes = ref([
  'Студия',
  '1 комната',
  '2 комнаты',
  '3 комнаты',
  '4+ комнат',
  'Пентхаус',
  'Дуплекс'
])

const timelines = ref([
  'Сдан',
  '2024 год',
  '2025 год',
  '2026 год',
  '2027+ год'
])

const statuses = ref([
  'В продаже',
  'Бронирование',
  'Скоро в продаже',
  'Завершен'
])

// Методы для работы с фильтрами
const toggleDropdown = (dropdownName) => {
  if (activeDropdown.value === dropdownName) {
    activeDropdown.value = null
  } else {
    activeDropdown.value = dropdownName
  }
}

const selectCity = (city) => {
  selectedCity.value = city
  activeDropdown.value = null
  analytics.sendEvent(0, "filter_city_selected", city)
}

const selectType = (type) => {
  selectedType.value = type
  activeDropdown.value = null
  analytics.sendEvent(0, "filter_type_selected", type)
}

const selectTimeline = (timeline) => {
  selectedTimeline.value = timeline
  activeDropdown.value = null
  analytics.sendEvent(0, "filter_timeline_selected", timeline)
}

const selectStatus = (status) => {
  selectedStatus.value = status
  activeDropdown.value = null
  analytics.sendEvent(0, "filter_status_selected", status)
}

// Закрытие выпадающих меню при клике вне их
const handleClickOutside = (event) => {
  if (!event.target.closest('.filter-dropdown')) {
    activeDropdown.value = null
  }
}

const handleSearch = () => {
  analytics.sendEvent(0, "hero_search_click")
  emit('search-complexes')
}
</script>

<style scoped>
.hero-gallery {
  margin-top: 70px;
  background: linear-gradient(135deg, #007aff 0%, #0056cc 100%);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.hero-main-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  box-shadow: none;
}

.hero-container {
  max-width: 100vw;
  margin: 0 auto;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background: none;
  box-shadow: none;
}

.hero-content {
  color: white;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  line-height: 1.2;
}

.hero-subtitle {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  opacity: 0.9;
  line-height: 1.6;
}

.hero-filters {
  display: flex;
  gap: 0.5rem;
  max-width: 600px;
  flex-wrap: wrap;
}

.filter-dropdown {
  position: relative;
  flex: 1;
  min-width: 120px;
}

.filter-btn {
  width: 100%;
  background: rgba(255, 255, 255, 0.9);
  color: #000000;
  border: none;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter-btn:hover {
  background: rgba(255, 255, 255, 1);
  transform: translateY(-1px);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  margin-top: 4px;
  max-height: 200px;
  overflow-y: auto;
}

.dropdown-item {
  padding: 12px 16px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  border-bottom: 1px solid #f0f0f0;
  color: #000000;
}

.dropdown-item:last-child {
  border-bottom: none;
}

.dropdown-item:hover {
  background-color: #f8f9fa;
}

.dropdown-arrow {
  margin-left: 8px;
  font-size: 0.8rem;
  transition: transform 0.3s ease;
}

.filter-dropdown:hover .dropdown-arrow {
  transform: rotate(180deg);
}

.search-btn {
  background: #007aff;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.search-btn:hover {
  background: #0056cc;
  transform: translateY(-1px);
}

@media (max-width: 1024px) {
  .hero-container {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .hero-title {
    font-size: 2.5rem;
  }
}

@media (max-width: 768px) {
  .hero-container {
    padding: 2rem 1rem;
  }
  
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-subtitle {
    font-size: 1rem;
  }
  
  .hero-filters {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .filter-dropdown {
    min-width: auto;
  }
  
  .filter-btn {
    padding: 14px 16px;
    font-size: 1rem;
  }
  
  .search-btn {
    padding: 14px 24px;
    font-size: 1rem;
  }
}

/* LogoSlider стили */
.logo-slider-container {
  width: 100%;
  overflow: hidden;
  padding: 20px;
  white-space: nowrap;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  justify-content: center;
  align-items: center;
}

.logo-track {
  display: flex;
  gap: 60px;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 1200px;
  min-width: max-content;
  transition: all 0.3s ease;
  padding: 0 20px;
  animation: scroll 60s linear infinite;
}

@keyframes scroll {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(calc(-33.333% - 40px));
  }
}

.logo-item {
  display: inline-block;
  transition: transform 0.3s ease;
  filter: brightness(0) invert(1);
  flex-shrink: 0;
}

.logo-item img {
  height: 50px;
  width: auto;
  transition: transform 0.3s ease;
  opacity: 0.8;
}

.logo-item:hover img {
  transform: scale(1.1);
  opacity: 1;
  animation-play-state: paused;
}

/* Скрываем скроллбар для красоты */
.logo-slider-container::-webkit-scrollbar {
  display: none;
}

.logo-slider-container {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style> 