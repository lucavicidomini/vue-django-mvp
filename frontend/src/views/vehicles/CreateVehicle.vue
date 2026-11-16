<script setup lang="ts">
import { MTitle, MFlex, useToast } from '@m3ui-vue/m3ui-vue';
import { type Vehicle } from '@/stores/vehicle';
import { useMutation, useQueryClient } from '@tanstack/vue-query';
import { vehicleApis } from '@/services/vehicles';
import { useRouter } from 'vue-router';

import VehicleForm from './VehicleForm.vue';

const router = useRouter()
const queryClient = useQueryClient()
const toast = useToast()

const { mutateAsync } = useMutation({
  mutationFn: (vehicle: Vehicle) => vehicleApis.createVehicle(vehicle),
})

const onSubmit = async (model: Vehicle) => {
  try {
    await mutateAsync(model)

    await queryClient.invalidateQueries({
      queryKey: ['vehicle', model.id],
    })

    toast.success('Vehicle created')
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
  <MFlex justify="between">
    <MTitle>
      Add new vehicle
    </MTitle>
  </MFlex>
  <VehicleForm @submit="onSubmit"></VehicleForm>
</template>

<style scoped></style>
