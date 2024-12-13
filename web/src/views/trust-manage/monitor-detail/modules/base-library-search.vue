<script setup lang="ts">
import { trustLogStatusOptions } from '@/constants/business';
import { $t } from '@/locales';
import { translateOptions } from '@/utils/common';

defineOptions({
  name: 'BaseLibrarySearch'
});

interface Emits {
  (e: 'reset'): void;
  (e: 'search'): void;
}

const emit = defineEmits<Emits>();

const model = defineModel<Api.TrustManage.TrustLogSearchParams>('model', { required: true });

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
            <NFormItemGi
              span="24 s:12 m:6"
              :label="$t('page.trust-manage.base-library.path')"
              path="ip"
              class="pr-24px"
            >
              <NInput v-model:value="model.path" :placeholder="$t('page.trust-manage.base-library.form.path')" />
            </NFormItemGi>
            <NFormItemGi
              span="24 s:12 m:6"
              :label="$t('page.trust-manage.base-library.base-value')"
              path="remark"
              class="pr-24px"
            >
              <NInput
                v-model:value="model.baseValue"
                :placeholder="$t('page.trust-manage.base-library.form.base-value')"
              />
            </NFormItemGi>
            <NFormItemGi
              span="24 s:12 m:6"
              :label="$t('page.trust-manage.base-library.log-status')"
              path="powerStatus"
              class="pr-24px"
            >
              <NSelect
                v-model:value="model.logStatus"
                :placeholder="$t('page.trust-manage.base-library.form.log-status')"
                :options="translateOptions(trustLogStatusOptions)"
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
