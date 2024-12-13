<script setup lang="tsx">
import MonitorDetailHeader from './modules/monitor-detail-header.vue';

interface Props {
  id: string;
}

defineProps<Props>();
</script>

<template>
  <div class="min-h-500px flex-col-stretch gap-16px overflow-hidden lt-sm:overflow-auto">
    <MonitorDetailHeader :id="id"></MonitorDetailHeader>
  </div>
</template>
