# Git 常用命令
## 一、GIT搭建
* 安装GIT<br>
`sudo apt-git install git`

* 创建用户<br>
`adduser git`

* 修改用户名和邮箱地址<br>
`git config --global user.name "username"`<br>
`git config --global user.email "email"`

* 查看用户名和邮箱地址<br>
`git config user.name`<br>
`git config user.email`
---

## 二、仓库管理
* 初始化仓库（裸仓库、无工作区）<br>
`git init --bare sample.git`

* 更改仓库所有者<br>
`sudo chown -R git:git sample.git`

* 禁止git用户登陆shell，<font color=red>通过编辑/etc/passwd</font><br>
`git:x:1001:1001:,,,:/home/git:/bin/bash`<br>
修改为：<br>
`git:x:1001:1001:,,,:/home/git:/usr/bin/git-shell`

* 提交次数统计<br>
`git log | grep -e 'commit [a-zA-Z0-9*]' | wc -l`
---
## 三、分支管理
* 新建分支<br>
`git branch <branchName>`

* 切换分支<br>
`git checkout <branchName>`

* 新建并切换分支<br>
`git checkout -b <branchName>`

* 合并分支到主干master<br>
`git merge <branchName>`

* 合并后删除分支信息<br>
`git branch -d <branchName>`

* 删除远程分支信息<br>
`git push origin --delete <branchName>`
---
## 四、tag管理
* 新建tag<br>
`git tag -a vx.x.x -m "detail message"`

* 显示tag<br>
`git tag 或者 git tag -l`

* 显示详细tag<br>
`git show vx.x.x或者commit号`

* 共享tag（单个）<br>
`git push origin vx.x.x`

* 共享tag（多个）<br>
`git push origin --tags`
---
## 五、撤销操作
* 丢弃工作区修改<br>
`git checkout -- file` 
> 命令中的--很重要，没有--，就变成了“切换到另一个分支”的命令

* 撤销pull<br>
`git reflog`
`git reset --hard HEAD@{n}`
> n是要回退到的引用位置。

* 重新填写commit log<br>
`git commit --amend`

---

## 六、导出
* 导出干净代码<br>
`git archive --format=zip --output="./output.zip" master -0`

---

## 七、查看文件修改记录
* 查看单个文件详细修改记录<br>
`git log -p <filename>`

* 查看单个文件相关提交记录<br>
`git log <filename>`
---
