import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import PrimeVue from "primevue/config";

import 'primevue/resources/primevue.min.css';
import 'primeicons/primeicons.css';
import 'primeflex/primeflex.css';
import 'primevue/resources/themes/saga-blue/theme.css'; 


import Toolbar from "primevue/toolbar";
import Sidebar from "primevue/sidebar";
import router from "./router/index.js";
import Dropdown from 'primevue/dropdown';



createApp(App)
    .use(router)
    .use(PrimeVue, {ripple: true})
    .component('pv-toolbar', Toolbar)
    .component('pv-sidebar', Sidebar)
    .component('pv-dropdown', Dropdown)
    .mount('#app')

