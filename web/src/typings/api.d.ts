/**
 * Namespace Api
 *
 * All backend api type
 */
declare namespace Api {
  namespace Common {
    /** common params of paginating */
    interface PaginatingCommonParams {
      /** current page number */
      current: number;
      /** page size */
      size: number;
      /** total count */
      total: number;
    }

    /** common params of paginating query list data */
    interface PaginatingQueryRecord<T = any> extends PaginatingCommonParams {
      records: T[];
    }

    /** common search params of table */
    type CommonSearchParams = Pick<Common.PaginatingCommonParams, 'current' | 'size'>;

    /**
     * enable status
     *
     * - "1": enabled
     * - "2": disabled
     */
    type EnableStatus = '1' | '2';

    /** common record */
    type CommonRecord<T = any> = {
      /** record id */
      id: number;
      /** record creator */
      createBy: string;
      /** record create time */
      createTime: string;
      /** record updater */
      updateBy: string;
      /** record update time */
      updateTime: string;
      /** record status */
      status: EnableStatus | null;
    } & T;
  }

  /**
   * namespace Auth
   *
   * backend api module: "auth"
   */
  namespace Auth {
    interface LoginToken {
      token: string;
      refreshToken: string;
    }

    interface UserInfo {
      userId: string;
      userName: string;
      roles: string[];
      buttons: string[];
    }
  }

  /**
   * namespace Route
   *
   * backend api module: "route"
   */
  namespace Route {
    type ElegantConstRoute = import('@elegant-router/types').ElegantConstRoute;

    interface MenuRoute extends ElegantConstRoute {
      id: string;
    }

    interface UserRoute {
      routes: MenuRoute[];
      home: import('@elegant-router/types').LastLevelRouteKey;
    }
  }

  /**
   * namespace SystemManage
   *
   * backend api module: "systemManage"
   */
  namespace SystemManage {
    type CommonSearchParams = Pick<Common.PaginatingCommonParams, 'current' | 'size'>;

    /** permission */
    type Permission = Common.CommonRecord<{
      /** permission name */
      permName: string;
      /** permission code */
      permCode: string;
      /** permission description */
      permDesc: string;
    }>;

    type PermModel = Pick<Api.SystemManage.Permission, 'permName' | 'permCode' | 'permDesc' | 'status'>;

    /** permission search params */
    type PermSearchParams = CommonType.RecordNullable<
      Pick<Api.SystemManage.Permission, 'permName' | 'permCode' | 'permDesc' | 'status'> & CommonSearchParams
    >;

    /** role list */
    type PermList = Common.PaginatingQueryRecord<Permission>;

    /** all role */
    type AllPerm = Pick<Permission, 'id' | 'permName' | 'permCode'>;

    /** role */
    type Role = Common.CommonRecord<{
      /** role name */
      roleName: string;
      /** role code */
      roleCode: string;
      /** role description */
      roleDesc: string;
      /** role permissions */
      rolePerms: string[];
    }>;

    type RoleModel = Pick<Api.SystemManage.Role, 'roleName' | 'roleCode' | 'roleDesc' | 'status' | 'rolePerms'>;

    /** role search params */
    type RoleSearchParams = CommonType.RecordNullable<
      Pick<Api.SystemManage.Role, 'roleName' | 'roleCode' | 'roleDesc' | 'status' | 'rolePerms'> & CommonSearchParams
    >;

    /** role list */
    type RoleList = Common.PaginatingQueryRecord<Role>;

    /** all role */
    type AllRole = Pick<Role, 'id' | 'roleName' | 'roleCode'>;

    /**
     * user gender
     *
     * - "1": "male"
     * - "2": "female"
     */
    type UserGender = '1' | '2';

    /** user */
    type User = Common.CommonRecord<{
      /** user name */
      userName: string;
      /** user gender */
      userGender: UserGender | null;
      /** user nick name */
      userPasswd: string;
      nickName: string;
      /** user phone */
      userPhone: string;
      /** user email */
      userEmail: string;
      /** user role code collection */
      userRoles: string[];
    }>;

    type UserModel = Pick<
      Api.SystemManage.User,
      'userName' | 'userGender' | 'nickName' | 'userPasswd' | 'userEmail' | 'userRoles' | 'status'
    >;

    /** user search params */
    type UserSearchParams = CommonType.RecordNullable<
      Pick<Api.SystemManage.User, 'userName' | 'userGender' | 'nickName' | 'userEmail' | 'status' | 'userRoles'> &
        CommonSearchParams
    >;

    /** user list */
    type UserList = Common.PaginatingQueryRecord<User>;

    /**
     * menu type
     *
     * - "1": directory
     * - "2": menu
     */
    type MenuType = '1' | '2';

    type MenuButton = {
      /**
       * button code
       *
       * it can be used to control the button permission
       */
      code: string;
      /** button description */
      desc: string;
    };

    /**
     * icon type
     *
     * - "1": iconify icon
     * - "2": local icon
     */
    type IconType = '1' | '2';

    type MenuPropsOfRoute = Pick<
      import('vue-router').RouteMeta,
      | 'i18nKey'
      | 'keepAlive'
      | 'constant'
      | 'order'
      | 'href'
      | 'hideInMenu'
      | 'activeMenu'
      | 'multiTab'
      | 'fixedIndexInTab'
      | 'query'
    >;

    type Menu = Common.CommonRecord<{
      /** parent menu id */
      parentId: number;
      /** menu type */
      menuType: MenuType;
      /** menu name */
      menuName: string;
      /** route name */
      routeName: string;
      /** route path */
      routePath: string;
      /** component */
      component?: string;
      /** iconify icon name or local icon name */
      icon: string;
      /** icon type */
      iconType: IconType;
      /** buttons */
      buttons?: MenuButton[] | null;
      /** children menu */
      children?: Menu[] | null;
    }> &
      MenuPropsOfRoute;

    /** menu list */
    type MenuList = Common.PaginatingQueryRecord<Menu>;

    type MenuTree = {
      id: number;
      label: string;
      pId: number;
      children?: MenuTree[];
    };
  }

  /**
   * namespace TrustManage
   *
   * backend api module: "trustManage"
   */
  namespace TrustManage {
    type CommonSearchParams = Pick<Common.PaginatingCommonParams, 'current' | 'size'>;

    /**
     * host power status
     *
     * - "1": "on"
     * - "2": "off"
     */
    type PowerStatus = '1' | '2';

    type PowerOperator = 'on' | 'off' | 'reboot';

    /**
     * host trust status
     *
     * - "1": "trust"
     * - "2": "mistrust"
     */
    type TrustStatus = '1' | '2';

    /** monitor */
    type Monitor = Common.CommonRecord<{
      /** ip address */
      ipAddress: string;
      /** power status */
      powerStatus: PowerStatus;
      /** trust status */
      trustStatus: TrustStatus;
      /** remark message */
      remark: string;
      /** first connect time */
      createTime: string;
      /** last power-on time */
      logoutTime: string;
      /** last update base time */
      updateBaseTime: string;
      /** last certify time */
      certifyTime: string;
      /** certify times since last reboot */
      certifyTimes: number;
    }>;

    /** monitor search params */
    type MonitorSearchParams = CommonType.RecordNullable<
      Pick<Api.TrustManage.Monitor, 'ipAddress' | 'remark' | 'powerStatus' | 'trustStatus'> & CommonSearchParams
    >;

    /** monitor list */
    type MonitorList = Common.PaginatingQueryRecord<Monitor>;

    /**
     * host trust status
     *
     * - "1": "Not verified"
     * - "2": "Verification successful"
     * - "3": "Verification failed"
     */
    type LogStatus = '1' | '2' | '3';

    /** trust log */
    type TrustLog = Common.CommonRecord<{
      /** log status */
      logStatus: LogStatus;
      /** pcr list */
      pcr: number[];
      /** file path */
      path: string;
      /** base value */
      baseValue: string;
      /** verify value */
      verifyValue: string;
    }>;

    /** trust log search params */
    type TrustLogSearchParams = CommonType.RecordNullable<
      Pick<Api.TrustManage.TrustLog, 'id' | 'path' | 'logStatus' | 'baseValue'> & CommonSearchParams
    >;

    /** trust log list */
    type TrustLogList = Common.PaginatingQueryRecord<TrustLog>;
  }
}
