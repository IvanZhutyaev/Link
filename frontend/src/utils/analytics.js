const API_BASE_URL = 'http://localhost:8000'

// Генерируем или получаем ID пользователя
const getUserId = () => {
  let userId = localStorage.getItem("user_id")
  if (!userId) {
    userId = crypto.randomUUID()
    localStorage.setItem("user_id", userId)
  }
  return userId
}

// Функция для отправки событий
const sendEvent = async (apartmentId, eventType, value = null) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/track-event`, {
      method: "POST",
      headers: { 
        "Content-Type": "application/json" 
      },
      body: JSON.stringify({
        apartment_id: apartmentId,
        user_id: getUserId(),
        event_type: eventType,
        event_value: value
      })
    })
    
    if (!response.ok) {
      console.error('Ошибка отправки аналитики:', response.status)
    }
  } catch (error) {
    console.error('Ошибка отправки аналитики:', error)
  }
}

// Функция для отслеживания времени на странице
const trackTimeOnPage = (apartmentId) => {
  const startTime = Date.now()
  
  const sendTimeEvent = () => {
    const duration = (Date.now() - startTime) / 1000
    sendEvent(apartmentId, "time_on_page", duration)
  }
  
  // Отправляем событие при уходе со страницы
  window.addEventListener("beforeunload", sendTimeEvent)
  
  // Отправляем событие при скрытии вкладки
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === 'hidden') {
      sendTimeEvent()
    }
  })
  
  return sendTimeEvent
}

// Функция для отслеживания просмотра квартиры
const trackApartmentView = (apartmentId) => {
  sendEvent(apartmentId, "view_apartment")
}

// Функция для отслеживания клика по 3D туру
const track3DTourClick = (apartmentId) => {
  sendEvent(apartmentId, "click_3d_tour")
}

// Функция для отслеживания клика по бронированию
const trackBookClick = (apartmentId) => {
  sendEvent(apartmentId, "click_book")
}

// Функция для отслеживания поиска
const trackSearch = (searchParams) => {
  // Используем ID 0 для общих событий поиска
  sendEvent(0, "search_property", Object.keys(searchParams).length)
}

// Функция для отслеживания применения фильтров
const trackFilterApplied = (filterCount) => {
  sendEvent(0, "filter_applied", filterCount)
}

// Функция для отслеживания клика по карте
const trackMapClick = (apartmentId) => {
  sendEvent(apartmentId, "click_map")
}

// Функция для отслеживания просмотра галереи
const trackGalleryView = (apartmentId) => {
  sendEvent(apartmentId, "view_gallery")
}

// Функция для отслеживания клика по контактам
const trackContactClick = (apartmentId) => {
  sendEvent(apartmentId, "click_contact")
}

// Функция для получения аналитики квартиры
const getApartmentAnalytics = async (apartmentId, days = 30) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/analytics/apartment/${apartmentId}?days=${days}`)
    if (response.ok) {
      return await response.json()
    }
  } catch (error) {
    console.error('Ошибка получения аналитики:', error)
  }
  return null
}

// Функция для получения общей аналитики
const getAnalyticsSummary = async (days = 30) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/analytics/summary?days=${days}`)
    if (response.ok) {
      return await response.json()
    }
  } catch (error) {
    console.error('Ошибка получения сводки аналитики:', error)
  }
  return null
}

// Функция для получения аналитики застройщика
const getDeveloperAnalytics = async (developerId, days = 30) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/analytics/developer/${developerId}?days=${days}`)
    if (response.ok) {
      return await response.json()
    }
  } catch (error) {
    console.error('Ошибка получения аналитики застройщика:', error)
  }
  return null
}

export default {
  sendEvent,
  trackTimeOnPage,
  trackApartmentView,
  track3DTourClick,
  trackBookClick,
  trackSearch,
  trackFilterApplied,
  trackMapClick,
  trackGalleryView,
  trackContactClick,
  getApartmentAnalytics,
  getAnalyticsSummary,
  getDeveloperAnalytics,
  getUserId
} 