<script setup lang="ts">
import { FuelType, type Vehicle } from '@/stores/vehicle';
import { MButton, MNumberField, MSelect, MTextField } from '@m3ui-vue/m3ui-vue';
import { reactive, type PropType } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter()

defineEmits(['submit'])

const props = defineProps({
  vehicle: {
    type: Object as PropType<Vehicle>,
    required: false,
  },
});

const vehicle = props.vehicle ?? { id: 0, name: '', fuel_type: FuelType.EV, usable_battery: 0 } as Vehicle
const form = reactive<Vehicle>({ ... vehicle})

const fuelTypes = Object.entries(FuelType)
  .filter(([, value]) => typeof value === 'number')
  .map(([key, value]) => ({ label: key, value }));

</script>

<template>
  <MTextField
    v-model="form.name"
    label="Name"
    variant="outlined"
    :required="true"
  />
  <MSelect
    v-model="form.fuel_type"
    label="Fuel Type"
    variant="outlined"
    :options="fuelTypes"
    :required="true"
  />
  <MNumberField
    v-model="form.usable_battery"
    :label="form.fuel_type === FuelType.EV ? 'Usable Battery (kWh)' : 'Tank capacity (L)'" variant="outlined"
    :required="true"
    :stepper="false"
  />
  <MButton @click="router.back()">Cancel</MButton>
  <MButton @click="$emit('submit', form)">Save</MButton>
</template>

<style scoped></style>
