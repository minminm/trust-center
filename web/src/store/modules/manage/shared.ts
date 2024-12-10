import { fetchGetAllRoles } from '@/service/api';

export async function getAllRoles() {
  const { error, data } = await fetchGetAllRoles();
  const allRoles = [];

  if (!error) {
    allRoles.push(...data);
  }

  return allRoles;
}
