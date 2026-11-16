<script setup lang="ts">
import { type VehicleScenario } from '@/stores/vehicle';
import {  MButton, MSection, MTextField, MList, MListItem, MDialog, MGrid } from '@m3ui-vue/m3ui-vue';
import { computed, reactive, ref, watch, type PropType } from 'vue';

const props = defineProps({
  scenarios: {
    type: Array as PropType<VehicleScenario[]>,
    required: false,
  },
});

interface VehicleScenarioItem extends VehicleScenario {
    _key: number;
}

const emit = defineEmits(['update'])
const scenarios = (props.scenarios ?? [] as VehicleScenario[]).map((scenario, i) => ({ ...scenario, _key: i }))
const rows = reactive<VehicleScenarioItem[]>([ ... scenarios ])

const emptyScenario: () => VehicleScenarioItem = () => ({ _key: rows.length, id: 0, name: '', consumption: 0 })
const selectedScenario = ref<VehicleScenarioItem | null>(null)
const editScenario = (scenario: VehicleScenarioItem) => selectedScenario.value = ({ ...scenario })
const saveSelectedScenario = () => {
  const scenario = selectedScenario.value as VehicleScenarioItem;
  if (selectedScenario.value) {
    const index = rows.findIndex(r => r._key === scenario!._key)
    if (index !== -1) {
      rows[index] = { ...scenario }
    } else {
      rows.push({ ...scenario })
    }
    selectedScenario.value = null
    emit('update', [...rows])
  }
}
const deleteSelectedScenario = () => {
  if (selectedScenario.value) {
    const index = rows.findIndex(r => r._key === selectedScenario.value!._key)
    if (index !== -1) {
      rows.splice(index, 1)
    }
    selectedScenario.value = null
    emit('update', [...rows])
  }
}

const open = computed(() => !!selectedScenario.value)

</script>

<template>
  <MDialog v-model="open" title="Consumption scenario" :closable="false">
    <MGrid v-if="selectedScenario" class="gap-4" :cols="2" :sm="1">
      <MTextField v-model="selectedScenario.name" required label="Name" />
      <MTextField v-model="selectedScenario.consumption" required label="Consumption" />
    </MGrid>
    <template #actions>
      <MButton variant="text" @click="selectedScenario = null">Cancel</MButton>
      <MButton variant="text" color="error" @click="deleteSelectedScenario()">Delete</MButton>
      <MButton variant="text" @click="saveSelectedScenario()">Save</MButton>
    </template>
  </MDialog>

  <MSection
    gap="none"
    title="Consumption scenarios"
  >
    <template #actions>
      <MButton variant="text" size="sm" @click="selectedScenario = emptyScenario()">Add scenario</MButton>
    </template>

    <MList segmented>
      <MListItem
        v-for="scenario in rows"
        :key="scenario._key"
        :title="scenario.name"
        :subtitle="scenario.consumption?.toString()"
        @click="editScenario(scenario)"
        class="bg-surface-container-lowest"
      ></MListItem>
    </MList>
  </MSection>
  
</template>

<style scoped></style>
