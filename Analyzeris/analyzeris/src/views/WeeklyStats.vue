<script lang="ts">
import { defineComponent, computed, PropType } from 'vue'
import { Line } from 'vue-chartjs'
import { PurchaseData } from '../types/types'

import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js'

// Register ChartJS components
ChartJS.register( CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend )

export default defineComponent({
  name: 'WeeklyStats',
  components: {
    Line
  },
  props: {
    advertisements: {
      type: Array as PropType<PurchaseData[]>,
      required: true
    }
  },
  setup(props) {
    // duomenu apdorojimas statiskikai isgauti
    const weeklyData = computed(() => {
      const countsByWeek = new Map<string, number>();
      
      props.advertisements.forEach(ad => {
        if (ad.data) {
          // savaites pradzios dienos gavimas
          const date = new Date(ad.data);
          date.setHours(0, 0, 0, 0);
          date.setDate(date.getDate() - date.getDay()); // nustatoma savaites pradzia
          const weekKey = date.toISOString().split('T')[0];
          
          countsByWeek.set(weekKey, (countsByWeek.get(weekKey) || 0) + 1);
        }
      });

      // pakeiciam i surikiuota masyva
      return Array.from(countsByWeek.entries())
        .sort(([a], [b]) => a.localeCompare(b))
        .map(([week, count]) => ({ week, count }));
    });

    const chartData = computed(() => ({
      labels: weeklyData.value.map(item => item.week),
      datasets: [
        {
          label: 'Skelbimų per savaitę',
          data: weeklyData.value.map(item => item.count),
          borderColor: '#2563eb',
          backgroundColor: 'rgba(37, 99, 235, 0.2)',
          tension: 0.4,
          fill: true
        }
      ]
    }));

    const chartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top' as const,
        },
        title: {
          display: true,
          text: 'Savaitinė skelbimų statistika'
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Skelbimų kiekis'
          }
        },
        x: {
          title: {
            display: true,
            text: 'Savaitė'
          }
        }
      }
    };

    return {
      chartData,
      chartOptions
    };
  }
});
</script>

<template>
  <div class="p-4 bg-white rounded-lg shadow">
    <div class="h-64">
      <Line
        :data="chartData"
        :options="chartOptions"
      />
    </div>
  </div>
</template>