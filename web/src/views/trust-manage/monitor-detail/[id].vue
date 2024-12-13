<script setup lang="tsx">
import { NTag } from 'naive-ui';
import { useTable, useTableOperate } from '@/hooks/common/table';
import { fetchGetTrustLogList } from '@/service/api';
import { useAppStore } from '@/store/modules/app';
import { $t } from '@/locales';
import { trustLogStatusRecord } from '@/constants/business';
import MonitorDetailHeader from './modules/monitor-detail-header.vue';
import BaseLibrarySearch from './modules/base-library-search.vue';

interface Props {
  id: string;
}

const props = defineProps<Props>();

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
  apiFn: fetchGetTrustLogList,
  apiParams: {
    current: 1,
    size: 10,
    id: Number(props.id),
    // if you want to use the searchParams in Form, you need to define the following properties, and the value is null
    // the value can not be undefined, otherwise the property in Form will not be reactive
    path: null,
    logStatus: null,
    baseValue: null
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
      key: 'path',
      title: $t('page.trust-manage.base-library.path'),
      align: 'center',
      minWidth: 120
    },
    {
      key: 'pcr',
      title: $t('page.trust-manage.base-library.pcr'),
      align: 'center',
      width: 120,
      render: row => {
        return (
          <div class="flex flex-wrap justify-center gap-8px">
            {row.pcr.map(id => (
              <NTag type="info" size="small">
                {id}
              </NTag>
            ))}
          </div>
        );
      }
    },
    {
      key: 'baseValue',
      title: $t('page.trust-manage.base-library.base-value'),
      align: 'center',
      minWidth: 200
    },
    {
      key: 'verifyValue',
      title: $t('page.trust-manage.base-library.verify-value'),
      align: 'center',
      minWidth: 200
    },
    {
      key: 'logStatus',
      title: $t('page.trust-manage.base-library.log-status'),
      align: 'center',
      width: 80,
      render: row => {
        const tagMap: Record<Api.TrustManage.LogStatus, NaiveUI.ThemeColor> = {
          '1': 'warning',
          '2': 'success',
          '3': 'error'
        };

        const label = $t(trustLogStatusRecord[row.logStatus]);

        return <NTag type={tagMap[row.logStatus]}>{label}</NTag>;
      }
    },
    {
      key: 'updateTime',
      title: $t('page.trust-manage.base-library.update-time'),
      align: 'center',
      width: 200
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
    <MonitorDetailHeader :id="id"></MonitorDetailHeader>
    <BaseLibrarySearch v-model:model="searchParams" @reset="resetSearchParams" @search="getDataByPage" />
    <NCard
      :title="$t('page.trust-manage.base-library.title')"
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
