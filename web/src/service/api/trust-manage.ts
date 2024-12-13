import { request } from '../request';

/** get monitor list */
export function fetchGetMonitorList(params?: Api.TrustManage.MonitorSearchParams) {
  return request<Api.TrustManage.MonitorList>({
    url: '/trustManage/getMonitorList',
    method: 'post',
    data: params
  });
}

/** get monitor detail */
export function fetchGetMonitorInfo(id: number) {
  return request<Api.TrustManage.Monitor>({
    url: '/trustManage/getMonitorInfo',
    method: 'get',
    params: { id }
  });
}

/** power on */
export function powerOn(id: number) {
  return request({
    url: '/trustManage/powerOn',
    method: 'post',
    params: { id }
  });
}

/** power off */
export function powerOff(id: number) {
  return request({
    url: '/trustManage/powerOff',
    method: 'post',
    params: { id }
  });
}

/** certify */
export function certify(id: number) {
  return request({
    url: '/trustManage/certify',
    method: 'post',
    params: { id }
  });
}

/** update base */
export function updateBase(id: number) {
  return request({
    url: '/trustManage/updateBase',
    method: 'post',
    params: { id }
  });
}

/** batch power on */
export function batchPowerOn(ids: number[]) {
  return request({
    url: '/trustManage/batchPowerOn',
    method: 'post',
    data: { ids }
  });
}

/** batch power off */
export function batchPowerOff(ids: number[]) {
  return request({
    url: '/trustManage/batchPowerOff',
    method: 'post',
    data: { ids }
  });
}

/** batch certify */
export function batchCertify(ids: number[]) {
  return request({
    url: '/trustManage/batchCertify',
    method: 'post',
    data: { ids }
  });
}

/** batch update base */
export function batchUpdateBase(ids: number[]) {
  return request({
    url: '/trustManage/batchUpdateBase',
    method: 'post',
    data: { ids }
  });
}
