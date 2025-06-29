<template>
  <div class="complex-search">
    <div class="search-header">
      <h2>Поиск жилых комплексов</h2>
      <div class="search-filters">
        <input 
          v-model="searchFilters.city" 
          type="text" 
          placeholder="Город"
          class="filter-input"
        />
        <select v-model="searchFilters.housing_class" class="filter-select">
          <option value="">Все классы</option>
          <option value="эконом">Эконом</option>
          <option value="комфорт">Комфорт</option>
          <option value="бизнес">Бизнес</option>
          <option value="премиум">Премиум</option>
          <option value="элит">Элит</option>
        </select>
        <button @click="searchComplexes" class="search-btn">Поиск</button>
      </div>
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Поиск жилых комплексов...</p>
    </div>

    <div v-else-if="complexes.length === 0" class="no-results">
      <p>Жилые комплексы не найдены</p>
    </div>

    <div v-else class="complexes-list">
      <div 
        v-for="complex in complexes" 
        :key="complex.id"
        class="complex-card"
        @click="openTourModal(complex)"
      >
        <div class="complex-image">
          <img :src="complex.avatar_url || '/default-complex.jpg'" :alt="complex.name" />
        </div>
        <div class="complex-info">
          <h3 class="complex-name">{{ complex.name }}</h3>
          <p class="developer-name">{{ complex.developer_name }}</p>
          
          <!-- Рейтинг застройщика -->
          <div class="developer-rating" v-if="complex.developer_rating">
            <div class="stars">
              <span 
                v-for="i in 5" 
                :key="i" 
                class="star"
                :class="{ filled: i <= Math.round(complex.developer_rating) }"
              >
                ★
              </span>
            </div>
            <span class="rating-text">{{ complex.developer_rating.toFixed(1) }}</span>
          </div>
          
          <p class="commissioning-date">Срок эксплуатации: {{ complex.commissioning_date || 'Не указан' }}</p>
          <p class="complex-address">{{ complex.address }}</p>
        </div>
        
        <!-- Тип ЖК справа снизу -->
        <div class="complex-type">
          <span class="type-badge" :class="getTypeClass(complex.housing_class)">
            {{ getTypeText(complex.housing_class) }}
          </span>
        </div>
      </div>
    </div>

    <!-- Модальное окно для 3D-тура -->
    <div v-if="showTourModal" class="modal-overlay" @click.self="closeTourModal">
      <div class="modal-content">
        <button class="modal-close" @click="closeTourModal">×</button>
        <template v-if="selectedComplex && selectedComplex.avaline_url">
          <iframe
            :src="selectedComplex.avaline_url"
            width="100%"
            height="500px"
            frameborder="0"
            allowfullscreen
          ></iframe>
        </template>
        <template v-else>
          <p>3D-тур для этого ЖК пока не добавлен.</p>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import { complexAPI, developerRatingAPI } from '../utils/api.js'

export default {
  name: 'ComplexSearch',
  data() {
    return {
      complexes: [],
      loading: false,
      searchFilters: {
        city: '',
        housing_class: ''
      },
      showTourModal: false,
      selectedComplex: null
    }
  },
  async mounted() {
    await this.searchComplexes()
  },
  methods: {
    async searchComplexes() {
      this.loading = true
      try {
        const complexes = await complexAPI.getAllComplexes({
          city: this.searchFilters.city,
          housing_class: this.searchFilters.housing_class
        })
        
        // Получаем рейтинги застройщиков для каждого ЖК
        const complexesWithRatings = await Promise.all(
          complexes.map(async (complex) => {
            try {
              const ratingResponse = await developerRatingAPI.getRating(complex.zastroy_id)
              return {
                ...complex,
                developer_rating: ratingResponse.rating
              }
            } catch (error) {
              console.error(`Ошибка при получении рейтинга застройщика ${complex.zastroy_id}:`, error)
              return {
                ...complex,
                developer_rating: null
              }
            }
          })
        )
        
        this.complexes = complexesWithRatings
      } catch (error) {
        console.error('Ошибка при поиске ЖК:', error)
        this.complexes = []
      } finally {
        this.loading = false
      }
    },
    
    openTourModal(complex) {
      this.selectedComplex = complex
      this.showTourModal = true
    },
    
    closeTourModal() {
      this.showTourModal = false
      this.selectedComplex = null
    },
    
    getTypeClass(housingClass) {
      const classMap = {
        'эконом': 'economy',
        'комфорт': 'comfort',
        'бизнес': 'business',
        'премиум': 'premium',
        'элит': 'elite'
      }
      return classMap[housingClass?.toLowerCase()] || 'default'
    },
    
    getTypeText(housingClass) {
      const textMap = {
        'эконом': 'Эконом',
        'комфорт': 'Комфорт',
        'бизнес': 'Бизнес',
        'премиум': 'Премиум',
        'элит': 'Элит'
      }
      return textMap[housingClass?.toLowerCase()] || 'Не указан'
    },
    
    formatPrice(price) {
      return new Intl.NumberFormat('ru-RU').format(price)
    }
  }
}
</script>

<style scoped>
.complex-search {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.search-header {
  margin-bottom: 30px;
}

.search-header h2 {
  margin-bottom: 20px;
  color: #333;
  font-size: 28px;
}

.search-filters {
  display: flex;
  gap: 15px;
  align-items: center;
  flex-wrap: wrap;
}

.filter-input,
.filter-select {
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  min-width: 150px;
}

.search-btn {
  padding: 12px 24px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: background 0.2s;
}

.search-btn:hover {
  background: #0056b3;
}

.complexes-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.complex-card {
  display: flex;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  background: white;
  position: relative;
}

.complex-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.1);
}

.complex-image {
  width: 200px;
  height: 150px;
  overflow: hidden;
  flex-shrink: 0;
}

.complex-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.complex-info {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.complex-name {
  margin: 0;
  color: #333;
  font-size: 20px;
  font-weight: 600;
}

.developer-name {
  margin: 0;
  color: #666;
  font-size: 16px;
  font-weight: 500;
}

.developer-rating {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 4px 0;
}

.stars {
  display: flex;
  gap: 2px;
}

.star {
  color: #ddd;
  font-size: 16px;
}

.star.filled {
  color: #ffc107;
}

.rating-text {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.commissioning-date {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.complex-address {
  margin: 0;
  color: #888;
  font-size: 14px;
}

.complex-type {
  position: absolute;
  bottom: 15px;
  right: 15px;
}

.type-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: white;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.type-badge.economy {
  background: #28a745;
}

.type-badge.comfort {
  background: #17a2b8;
}

.type-badge.business {
  background: #ffc107;
  color: #333;
}

.type-badge.premium {
  background: #fd7e14;
}

.type-badge.elite {
  background: #dc3545;
}

.type-badge.default {
  background: #6c757d;
}

.loading {
  text-align: center;
  padding: 40px;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.no-results {
  text-align: center;
  padding: 40px;
  color: #666;
  font-size: 18px;
}

/* Адаптивность */
@media (max-width: 768px) {
  .complex-card {
    flex-direction: column;
  }
  
  .complex-image {
    width: 100%;
    height: 200px;
  }
  
  .complex-type {
    position: static;
    align-self: flex-end;
    margin-top: 10px;
  }
  
  .search-filters {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filter-input,
  .filter-select {
    min-width: auto;
  }
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal-content {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  max-width: 800px;
  width: 90vw;
  position: relative;
  box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}
.modal-close {
  position: absolute;
  top: 12px;
  right: 16px;
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: #888;
}
</style> 