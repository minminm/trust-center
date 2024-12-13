<script setup lang="ts">
import { useRouter } from 'vue-router';
import { h, onMounted, ref } from 'vue';
import { NGi, NGrid, NStatistic } from 'naive-ui';
import { fetchGetMonitorInfo } from '@/service/api';
import { $t } from '@/locales';
import { powerStatusRecord, trustStatusRecord } from '@/constants/business';

interface Props {
  id: string;
}

const props = defineProps<Props>();

const hostInfo = ref<Api.TrustManage.Monitor>();

onMounted(async () => {
  const { error, data } = await fetchGetMonitorInfo(Number(props.id));

  if (!error) {
    hostInfo.value = data;

    console.log(hostInfo.value);
  }
});

const router = useRouter();

function navigateBack() {
  router.push({ name: 'trust-manage_monitor' });
}

// const gridData = [
//   { label: $t('page.trust-manage.monitor.form.ipAddress'), value: hostInfo.value?.ipAddress },
//   { label: $t('page.trust-manage.monitor.power-status'), value: hostInfo.value?.powerStatus }
// ];

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
        label: $t('page.trust-manage.monitor.logout-time'),
        value: hostInfo.value?.logoutTime || '暂无'
      })
  },
  {
    render: () =>
      h(NStatistic, {
        label: $t('page.trust-manage.monitor.certify-time'),
        value: hostInfo.value?.certifyTime || '暂无'
      })
  },
  {
    render: () =>
      h(NStatistic, {
        label: $t('page.trust-manage.monitor.update-base-time'),
        value: hostInfo.value?.updateBaseTime || '暂无'
      })
  }
];
</script>

<template>
  <NCard :bordered="false" size="small" class="card-wrapper">
    <NPageHeader @back="navigateBack">
      <template #header>{{ $t('route.trust-manage_monitor-detail') }}</template>
      <template #title>IP: {{ hostInfo?.ipAddress }}</template>
      <template #subtitle>{{ hostInfo?.remark }}</template>
      <NGrid :cols="columns.length">
        <template v-for="column in columns" :key="column.key">
          <NGi>
            <component :is="column.render" />
          </NGi>
        </template>
      </NGrid>
      <!--
 <NGrid :cols="gridData.length">
        <NGi>
          <NStatistic label="正片" value="125 集" />
        </NGi>
        <NGi>
          <NStatistic label="嘉宾" value="22 位" />
        </NGi>
        <NGi>
          <NStatistic label="道歉" value="36 次" />
        </NGi>
        <NGi>
          <NStatistic label="话题" value="83 个" />
        </NGi>
        <NGi>
          <NStatistic label="参考链接" value="2,346 个" />
        </NGi>
      </NGrid>
-->
      <!--
 <template #avatar>
        <NAvatar src="https://cdnimg103.lizhi.fm/user/2017/02/04/2583325032200238082_160x160.jpg" />
      </template>
-->
      <!--
 <template #extra>
      <NSpace>
        <NButton>催更</NButton>
        <NDropdown :options="options" placement="bottom-start">
          <NButton :bordered="false" style="padding: 0 4px">···</NButton>
        </NDropdown>
      </NSpace>
    </template>
-->
      <template #footer>{{ $t('page.trust-manage.monitor.create-time') }} : {{ hostInfo?.createTime }}</template>
    </NPageHeader>
  </NCard>
</template>

<style scoped></style>
