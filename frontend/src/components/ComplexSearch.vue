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

    <div v-else class="complexes-grid">
      <div 
        v-for="complex in complexes" 
        :key="complex.id"
        class="complex-card"
        @click="selectComplex(complex)"
      >
        <div class="complex-image">
          <img :src="complex.avatar_url || '/default-complex.jpg'" :alt="complex.name" />
          <div class="complex-status" :class="complex.status">
            {{ getStatusText(complex.status) }}
          </div>
        </div>
        <div class="complex-info">
          <h3>{{ complex.name }}</h3>
          <p class="complex-address">{{ complex.address }}</p>
          <p class="complex-city">{{ complex.city }}</p>
          <p class="complex-class">Класс: {{ complex.housing_class || 'Не указан' }}</p>
          <p class="complex-date">Ввод в эксплуатацию: {{ complex.commissioning_date || 'Не указана' }}</p>
          
          <!-- Рейтинг -->
          <div class="complex-rating" v-if="complex.rating">
            <div class="stars">
              <span 
                v-for="i in 5" 
                :key="i" 
                class="star"
                :class="{ filled: i <= complex.rating }"
              >
                ★
              </span>
            </div>
            <span class="rating-text">{{ complex.rating.toFixed(1) }} ({{ complex.rating_count }} оценок)</span>
          </div>
          
          <div class="complex-actions">
            <button class="action-btn primary" @click.stop="viewComplex(complex.id)">
              Просмотр
            </button>
            <button class="action-btn secondary" @click.stop="viewApartments(complex.id)">
              Квартиры
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно с квартирами ЖК -->
    <div v-if="showApartmentsModal" class="modal-overlay" @click="closeApartmentsModal">
      <div class="modal-content apartments-modal" @click.stop>
        <div class="modal-header">
          <h3>Квартиры в ЖК "{{ selectedComplex?.name }}"</h3>
          <button class="close-btn" @click="closeApartmentsModal">×</button>
        </div>
        
        <div v-if="apartmentsLoading" class="loading">
          <div class="spinner"></div>
          <p>Загрузка квартир...</p>
        </div>
        
        <div v-else-if="apartments.length === 0" class="no-results">
          <p>Квартиры в этом ЖК не найдены</p>
        </div>
        
        <div v-else class="apartments-list">
          <div 
            v-for="apartment in apartments" 
            :key="apartment.id"
            class="apartment-item"
          >
            <div class="apartment-image">
              <img :src="apartment.image_url || '/default-apartment.jpg'" :alt="apartment.name" />
            </div>
            <div class="apartment-info">
              <h4>{{ apartment.name }}</h4>
              <p class="apartment-address">{{ apartment.address }}</p>
              <p class="apartment-price">{{ formatPrice(apartment.price) }} ₽</p>
              <p class="apartment-details">
                {{ apartment.area }} м² • {{ apartment.rooms }} комн. • {{ apartment.floor }} этаж
              </p>
              
              <!-- Рейтинг квартиры -->
              <div class="apartment-rating" v-if="apartment.rating">
                <div class="stars">
                  <span 
                    v-for="i in 5" 
                    :key="i" 
                    class="star"
                    :class="{ filled: i <= apartment.rating }"
                  >
                    ★
                  </span>
                </div>
                <span class="rating-text">{{ apartment.rating.toFixed(1) }}</span>
              </div>
              
              <div class="apartment-actions">
                <button class="action-btn primary" @click="bookApartment(apartment.id)">
                  Забронировать
                </button>
                <button class="action-btn secondary" @click="viewApartment(apartment.id)">
                  Подробнее
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { api } from '../utils/api.js'

export default {
  name: 'ComplexSearch',
  data() {
    return {
      complexes: [],
      apartments: [],
      loading: false,
      apartmentsLoading: false,
      showApartmentsModal: false,
      selectedComplex: null,
      searchFilters: {
        city: '',
        housing_class: ''
      }
    }
  },
  async mounted() {
    await this.searchComplexes()
  },
  methods: {
    async searchComplexes() {
      this.loading = true
      try {
        const params = new URLSearchParams()
        if (this.searchFilters.city) params.append('city', this.searchFilters.city)
        if (this.searchFilters.housing_class) params.append('housing_class', this.searchFilters.housing_class)
        
        const response = await api.get(`/zastroys/residential-complexes/?${params}`)
        this.complexes = response.data
      } catch (error) {
        console.error('Ошибка при поиске ЖК:', error)
        this.complexes = []
      } finally {
        this.loading = false
      }
    },
    
    async viewApartments(complexId) {
      this.apartmentsLoading = true
      this.showApartmentsModal = true
      this.selectedComplex = this.complexes.find(c => c.id === complexId)
      
      try {
        const response = await api.get(`/zastroys/residential-complexes/${complexId}/apartments`)
        this.apartments = response.data
      } catch (error) {
        console.error('Ошибка при загрузке квартир:', error)
        this.apartments = []
      } finally {
        this.apartmentsLoading = false
      }
    },
    
    closeApartmentsModal() {
      this.showApartmentsModal = false
      this.selectedComplex = null
      this.apartments = []
    },
    
    selectComplex(complex) {
      this.$emit('complex-selected', complex)
    },
    
    viewComplex(complexId) {
      this.$router.push(`/complex/${complexId}`)
    },
    
    async bookApartment(apartmentId) {
      try {
        const userId = 1 // В реальном приложении брать из авторизации
        await api.post('/properties/book', {
          property_id: apartmentId
        }, {
          params: { user_id: userId }
        })
        alert('Квартира забронирована!')
        // Обновляем список квартир
        if (this.selectedComplex) {
          this.viewApartments(this.selectedComplex.id)
        }
      } catch (error) {
        console.error('Ошибка при бронировании квартиры:', error)
        alert('Ошибка при бронировании квартиры')
      }
    },
    
    viewApartment(apartmentId) {
      this.$router.push(`/apartment/${apartmentId}`)
    },
    
    getStatusText(status) {
      const statusMap = {
        'строится': 'Строится',
        'сдан': 'Сдан',
        'планируется': 'Планируется'
      }
      return statusMap[status] || status
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
}

.search-header {
  margin-bottom: 30px;
}

.search-header h2 {
  margin-bottom: 20px;
  color: #333;
}

.search-filters {
  display: flex;
  gap: 15px;
  align-items: center;
  flex-wrap: wrap;
}

.filter-input,
.filter-select {
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
}

.search-btn {
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.search-btn:hover {
  background: #0056b3;
}

.complexes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.complex-card {
  border: 1px solid #ddd;
  border-radius: 10px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.complex-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.complex-image {
  position: relative;
  height: 200px;
  overflow: hidden;
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
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 12px;
  font-weight: bold;
  color: white;
}

.complex-status.строится {
  background: #ffc107;
}

.complex-status.сдан {
  background: #28a745;
}

.complex-status.планируется {
  background: #17a2b8;
}

.complex-info {
  padding: 20px;
}

.complex-info h3 {
  margin: 0 0 10px 0;
  color: #333;
}

.complex-address,
.complex-city,
.complex-class,
.complex-date {
  margin: 5px 0;
  color: #666;
  font-size: 14px;
}

.complex-rating {
  margin: 15px 0;
  display: flex;
  align-items: center;
  gap: 10px;
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
  font-size: 12px;
  color: #666;
}

.complex-actions {
  margin-top: 15px;
  display: flex;
  gap: 10px;
}

.action-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.2s;
}

.action-btn.primary {
  background: #007bff;
  color: white;
}

.action-btn.primary:hover {
  background: #0056b3;
}

.action-btn.secondary {
  background: #6c757d;
  color: white;
}

.action-btn.secondary:hover {
  background: #545b62;
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
}

/* Модальное окно */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 10px;
  max-width: 90%;
  max-height: 90%;
  overflow: auto;
}

.apartments-modal {
  width: 800px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #ddd;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
}

.close-btn:hover {
  color: #333;
}

.apartments-list {
  padding: 20px;
}

.apartment-item {
  display: flex;
  gap: 15px;
  padding: 15px;
  border: 1px solid #eee;
  border-radius: 8px;
  margin-bottom: 15px;
}

.apartment-image {
  width: 120px;
  height: 90px;
  overflow: hidden;
  border-radius: 5px;
}

.apartment-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.apartment-info {
  flex: 1;
}

.apartment-info h4 {
  margin: 0 0 8px 0;
  color: #333;
}

.apartment-address,
.apartment-price,
.apartment-details {
  margin: 4px 0;
  color: #666;
  font-size: 14px;
}

.apartment-price {
  font-weight: bold;
  color: #007bff;
  font-size: 16px;
}

.apartment-rating {
  margin: 8px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.apartment-actions {
  margin-top: 10px;
  display: flex;
  gap: 8px;
}

.apartment-actions .action-btn {
  padding: 6px 12px;
  font-size: 12px;
}
</style> 