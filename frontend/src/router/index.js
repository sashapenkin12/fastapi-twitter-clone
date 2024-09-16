import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

const routes = [
  {
    path: '/',
    name: 'Home',
    meta: {
      label: 'Главная',
    },
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/login',
    name: 'Login',
    beforeEnter: loginGuardian,
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/profile/:profileId',
    name: 'Profile',
    component: () => import('@/views/Profile.vue')
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  store.commit('setMobileMenuState', false)
  const isLoggedIn = store.getters.getLoginStatus

  if(isLoggedIn === false){
    if(to.name !== 'Login'){
      next({path: '/login'})
    }
    else {
      next()
    }
  }
  else {
    if(to.name === 'Home' && from?.redirectedFrom?.name === 'Profile') {
      next({ name: 'Profile', params: { profileId: from?.redirectedFrom?.params?.profileId }});
      return;
    }
  
    next()
  }
})

function loginGuardian(to, from, next){
  const isLoggedIn = store.getters.getLoginStatus
  if(isLoggedIn){
    next(from)
  }else{
    next()
  }
}


export default router
