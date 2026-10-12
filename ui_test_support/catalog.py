"""2026-10-12 在 Edge 实际访问后建立的页面/标签覆盖清单。"""
from dataclasses import dataclass


@dataclass(frozen=True)
class PageSpec:
    id: str
    group: str
    name: str
    path: str
    anchors: tuple[str, ...]


PAGES = [
    PageSpec("home", "", "首页", "/index", ("教师工作量管理首页", "SIS 同步明细", "学科部年度概览")),
    PageSpec("budget_standard", "教学计划管理", "学院工作量标准", "/hss-budget/control", ("当前学年", "跨学年对比")),
    PageSpec("course", "教学计划管理", "开课管理", "/hss-budget/course", ("Course Offering", "开课列表", "历史导入记录")),
    PageSpec("tracking", "教学计划管理", "审批跟踪", "/hss-budget/approval-tracking", ("当前查看", "提交时间", "当前节点")),
    PageSpec("settlement", "工作量结算管理", "工作量结算管理", "/hss-settlement/index", ("结算批次", "结算引擎", "结算报告")),
    PageSpec("compliance", "工作量结算管理", "达标情况对比", "/hss-settlement/compliance", ("当前学年", "导出汇总", "判定")),
    PageSpec("approval", "工作量结算管理", "特殊审批", "/hss-settlement/approval", ("特殊案例类型说明", "学部主任意见汇总", "结算批准三级流程")),
    PageSpec("query", "工作量结算管理", "工作量查询", "/hss-settlement/query", ("个人查询", "管理查询", "课程明细")),
    PageSpec("task", "待办任务", "待办任务", "/hss-task/index", ("任务管理", "全部待办", "审批状态")),
    PageSpec("academic", "系统配置管理", "学年学期管理", "/hss-config/academic-term", ("学年管理", "学期管理", "版本")),
    PageSpec("config_standard", "系统配置管理", "学院工作量标准", "/hss-config/workload-standard", ("全年标准工作量", "全年课时标准", "容差比例")),
    PageSpec("rule", "系统配置管理", "计算规则管理", "/hss-config/rule", ("Teaching Load", "计算流程图", "测试计算引擎")),
    PageSpec("special_course", "系统配置管理", "课程信息维护", "/hss-config/special-course", ("课程编号", "是否论文指导", "是否体育课")),
    PageSpec("teacher", "系统配置管理", "教师管理", "/hss-config/teacher", ("关键字", "教师姓名", "工号")),
    PageSpec("user", "系统管理", "用户管理", "/system/user", ("登录账号", "用户名", "合同类型")),
    PageSpec("role", "系统管理", "角色管理", "/system/role", ("角色分类", "角色标识", "角色名称")),
    PageSpec("menu", "系统管理", "菜单管理", "/system/menu", ("菜单分类", "刷新菜单缓存", "组件路径")),
    PageSpec("dept", "系统管理", "部门管理", "/system/dept", ("部门名称", "负责人", "部门编号")),
    PageSpec("post", "系统管理", "岗位管理", "/system/post", ("岗位名称", "岗位编码", "岗位编号")),
    PageSpec("dict", "系统管理", "字典管理", "/system/dict", ("字典名称", "字典类型", "字典编号")),
    PageSpec("dict_data", "", "字典数据", "/dict/type/data/hss_course_belongs", ("字典标签", "字典键值", "字典编码")),
    PageSpec("notify", "", "系统消息", "/user/notify-message", ("接收时间", "消息类型", "消息内容", "全部已读")),
]
PAGE = {p.id: p for p in PAGES}

# (页面、标签名称/前缀、标签内容的业务锚点)
TABS = [
    ("academic", "学年管理", "新增学年"), ("academic", "学期管理", "学期代码"),
    ("rule", "计算流程图", "解析原始课时"), ("rule", "系数规则库", "系数配置"),
    ("rule", "测试计算引擎", "输入参数"),
    ("course", "课时减免", "实际减免时数"), ("course", "跨学年结转", "来源学年"),
    ("course", "开课列表", "课程代码"), ("course", "计划版", "导出计划版"),
    ("course", "历史导入记录", "导入时间"),
    ("settlement", "co-list", "新增课程代码"), ("settlement", "SIS同步明细", "SIS数据导入"),
    ("settlement", "结算引擎", "运行结算引擎"), ("settlement", "计划vs实际对比", "运算结果"),
    ("settlement", "工作量明细", "最终工作量"), ("settlement", "结算报告", "教师明细表"),
    ("compliance", "计划版", "Hours(实际/全年标准)"),
    ("compliance", "预估版", "Hours(实际/全年标准)"),
    ("compliance", "实际版", "Hours(实际/全年标准)"),
    ("query", "个人查询", "个人信息"), ("query", "管理查询", "教学工作量"),
    ("task", "全部待办", "审批状态"), ("task", "待学科部主任审批", "审批状态"),
    ("task", "待学院行政审批", "审批状态"), ("task", "待学院行政主管审批", "审批状态"),
    ("task", "待主管领导审批", "审批状态"),
]
RULE_GROUPS = [
    ("课时计算", "分钟取整规则", "CEIL_HALF"),
    ("课时计算", "异常检测阈值", "DATETIME_FORMAT"),
    ("课时计算", "论文指导人数系数", "人数"),
    ("逻辑规则", "多教室归并阈值", "CLASSROOM_MAX"),
    ("SCH计算规则", "学分系数", "DEFAULT"),
    ("SCH计算规则", "课程类型系数", "CEC"),
    ("SCH计算规则", "评分基础权重", "DPF"),
    ("工作量计算规则", "上课频率系数", "BIWEEKLY"),
    ("工作量计算规则", "学期类型系数", "TERM_1"),
]
FORMS = [
    ("user", "新增", "登录账号", "取 消"),
    ("role", "新增", "角色标识", "取 消"),
    ("menu", "新增", "路由地址", "取 消"),
    ("dept", "新增", "上级部门", "取 消"),
    ("post", "新增", "岗位编码", "取 消"),
    ("dict", "新增", "字典类型", "取 消"),
    ("dict_data", "新增", "数据键值", "取 消"),
    ("academic", "新增学年", "生效起始日", "取消"),
    ("config_standard", "新增", "合同类型", "取消"),
    ("special_course", "新增", "课程编号", "取消"),
    ("teacher", "新增", "工号", "取消"),
    ("approval", "提交申请", "详细描述", "取消"),
]
SEARCHES = [
    ("teacher", "姓名 / 工号 / 邮箱"), ("special_course", "请输入课程编号"),
    ("user", "请输入登录账号"), ("role", "请输入角色标识"),
    ("dict", "请输入字典类型"), ("dict_data", "请输入字典标签"),
]
