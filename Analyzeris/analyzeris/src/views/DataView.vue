<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { PurchaseData } from '../types/types';
import WeeklyStats from './WeeklyStats.vue'

export default defineComponent({
  components:{
    WeeklyStats
  },
  setup() {
    const advertisements = ref<PurchaseData[]>([])
    const loading = ref(false)
    const error = ref('')
    const authStore = useAuthStore()
    const router = useRouter()

    const filters = ref({
      purchaseType: '',
      adType: '',
      created: '',
      deadline: ''
    })

    const fetchData = async () => {
      try {
        loading.value = true
        const response = await axios.get('http://localhost:8000/api/data/', {
          headers: {
            Authorization: `Bearer ${JSON.parse(localStorage.getItem('access_token'))}`,
            'Content-Type': 'application/json'
          }
        })
        advertisements.value = response.data
      } catch (err) {
        error.value = 'Nepavyko uzkrauti duomenu :('
        if (axios.isAxiosError(err) && err.response?.status === 401) {
          authStore.logout()
          router.push('/login')
        }
      } finally {
        loading.value = false
      }
    }

    const triggerScrape = async () => {
      try {
        loading.value = true

        await axios.post('http://localhost:8000/api/scrape/',
        {
          purchaseType: filters.value.purchaseType,
          adType: filters.value.adType,
          created: filters.value.created,
          deadline: filters.value.deadline
         },
          {
          headers: {
            Authorization: `Bearer ${JSON.parse(localStorage.getItem('access_token'))}`,
            'Content-Type': 'application/json'
          }
        }
      )
        // po skaitymo atnaujinama informacija
        await fetchData()
      } catch (err) {
        error.value = 'Nepavyko isgauti informacijos'
      } finally {
        loading.value = false
      }
    }

    onMounted(fetchData)

    return { advertisements, loading, error, filters, triggerScrape }
  }
})
</script>

<template>
  <div class="p-4">
    <!-- Statistika -->
    <div class="mt-8">
        <h2 class="text-xl font-semibold mb-4">Savaitinės statistikos</h2>
        <WeeklyStats :advertisements="advertisements" />
    </div>

    <div class="mb-4">
      <h2 class="text-xl mb-4">Pirkimų informacija</h2>
      <div class="flex gap-4 mb-4">
        <input 
          v-model="filters.adType" 
          placeholder="Skelbimo tipas" 
          class="border p-2"
        />
        <input 
          v-model="filters.purchaseType" 
          placeholder="BVPZ kodas" 
          class="border p-2"
        />
        <input 
          v-model="filters.created" 
          placeholder="Sukūrta (YYYY-MM-DD)" 
          class="border p-2"
        />
        <input 
          v-model="filters.deadline" 
          placeholder="Terminas (YYYY-MM-DD)" 
          class="border p-2"
        />
        <button 
          @click="triggerScrape"
          class="bg-blue-500 text-white p-2 rounded"
        >
          Filtruoti
        </button>
      </div>
    </div>

    <div v-if="loading" class="text-center">
      Kraunama...
    </div>
    <div v-else-if="error" class="text-red-500">
      {{ error }}
    </div>
    <div v-else class="grid gap-4">
      <div 
        v-for="ad in advertisements" 
        :key="ad.pavadinimas"
        class="border p-4 rounded"
      >
        <h3 class="font-bold">{{ ad.pavadinimas }}</h3>
        <p>Pirkėjas: {{ ad.vykdytojoPavadinimas }}</p>
        <p>BVPZ: {{ ad.bvpzKodas }}</p>
        <p>Skelbimo tipas: {{ ad.skelbimoTipas }}</p>
        <p>Sukūrta: {{ ad.data }}</p>
        <p>Terminas: {{ ad.terminas }}</p>
        <a :href="ad.nuoroda" target="_blank" class="text-blue-500">Peržiūrėti pirkėjo svetainę</a>
      </div>
    </div>
  </div>

  
  
</template>


