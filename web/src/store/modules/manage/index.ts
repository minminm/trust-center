import { defineStore } from 'pinia';
import { ref } from 'vue';
import { SetupStoreId } from '@/enum';
// import { useAuthStore } from '../auth';

import { getAllRoles } from './shared';

export const useManageRouteStore = defineStore(SetupStoreId.Manage, () => {
  // const authStore = useAuthStore();

  const allRoles = ref<Api.SystemManage.AllRole[]>([]);

  async function updateRoles() {
    allRoles.value = await getAllRoles();
  }

  return {
    allRoles,
    updateRoles
  };
});
