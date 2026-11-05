# GenLayer Contract Templates

三个可以直接抄的 GenLayer 智能合约模板，配一份中文踩坑记录。

写给和我一样第一次碰 GenLayer 的人。官方示例讲的是"能跑"，这里补的是"别踩"。

## 模板

### 01 最小可用合约

`contracts/01_note_registry.py`

不碰外部数据，只演示存储类型和权限检查：地址、计数器、追加数组、键值映射。

建议先部署这个，确认工具链通了，再去碰非确定性逻辑。搞不清问题出在合约还是环境的时候，这三十行就是很好的分界线。

### 02 外部数据加验证者共识

`contracts/02_price_oracle.py`

从 HTTP 接口取价格，然后用自定义验证者做 0.5% 容差比较。

这份的重点不是请求接口，是后半段。不同节点在同一秒拿到的数字不一样，用 `strict_eq` 必然失败，只能比区间。

### 03 双证据判定

`contracts/03_evidence_judge.py`

读两个网页，让模型判断某个主张成不成立，输出只能是 PASS、FAIL、INSUFFICIENT 三选一。

争议判定类合约的骨架。里面写了两条安全规则：网页内容只当证据不当指令，判定结果必须是有限枚举。

## 怎么看这份仓库

`docs/pitfalls.md` 是核心。八条坑，每条都是那种不看文档、跑一遍、白干三小时才能撞上的。

比如两个 RPC 入口 chainId 一样但指向不同部署，比如回执 `status 0x1` 但合约根本没创建。

## 用之前先知道

模板按官方文档的 API 写的，包括 `gl.nondet.web.*`、`gl.vm.run_nondet_unsafe`、
`gl.eq_principle.*`、`DynArray` / `TreeMap` 这些。

合约里的 `Depends` 头要和当前 py-genlayer 版本对得上，版本号在官方文档的部署那一页能查到，
换了版本记得改这一行。

仓库里的文件是模板和笔记，不是生产代码。拿去改，别直接上主网。
