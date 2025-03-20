<script>
import axios from 'axios';

export default {
  data() {
    return {
      mapHtml: '',
      state: '',
      cost: ''
    };
  },
  methods: {
    async loadMap() {
        this.state = "loading"
        try {
          const response = await axios.get('http://127.0.0.1:5000/api/v1.0/hydrants_map');
          var res = response.data;
          this.mapHtml = res.map;
          this.cost = (res.cost / 1000).toFixed(4);
          this.state = "success"
        } catch (error) {
          this.message = "error"
        }
      },
    reloadMap() {
      this.loadMap();
    }

  },
  mounted() {
      this.loadMap();
  }
};
</script>

<template>
  <div class="hidrants-net-content">
    <h1>Red de Hidrantes del Callao</h1>
    <p>Visualiza la Red óptima de hidrantes para su correcto mantenimiento. Con esta red <br> se tendrá un mantenimiento mucho más eficiente y exitoso de los hidrantes de la ciudad del Callao.</p>
    <div class="map-visualizer">
      <div class="container-map">

            <div v-if="state == 'success'" class="redHydrants-map" v-html="mapHtml"></div> 

            <div class="loading-redHydrants" v-if="state == 'loading'">
              <div class="spinner"></div>
              <p>Cargando mapa...</p>
            </div>
      </div>
      <h1 v-if="state == 'success'" class="total_cost">El costo total de la red de hidrantes en kilómetros es: {{cost}} </h1>
      <button v-if="state == 'success'" class="button-reload" @click="reloadMap">Actualizar Mapa</button>

    </div>
  </div>
</template>

<style>

.hidrants-net-content{
  padding: 5rem 2rem;
  justify-content: center;
  align-items: center;
  display: flex;
  flex-direction: column;
}

.hidrants-net-content h1,.hidrants-net-content p{
  color: #4E171C;
  text-align: center;
}

.hidrants-net-content p{
  padding-top: 1.5rem;
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

.total_cost{
  padding-top: 2.5rem;
  font-size: 1.8rem;
}

.redHydrants-map iframe,
.map-container .folium-map, 
.map-container > div{  
  width: 100% !important;
  height: 535px !important;
}

.redHydrants-map{
  position: relative !important;
  width: 100% !important  ;
  height: 100% !important ;
}

.button-reload{
  background-color: #4E171C;
  color: white;
  padding: 0.8rem 2rem;
  border: none;
  border-radius: 30px;
  cursor: pointer;
  margin-top: 1rem;
  font-size: 1.1rem;
  align-items: center;
}

.loading-redHydrants {
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

@media(max-width: 768px){
  .container-map{
    width: 100%;
  }

  .hidrants-net-content{
    padding: 5rem 0rem;
  }
}

</style>