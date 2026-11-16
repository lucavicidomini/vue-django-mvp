<script setup lang="ts">
import { MChip, MEmptyState, MTextField, MList, MListItem, MLoadingIndicator, MResult, MTitle, MFlex, MButton, MDialog, MGrid, useToast, MSegmentedButton, type SegmentedOption } from '@m3ui-vue/m3ui-vue';
import { FuelType, type Fuel } from '@/stores/fuel';
import { useMutation, useQueryClient } from '@tanstack/vue-query';
import { fuelApis, useFuelsQuery } from '@/services/fuels';
import { computed, ref } from 'vue';

const { data, isFetching, isError } = useFuelsQuery();

const { mutateAsync } = useMutation({
  mutationFn: (fuel: Fuel) => fuelApis.updateFuel(fuel),
})

const selectedFuel = ref<Fuel | null>(null)
const open = computed(() => !!selectedFuel.value)
const queryClient = useQueryClient()
const toast = useToast()

const invertedOptions = computed<SegmentedOption[]>(() => [
  { label: `km/${selectedFuel.value?.unit}`, value: '0' },
  { label: `${selectedFuel.value?.unit}/100km`, value: '1' },
]);

const saveselectedFuel = async () => {
  console.log(selectedFuel.value)
  const fuel = selectedFuel.value as Fuel;
  try {
    await mutateAsync(fuel)

    await queryClient.invalidateQueries({
      queryKey: ['fuels'],
    })

    toast.success('Fuel updated')
    selectedFuel.value = null
  } catch (error) {
    toast.error(
      error instanceof Error
        ? error.message
        : 'Unable to save the fuel',
    )
  }
}

</script>

<template>
    <MDialog v-model="open" title="Edit fuel" :closable="false">
      <MGrid v-if="selectedFuel" class="gap-4" :cols="2" :sm="1">
        <MTextField v-model="selectedFuel.name" required label="Name" />
        <MTextField v-model="selectedFuel.price" required label="Price" />
        <MTextField v-model="selectedFuel.unit" required label="Unit" />
        <MSegmentedButton
          :model-value="selectedFuel.inverted ? '1' : '0'"
          @update:model-value="selectedFuel.inverted = $event === '1'"
          :options="invertedOptions"
        ></MSegmentedButton>
      </MGrid>
      <template #actions>
        <MButton variant="text" @click="selectedFuel = null">Cancel</MButton>
        <MButton variant="text" @click="saveselectedFuel()">Save</MButton>
      </template>
    </MDialog>
  
  <MTitle>
    Fuels
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
    title="No fuels"
  >
  </MEmptyState>
  <MList
    v-else
    segmented
  >
    <template v-for="fuel in data" :key="fuel.id">
      <MListItem
        trailing-icon="chevron_right"
        @click="selectedFuel = {... fuel}"
      >
        <template #default>
          <div class="truncate text-body-large mb-1">
            {{ fuel.name }}
          </div>
          <MFlex>
            <MChip :icon="fuel.id === FuelType.EV ? 'battery_android_5' : 'humidity_low'">{{ fuel.price }} €/{{ fuel.unit }}</MChip>
          </MFlex>
        </template>
      </MListItem>
    </template>
  </MList>
</template>

<style scoped></style>
