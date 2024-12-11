<script setup lang="ts">
import { $t } from '@/locales';

defineOptions({
  name: 'TableHeaderOperation'
});

interface Props {
  itemAlign?: NaiveUI.Align;
  disabled?: boolean;
  loading?: boolean;
}

const props = defineProps<Props>();

interface Emits {
  (e: 'batchPower', op: Api.TrustManage.PowerOperator): void;
  (e: 'batchCertify'): void;
  (e: 'batchUpdateBase'): void;
  (e: 'refresh'): void;
}

const emit = defineEmits<Emits>();

const columns = defineModel<NaiveUI.TableColumnCheck[]>('columns', {
  default: () => []
});

function batchReboot() {
  emit('batchPower', 'reboot');
}

function batchPowerOn() {
  emit('batchPower', 'on');
}

function batchPowerOff() {
  emit('batchPower', 'off');
}

function batchCertify() {
  emit('batchCertify');
}

function batchUpdateBase() {
  emit('batchUpdateBase');
}

function refresh() {
  emit('refresh');
}
</script>

<template>
  <NSpace :align="props.itemAlign" wrap justify="end" class="lt-sm:w-200px">
    <slot name="prefix"></slot>
    <slot name="default">
      <NPopconfirm @positive-click="batchPowerOn">
        <template #trigger>
          <NButton size="small" ghost type="info" :disabled="disabled">
            <template #icon>
              <icon-ic-round-delete class="text-icon" />
            </template>
            {{ $t('page.trust-manage.monitor.op.batch-power-on') }}
          </NButton>
        </template>
        {{ $t('page.trust-manage.monitor.op.confirm-on') }}
      </NPopconfirm>
      <NPopconfirm @positive-click="batchReboot">
        <template #trigger>
          <NButton size="small" ghost type="info" :disabled="disabled">
            <template #icon>
              <icon-ic-round-delete class="text-icon" />
            </template>
            {{ $t('page.trust-manage.monitor.op.batch-power-reboot') }}
          </NButton>
        </template>
        {{ $t('page.trust-manage.monitor.op.confirm-reboot') }}
      </NPopconfirm>
      <NPopconfirm @positive-click="batchPowerOff">
        <template #trigger>
          <NButton size="small" ghost type="info" :disabled="disabled">
            <template #icon>
              <icon-ic-round-delete class="text-icon" />
            </template>
            {{ $t('page.trust-manage.monitor.op.batch-power-off') }}
          </NButton>
        </template>
        {{ $t('page.trust-manage.monitor.op.confirm-off') }}
      </NPopconfirm>
      <NPopconfirm @positive-click="batchUpdateBase">
        <template #trigger>
          <NButton size="small" ghost type="info" :disabled="disabled">
            <template #icon>
              <icon-ic-round-delete class="text-icon" />
            </template>
            {{ $t('page.trust-manage.monitor.op.batch-update-base') }}
          </NButton>
        </template>
        {{ $t('page.trust-manage.monitor.op.confirm-update-base') }}
      </NPopconfirm>
      <NPopconfirm @positive-click="batchCertify">
        <template #trigger>
          <NButton size="small" ghost type="info" :disabled="disabled">
            <template #icon>
              <icon-ic-round-delete class="text-icon" />
            </template>
            {{ $t('page.trust-manage.monitor.op.batch-certify') }}
          </NButton>
        </template>
        {{ $t('page.trust-manage.monitor.op.confirm-certify') }}
      </NPopconfirm>
    </slot>
    <NButton size="small" @click="refresh">
      <template #icon>
        <icon-mdi-refresh class="text-icon" :class="{ 'animate-spin': loading }" />
      </template>
      {{ $t('common.refresh') }}
    </NButton>
    <TableColumnSetting v-model:columns="columns" />
    <slot name="suffix"></slot>
  </NSpace>
</template>

<style scoped></style>
