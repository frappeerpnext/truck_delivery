import { createApp, reactive } from "vue";
import App from "./App.vue";
import "./assets/css/theme.css";
//core
import '/node_modules/primevue/resources/themes/bootstrap4-light-blue/theme.css'
import '/node_modules/primeflex/primeflex.css'
import 'primeicons/primeicons.css';
import router from './router';
import resourceManager from "../../../doppio/libs/resourceManager";
import call from "../../../doppio/libs/controllers/call";
import socket from "../../../doppio/libs/controllers/socket";
import Auth from "../../../doppio/libs/controllers/auth";
import { FrappeApp } from "frappe-js-sdk"
import PrimeVue from 'primevue/config';
import Button from 'primevue/button';
import Dropdown from 'primevue/dropdown';


const app = createApp(App);
const auth = reactive(new Auth());
const frappe = new FrappeApp()
// Plugins
app.use(router);
app.use(resourceManager);
app.use(PrimeVue);
app.provide("$auth", auth);
app.provide("$call", call);
app.provide("$socket", socket);


// Configure route gaurds
router.beforeEach(async (to, from, next) => {
	if (to.matched.some((record) => !record.meta.isLoginPage)) {
		// this route requires auth, check if logged in
		// if not, redirect to login page.
		if (!auth.isLoggedIn) {
			next({ name: 'Login', query: { route: to.path } });
		} else {
			next();
		}
	} else {
		if (auth.isLoggedIn) {
			next({ name: 'Home' });
		} else {
			next();
		}
	}
});
app.use(frappe)
app.provide("$frappe", frappe);
app.component('Button', Button);
app.component('Dropdown', Dropdown);
app.mount("#app");
