import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import authRoutes from './auth';

const routes = [
  { path: "/", redirect: '/scheme' }, 
  {
    path: "/scheme",
    name: "Home",
    component: Home,
  },
  ...authRoutes,
];

const router = createRouter({
  base: "/scheme/",
  history: createWebHistory(),
  routes,
});

export default router;
