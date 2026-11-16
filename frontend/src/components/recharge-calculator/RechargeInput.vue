<script setup lang="ts">
import { MBox, MFlex, MSlider, MTextField } from '@m3ui-vue/m3ui-vue';
import { computed, ref, watch } from 'vue';

const props = defineProps({
  modelValue: {
    type: Object as () => [number, number],
    required: true
  }
});

const emit = defineEmits(['update:modelValue'])
const fromValue = ref(props.modelValue[0].toFixed(0))
const toValue = ref(props.modelValue[1].toFixed(0))
const fromError = ref(false)
const toError = ref(false)

const onUpdateFrom = (value: string) => {
  const numericValue = Number.parseInt(value)
  const clampedValue = Math.min(props.modelValue[1] - 1, Math.max(0, numericValue))
  if (numericValue === clampedValue) {
    emit('update:modelValue', [numericValue, props.modelValue[1]])
  } else {
    fromError.value = true
  }
}

const onUpdateTo = (value: string) => {
  const numericValue = Number.parseInt(value)
  const clampedValue = Math.min(100, Math.max(props.modelValue[0] + 1, numericValue))
  if (numericValue === clampedValue) {
    emit('update:modelValue', [props.modelValue[0], numericValue])
  } else {
    toError.value = true
  }
}

watch(() => props.modelValue, (newValue) => {
  fromValue.value = newValue[0].toFixed(0)
  toValue.value = newValue[1].toFixed(0)
  fromError.value = false
  toError.value = false
})

</script>

<template>
  <MBox
    :border="true"
    rounded="lg"
    padding="sm"
  >
    <MFlex
      gap="md"
      align="center"
    >
      <MTextField
        label="From"
        type="number"
        v-model="fromValue"
        @update:model-value="onUpdateFrom"
        :error="fromError"
      >
        <template #trailing>%</template>
      </MTextField>
      <MSlider
        :min="0"
        :max="100"
        :model-value="props.modelValue"
        variant="range"
        class="flex-grow"
        @update:model-value="$emit('update:modelValue', $event)"
      />
      <MTextField
        label="To"
        type="number"
        v-model="toValue"
        @update:model-value="onUpdateTo"
        :error="toError"
      >
        <template #trailing>%</template>
      </MTextField>
    </MFlex>
  </MBox>
</template>

<style scoped></style>
