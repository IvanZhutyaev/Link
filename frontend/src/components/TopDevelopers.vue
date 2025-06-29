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
      // Эмитим событие для перехода к застройщику
      this.$emit('developer-selected', developerId)
    }
  }
}
</script>

<style scoped>
.top-developers {
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
  margin: 40px 0;
  position: relative;
  overflow: hidden;
}

.top-developers::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #007aff, #34c759, #ff9500, #af52de);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
  padding-bottom: 20px;
  border-bottom: 2px solid rgba(0, 122, 255, 0.1);
  position: relative;
}

.section-header::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 60px;
  height: 2px;
  background: linear-gradient(90deg, #007aff, #34c759);
  border-radius: 1px;
}

.section-header h2 {
  margin: 0;
  color: #1a202c;
  font-size: 2.2rem;
  font-weight: 800;
  background: linear-gradient(135deg, #007aff, #34c759);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  position: relative;
}

.header-actions {
  display: flex;
  gap: 15px;
  align-items: center;
}

.limit-select {
  padding: 12px 20px;
  border: 2px solid rgba(0, 122, 255, 0.2);
  border-radius: 12px;
  background: white;
  font-size: 0.95rem;
  font-weight: 500;
  color: #1a202c;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 122, 255, 0.1);
}

.limit-select:focus {
  outline: none;
  border-color: #007aff;
  box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.1);
}

.refresh-btn {
  padding: 12px 24px;
  background: linear-gradient(135deg, #007aff, #0056cc);
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 122, 255, 0.3);
  position: relative;
  overflow: hidden;
}

.refresh-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.refresh-btn:hover::before {
  left: 100%;
}

.refresh-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 122, 255, 0.4);
}

.loading-indicator {
  text-align: center;
  padding: 60px 40px;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(0, 122, 255, 0.1);
  border-top: 4px solid #007aff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
  box-shadow: 0 4px 15px rgba(0, 122, 255, 0.2);
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-indicator p {
  color: #64748b;
  font-size: 1.1rem;
  font-weight: 500;
}

.empty-state {
  text-align: center;
  padding: 60px 40px;
  color: #64748b;
  font-size: 1.1rem;
  font-weight: 500;
}

.developers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 25px;
}

.developer-card {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 25px;
  border: none;
  border-radius: 16px;
  background: white;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.developer-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #e2e8f0, #cbd5e0);
  transition: all 0.3s ease;
}

.developer-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.developer-card:hover::before {
  background: linear-gradient(90deg, #007aff, #34c759);
}

.developer-card.top-3 {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  box-shadow: 0 8px 30px rgba(102, 126, 234, 0.4);
}

.developer-card.top-3::before {
  background: linear-gradient(90deg, #ffd700, #ffed4e, #ffd700);
  height: 4px;
}

.developer-card.top-3:hover {
  box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
}

.developer-rank {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  min-width: 70px;
}

.rank-number {
  font-size: 2.5rem;
  font-weight: 900;
  color: #007aff;
  line-height: 1;
  text-shadow: 0 2px 4px rgba(0, 122, 255, 0.2);
}

.top-3 .rank-number {
  color: #ffd700;
  text-shadow: 0 2px 4px rgba(255, 215, 0, 0.3);
}

.rank-medal {
  font-size: 1.8rem;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

.developer-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.developer-name {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 700;
  color: #1a202c;
  line-height: 1.3;
}

.top-3 .developer-name {
  color: white;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.developer-rating {
  display: flex;
  align-items: center;
  gap: 15px;
}

.rating-score {
  display: flex;
  align-items: baseline;
  gap: 3px;
}

.rating-number {
  font-size: 1.8rem;
  font-weight: 800;
  color: #ff9500;
  text-shadow: 0 1px 2px rgba(255, 149, 0, 0.2);
}

.top-3 .rating-number {
  color: #ffd700;
  text-shadow: 0 1px 2px rgba(255, 215, 0, 0.3);
}

.rating-max {
  font-size: 1rem;
  color: #64748b;
  font-weight: 500;
}

.top-3 .rating-max {
  color: rgba(255, 255, 255, 0.8);
}

.rating-stars {
  display: flex;
  gap: 2px;
}

.star {
  font-size: 1rem;
  color: #e2e8f0;
  transition: all 0.3s ease;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.1));
}

.star.filled {
  color: #ffd700;
  transform: scale(1.1);
}

.developer-stats {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.95rem;
  padding: 6px 12px;
  background: rgba(0, 122, 255, 0.05);
  border-radius: 8px;
  transition: all 0.3s ease;
}

.stat-item:hover {
  background: rgba(0, 122, 255, 0.1);
  transform: translateX(5px);
}

.top-3 .stat-item {
  background: rgba(255, 255, 255, 0.1);
}

.top-3 .stat-item:hover {
  background: rgba(255, 255, 255, 0.2);
}

.stat-icon {
  font-size: 1.1rem;
}

.stat-label {
  color: #64748b;
  font-weight: 500;
}

.top-3 .stat-label {
  color: rgba(255, 255, 255, 0.8);
}

.stat-value {
  font-weight: 700;
  color: #1a202c;
  margin-left: auto;
}

.top-3 .stat-value {
  color: #ffd700;
}

.developer-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.view-btn {
  padding: 12px 24px;
  background: linear-gradient(135deg, #007aff, #0056cc);
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 600;
  transition: all 0.3s ease;
  white-space: nowrap;
  box-shadow: 0 4px 15px rgba(0, 122, 255, 0.3);
  position: relative;
  overflow: hidden;
}

.view-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.view-btn:hover::before {
  left: 100%;
}

.view-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 122, 255, 0.4);
}

.top-3 .view-btn {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(10px);
}

.top-3 .view-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 255, 255, 0.2);
}

/* Адаптивность */
@media (max-width: 768px) {
  .top-developers {
    padding: 30px 20px;
    margin: 20px 0;
  }
  
  .section-header {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }
  
  .section-header h2 {
    font-size: 1.8rem;
  }
  
  .developers-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .developer-card {
    flex-direction: column;
    text-align: center;
    padding: 20px;
  }
  
  .developer-rank {
    flex-direction: row;
    gap: 15px;
    margin-bottom: 10px;
  }
  
  .developer-stats {
    flex-direction: row;
    justify-content: center;
    gap: 15px;
    flex-wrap: wrap;
  }
  
  .stat-item {
    min-width: 120px;
  }
}

@media (max-width: 480px) {
  .top-developers {
    padding: 20px 15px;
  }
  
  .section-header h2 {
    font-size: 1.5rem;
  }
  
  .header-actions {
    flex-direction: column;
    gap: 10px;
  }
  
  .developer-card {
    padding: 15px;
  }
  
  .developer-stats {
    flex-direction: column;
    gap: 8px;
  }
}
</style> 