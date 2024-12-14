<script setup lang="tsx">
import { NButton, NPopconfirm, NTag } from 'naive-ui';
import { useRouter } from 'vue-router';
import { useAppStore } from '@/store/modules/app';
import { useTable, useTableOperate } from '@/hooks/common/table';
import { $t } from '@/locales';
import { powerStatusRecord, trustStatusRecord } from '@/constants/business';
import {
  batchCertify,
  batchPowerOff,
  batchPowerOn,
  batchUpdateBase,
  certify,
  fetchGetMonitorList,
  powerOff,
  powerOn,
  updateBase
} from '@/service/api';
import MonitorSearch from './modules/monitor-search.vue';
import MonitorTableHeaderOperation from './modules/monitor-table-header-operation.vue';

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
  apiFn: fetchGetMonitorList,
  apiParams: {
    current: 1,
    size: 10,
    // if you want to use the searchParams in Form, you need to define the following properties, and the value is null
    // the value can not be undefined, otherwise the property in Form will not be reactive
    ipAddress: null,
    powerStatus: null,
    trustStatus: null,
    remark: null
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
      title: $t('page.trust-manage.monitor.ip'),
      align: 'center',
      minWidth: 120
    },
    {
      key: 'remark',
      title: $t('page.trust-manage.monitor.remark'),
      align: 'center',
      minWidth: 80
    },
    {
      key: 'powerStatus',
      title: $t('page.trust-manage.monitor.power-status'),
      align: 'center',
      width: 100,
      render: row => {
        if (row.powerStatus === null) {
          return null;
        }

        const tagMap: Record<Api.Common.EnableStatus, NaiveUI.ThemeColor> = {
          '1': 'success',
          '2': 'warning'
        };

        const label = $t(powerStatusRecord[row.powerStatus]);

        return <NTag type={tagMap[row.powerStatus]}>{label}</NTag>;
      }
    },
    {
      key: 'trustStatus',
      title: $t('page.trust-manage.monitor.trust-status'),
      align: 'center',
      width: 100,
      render: row => {
        if (row.trustStatus === null) {
          return null;
        }

        const tagMap: Record<Api.Common.EnableStatus, NaiveUI.ThemeColor> = {
          '1': 'success',
          '2': 'error'
        };

        const label = $t(trustStatusRecord[row.trustStatus]);

        return <NTag type={tagMap[row.trustStatus]}>{label}</NTag>;
      }
    },
    {
      key: 'createTime',
      title: $t('page.trust-manage.monitor.create-time'),
      align: 'center',
      minWidth: 120
    },
    {
      key: 'logoutTime',
      title: $t('page.trust-manage.monitor.logout-time'),
      align: 'center',
      minWidth: 120
    },
    {
      key: 'operate',
      title: $t('page.trust-manage.monitor.trust-control'),
      align: 'center',
      width: 150,
      render: row => (
        <div class="flex-center gap-8px">
          {row.powerStatus === '1' ? (
            <>
              {/* 重启按钮 */}
              <NPopconfirm onPositiveClick={() => handlePower(row.id, 'reboot')}>
                {{
                  default: () => $t('page.trust-manage.monitor.op.confirm-reboot'),
                  trigger: () => (
                    <NButton type="warning" strong secondary size="medium">
                      {$t('page.trust-manage.monitor.op.power-reboot')}
                    </NButton>
                  )
                }}
              </NPopconfirm>

              {/* 断电按钮 */}
              <NPopconfirm onPositiveClick={() => handlePower(row.id, 'off')}>
                {{
                  default: () => $t('page.trust-manage.monitor.op.confirm-off'),
                  trigger: () => (
                    <NButton type="error" strong secondary size="medium">
                      {$t('page.trust-manage.monitor.op.power-off')}
                    </NButton>
                  )
                }}
              </NPopconfirm>
            </>
          ) : (
            <>
              {/* 上电按钮 */}
              <NButton type="primary" strong secondary size="medium" onClick={() => handlePower(row.id, 'on')}>
                {$t('page.trust-manage.monitor.op.power-on')}
              </NButton>
            </>
          )}
        </div>
      )
    },
    {
      key: 'operate2',
      title: $t('page.trust-manage.monitor.trust-certify'),
      align: 'center',
      width: 220,
      render: row => (
        <div class="flex-center gap-8px">
          <NButton type="info" tertiary size="small" onClick={() => handleCertify(row.id)}>
            {$t('page.trust-manage.monitor.op.certify')}
          </NButton>
          <NPopconfirm onPositiveClick={() => handleUpdateBase(row.id)}>
            {{
              default: () => $t('page.trust-manage.monitor.op.confirm-update-base'),
              trigger: () => (
                <NButton type="error" tertiary size="small">
                  {$t('page.trust-manage.monitor.op.update-base')}
                </NButton>
              )
            }}
          </NPopconfirm>
        </div>
      )
    },
    {
      key: 'operate3',
      title: $t('common.otherAction'),
      align: 'center',
      width: 100,
      render: row => (
        <NButton type="info" text onClick={() => navigateToDetail(row.id)}>
          {$t('page.trust-manage.monitor.detail')}
        </NButton>
      )
    }
  ]
});

const router = useRouter();

function navigateToDetail(id: number) {
  router.push({ name: 'trust-manage_monitor-detail', params: { id } });
}

const {
  checkedRowKeys
  // closeDrawer
} = useTableOperate(data, getData);

async function handlePower(id: number, op: Api.TrustManage.PowerOperator) {
  const apiFn = op === 'off' ? powerOff : powerOn;
  let successI18nKey: App.I18n.I18nKey;
  switch (op) {
    case 'on':
      successI18nKey = 'page.trust-manage.monitor.op.power-on-success';
      break;
    case 'reboot':
      successI18nKey = 'page.trust-manage.monitor.op.reboot-success';
      break;
    default:
      successI18nKey = 'page.trust-manage.monitor.op.power-off-success';
      break;
  }

  const { error } = await apiFn(id);

  if (!error) {
    window.$message?.success($t(successI18nKey));
    await getData();
  }
}

async function handleCertify(id: number) {
  loading.value = true;

  const { error, data: msg } = await certify(id);

  if (!error) {
    window.$message?.success($t('page.trust-manage.monitor.op.certify-success') + msg);
    await getData();
  }

  loading.value = false;
}

async function handleUpdateBase(id: number) {
  const { error, data: msg } = await updateBase(id);

  if (!error) {
    window.$message?.success($t('page.trust-manage.monitor.op.update-base-success') + msg);
    await getData();
  }
}

async function handlebactchPower(op: Api.TrustManage.PowerOperator) {
  const ids = checkedRowKeys.value.map(key => Number(key));

  const apiFn = op === 'off' ? batchPowerOn : batchPowerOff;
  let successI18nKey: App.I18n.I18nKey;
  switch (op) {
    case 'on':
      successI18nKey = 'page.trust-manage.monitor.op.power-off-success';
      break;
    case 'reboot':
      successI18nKey = 'page.trust-manage.monitor.op.reboot-success';
      break;
    default:
      successI18nKey = 'page.trust-manage.monitor.op.power-off-success';
      break;
  }

  const { error } = await apiFn(ids);

  if (!error) {
    window.$message?.success($t(successI18nKey));
    await getData();
  }
}

async function handleBatchCertify() {
  const ids = checkedRowKeys.value.map(key => Number(key));

  const { error, data: msg } = await batchCertify(ids);

  if (!error) {
    window.$message?.success($t('page.trust-manage.monitor.op.certify-success') + msg);
    await getData();
  }
}

async function handleBatchUpdateBase() {
  const ids = checkedRowKeys.value.map(key => Number(key));

  const { error } = await batchUpdateBase(ids);

  if (!error) {
    window.$message?.success($t('page.trust-manage.monitor.op.update-base-success'));
    await getData();
  }
}
</script>

<template>
  <div class="min-h-500px flex-col-stretch gap-16px overflow-hidden lt-sm:overflow-auto">
    <MonitorSearch v-model:model="searchParams" @reset="resetSearchParams" @search="getDataByPage" />
    <NCard
      :title="$t('page.trust-manage.monitor.title')"
      :bordered="false"
      size="small"
      class="sm:flex-1-hidden card-wrapper"
    >
      <template #header-extra>
        <MonitorTableHeaderOperation
          v-model:columns="columnChecks"
          :hide-add="true"
          :hide-delete="true"
          :loading="loading"
          @refresh="getData"
          @batch-power="handlebactchPower"
          @batch-certify="handleBatchCertify"
          @batch-update-base="handleBatchUpdateBase"
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
