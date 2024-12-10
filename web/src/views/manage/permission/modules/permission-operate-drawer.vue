<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useFormRules, useNaiveForm } from '@/hooks/common/form';
import { $t } from '@/locales';
import { enableStatusOptions } from '@/constants/business';
import { addPermission, updatePermission } from '@/service/api/system-manage';

defineOptions({
  name: 'PermissionOperateDrawer'
});

interface Props {
  /** the type of operation */
  operateType: NaiveUI.TableOperateType;
  /** the edit row data */
  rowData?: Api.SystemManage.Permission | null;
}

const props = defineProps<Props>();

interface Emits {
  (e: 'submitted'): void;
}

const emit = defineEmits<Emits>();

const visible = defineModel<boolean>('visible', {
  default: false
});

const { formRef, validate, restoreValidation } = useNaiveForm();
const { defaultRequiredRule } = useFormRules();

const title = computed(() => {
  const titles: Record<NaiveUI.TableOperateType, string> = {
    add: $t('page.manage.permission.addPerm'),
    edit: $t('page.manage.permission.editPerm')
  };
  return titles[props.operateType];
});

type Model = Api.SystemManage.PermModel;

const model = ref(createDefaultModel());

function createDefaultModel(): Model {
  return {
    permName: '',
    permCode: '',
    permDesc: '',
    status: null
  };
}

type RuleKey = Extract<keyof Model, 'permName' | 'permCode' | 'status'>;

const rules: Record<RuleKey, App.Global.FormRule> = {
  permName: defaultRequiredRule,
  permCode: defaultRequiredRule,
  status: defaultRequiredRule
};

function handleInitModel() {
  model.value = createDefaultModel();

  if (props.operateType === 'edit' && props.rowData) {
    Object.assign(model.value, props.rowData);
  }
}

function closeDrawer() {
  visible.value = false;
}

async function handleSubmit() {
  await validate();

  const submitMethod = props.operateType === 'edit' ? updatePermission : addPermission;
  const successI18nKey = props.operateType === 'edit' ? 'common.updateSuccess' : 'common.addSuccess';
  const failedI18nKey = props.operateType === 'edit' ? 'common.updateFailed' : 'common.addFailed';

  const { error } = await submitMethod(model.value);

  if (!error) {
    window.$message?.success($t(successI18nKey));
    closeDrawer();
    emit('submitted');
  } else {
    window.$message?.error($t(failedI18nKey));
  }
}

watch(visible, () => {
  if (visible.value) {
    handleInitModel();
    restoreValidation();
  }
});
</script>

<template>
  <NDrawer v-model:show="visible" display-directive="show" :width="360">
    <NDrawerContent :title="title" :native-scrollbar="false" closable>
      <NForm ref="formRef" :model="model" :rules="rules">
        <NFormItem :label="$t('page.manage.permission.permName')" path="permName">
          <NInput v-model:value="model.permName" :placeholder="$t('page.manage.permission.form.permName')" />
        </NFormItem>
        <NFormItem :label="$t('page.manage.permission.permCode')" path="permCode">
          <NInput v-model:value="model.permCode" :placeholder="$t('page.manage.permission.form.permCode')" />
        </NFormItem>
        <NFormItem :label="$t('page.manage.permission.permStatus')" path="status">
          <NRadioGroup v-model:value="model.status">
            <NRadio v-for="item in enableStatusOptions" :key="item.value" :value="item.value" :label="$t(item.label)" />
          </NRadioGroup>
        </NFormItem>
        <NFormItem :label="$t('page.manage.permission.permDesc')" path="permDesc">
          <NInput v-model:value="model.permDesc" :placeholder="$t('page.manage.permission.form.permDesc')" />
        </NFormItem>
      </NForm>
      <template #footer>
        <NSpace :size="16">
          <NButton @click="closeDrawer">{{ $t('common.cancel') }}</NButton>
          <NButton type="primary" @click="handleSubmit">{{ $t('common.confirm') }}</NButton>
        </NSpace>
      </template>
    </NDrawerContent>
  </NDrawer>
</template>

<style scoped></style>
