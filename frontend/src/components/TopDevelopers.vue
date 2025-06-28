<template>
  <div class="top-developers">
    <div class="section-header">
      <h2>Топ застройщиков</h2>
      <div class="header-actions">
        <select v-model="selectedLimit" @change="loadTopDevelopers" class="limit-select">
          <option value="5">Топ 5</option>
          <option value="10">Топ 10</option>
          <option value="20">Топ 20</option>
        </select>
        <button class="refresh-btn" @click="loadTopDevelopers">
          🔄 Обновить
        </button>
      </div>
    </div>

    <div v-if="loading" class="loading-indicator">
      <div class="loading-spinner"></div>
      <p>Загрузка топ застройщиков...</p>
    </div>

    <div v-else-if="developers.length === 0" class="empty-state">
      <p>Нет данных о застройщиках</p>
    </div>

    <div v-else class="developers-grid">
      <div 
        v-for="(developer, index) in developers" 
        :key="developer.id"
        class="developer-card"
        :class="{ 'top-3': index < 3 }"
      >
        <div class="developer-rank">
          <div class="rank-number">{{ index + 1 }}</div>
          <div class="rank-medal" v-if="index < 3">
            {{ index === 0 ? '🥇' : index === 1 ? '🥈' : '🥉' }}
          </div>
        </div>
        
        <div class="developer-info">
          <h3 class="developer-name">{{ developer.company_name }}</h3>
          
          <div class="developer-rating">
            <div class="rating-score">
              <span class="rating-number">{{ developer.rating }}</span>
              <span class="rating-max">/10</span>
            </div>
            <div class="rating-stars">
              <span 
                v-for="i in 10" 
                :key="i" 
                class="star"
                :class="{ 'filled': i <= Math.round(developer.rating) }"
              >
                ★
              </span>
            </div>
          </div>
          
          <div class="developer-stats">
            <div class="stat-item">
              <span class="stat-icon">🏗️</span>
              <span class="stat-label">Проектов:</span>
              <span class="stat-value">{{ developer.completed_projects }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-icon">📅</span>
              <span class="stat-label">Лет на рынке:</span>
              <span class="stat-value">{{ developer.years_on_market }}</span>
            </div>
          </div>
        </div>
        
        <div class="developer-actions">
          <button class="view-btn" @click="viewDeveloper(developer.id)">
            Просмотр
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { developerRatingAPI } from '../utils/api.js'

export default {
  name: 'TopDevelopers',
  data() {
    return {
      developers: [],
      loading: false,
      selectedLimit: 10
    }
  },
  mounted() {
    this.loadTopDevelopers()
  },
  methods: {
    async loadTopDevelopers() {
      try {
        this.loading = true
        this.developers = await developerRatingAPI.getTopDevelopers(this.selectedLimit)
      } catch (error) {
        console.error('Ошибка загрузки топ застройщиков:', error)
        this.developers = []
      } finally {
        this.loading = false
      }
    },
    
    viewDeveloper(developerId) {
      // Переход к странице застройщика
      this.$router.push(`/developer/${developerId}`)
    }
  }
}
</script>

<style scoped>
.top-developers {
  background: white;
  border-radius: 10px;
  padding: 25px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 2px solid #007bff;
}

.section-header h2 {
  margin: 0;
  color: #333;
  font-size: 1.5rem;
}

.header-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.limit-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background: white;
  font-size: 0.9rem;
}

.refresh-btn {
  padding: 8px 16px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.refresh-btn:hover {
  background: #0056b3;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.loading-indicator {
  text-align: center;
  padding: 40px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #666;
}

.developers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.developer-card {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  background: white;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.developer-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0,0,0,0.15);
}

.developer-card.top-3 {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
}

.developer-card.top-3::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #ffd700, #ffed4e);
}

.developer-rank {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  min-width: 60px;
}

.rank-number {
  font-size: 2rem;
  font-weight: bold;
  color: #007bff;
  line-height: 1;
}

.top-3 .rank-number {
  color: #ffd700;
}

.rank-medal {
  font-size: 1.5rem;
}

.developer-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.developer-name {
  margin: 0;
  font-size: 1.2rem;
  font-weight: bold;
  color: #333;
}

.top-3 .developer-name {
  color: white;
}

.developer-rating {
  display: flex;
  align-items: center;
  gap: 10px;
}

.rating-score {
  display: flex;
  align-items: baseline;
  gap: 2px;
}

.rating-number {
  font-size: 1.5rem;
  font-weight: bold;
  color: #ffc107;
}

.top-3 .rating-number {
  color: #ffd700;
}

.rating-max {
  font-size: 0.9rem;
  color: #666;
}

.top-3 .rating-max {
  color: rgba(255,255,255,0.8);
}

.rating-stars {
  display: flex;
  gap: 1px;
}

.star {
  font-size: 0.9rem;
  color: #ccc;
  transition: color 0.3s ease;
}

.star.filled {
  color: #ffd700;
}

.developer-stats {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
}

.stat-icon {
  font-size: 1rem;
}

.stat-label {
  color: #666;
  font-weight: 500;
}

.top-3 .stat-label {
  color: rgba(255,255,255,0.8);
}

.stat-value {
  font-weight: bold;
  color: #333;
}

.top-3 .stat-value {
  color: #ffd700;
}

.developer-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.view-btn {
  padding: 8px 16px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.view-btn:hover {
  background: #0056b3;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.top-3 .view-btn {
  background: rgba(255,255,255,0.2);
  color: white;
  border: 1px solid rgba(255,255,255,0.3);
}

.top-3 .view-btn:hover {
  background: rgba(255,255,255,0.3);
}

/* Адаптивность */
@media (max-width: 768px) {
  .section-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
  
  .developers-grid {
    grid-template-columns: 1fr;
  }
  
  .developer-card {
    flex-direction: column;
    text-align: center;
  }
  
  .developer-rank {
    flex-direction: row;
    gap: 10px;
  }
  
  .developer-stats {
    flex-direction: row;
    justify-content: center;
    gap: 20px;
  }
}
</style> 