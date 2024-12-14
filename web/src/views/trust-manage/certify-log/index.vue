<script setup lang="tsx">
import { NTag } from 'naive-ui';
import { useAppStore } from '@/store/modules/app';
import { useTable, useTableOperate } from '@/hooks/common/table';
import { $t } from '@/locales';
import { trustStatusRecord } from '@/constants/business';
import { fetchGetCertifyLogList } from '@/service/api';
import CertifyLogSearch from './modules/certify-log-search.vue';
// import MonitorSearch from './modules/monitor-search.vue';
// import MonitorTableHeaderOperation from './modules/monitor-table-header-operation.vue';

const appStore = useAppStore();

const {
  columns,
  columnChecks,
  data,
  loading,
  getData,
  getDataByPage,
  mobilePagination,
  searchParams,
  resetSearchParams
} = useTable({
  apiFn: fetchGetCertifyLogList,
  apiParams: {
    current: 1,
    size: 10,
    // if you want to use the searchParams in Form, you need to define the following properties, and the value is null
    // the value can not be undefined, otherwise the property in Form will not be reactive
    ipAddress: null,
    logStatus: null,
    createBy: null
  },
  columns: () => [
    {
      type: 'selection',
      align: 'center',
      width: 48
    },
    {
      key: 'index',
      title: $t('common.index'),
      width: 64,
      align: 'center'
    },
    {
      key: 'ipAddress',
      title: $t('page.trust-manage.certify-log.ip'),
      align: 'center',
      minWidth: 120
    },
    {
      key: 'successNum',
      title: $t('page.trust-manage.certify-log.success-num'),
      align: 'center',
      minWidth: 80
    },
    {
      key: 'failedNum',
      title: $t('page.trust-manage.certify-log.failed-num'),
      align: 'center',
      minWidth: 100
    },
    {
      key: 'notVerifyNum',
      title: $t('page.trust-manage.certify-log.not-verify-num'),
      align: 'center',
      minWidth: 100
    },
    {
      key: 'createTime',
      title: $t('page.trust-manage.certify-log.create-at'),
      align: 'center',
      minWidth: 120
    },
    {
      key: 'createBy',
      title: $t('page.trust-manage.certify-log.create-by'),
      align: 'center',
      minWidth: 120
    },
    {
      key: 'logStatus',
      title: $t('page.trust-manage.certify-log.log-status'),
      align: 'center',
      width: 120,
      render: row => {
        if (row.logStatus === null) {
          return null;
        }

        const tagMap: Record<Api.Common.EnableStatus, NaiveUI.ThemeColor> = {
          '1': 'success',
          '2': 'error'
        };

        const label = $t(trustStatusRecord[row.logStatus]);

        return <NTag type={tagMap[row.logStatus]}>{label}</NTag>;
      }
    }
  ]
});

const {
  checkedRowKeys
  // closeDrawer
} = useTableOperate(data, getData);
</script>

<template>
  <div class="min-h-500px flex-col-stretch gap-16px overflow-hidden lt-sm:overflow-auto">
    <CertifyLogSearch v-model:model="searchParams" @reset="resetSearchParams" @search="getDataByPage" />
    <NCard
      :title="$t('page.trust-manage.certify-log.title')"
      :bordered="false"
      size="small"
      class="sm:flex-1-hidden card-wrapper"
    >
      <template #header-extra>
        <TableHeaderOperation
          v-model:columns="columnChecks"
          :hide-add="true"
          :hide-delete="true"
          :loading="loading"
          @refresh="getData"
        />
      </template>
      <NDataTable
        v-model:checked-row-keys="checkedRowKeys"
        :columns="columns"
        :data="data"
        size="small"
        :flex-height="!appStore.isMobile"
        :scroll-x="1000"
        :loading="loading"
        remote
        :row-key="row => row.id"
        :pagination="mobilePagination"
        class="sm:h-full"
      />
    </NCard>
  </div>
</template>

<style scoped></style>
