# AutoClockIn
The project contains auto clock in script for example wps.

<h2>How To Use</h2>
1.登陆网页版WPS：https://zt.wps.cn/2018/clock_in，
微信登陆后F12查看cookies信息，找到application里的wps_id如图

![](https://github.com/wjkV587/AutoClockIn/raw/master/images/wps.png)

2.找到自己的个人id，如图

![](https://github.com/wjkV587/AutoClockIn/raw/master/images/id.png)

3.利用腾讯云函数服务来完成每日的自动打卡
登陆https://console.cloud.tencent.com/scf/index?rid=1，
点击函数服务-新建，随便命名一个如下，注意选择python3.6+空白函数

![](https://github.com/wjkV587/AutoClockIn/raw/master/images/tx1.png)

执行方法填autowps.wps_main，点击文件-新建文件autowps.py，将本项目的autowps.py的内容拷贝粘贴过去完成，接下来注意替换掉脚本的wpsid和个人id，
将步骤1和2的值替换到脚本最后的位置如图，保存并测试即可。

![](https://github.com/wjkV587/AutoClockIn/raw/master/images/tx2.png)

![](https://github.com/wjkV587/AutoClockIn/raw/master/images/tx3.png)


