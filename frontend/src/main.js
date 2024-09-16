import {createApp} from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import { notification } from '@/utils/notification'
// import the package
import VueAwesomePaginate from "vue-awesome-paginate";

// import the necessary css file
import "vue-awesome-paginate/dist/style.css";

const app = createApp(App).use(VueAwesomePaginate)

app.config.globalProperties.$notification = notification

app.use(router)
app.use(store)
app.mount('#app')
