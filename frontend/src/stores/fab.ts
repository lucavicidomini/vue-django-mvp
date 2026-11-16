import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useFabStore = defineStore('fab', () => {
  const isVisible = ref(false)
  const icon = ref('add')
  const label = ref('')
  const action = ref<(() => void) | null>(null)

  function setFab(config: {
    icon: string
    label?: string
    action: () => void
  }) {
    isVisible.value = true
    icon.value = config.icon
    label.value = config.label ?? ''
    action.value = config.action
  }

  function clearFab() {
    isVisible.value = false
    icon.value = 'add'
    label.value = ''
    action.value = null
  }

  return { isVisible, icon, label, action, setFab, clearFab }
})