<script setup lang="ts">
import { useRouter } from 'vue-router';
import { computed, h, onMounted, ref } from 'vue';
import { NConfigProvider, NGi, NGrid, NStatistic } from 'naive-ui';
import { fetchGetMonitorInfo } from '@/service/api';
import { $t } from '@/locales';
import { powerStatusRecord, trustStatusRecord } from '@/constants/business';

interface Props {
  id: string;
}

const props = defineProps<Props>();

const hostInfo = ref<Api.TrustManage.Monitor>();

const loading = ref<boolean>(false);

async function getMonitorInfo(mount: boolean) {
  loading.value = true;

  const { error, data } = await fetchGetMonitorInfo(Number(props.id));

  if (!error) {
    hostInfo.value = data;
    if (!mount) {
      window.$message?.success($t('common.refreshSuccess'));
    }
  } else if (!mount) {
    window.$message?.error($t('common.refreshFailed'));
  }

  loading.value = false;
}

onMounted(() => {
  getMonitorInfo(true);
});

const router = useRouter();

function navigateBack() {
  router.push({ name: 'trust-manage_monitor' });
}

const subtitle = computed(() => {
  if (hostInfo.value?.remark) {
    return `${hostInfo.value?.remark} -- `;
  }
  return '';
});

function createStyledStatistic(label: string, value: string, themeOverrides = {}) {
  // 默认主题覆盖
  const defaultThemeOverrides = {
    Statistic: {
      valueFontSize: '20px', // 默认字体大小
      ...themeOverrides // 合并传入的自定义样式
    }
  };

  return h(
    NConfigProvider,
    {
      themeOverrides: defaultThemeOverrides
    },
    () =>
      h(NStatistic, {
        label,
        value
      })
  );
}

const columns = [
  {
    render: () => {
      const powerStatus = hostInfo.value?.powerStatus;
      if (powerStatus === null || powerStatus === undefined) {
        return null;
      }

      return h(NStatistic, {
        label: $t('page.trust-manage.monitor.power-status'),
        value: $t(powerStatusRecord[powerStatus])
      });
    }
  },
  {
    render: () => {
      const trustStatus = hostInfo.value?.trustStatus;
      if (trustStatus === null || trustStatus === undefined) {
        return null;
      }

      return h(NStatistic, {
        label: $t('page.trust-manage.monitor.trust-status'),
        value: $t(trustStatusRecord[trustStatus])
      });
    }
  },
  {
    render: () =>
      h(NStatistic, {
        label: $t('page.trust-manage.monitor.certify-times'),
        value: hostInfo.value?.certifyTimes
      })
  },
  {
    render: () => {
      const label = $t('page.trust-manage.monitor.certify-time');
      const value = hostInfo.value?.certifyTime || '暂无';
      return createStyledStatistic(label, value);
    }
  },
  {
    render: () => {
      const label = $t('page.trust-manage.monitor.update-base-time');
      const value = hostInfo.value?.updateBaseTime || '暂无';
      return createStyledStatistic(label, value);
    }
  },
  {
    render: () => {
      const label = $t('page.trust-manage.monitor.logout-time');
      const value = hostInfo.value?.logoutTime || '暂无';
      return createStyledStatistic(label, value);
    }
  }
];
</script>

<template>
  <NCard :bordered="false" size="small" class="card-wrapper">
    <NSpin :show="loading">
      <NPageHeader @back="navigateBack">
        <template #header>{{ $t('route.trust-manage_monitor-detail') }}</template>
        <template #title>IP: {{ hostInfo?.ipAddress }}</template>
        <template #subtitle>
          {{ subtitle }} {{ $t('page.trust-manage.monitor.create-time') }} : {{ hostInfo?.createTime }}
        </template>
        <NGrid :cols="columns.length">
          <template v-for="column in columns" :key="column.key">
            <NGi>
              <component :is="column.render" />
            </NGi>
          </template>
        </NGrid>
        <!--
 <template #avatar>
        <NAvatar src="https://cdnimg103.lizhi.fm/user/2017/02/04/2583325032200238082_160x160.jpg" />
      </template>
-->

        <template #extra>
          <NSpace>
            <NButton size="small" @click="getMonitorInfo(false)">
              <template #icon>
                <icon-mdi-refresh class="text-icon" :class="{ 'animate-spin': loading }" />
              </template>
              {{ $t('common.refresh') }}
            </NButton>
          </NSpace>
        </template>

        <!-- <template #footer>{{ $t('page.trust-manage.monitor.create-time') }} : {{ hostInfo?.createTime }}</template> -->
      </NPageHeader>
    </NSpin>
  </NCard>
</template>

<style scoped></style>
