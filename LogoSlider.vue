<template>
  <div class="logo-slider-container">
    <div class="logo-track">
      <div
        v-for="(logo, index) in logos"
        :key="index"
        class="logo-item"
      >
        <img :src="logo" alt="Logo" />
      </div>
    </div>
  </div>
</template>

<script setup>
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
</script>

<style scoped>
.logo-slider-container {
  width: 100vw;
  margin-left: 50%;
  transform: translateX(-50%);
  overflow-x: auto;
  padding: 20px 0;
  white-space: nowrap;
  background: #fff;
}

.logo-track {
  display: flex;
  gap: 60px;
  align-items: center;
  width: 100%;
  min-width: max-content;
  transition: all 0.3s ease;
}

.logo-item {
  display: inline-block;
  transition: transform 0.3s ease;
}

.logo-item img {
  height: 50px;
  width: auto;
  transition: transform 0.3s ease;
}

.logo-item:hover img {
  transform: scale(1.2);
}
</style>
