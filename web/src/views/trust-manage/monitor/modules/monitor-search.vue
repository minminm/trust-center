<script setup lang="ts">
import { $t } from '@/locales';
import { powerStatusOptions, trustStatusOptions } from '@/constants/business';
import { translateOptions } from '@/utils/common';

defineOptions({
  name: 'MonitorSearch'
});

interface Emits {
  (e: 'reset'): void;
  (e: 'search'): void;
}

const emit = defineEmits<Emits>();

const model = defineModel<Api.TrustManage.MonitorSearchParams>('model', { required: true });

function reset() {
  emit('reset');
}

function search() {
  emit('search');
}
</script>

<template>
  <NCard :bordered="false" size="small" class="card-wrapper">
    <NCollapse>
      <NCollapseItem :title="$t('common.search')" name="monitor-search">
        <NForm :model="model" label-placement="left" :label-width="80">
          <NGrid responsive="screen" item-responsive>
            <NFormItemGi span="24 s:12 m:6" :label="$t('page.trust-manage.monitor.ip')" path="ip" class="pr-24px">
              <NInput v-model:value="model.ipAddress" :placeholder="$t('page.trust-manage.monitor.form.ipAddress')" />
            </NFormItemGi>
            <NFormItemGi
              span="24 s:12 m:6"
              :label="$t('page.trust-manage.monitor.remark')"
              path="remark"
              class="pr-24px"
            >
              <NInput v-model:value="model.remark" :placeholder="$t('page.trust-manage.monitor.form.remark')" />
            </NFormItemGi>
            <NFormItemGi
              span="24 s:12 m:6"
              :label="$t('page.trust-manage.monitor.power-status')"
              path="powerStatus"
              class="pr-24px"
            >
              <NSelect
                v-model:value="model.powerStatus"
                :placeholder="$t('page.trust-manage.monitor.form.powerStatus')"
                :options="translateOptions(powerStatusOptions)"
                clearable
              />
            </NFormItemGi>
            <NFormItemGi
              span="24 s:12 m:6"
              :label="$t('page.trust-manage.monitor.trust-status')"
              path="powerStatus"
              class="pr-24px"
            >
              <NSelect
                v-model:value="model.trustStatus"
                :placeholder="$t('page.trust-manage.monitor.form.trustStatus')"
                :options="translateOptions(trustStatusOptions)"
                clearable
              />
            </NFormItemGi>
            <NFormItemGi span="24 s:12 m:6">
              <NSpace class="w-full" justify="end">
                <NButton @click="reset">
                  <template #icon>
                    <icon-ic-round-refresh class="text-icon" />
                  </template>
                  {{ $t('common.reset') }}
                </NButton>
                <NButton type="primary" ghost @click="search">
                  <template #icon>
                    <icon-ic-round-search class="text-icon" />
                  </template>
                  {{ $t('common.search') }}
                </NButton>
              </NSpace>
            </NFormItemGi>
          </NGrid>
        </NForm>
      </NCollapseItem>
    </NCollapse>
  </NCard>
</template>

<style scoped></style>
