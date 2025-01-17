<script lang="ts">
import { defineComponent, ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

export default defineComponent({
  setup() {
    const username = ref('')
    const email = ref('')
    const password = ref('')
    const error = ref('')
    const authStore = useAuthStore()
    const router = useRouter()

    const handleRegister = async () => {
      const success = await authStore.register(username.value, email.value, password.value)
      if (success) {
        router.push('/login')
      } else {
        error.value = 'Registracija nepavyko'
      }
    }

    return { username, email, password, error, handleRegister }
  }
})
</script>

<template>
  <div class="p-4">
    <h2 class="text-xl mb-4">Registracija</h2>
    <form @submit.prevent="handleRegister" class="space-y-4">
      <div>
        <input v-model="username" type="text" placeholder="Naudotojo vardas" class="border p-2 w-full" />
      </div>
      <div>
        <input v-model="email" type="email" placeholder="E. paštas" class="border p-2 w-full" />
      </div>
      <div>
        <input v-model="password" type="password" placeholder="Slaptažodis" class="border p-2 w-full" />
      </div>
      <div v-if="error" class="text-red-500">{{ error }}</div>
      <button type="submit" class="bg-blue-500 text-white p-2 rounded">Registruotis</button>
    </form>
  </div>
</template>