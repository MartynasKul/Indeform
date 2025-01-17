<script lang="ts">
import { defineComponent, ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

export default defineComponent({
  setup() {
    const username = ref('')
    const password = ref('')
    const error = ref('')
    const authStore = useAuthStore()
    const router = useRouter()

    const handleLogin = async () => {
      try {
        const success = await authStore.login(username.value, password.value)
        if (success) {
          setTimeout(() => {
            router.push('/data')
          }, 100)
        } else {
          error.value = 'Prisijungimas nepavyko'
        }
      } catch (e) {
        error.value = 'Prisijungimas nepavyko'
        console.error(e)
      }
    }

    return { username, password, error, handleLogin }
  }
})
</script>

<template>
  <div class="p-4">
    <h2 class="text-xl mb-4">Prisijungimas</h2>
    <form @submit.prevent="handleLogin" class="space-y-4">
      <div>
        <input v-model="username" type="text" placeholder="Naudotojo vardas" class="border p-2 w-full" />
      </div>
      <div>
        <input v-model="password" type="password" placeholder="Slaptažodis" class="border p-2 w-full" />
      </div>
      <div v-if="error" class="text-red-500">{{ error }}</div>
      <button type="submit" class="bg-blue-500 text-white p-2 rounded">Prisijungti</button>
    </form>
  </div>
</template>