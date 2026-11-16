<script setup lang="ts">
import { MChip, MEmptyState, MList, MListItem, MLoadingIndicator, MResult, MTitle, MFlex, MButton } from '@m3ui-vue/m3ui-vue';
import { FuelType } from '@/stores/vehicle';
import { useQuery } from '@tanstack/vue-query';
import { vehicleApis } from '@/services/vehicles';
import { useFabStore } from '@/stores/fab';
import { useRouter } from 'vue-router';
import { onMounted, onUnmounted } from 'vue';

const { data, isFetching, isError } = useQuery({
  queryKey: ['vehicles'],
  queryFn: vehicleApis.getVehicles,
});

const fab = useFabStore()
const router = useRouter()

onMounted(() => fab.setFab({
    icon: 'add',
    label: 'Add vehicle',
    action: () => router.push('/vehicles/new'),
  })
)

onUnmounted(() => fab.clearFab())
</script>

<template>
  <MTitle>
    Vehicles
  </MTitle>
  <MLoadingIndicator
    v-if="isFetching"
  />
  <MResult
    v-else-if="isError"
    status="error"
  >
  </MResult>
  <MEmptyState
    v-else-if="!data?.length"
    title="No vehicles"
  >
  </MEmptyState>
  <MList
    v-else
    segmented
  >
    <template v-for="vehicle in data" :key="vehicle.id">
      <MListItem
        trailing-icon="chevron_right"
        :to="`/vehicles/${vehicle.id}`"
      >
        <template #default>
          <div class="truncate text-body-large mb-1">
            {{ vehicle.name }}
          </div>
          <MFlex>
            <MChip v-if="vehicle.fuel_type === FuelType.EV" icon="battery_android_5">{{ vehicle.usable_battery }} kWh</MChip>
            <MChip v-else icon="humidity_low">{{ FuelType[vehicle.fuel_type] }}</MChip>
          </MFlex>
        </template>
      </MListItem>
    </template>
  </MList>
</template>

<style scoped></style>
