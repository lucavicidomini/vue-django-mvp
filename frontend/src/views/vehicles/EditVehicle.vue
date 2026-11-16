<script setup lang="ts">
import { MEmptyState, MLoadingIndicator, MResult, MTitle, useToast } from '@m3ui-vue/m3ui-vue';
import { type Vehicle } from '@/stores/vehicle';
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query';
import { vehicleApis } from '@/services/vehicles';
import { useRoute, useRouter } from 'vue-router';

import VehicleForm from './VehicleForm.vue';
import { useFuelsQuery } from '@/services/fuels.ts';

const route = useRoute()
const router = useRouter()
const queryClient = useQueryClient()
const toast = useToast()

const vehicleId = Number(route.params.id)

const { data, isFetching } = useQuery({
  queryKey: ['vehicle', vehicleId],
  queryFn: () => vehicleApis.getVehicle(vehicleId),
})

const { data: fuels } = useFuelsQuery();

const { mutateAsync } = useMutation({
  mutationFn: (vehicle: Vehicle) => vehicleApis.updateVehicle(vehicle),
})

const { mutateAsync: deleteAsync } = useMutation({
  mutationFn: () => vehicleApis.deleteVehicle(vehicleId),
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

const onDelete = async () => {
  try {
    await deleteAsync()

    toast.success('Vehicle deleted')
    router.back()
    
    await queryClient.invalidateQueries({
      queryKey: ['vehicle', vehicleId],
    })
  } catch (error) {
    toast.error(
      error instanceof Error
        ? error.message
        : 'Unable to delete the vehicle',
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
  <MEmptyState
    v-else-if="!data"
    title="Vehicle not found"
  />
  <VehicleForm
    v-else
    :vehicle="data"
    :fuels="fuels"
    @submit="onSubmit"
    @delete="onDelete"
  />
</template>

<style scoped></style>
