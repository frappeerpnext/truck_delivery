import { createApp, reactive } from "vue";
import App from "./App.vue";
import "./assets/css/theme.css";
//core
import '/node_modules/primevue/resources/themes/bootstrap4-light-blue/theme.css'
import '/node_modules/primeflex/primeflex.css'
import 'primeicons/primeicons.css';
import router from './router';
import { FrappeApp } from "frappe-js-sdk"
import PrimeVue from 'primevue/config';
import Button from 'primevue/button';
import Dropdown from 'primevue/dropdown';
import AutoComplete from 'primevue/autocomplete';


const app = createApp(App);
const frappe = new FrappeApp()
// Plugins
app.use(router);
app.use(PrimeVue);


// Configure route gaurds
router.beforeEach(async (to, from, next) => {
	next();
});
app.use(frappe)
app.provide("$frappe", frappe);
app.component('Button', Button);
app.component('Dropdown', Dropdown);
app.component('AutoComplete', AutoComplete);
app.mount("#app");
