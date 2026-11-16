<script setup lang="ts">
import { FuelType, type Vehicle, type VehicleRechargeSpeed, type VehicleScenario } from '@/stores/vehicle';
import { MFlex, MConfirmDialog, MButton, MNumberField, MSelect, MTextField, MBox, MGrid } from '@m3ui-vue/m3ui-vue';
import { computed, reactive, ref, type PropType } from 'vue';
import { useRouter } from 'vue-router';
import ScenarioList from './ScenarioList.vue';
import RechargeSpeedList from './RechargeSpeedList.vue';
import type { Fuel } from '@/stores/fuel.ts';

const router = useRouter()

const props = defineProps({
  vehicle: {
    type: Object as PropType<Vehicle>,
    required: false,
  },
  fuels: {
    type: Array as PropType<Fuel[]>,
    required: false,
  },
});
const emit = defineEmits(['delete', 'submit'])
const vehicle = props.vehicle ?? { id: 0, name: '', fuel_type: FuelType.EV, usable_battery: 0 } as Vehicle
const form = reactive<Vehicle>({ ... vehicle})
const open = ref(false)

const fuelTypes = computed(() => (props.fuels ?? []).map(fuel => ({ label: fuel.name, value: fuel.id })))
const selectedFuel = computed(() => props.fuels?.find(fuel => fuel.id === form.fuel_type))
const consumptionUnit = computed(() => {
  const fuel = selectedFuel.value;
  if (!fuel?.unit) {
    return undefined;
  }
  return fuel.inverted ? `${fuel.unit}/100km` : `km/${fuel.unit}`
})

const onUpdateScenarios = (scenarios: VehicleScenario[]) => {
  form.scenarios = scenarios
}
const onUpdateRechargeSpeeds = (recharge_speeds: VehicleRechargeSpeed[]) => {
  form.recharge_speeds = recharge_speeds
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
    <MGrid :cols="1" :sm="2">
      <MBox surface="container" rounded="xl" class="p-4">
        <ScenarioList :scenarios="form.scenarios" :unit="consumptionUnit" @update="onUpdateScenarios"></ScenarioList>
      </MBox>
      <MBox surface="container" rounded="xl" class="p-4">
        <RechargeSpeedList :recharge_speeds="form.recharge_speeds" @update="onUpdateRechargeSpeeds"></RechargeSpeedList>
      </MBox>
    </MGrid>
    <MFlex class="gap-3" >
      <MButton @click="router.back()" variant="outlined">Cancel</MButton>
      <MButton v-if="vehicle.id !== 0" @click="open = true" color="error">Delete</MButton>
      <MButton @click="$emit('submit', form)">Save</MButton>
    </MFlex>
  </MFlex>
</template>

<style scoped></style>
