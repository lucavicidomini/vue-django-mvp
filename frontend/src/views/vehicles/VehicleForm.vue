<script setup lang="ts">
import { FuelType, type Vehicle, type VehicleScenario } from '@/stores/vehicle';
import { MFlex, MConfirmDialog, MButton, MNumberField, MSelect, MTextField, MBox } from '@m3ui-vue/m3ui-vue';
import { reactive, ref, type PropType } from 'vue';
import { useRouter } from 'vue-router';
import ScenarioList from './ScenarioList.vue';

const router = useRouter()

const props = defineProps({
  vehicle: {
    type: Object as PropType<Vehicle>,
    required: false,
  },
});
const emit = defineEmits(['delete', 'submit'])
const vehicle = props.vehicle ?? { id: 0, name: '', fuel_type: FuelType.EV, usable_battery: 0 } as Vehicle
const form = reactive<Vehicle>({ ... vehicle})
const open = ref(false)

const fuelTypes = Object.entries(FuelType)
  .filter(([, value]) => typeof value === 'number')
  .map(([key, value]) => ({ label: key, value }));

const onUpdateScenarios = async (scenarios: VehicleScenario[]) => {
  form.scenarios = scenarios
}

const onDelete = () => {
  open.value = false
  emit('delete')
}

</script>

<template>
  <MConfirmDialog
    v-model="open"
    title="Delete vehicle?"
    message="This action cannot be undone."
    :danger="true"
    confirm-label="Delete"
    @confirm="onDelete"
  />
  <MFlex direction="column" class="gap-3">
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
    <MBox surface="container" rounded="xl" class="p-4">
      <ScenarioList :scenarios="form.scenarios" @update="onUpdateScenarios"></ScenarioList>
    </MBox>
    <MFlex class="gap-3" >
      <MButton @click="router.back()" variant="outlined">Cancel</MButton>
      <MButton v-if="vehicle.id !== 0" @click="open = true" color="error">Delete</MButton>
      <MButton @click="$emit('submit', form)">Save</MButton>
    </MFlex>
  </MFlex>
</template>

<style scoped></style>
