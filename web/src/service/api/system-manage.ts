import { request } from '../request';
/** get permission list */
export function fetchGetPermList(params?: Api.SystemManage.PermSearchParams) {
  return request<Api.SystemManage.PermList[]>({
    url: '/perm/getPermList',
    method: 'post',
    data: params
  });
}

/** get role list */
export function fetchGetRoleList(params?: Api.SystemManage.RoleSearchParams) {
  return request<Api.SystemManage.RoleList>({
    url: '/role/getRoleList',
    method: 'post',
    data: params
  });
}

/**
 * get all permissions
 *
 * these permissions are all enabled
 */
export function fetchGetAllPerms() {
  return request<Api.SystemManage.AllPerm[]>({
    url: '/perm/getAllPerms',
    method: 'get'
  });
}

/**
 * get all roles
 *
 * these roles are all enabled
 */
export function fetchGetAllRoles() {
  return request<Api.SystemManage.AllRole[]>({
    url: '/role/getAllRoles',
    method: 'get'
  });
}

/** get user list */
export function fetchGetUserList(params?: Api.SystemManage.UserSearchParams) {
  return request<Api.SystemManage.UserList>({
    url: '/user/getUserList',
    method: 'post',
    data: params
  });
}

/** get menu list */
export function fetchGetMenuList() {
  return request<Api.SystemManage.MenuList>({
    url: '/systemManage/getMenuList/v2',
    method: 'get'
  });
}

/** get all pages */
export function fetchGetAllPages() {
  return request<string[]>({
    url: '/systemManage/getAllPages',
    method: 'get'
  });
}

/** get menu tree */
export function fetchGetMenuTree() {
  return request<Api.SystemManage.MenuTree[]>({
    url: '/systemManage/getMenuTree',
    method: 'get'
  });
}

/** add user */
export function addUser(data: Api.SystemManage.UserModel) {
  return request<Api.SystemManage.User>({
    url: '/user/addUser',
    method: 'post',
    data
  });
}

/** update user */
export function updateUser(data: Api.SystemManage.UserModel) {
  return request<Api.SystemManage.User>({
    url: '/user/updateUser',
    method: 'post',
    data
  });
}

/** delete user */
export function deleteUser(id: number) {
  return request({
    url: '/user/deleteUser',
    method: 'delete',
    params: { id }
  });
}

/** batch delete user */
export function batchDeleteUser(ids: number[]) {
  return request({
    url: '/user/batchDeleteUser',
    method: 'delete',
    data: { ids }
  });
}

/** add role */
export function addRole(data: Api.SystemManage.RoleModel) {
  return request<Api.SystemManage.Role>({
    url: '/role/addRole',
    method: 'post',
    data
  });
}

/** update role */
export function updateRole(data: Api.SystemManage.RoleModel) {
  return request<Api.SystemManage.Role>({
    url: '/role/updateRole',
    method: 'post',
    data
  });
}

/** delete role */
export function deleteRole(id: number) {
  return request({
    url: '/role/deleteRole',
    method: 'delete',
    params: { id }
  });
}

/** batch delete role */
export function batchDeleteRole(ids: number[]) {
  return request({
    url: '/role/batchDeleteRole',
    method: 'delete',
    data: { ids }
  });
}
