<template>
  <div>
    <button id="assistant-toggle" @click="toggleChat">💬</button>
    <div id="chat-container" :style="{display: chatVisible ? 'flex' : 'none'}">
      <div id="chat-header">
        <h3>🤖 ИИ-Риэлтор</h3>
        <div id="customVoiceIndicator" ref="voiceIndicator"></div>
        <button id="stopAudioBtn" @click="stopCurrentAudio" :style="{display: currentAudio ? 'inline-block' : 'none'}">⏹️</button>
      </div>
      <div id="chat-window" ref="chatWindow"></div>
      <input id="userInput" v-model="userInput" @keyup.enter="askAI" placeholder="Например: Квартира до 6 млн в центре" />
      <button class="ask-button" @click="askAI">Спросить</button>
      <div class="quick-actions">
        <button @click="quickAction('Найди квартиры в Краснодаре до 5 миллионов рублей')" class="quick-btn">
          🏠 Поиск жилья
        </button>
        <button @click="quickAction('Проанализируй выгоду покупки квартиры в Краснодаре')" class="quick-btn">
          📊 Анализ выгоды
        </button>
        <button @click="quickAction('Дай инвестиционные советы по недвижимости')" class="quick-btn">
          💰 Инвестиции
        </button>
        <button @click="quickAction('Какие документы нужны для покупки квартиры?')" class="quick-btn">
          📋 Документы
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChatAssistant',
  data() {
    return {
      chatVisible: false,
      userInput: '',
      currentAudio: null,
      systemPrompt: `Ты —девушка ,опытный риэлтор-консультант с многолетним опытом. У тебя есть база данных с информацией о квартирах и ЖК. Твои функции:\n\n🏠 ПОИСК НЕДВИЖИМОСТИ: Подбирай жильё по параметрам, используя только данные из базы\n\n📊 АНАЛИЗ ВЫГОДЫ: Рассчитывай стоимость кв.м, сравнивай цены, анализируй соотношение цена/качество, оценивай перспективы роста стоимости\n\n💰 ИНВЕСТИЦИОННЫЕ СОВЕТЫ: Определяй ликвидность, анализируй потенциал аренды, оценивай риски и доходность, рекомендуй стратегии\n\n📋 ПОМОЩЬ С ДОКУМЕНТАМИ: Объясняй необходимые документы, порядок оформления, налоги, ипотечные программы, юридические вопросы\n\n🏠 ПОЛНЫЙ КОНСАЛТИНГ: Помогай с выбором района, планировкой, особенностями застройщиков, планированием бюджета\n\nОтвечай ТОЛЬКО на основе предоставленных данных. Если подходящих вариантов нет - честно говори об этом. Давай практические советы и конкретные рекомендации!`,
    };
  },
  methods: {
    toggleChat() {
      this.chatVisible = !this.chatVisible;
      this.$nextTick(() => {
        if (this.chatVisible) {
          this.scrollToBottom();
        }
      });
    },
    async askAI() {
      const userInput = this.userInput.trim();
      if (!userInput) return;
      this.stopCurrentAudio();
      this.addMessage(userInput, 'user');
      this.userInput = '';
      try {
        const response = await fetch('/api/ask', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            system: this.systemPrompt,
            user: userInput
          })
        });
        const data = await response.json();
        if (data.error) {
          this.addMessage(`Ошибка: ${data.error}`, 'bot');
          return;
        }
        if (data.answer) {
          this.addMessage(data.answer, 'bot');
          if (data.audio) {
            this.playAudio(data.audio, data.audioUrl);
          }
        }
      } catch (error) {
        this.addMessage('Извините, произошла ошибка. Попробуйте еще раз.', 'bot');
      }
    },
    async quickAction(prompt) {
      this.userInput = prompt;
      await this.askAI();
    },
    addMessage(text, sender) {
      const chatWindow = this.$refs.chatWindow;
      const bubble = document.createElement('div');
      bubble.className = `chat-bubble ${sender}`;
      bubble.innerText = text;
      chatWindow.appendChild(bubble);
      this.scrollToBottom();
    },
    scrollToBottom() {
      const chatWindow = this.$refs.chatWindow;
      chatWindow.scrollTop = chatWindow.scrollHeight;
    },
    stopCurrentAudio() {
      if (this.currentAudio) {
        this.currentAudio.pause();
        this.currentAudio.currentTime = 0;
        this.currentAudio = null;
        this.$refs.voiceIndicator.innerHTML = '';
      }
    },
    playAudio(audioBase64, audioUrl = null) {
      this.stopCurrentAudio();
      let audioSource;
      if (audioUrl) {
        audioSource = audioUrl;
      } else {
        audioSource = `data:audio/mp3;base64,${audioBase64}`;
      }
      this.currentAudio = new Audio(audioSource);
      this.showVoiceWaves();
      this.currentAudio.play().then(() => {}).catch(() => {
        this.$refs.voiceIndicator.innerHTML = '';
        this.currentAudio = null;
      });
      this.currentAudio.onended = () => {
        this.$refs.voiceIndicator.innerHTML = '';
        this.currentAudio = null;
      };
      this.currentAudio.onerror = () => {
        if (audioUrl && audioBase64) {
          this.playAudio(audioBase64);
        } else {
          this.$refs.voiceIndicator.innerHTML = '';
          this.currentAudio = null;
        }
      };
    },
    showVoiceWaves() {
      this.$refs.voiceIndicator.innerHTML = `
        <div class="wave"></div>
        <div class="wave"></div>
        <div class="wave"></div>
        <div class="wave"></div>
      `;
    }
  }
}
</script>

<style scoped>
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background: #020a12;
}
#assistant-toggle {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #007aff;
  color: white;
  border: none;
  border-radius: 50%;
  width: 60px;
  height: 60px;
  font-size: 28px;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
  z-index: 1000;
}
#chat-container {
  position: fixed;
  bottom: 100px;
  right: 20px;
  width: 360px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.15);
  padding: 16px;
  z-index: 999;
  display: flex;
  flex-direction: column;
  max-height: 80vh;
}
#chat-header {
  background: #f8f9fa;
  padding: 15px;
  border-bottom: 1px solid #e9ecef;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
#chat-header h3 {
  margin: 0;
  font-size: 16px;
}
#customVoiceIndicator {
  width: 32px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2px;
}
.wave {
  display: inline-block;
  width: 3px;
  height: 16px;
  background: linear-gradient(180deg, #007aff 0%, #0056b3 100%);
  border-radius: 2px;
  animation: wave 1.5s infinite ease-in-out;
  box-shadow: 0 0 4px rgba(0, 122, 255, 0.3);
}
.wave:nth-child(1) { 
  animation-delay: -1.2s; 
  height: 12px;
}
.wave:nth-child(2) { 
  animation-delay: -0.8s; 
  height: 18px;
}
.wave:nth-child(3) { 
  animation-delay: -0.4s; 
  height: 14px;
}
.wave:nth-child(4) { 
  animation-delay: 0s; 
  height: 16px;
}
@keyframes wave {
  0%, 100% { 
    transform: scaleY(0.3); 
    opacity: 1;
  }
  50% { 
    transform: scaleY(1); 
    opacity: 1;
  }
}
#chat-window {
  flex-grow: 1;
  overflow-y: auto;
  padding-right: 4px;
  margin-bottom: 12px;
}
.chat-bubble,
.chat-bubble * {
  color: #111 !important;
  font-weight: 600 !important;
}
.chat-bubble.user {
  background: #007aff;
  color: white;
  align-self: flex-end;
  border-bottom-right-radius: 0;
  font-weight: 500;
}
.chat-bubble.bot {
  background: #f8f9fa;
  color: #000000;
  align-self: flex-start;
  border-bottom-left-radius: 0;
  font-weight: 500;
  border: 1px solid #e9ecef;
}
input, button {
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 14px;
}
#userInput {
  width: 80%;
  margin-bottom: 8px;
}
button.ask-button {
  width: 100%;
  background: #007aff;
  color: white;
  border: none;
  font-weight: bold;
  cursor: pointer;
}
.ask-button:hover {
  background-color: #0056b3;
}
.quick-actions {
  display: flex;
  gap: 10px;
  margin: 15px 0;
  flex-wrap: wrap;
  justify-content: center;
}
.quick-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
.quick-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}
.quick-btn:active {
  transform: translateY(0);
}
@media (max-width: 768px) {
  .quick-actions {
    flex-direction: column;
    align-items: center;
  }
  .quick-btn {
    width: 100%;
    max-width: 300px;
  }
}
#stopAudioBtn {
  background: #ff4444 !important;
  color: white !important;
  border: none !important;
  border-radius: 50% !important;
  width: 30px !important;
  height: 30px !important;
  cursor: pointer !important;
  font-size: 12px !important;
  transition: all 0.3s ease !important;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2) !important;
}
#stopAudioBtn:hover {
  background: #cc0000 !important;
  transform: scale(1.1) !important;
}
</style> 