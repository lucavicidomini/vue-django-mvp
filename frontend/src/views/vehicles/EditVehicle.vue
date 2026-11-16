<script setup lang="ts">
import { MEmptyState, MLoadingIndicator, MResult, MTitle, useToast } from '@m3ui-vue/m3ui-vue';
import { type Vehicle } from '@/stores/vehicle';
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query';
import { vehicleApis } from '@/services/vehicles';
import { useRoute, useRouter } from 'vue-router';

import VehicleForm from './VehicleForm.vue';

const route = useRoute()
const router = useRouter()
const queryClient = useQueryClient()
const toast = useToast()

const vehicleId = Number(route.params.id)

const { data, isFetching } = useQuery({
  queryKey: ['vehicle', vehicleId],
  queryFn: () => vehicleApis.getVehicle(vehicleId),
})

const { isError, mutateAsync } = useMutation({
  mutationFn: (vehicle: Vehicle) => vehicleApis.updateVehicle(vehicle),
})

const onSubmit = async (model: Vehicle) => {
  try {
    await mutateAsync(model)

    await queryClient.invalidateQueries({
      queryKey: ['vehicle', model.id],
    })

    toast.success('Vehicle updated')
    router.back()
  } catch (error) {
    toast.error(
      error instanceof Error
        ? error.message
        : 'Unable to save the vehicle',
    )
  }
}
</script>

<template>
  <MTitle>
    Edit {{ data?.name }}
  </MTitle>
  <MLoadingIndicator
    v-if="isFetching"
  />
  <MResult
    v-else-if="isError"
    status="error"
  />
  <MEmptyState
    v-else-if="!data"
    title="Vehicle not found"
  />
  <VehicleForm
    v-else
    :vehicle="data"
    @submit="onSubmit"
  />
</template>

<style scoped></style>
