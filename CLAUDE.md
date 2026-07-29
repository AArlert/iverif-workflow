# iverif-workflow — iverif 0.8

验证工作流：证据链是唯一接口。任何"通过/关闭/完成"都由机器生成、可重放
的证据记录支撑；脚本从证据推导状态与下一步。不靠记忆、聊天记录、手改状态。

## 五条不变量（硬门）

1. 无 sim log 不 ✅ — 只有 `make evidence` 能把场景变绿。
2. 记录首行即重放命令 — 每条记录按原样可复现（TEST=/SEED= 或 CMD:）。
3. closer ≠ fixer — 关闭需要非修复者的独立重跑，由 orch 派卡时决定
   （修复卡与关闭卡分两次派发，不派给同一个执行者）——这是判断，不是
   字符串比对；git 作者在同一身份/同一 VM 下本就不是可靠信号，装一层
   机器检查只会造出一道看起来存在、实则拦不住任何人的假门。
4. spec 钉死 — 期望只来自 sha256 钉住的 `doc/spec.md`，永不来自被测 RTL。
5. 无击杀不采信 — 每 milestone 每类 checker 至少一次注伤自证：
   植入缺陷→红→恢复→绿，`doc/bugs.md` 记一行 `KILL`。从未红过的检查不算
   证据。机器背书：`make check MILESTONE=<n>` 核验本里程碑范围内至少有一条
   KILL 记录，缺失即红——这条不变量不是唯一一条只靠人记的。

## 循环

登记场景(🔲) → 写码 → `make run` → `make evidence`(✅) → 评审 → `make next` ─循环
失败走 bug 环：`doc/bugs.md` 登记(无条件) → 五类定性(成本序) → 修 → 独立关闭 → 守卫

## 目录（谁写什么）

| 路径 | 谁写 | 是什么 |
|---|---|---|
| doc/spec.md | 人/arch | 唯一期望来源，sha256 钉住（doc/spec.sha256） |
| design-prompt/ | arch | 设计提示，de 的输入 |
| doc/feature-matrix.md | de | 实现了什么，行引 testplan id |
| doc/testplan.md | dv | 场景真相表；dv 只出计划+搭组件+写测试 |
| doc/milestone.md | orch | 里程碑定义与出口条件 |
| doc/bugs.md + bugs/ | 全员 | 台账+详情；登记无条件 |
| doc/status.jsonl + log.md | 脚本+人 | 薄读口；满了 `make archive` |
| doc/evidence/ | 仅脚本 | 机器生成，与所证代码同 commit |
| doc/VENDOR.md | de | vendored-DUT 上游 patch 追踪（P-xxx 编号 + sha 锁定表） |
| workflow/ · scripts/ | 上游 | 4 份契约 + 机械层（含自测），本地修改自行维护 |

## make（脚本能干的，绝不让人或 agent 干）

| 目标 | 干什么 |
|---|---|
| handoff | 接手简报：status 头 + log 尾块 + open bugs + next |
| run TEST= SEED= | 跑一个场景 |
| evidence TEST= SEED= | 抓证据：重放行+env+git rev+关键行+双腿判决(UVM+SVA)，回填 testplan |
| evidence BUG= CMD= EXPECT= | 非仿真闭环（CMD 形态，fail-closed×2） |
| next | 三队列：未闭环 / 未开工 / 探索前沿(spec 未引用章节+覆盖洞) |
| regress | **纯转发**：`@$(MAKE) -C sim regress`，和 smoke/cov/lint/verdi/clean 同一模式；canon 不再拥有循环，判据原语见 `scripts/svacheck.py --judge` |
| check [SCEN=\|MILESTONE=] | docs-check+链审计：ghost ref / ✅无证据 / 断链 / 本里程碑 KILL 覆盖（不变量 5 的机器背书，缺失即红）；SCEN 收窄成单场景全链，MILESTONE 收窄成签核预检(含 rubric 人工清单打印+KILL 覆盖检查) |
| guards FILES= | 打印绑定给这些文件的 regression_guard（派卡时的共模防火墙——机器可粘贴的片段，不是审计报告，故不并入 check） |
| bump | VERSION+CHANGELOG+tag 一步；距上次发布过久时额外打印一行提示，抽查已知下游 fork 的 workflow/ 是否分叉过大 |
| commit | add+commit 一步，message 带证据摘要；只到本地，不含 push——推送是对外不可逆动作，留给人手动 `git push` |
| archive | 滚动归档 log/status（厚存储，薄读口） |

被砍掉的两个目标：`replay SCEN=`——不变量 2 已经保证首行就是命令，包一层
make 目标没有换来任何新能力，纯粹多一个要记的名字。`signoff-check`——它和
`chain-audit` 是同一份底层审计加一层里程碑过滤+人工清单打印，折进
`check MILESTONE=` 而不是单独占一个动词。`chain SCEN=` 同理折进
`check SCEN=`。四个名字收成一个 `check`，参数决定视图，不是四套代码。

## 派卡（orch）：按风险定级，级别决定链与模型

| 级 | 面 | 链 | 模型 |
|---|---|---|---|
| L0 | 文档/构建/lint | 脚本验收即可，无 rev | haiku |
| L1 | TB/序列/覆盖 | dv 卡+sim 证据；rev 按节奏不按卡 | sonnet |
| L2 | RTL/SVA/记分板 | 全隔离链+独立复验 | opus |
| L3 | spec/豁免/签核 | rev 必到，全 rubric | opus |

拿不准就升级。可靠性在脚本与门里，不在模型档位里——L0 交 haiku 是安全的。
谁执笔（人/agent）是卡上一个字段，不是两种流程：人想亲写 de/dv，rev 照常。

## BUG 五类（成本序：先便宜的假设，最贵的指控最后）

TOOL_ENV → TB_BUG / CONSTRAINT_BUG → SPEC_ISSUE → DUT_BUG
CONSTRAINT_BUG 会作废历史：同约束的既往绿必须回审。指认 DUT 需 rev 签核。
细则与各类下一步：`workflow/bugs.md`。

## 编码纪律（细则 workflow/discipline.md）

想清再动手 · 最小实现 · 外科手术式修改 · 目标即门 · 小闭环即停。
唯一例外是门：永不为过卡放宽门，永不"顺手简化"一个 fail-closed 检查。

## 升级

这份仓库本身就是可 clone 的模板；想跟上游改进：保留 remote，
`git cherry-pick` 感兴趣的提交，愿意就拉，不拉也不红——`workflow/` 与
`scripts/` 是上游文件，本地怎么改是你自己的事，不再有 fwsync/manifest/
divergence 三态去检测漂移。设计沿革与被砍掉的机制见 `DESIGN.md`（canon-only，
克隆后可删可留）。
