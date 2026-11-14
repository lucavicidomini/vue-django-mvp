import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createM3UI } from '@m3ui-vue/m3ui-vue'

import App from './App.vue'
import router from './router'
import './main.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(createM3UI({ palette: 'teal' }))

app.mount('#app')
