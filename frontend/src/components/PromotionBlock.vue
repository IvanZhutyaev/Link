<template>
  <div class="promotion-block">
    <div class="section-header">
      <h2>Специальное предложение</h2>
      <div class="promotion-badge">
        <span class="badge-text">АКЦИЯ</span>
      </div>
    </div>

    <div class="promotion-card">
      <div class="promotion-image">
        <img src="/apartment.jpg" alt="Специальное предложение" />
        <div class="image-overlay">
          <div class="discount-badge">
            <span class="discount-text">-25%</span>
          </div>
        </div>
      </div>
      
      <div class="promotion-content">
        <div class="promotion-title">
          <h3>🏢 ЖК "Современный" - Скидка на все квартиры!</h3>
          <p class="promotion-description">
            Уникальное предложение! Скидка 25% на все квартиры в новом жилом комплексе 
            "Современный". Отличная локация, современная инфраструктура, 
            подземная парковка и детская площадка.
          </p>
        </div>
        
        <div class="promotion-details">
          <div class="detail-item">
            <span class="detail-icon">📍</span>
            <span class="detail-text">ул. Центральная, 15</span>
          </div>
          <div class="detail-item">
            <span class="detail-icon">💰</span>
            <span class="detail-text">от 2,500,000 ₽</span>
          </div>
          <div class="detail-item">
            <span class="detail-icon">🏠</span>
            <span class="detail-text">1-3 комнатные квартиры</span>
          </div>
        </div>
        
        <div class="countdown-section">
          <h4>⏰ До конца акции осталось:</h4>
          <div class="countdown-timer">
            <div class="time-block">
              <span class="time-number">{{ days }}</span>
              <span class="time-label">дней</span>
            </div>
            <div class="time-separator">:</div>
            <div class="time-block">
              <span class="time-number">{{ hours }}</span>
              <span class="time-label">часов</span>
            </div>
            <div class="time-separator">:</div>
            <div class="time-block">
              <span class="time-number">{{ minutes }}</span>
              <span class="time-label">минут</span>
            </div>
            <div class="time-separator">:</div>
            <div class="time-block">
              <span class="time-number">{{ seconds }}</span>
              <span class="time-label">секунд</span>
            </div>
          </div>
        </div>
        
        <div class="promotion-actions">
          <button class="primary-btn" @click="viewPromotion">
            🏠 Посмотреть квартиры
          </button>
          <button class="secondary-btn" @click="contactDeveloper">
            📞 Связаться с застройщиком
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PromotionBlock',
  data() {
    return {
      days: 0,
      hours: 0,
      minutes: 0,
      seconds: 0,
      countdownInterval: null
    }
  },
  mounted() {
    this.startCountdown()
  },
  beforeUnmount() {
    if (this.countdownInterval) {
      clearInterval(this.countdownInterval)
    }
  },
  methods: {
    startCountdown() {
      // Устанавливаем дату окончания акции (7 дней от текущего момента)
      const endDate = new Date()
      endDate.setDate(endDate.getDate() + 7)
      endDate.setHours(23, 59, 59, 999)
      
      const updateCountdown = () => {
        const now = new Date().getTime()
        const distance = endDate.getTime() - now
        
        if (distance < 0) {
          // Акция закончилась
          this.days = 0
          this.hours = 0
          this.minutes = 0
          this.seconds = 0
          clearInterval(this.countdownInterval)
          return
        }
        
        this.days = Math.floor(distance / (1000 * 60 * 60 * 24))
        this.hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
        this.minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60))
        this.seconds = Math.floor((distance % (1000 * 60)) / 1000)
      }
      
      updateCountdown()
      this.countdownInterval = setInterval(updateCountdown, 1000)
    },
    
    viewPromotion() {
      // Переход к просмотру акции
      console.log('Просмотр акции')
      // Здесь можно добавить логику перехода к странице с квартирами
    },
    
    contactDeveloper() {
      // Связь с застройщиком
      console.log('Связь с застройщиком')
      // Здесь можно добавить логику для связи
    }
  }
}
</script>

<style scoped>
.promotion-block {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
  margin: 40px 0;
  position: relative;
  overflow: hidden;
}

.promotion-block::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #ff6b6b, #ffd93d, #6bcf7f, #4d9de0);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  position: relative;
}

.section-header h2 {
  margin: 0;
  color: white;
  font-size: 2.2rem;
  font-weight: 800;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.promotion-badge {
  background: linear-gradient(135deg, #ff6b6b, #ff8e53);
  padding: 8px 16px;
  border-radius: 20px;
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.badge-text {
  color: white;
  font-weight: 700;
  font-size: 0.9rem;
  letter-spacing: 1px;
}

.promotion-card {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.promotion-image {
  position: relative;
  overflow: hidden;
}

.promotion-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.promotion-card:hover .promotion-image img {
  transform: scale(1.05);
}

.image-overlay {
  position: absolute;
  top: 20px;
  right: 20px;
}

.discount-badge {
  background: linear-gradient(135deg, #ff6b6b, #ff8e53);
  color: white;
  padding: 12px 20px;
  border-radius: 25px;
  font-weight: 800;
  font-size: 1.2rem;
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
}

.promotion-content {
  padding: 40px;
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.promotion-title h3 {
  margin: 0 0 15px 0;
  color: #1a202c;
  font-size: 1.5rem;
  font-weight: 700;
  line-height: 1.3;
}

.promotion-description {
  color: #64748b;
  font-size: 1rem;
  line-height: 1.6;
  margin: 0;
}

.promotion-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 15px;
  background: rgba(102, 126, 234, 0.05);
  border-radius: 10px;
  transition: all 0.3s ease;
}

.detail-item:hover {
  background: rgba(102, 126, 234, 0.1);
  transform: translateX(5px);
}

.detail-icon {
  font-size: 1.2rem;
}

.detail-text {
  color: #1a202c;
  font-weight: 500;
}

.countdown-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 25px;
  border-radius: 15px;
  color: white;
}

.countdown-section h4 {
  margin: 0 0 20px 0;
  font-size: 1.1rem;
  font-weight: 600;
  text-align: center;
}

.countdown-timer {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
}

.time-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  min-width: 60px;
}

.time-number {
  font-size: 2rem;
  font-weight: 800;
  background: rgba(255, 255, 255, 0.2);
  padding: 10px 15px;
  border-radius: 10px;
  min-width: 50px;
  text-align: center;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.time-label {
  font-size: 0.8rem;
  font-weight: 500;
  opacity: 0.9;
}

.time-separator {
  font-size: 1.5rem;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.8);
  margin-top: -10px;
}

.promotion-actions {
  display: flex;
  gap: 15px;
  margin-top: auto;
}

.primary-btn, .secondary-btn {
  flex: 1;
  padding: 15px 25px;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.primary-btn {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.primary-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
}

.secondary-btn {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  border: 2px solid rgba(102, 126, 234, 0.3);
}

.secondary-btn:hover {
  background: rgba(102, 126, 234, 0.2);
  transform: translateY(-2px);
}

/* Адаптивность */
@media (max-width: 768px) {
  .promotion-block {
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
  
  .promotion-card {
    grid-template-columns: 1fr;
    gap: 0;
  }
  
  .promotion-image {
    height: 250px;
  }
  
  .promotion-content {
    padding: 30px 20px;
  }
  
  .countdown-timer {
    gap: 10px;
  }
  
  .time-block {
    min-width: 50px;
  }
  
  .time-number {
    font-size: 1.5rem;
    padding: 8px 12px;
  }
  
  .promotion-actions {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .promotion-block {
    padding: 20px 15px;
  }
  
  .section-header h2 {
    font-size: 1.5rem;
  }
  
  .promotion-content {
    padding: 20px 15px;
  }
  
  .countdown-timer {
    gap: 8px;
  }
  
  .time-block {
    min-width: 40px;
  }
  
  .time-number {
    font-size: 1.2rem;
    padding: 6px 10px;
  }
  
  .time-label {
    font-size: 0.7rem;
  }
}
</style> 