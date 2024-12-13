<script setup lang="ts">
import { useRouter } from 'vue-router';

interface Props {
  id: string;
}

defineProps<Props>();

const router = useRouter();

function navigate() {
  router.push({ name: 'manage_user-detail', params: { id: '10' } });
}
</script>

<template>
  <div>
    <button @click="navigate">{{ id }}</button>
  </div>
</template>

<style scoped></style>
