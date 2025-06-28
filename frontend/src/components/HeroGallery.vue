<template>
  <section class="hero-gallery">
    <div class="hero-container">
      <div class="hero-content">
        <h1 class="hero-title">
          Найдите свой идеальный дом
        </h1>
        <p class="hero-subtitle">
          Более 50 000 новостроек по всей России. Проверенные застройщики, 
          прозрачные условия и выгодные цены.
        </p>
        <div class="hero-search">
          <input 
            type="text" 
            placeholder="Введите название города или района"
            class="search-input"
          />
          <button class="search-btn" @click="handleSearch">Найти</button>
        </div>
      </div>
      
      <div class="gallery">
        <div class="gallery-grid">
          <div 
            v-for="(item, index) in galleryItems" 
            :key="index"
            class="gallery-item"
            :class="`gallery-item-${index + 1}`"
            @click="handleGalleryItemClick(item)"
          >
            <div class="item-overlay">
              <h3>{{ item.title }}</h3>
              <p>{{ item.description }}</p>
              <span class="item-price">{{ item.price }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { propertyAPI } from '../utils/api.js'
import analytics from '../utils/analytics.js'

const currentSlide = ref(0)
const galleryItems = ref([])

// Загрузка данных о ЖК
const loadGalleryData = async () => {
  try {
    const properties = await propertyAPI.getAllProperties()
    galleryItems.value = properties.slice(0, 4).map(property => ({
      id: property.id,
      title: property.name,
      description: property.description || 'Современный жилой комплекс',
      price: `от ${property.price.toLocaleString()} ₽`
    }))
    
    // Отслеживаем загрузку галереи
    analytics.sendEvent(0, "gallery_loaded", properties.length)
  } catch (error) {
    console.error('Ошибка загрузки данных галереи:', error)
    // Fallback данные
    galleryItems.value = [
      {
        id: 1,
        title: 'ЖК "Солнечный"',
        description: 'Современный комплекс с развитой инфраструктурой',
        price: 'от 3.2 млн ₽'
      },
      {
        id: 2,
        title: 'ЖК "Парковый"',
        description: 'Зеленый район с собственным парком',
        price: 'от 4.1 млн ₽'
      },
      {
        id: 3,
        title: 'ЖК "Речной"',
        description: 'Вид на реку, элитное расположение',
        price: 'от 6.8 млн ₽'
      },
      {
        id: 4,
        title: 'ЖК "Центральный"',
        description: 'В самом сердце города',
        price: 'от 5.5 млн ₽'
      }
    ]
  }
}

const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % galleryItems.value.length
  // Отслеживаем переключение слайда
  analytics.sendEvent(0, "gallery_next_slide", currentSlide.value)
}

const prevSlide = () => {
  currentSlide.value = currentSlide.value === 0 
    ? galleryItems.value.length - 1 
    : currentSlide.value - 1
  // Отслеживаем переключение слайда
  analytics.sendEvent(0, "gallery_prev_slide", currentSlide.value)
}

const goToSlide = (index) => {
  currentSlide.value = index
  // Отслеживаем переход к конкретному слайду
  analytics.sendEvent(0, "gallery_go_to_slide", index)
}

const handleGalleryItemClick = (item) => {
  // Отслеживаем клик по элементу галереи
  analytics.trackApartmentView(item.id)
  console.log('Клик по элементу галереи:', item)
}

const handleSearch = () => {
  // Отслеживаем поиск в главной галерее
  analytics.sendEvent(0, "hero_search")
  console.log('Поиск в главной галерее')
}

onMounted(() => {
  loadGalleryData()
  
  // Автоматическое переключение слайдов
  setInterval(() => {
    nextSlide()
  }, 5000)
})
</script>

<style scoped>
.hero-gallery {
  margin-top: 70px;
  background: linear-gradient(135deg, #007aff 0%, #0056cc 100%);
  min-height: 100vh;
  display: flex;
  align-items: center;
}

.hero-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 4rem 2rem;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
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

.hero-search {
  display: flex;
  gap: 1rem;
  max-width: 500px;
}

.search-input {
  flex: 1;
  padding: 15px 20px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  outline: none;
}

.search-btn {
  background: #007aff;
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.search-btn:hover {
  background: #0056cc;
}

.gallery {
  position: relative;
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 1fr);
  gap: 1rem;
  height: 400px;
}

.gallery-item {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.gallery-item:hover {
  transform: scale(1.05);
}

.gallery-item-1 {
  background: linear-gradient(45deg, #007aff, #0056cc);
  grid-column: 1 / 2;
  grid-row: 1 / 3;
}

.gallery-item-2 {
  background: linear-gradient(45deg, #34c759, #28a745);
  grid-column: 2 / 3;
  grid-row: 1 / 2;
}

.gallery-item-3 {
  background: linear-gradient(45deg, #ff9500, #ff6b35);
  grid-column: 2 / 3;
  grid-row: 2 / 3;
}

.gallery-item-4 {
  background: linear-gradient(45deg, #af52de, #8e44ad);
  grid-column: 1 / 2;
  grid-row: 3 / 4;
}

.item-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.8));
  color: white;
  padding: 1.5rem;
  transform: translateY(100%);
  transition: transform 0.3s ease;
}

.gallery-item:hover .item-overlay {
  transform: translateY(0);
}

.item-overlay h3 {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.item-overlay p {
  font-size: 0.9rem;
  opacity: 0.9;
  margin-bottom: 0.5rem;
}

.item-price {
  font-size: 1.1rem;
  font-weight: 700;
  color: #007aff;
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
  
  .hero-search {
    flex-direction: column;
  }
  
  .gallery-grid {
    height: 300px;
  }
}
</style> 