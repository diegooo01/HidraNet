<script>
import axios from 'axios';

export default {
  data() {
    return {
      mapHtml: '',
      state: '',
      levelSelected: null,
      levels: [
          { name: 'Todos', id: '0' },
          { name: 'Alto', id: '1' },
          { name: 'Medio', id: '2' },
          { name: 'Bajo', id: '3' }
      ]
    };
  },
  methods: {
    async loadMap() {
        localStorage.removeItem('coordinates');
        this.state = 'loading';
        try {
          const response = await axios.get('http://127.0.0.1:5000/api/v1.0/nearHydrants_map');
          this.mapHtml = response.data;
          this.state = 'success';
          } catch (error) {
          this.state = 'error';
        }
    },
    async created_route() {
      var coordinates = JSON.parse(localStorage.getItem('coordinates'));
      var level = this.levelSelected;

      if (coordinates && level) {
        this.state = 'loading';
        var lat = coordinates.lat;
        var lng = coordinates.lng;
        console.log("Nivel de agua: " ,level);
        const url = `http://127.0.0.1:5000/api/v1.0/nearHydrants_map?lat=${lat}&lng=${lng}&level=${level}`;

        try {
          this.mapUrl = ''
          const response = await axios.get(url);
          this.mapHtml = response.data;
          this.state = 'success';
        } catch (error) {
          this.state = 'error';
        }
      } else {
        if(!coordinates) {alert("No se ha seleccionado una ubicación en el mapa")}
        if(!level) {alert("No se ha seleccionado un nivel de agua")}
      }
    },
  },
  mounted() {
      this.loadMap();
  }
};
</script>

<template>
  <div class="nearest-content">
    <h1>Los hidrantes más cercanos a ti...</h1>
    <p>Dale click a una zona del mapa del Callao para determinar <br> tu ubicación y darte la ruta más corta para el hidrante de la capacidad deseada y más cercano a ti.</p>
    <div class="index-hidrants">
      <p>Existen <span style="font-weight: bold; color: #4E171C">3 tipos</span> de hidrantes en el callo con 3 diferentes tipos de intensidad:</p>
      <div class="index-list">
        <div class="index-item">
          <img src="/public/map-icons/hidrant-icon-high-level.png" alt="Low level">
          <p>Hidrante de menor potencia</p>
        </div>
        <div class="index-item">
          <img src="/public/map-icons/hidrant-icon-mid-level.png" alt="Mid level">
          <p>Hidrante de media potencia</p>
        </div>
        <div class="index-item">
          <img src="/public/map-icons/hidrant-icon-low-level.png" alt="Low level">
          <p>Hidrante de mayor potencia</p>
        </div>
      </div>
    </div>
    <div class="map-visualizer">
      <div class="container-map">
        <div v-if="state == 'success' "class="activities">
          <pv-dropdown v-model="levelSelected" optionLabel="name" placeholder="Nivel de agua" :options="levels" optionValue="id"
          :inputStyle="{ color: '#4E171C'}" :pt = "{ itemLabel: {style: {color: 'inherit' }}}" />
          <div><button  class="button-calculate" @click="created_route">Calcular Ruta</button></div>
        </div>
        
        <div v-if="state == 'success'" class="nearHydrants-map" v-html="mapHtml"></div>
        
        <div class="loading-nearHydrants" v-if="state == 'loading'">
          <div class="spinner"></div>
          <p>Cargando mapa...</p>
        </div>
      </div>
    </div>
  </div>

</template>

<style>

.index-hidrants{
  padding: 1.2rem;
}

.index-list{
  display: flex;
  flex-direction: row;
  gap: 1.1rem;
}

.index-item img{
  width: 30px;
  height: 30px;
}


.index-item p{
  padding-bottom: 1rem;
}

.index-item{
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.7rem;
}

.nearest-content{
  padding: 5rem 2rem;
  justify-content: center;
  align-items: center;
  display: flex;
  flex-direction: column;
}

.nearest-content h1,.nearest-content p{
  color: #4E171C;
  text-align: center;
}

.nearest-content p{
  padding-top: 1.3rem;
}

.map-visualizer{
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 2rem;
}

.container-map{
  display: flex !important;
  position: relative !important;
  border: 3px solid #4e171c;
  border-radius: 5px;
  width: 90% !important;
  height: 540px !important;
}

.nearHydrants-map iframe,
.map-container .folium-map, 
.map-container > div{  
  width: 100% !important;
  height: 535px !important;
}


.nearHydrants-map{
  position: relative !important;
  width: 100% !important  ;
  height: 100% !important ;
}
.button-calculate{
  height: 100%;
  background-color: #4E171C;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  padding-inline: 1.5rem;
}

.loading-nearHydrants {
  position: absolute;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #4e171c;
  font-size: 1.2rem;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #4e171c;
  border-top: 5px solid transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}


.p-dropdown-item.p-highlight {
  background-color: #4e171c !important; 
  color: white !important;  
}

.p-dropdown-item	 {
  color: #4e171c !important;  
}

.p-dropdown-item.p-focus	 {
  background-color: #4e171c  !important;
  color: white !important;
}

.p-dropdown-trigger	 {
  color: #4e171c !important;
  background-color: #4e171c !important; 
  border-radius: 0px;
}

.p-dropdown{
  width: 200px;
  display: flex;
  border: 2px solid #4e171c !important;
  border-radius: 5px !important;
}

.p-dropdown.p-focus
.p-dropdown.p-overlay-open
.p-dropdown.p-highlight{
  outline: none !important; 
}

.activities{
  position: absolute;
  display: flex;
  flex-direction: row;
  align-items: stretch;
  gap: 1rem;
  z-index: 100;
  margin-top: 1rem;
  margin-left: 1rem;
}


@media(max-width: 830px) {

  .index-list{
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 0.2rem;
  }


  .activities{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap:0.5rem;
  }

  .activities button{
    width: 180px;
    height: 39px;
  }

  .container-map{
    width: 100%;
  }

  .nearest-content{
    padding: 5rem 0rem;
  }

  .p-dropdown{
    width: 180px;
    height: 39px;
    display: flex;
    border: 2px solid #4e171c !important;
    border-radius: 5px !important;

  }
}


</style>